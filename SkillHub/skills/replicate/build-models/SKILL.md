---
name: build-models
description: >
  Package and build custom AI models with Cog for deployment on Replicate.
  Use when creating a cog.yaml or predict.py, defining model inputs and
  outputs, loading model weights at setup time, building Docker images for
  ML models, serving locally with cog serve or cog predict, or porting a
  HuggingFace, GitHub, or ComfyUI model to run on Replicate. Trigger on
  phrases like "build a model", "package a model", "create a Cog model",
  "wrap a model", "containerize an AI model", "predict.py", "cog.yaml",
  "BasePredictor", or "Cog container", and when referencing cog.run,
  github.com/replicate/cog, or github.com/replicate/cog-examples. Covers
  GPU and CUDA setup, pget for fast weight downloads, async predictors
  with continuous batching, streaming outputs, and cold-boot optimization
  for image, video, audio, and LLM models. For pushing built models to
  Replicate, see publish-models. For running existing models, see
  run-models.
---

## Docs

- Cog reference (single file): <https://cog.run/llms.txt>
- `cog.yaml` reference: <https://cog.run/yaml>
- Python predictor reference: <https://cog.run/python>
- Examples: <https://github.com/replicate/cog-examples>
- Template: <https://github.com/replicate/cog-template>

## When to use this skill

- You have model code, weights, or a HuggingFace/GitHub project you want to host on Replicate.
- You're writing or editing a `cog.yaml`, `predict.py`, or `train.py`.
- For pushing a built model to Replicate, see `publish-models`.
- For running existing Replicate models, see `run-models`.

## Prerequisites

- Docker running locally.
- Cog installed: `brew install replicate/tap/cog` or `sh <(curl -fsSL https://cog.run/install.sh)`.
- Optional: `cog init` to scaffold `cog.yaml` and `predict.py`.

## Project layout

The canonical Replicate model layout:

```
cog.yaml
predict.py
weights.py                 # optional download helpers
requirements.txt
cog-safe-push-configs/
  default.yaml             # see publish-models skill
.github/workflows/
  ci.yaml
script/                    # github.com/github/scripts-to-rule-them-all
  lint
  test
  push
```

## cog.yaml essentials

A modern config for a GPU model:

```yaml
build:
  gpu: true
  cuda: "12.8"
  python_version: "3.12"
  python_requirements: requirements.txt
  system_packages:
    - libgl1
    - libglib2.0-0
predict: predict.py:Predictor
```

Notes:

- Pin Python to a specific minor version, and pin every line in `requirements.txt`. Floating versions break cold boots.
- Use `python_requirements` over inline `python_packages` once the list grows.
- `cuda` follows your torch wheel (e.g. `12.8` paired with `torch==2.7.1+cu128`).
- Add `train: train.py:train` if your model is fine-tunable.
- Add `image: r8.im/owner/name` to enable bare `cog push`.

For async predictors with continuous batching:

```yaml
concurrency:
  max: 32
```

## predict.py essentials

```python
from cog import BasePredictor, Input, Path

class Predictor(BasePredictor):
    def setup(self) -> None:
        """One-time loads. Heavy work goes here, not in predict()."""
        self.model = load_model("weights/")

    def predict(
        self,
        prompt: str = Input(description="Text prompt for generation"),
        seed: int = Input(description="Random seed; leave blank for random", default=None),
        num_steps: int = Input(description="Number of denoising steps", ge=1, le=50, default=20),
        output_format: str = Input(description="Output image format", choices=["webp", "jpg", "png"], default="webp"),
    ) -> Path:
        """Run a single prediction."""
        if not prompt.strip():
            raise ValueError("prompt cannot be empty")
        out = self.model.generate(prompt, seed=seed, steps=num_steps)
        return Path(out)
```

Input rules:

- Every input needs a `description`. The description shows up in the model schema and on Replicate's web UI.
- Use `ge`/`le` for numeric bounds, `choices=[...]` for enums, `regex=` for strings.
- Use `cog.Path` for file inputs and outputs, never raw bytes.
- Use `cog.Secret` for any token-like input (HF tokens, API keys), never plain `str`.
- Provide a default that's inside `choices` for categorical inputs.
- Validate inputs early in `predict()` and raise `ValueError`.

Streaming text output (for LLMs):

```python
from cog import BasePredictor, Input, ConcatenateIterator

class Predictor(BasePredictor):
    def predict(self, prompt: str = Input(description="Prompt")) -> ConcatenateIterator[str]:
        for token in self.model.stream(prompt):
            yield token
```

Async predictor with continuous batching (paired with `concurrency.max` in cog.yaml):

```python
from cog import BasePredictor, Input, AsyncConcatenateIterator

class Predictor(BasePredictor):
    async def setup(self) -> None:
        self.engine = await load_async_engine()

    async def predict(
        self,
        prompt: str = Input(description="Prompt"),
    ) -> AsyncConcatenateIterator[str]:
        async for token in self.engine.generate(prompt):
            yield token
```

Dynamic `choices` from on-disk assets (e.g. a `voices/` directory of audio samples):

```python
from pathlib import Path as _P
AVAILABLE_VOICES = sorted(p.stem for p in _P("voices").glob("*.wav"))

class Predictor(BasePredictor):
    def predict(
        self,
        speaker: str = Input(description="Voice", choices=AVAILABLE_VOICES, default=AVAILABLE_VOICES[0]),
    ) -> Path: ...
```

## Loading weights fast

Cold boot dominates user-perceived latency. Three patterns, ranked by simplicity:

### 1. Bake weights into the image at build time

Best for small or medium weights (< 5GB) that you want zero-cold-boot for.

For torchvision:

```python
import os
os.environ["TORCH_HOME"] = "."  # set before importing torch
import torch
from torchvision import models
```

For HuggingFace:

```python
import os
os.environ["HF_HUB_CACHE"] = "./.cache"
os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
```

Then download once during `cog build` (e.g. in a `run:` step or by running a small fetcher script as part of the build). The weights become part of the image layer.

### 2. Pull from `weights.replicate.delivery` with pget

Best for large weights, or when you want to share weights across multiple models. `pget` is Replicate's parallel HTTP fetcher.

In `cog.yaml`:

```yaml
build:
  run:
    - curl -o /usr/local/bin/pget -L "https://github.com/replicate/pget/releases/download/v0.8.2/pget_linux_x86_64"
    - chmod +x /usr/local/bin/pget
```

In `setup()`:

```python
import subprocess
from pathlib import Path

WEIGHTS_URL = "https://weights.replicate.delivery/default/my-model/weights.tar"
WEIGHTS_DIR = Path("weights")

class Predictor(BasePredictor):
    def setup(self) -> None:
        if not WEIGHTS_DIR.exists():
            # -x extracts tar in-memory; default concurrency is 4 * NumCPU
            subprocess.check_call(["pget", "-x", WEIGHTS_URL, str(WEIGHTS_DIR)])
        self.model = load_from(WEIGHTS_DIR)
```

For multiple files in one shot:

```python
manifest = "\n".join([
    f"{base}/unet.safetensors weights/unet.safetensors",
    f"{base}/vae.safetensors  weights/vae.safetensors",
    f"{base}/text_encoder.safetensors weights/text_encoder.safetensors",
])
subprocess.run(["pget", "multifile", "-"], input=manifest, text=True, check=True)
```

### 3. HuggingFace Hub with hf_transfer

Set `HF_HUB_ENABLE_HF_TRANSFER=1` and use `huggingface_hub.snapshot_download` or `from_pretrained`. Faster than vanilla HF downloads. Use a `cog.Secret` input for gated models.

## Weight cache for user-supplied weights

For LoRAs or any weights URL the user passes at predict time, use a sha256-keyed disk cache with LRU eviction:

```python
import hashlib, shutil, subprocess
from pathlib import Path

class WeightsDownloadCache:
    def __init__(self, cache_dir: str = "/tmp/weights-cache", min_disk_free_gb: int = 10):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.min_disk_free = min_disk_free_gb * 1024**3

    def ensure(self, url: str) -> Path:
        key = hashlib.sha256(url.encode()).hexdigest()
        target = self.cache_dir / key
        if target.exists():
            target.touch()  # bump LRU mtime
            return target
        self._evict_until_room()
        subprocess.check_call(["pget", url, str(target)])
        return target

    def _evict_until_room(self) -> None:
        while shutil.disk_usage(self.cache_dir).free < self.min_disk_free:
            entries = sorted(self.cache_dir.iterdir(), key=lambda p: p.stat().st_mtime)
            if not entries:
                return
            entries[0].unlink()
```

See `replicate/cog-flux/weights.py` for a production version that handles HF, CivitAI, Replicate, and arbitrary `.safetensors` URLs.

## Multi-LoRA composition

Reload only when the URL changes; compose two LoRAs with separate scales:

```python
class Predictor(BasePredictor):
    def setup(self) -> None:
        self.pipe = load_base_pipeline()
        self.loaded = {"main": None, "extra": None}

    def _ensure_lora(self, slot: str, url: str | None) -> None:
        if url == self.loaded[slot]:
            return
        if self.loaded[slot] is not None:
            self.pipe.unload_lora_weights(adapter_name=slot)
        if url:
            path = self.cache.ensure(url)
            self.pipe.load_lora_weights(str(path), adapter_name=slot)
        self.loaded[slot] = url

    def predict(
        self,
        prompt: str = Input(description="Prompt"),
        lora_url: str = Input(description="Primary LoRA URL", default=None),
        lora_scale: float = Input(description="Primary LoRA scale", ge=0.0, le=2.0, default=1.0),
        extra_lora_url: str = Input(description="Optional second LoRA URL", default=None),
        extra_lora_scale: float = Input(description="Second LoRA scale", ge=0.0, le=2.0, default=1.0),
    ) -> Path:
        self._ensure_lora("main", lora_url)
        self._ensure_lora("extra", extra_lora_url)
        adapters = [s for s, u in self.loaded.items() if u]
        scales = [lora_scale if s == "main" else extra_lora_scale for s in adapters]
        if adapters:
            self.pipe.set_adapters(adapters, adapter_weights=scales)
        return Path(self.pipe(prompt).images[0].save("/tmp/out.png"))
```

## Cold-boot tricks

From production diffusion models like `replicate/cog-flux` and `replicate/cog-flux-kontext`:

- Set perf flags once in `setup()`:
  ```python
  import torch
  torch.set_float32_matmul_precision("high")
  torch.backends.cuda.matmul.allow_tf32 = True
  torch.backends.cudnn.benchmark = True
  ```
- Compile and warm up:
  ```python
  self.model = torch.compile(self.model, dynamic=True)
  _ = self.predict(prompt="warmup", num_steps=1)  # absorbs compile cost in setup
  ```
- Load big weights with meta device + `assign=True` to avoid double-allocating:
  ```python
  with torch.device("meta"):
      model = build_model_skeleton()
  state = torch.load("weights.pt", map_location="cpu")
  model.load_state_dict(state, assign=True)
  ```
- Share VAE / text encoder across multiple pipelines (e.g. base + img2img + inpaint) instead of loading three copies.
- For fp8/int8, save quantized weights ahead of time and load directly; don't quantize at boot.

## Local development

```
cog init                                    # scaffold cog.yaml + predict.py
cog predict -i prompt="hello"               # build + run a single prediction
cog predict -i image=@input.jpg -o out.png  # file inputs and outputs
cog serve -p 8393                           # HTTP server matching production
cog exec python                             # interactive shell inside the build env
```

## Building

```
cog build -t my-model
cog build --separate-weights -t my-model    # weights in their own image layer
cog build --secret id=hf,src=$HOME/.hf_token -t my-model
```

Tips:

- Use `--separate-weights` for any model with weights > ~1GB. It speeds up cold boots and registry pushes.
- Use `--mount=type=cache,target=/root/.cache/pip` in `run:` steps to cache pip across builds.
- Use `--secret` instead of `ARG` to keep tokens out of image history.
- The default Cog base image (`--use-cog-base-image=true`) is faster than rolling your own.

## Training

If your model supports fine-tuning, add `train: train.py:train` to `cog.yaml` and write a `train()` function that returns `TrainingOutput(weights=Path("model.tar"))`. The predictor then accepts the URL via `setup(self, weights)` or the `COG_WEIGHTS` env var. See <https://cog.run/training> and `replicate/flux-fine-tuner` for a full example.

## Guidelines

- Keep `setup()` for one-time loads; keep `predict()` fast and deterministic in shape.
- Pin Python and every dependency. Use `numpy<2` if your torch is older.
- Always describe every input. Schemas without descriptions are unusable on the web UI.
- Use `cog.Path` for files and `cog.Secret` for tokens.
- Pin `pget` to a specific release (`v0.8.2`) for reproducibility.
- Set `HF_HUB_ENABLE_HF_TRANSFER=1` whenever you call HuggingFace Hub.
- Set `TRANSFORMERS_OFFLINE=1` after weights are loaded to prevent runtime HF lookups.
- Test with `cog predict` before pushing. If it doesn't work locally, it won't work in production.

## Production references

- <https://github.com/replicate/cog-examples> — minimal patterns (resnet, hello-world, streaming, training)
- <https://github.com/replicate/cog-template> — scaffolder for new model repos
- <https://github.com/replicate/cog-flux> — multi-variant FLUX models, weights cache, fp8 + torch.compile
- <https://github.com/replicate/cog-flux-kontext> — meta-device loading, warmup compilation
- <https://github.com/replicate/cog-vllm> — async LLM server with continuous batching, training-as-packaging
- <https://github.com/replicate/cog-comfyui> — ComfyUI workflows as a Cog model, custom-node helpers
- <https://github.com/replicate/flux-fine-tuner> — multi-LoRA composition, shared pipeline components
- <https://github.com/replicate/vibevoice> — TTS with dynamic `choices`, minimal cog.yaml
- <https://github.com/replicate/pget> — parallel weights fetcher
