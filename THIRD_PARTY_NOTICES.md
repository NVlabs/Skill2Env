# Third-party notices

This file documents skill2env's direct Python and build dependencies, documented host
tools, and generator container components. These components retain their respective
copyright and license terms. The license column summarizes the main component's
license; bundled code, documentation, and packaging may have additional terms in the
linked license files and notices.

Reviewed on 2026-09-16 against [pyproject.toml](pyproject.toml), [uv.lock](uv.lock),
[generator.Dockerfile](skill2env/generator.Dockerfile), and the host requirements in
[README.md](README.md#requirements). Transitive Python dependencies are recorded in
`uv.lock`; this is an inventory of the components below, not a complete transitive SBOM.

## Python and build dependencies

Resolved versions below come from `uv.lock`. The build backend, `setuptools`, has a
minimum version in `pyproject.toml` but is not pinned in that lockfile.

| Component / version | Copyright holder, where available | License | Source | License file / documentation |
| --- | --- | --- | --- | --- |
| harbor 0.16.0 (`==0.16.0`) | No holder named in the upstream LICENSE | Apache-2.0 | [Harbor framework](https://github.com/harbor-framework/harbor/tree/v0.16.0) | [LICENSE](https://raw.githubusercontent.com/harbor-framework/harbor/v0.16.0/LICENSE) |
| PyYAML 6.0.3 (`>=6.0`) | Ingy döt Net (2017–2021); Kirill Simonov (2006–2016) | MIT | [PyYAML](https://github.com/yaml/pyyaml/tree/6.0.3) | [LICENSE](https://raw.githubusercontent.com/yaml/pyyaml/6.0.3/LICENSE) |
| rich 15.0.0 (`>=13.9`) | Will McGugan (2020) | MIT | [Rich](https://github.com/Textualize/rich/tree/v15.0.0) | [LICENSE](https://raw.githubusercontent.com/Textualize/rich/v15.0.0/LICENSE) |
| setuptools (`>=68`, build backend) | No holder named in the upstream LICENSE | MIT | [setuptools](https://github.com/pypa/setuptools) | [LICENSE](https://raw.githubusercontent.com/pypa/setuptools/main/LICENSE) |

## Host runtime and build tools

These tools are installed separately on the host. Versions are selected by the user,
subject to the Python minimum version in `pyproject.toml`.

| Component / version | Copyright holder, where available | License | Source | License file / documentation |
| --- | --- | --- | --- | --- |
| Python / CPython (`>=3.12`) | Python Software Foundation; historical holders include BeOpen.com, CNRI, and Stichting Mathematisch Centrum | PSF-2.0, with historical and incorporated-software terms | [CPython](https://github.com/python/cpython) | [History and license, including incorporated software](https://docs.python.org/3.12/license.html) |
| uv | Astral Software Inc. | Apache-2.0 OR MIT | [uv](https://github.com/astral-sh/uv) | [LICENSE-APACHE](https://raw.githubusercontent.com/astral-sh/uv/main/LICENSE-APACHE), [LICENSE-MIT](https://raw.githubusercontent.com/astral-sh/uv/main/LICENSE-MIT) |
| Docker CLI and Docker Engine / Moby | Docker, Inc. and contributors | Apache-2.0; bundled components have additional notices | [CLI](https://github.com/docker/cli), [Moby](https://github.com/moby/moby) | [CLI LICENSE](https://raw.githubusercontent.com/docker/cli/master/LICENSE), [Moby LICENSE](https://raw.githubusercontent.com/moby/moby/master/LICENSE), [Moby NOTICE](https://raw.githubusercontent.com/moby/moby/master/NOTICE) |

## Generator container

`generator.Dockerfile` uses `node:22-bookworm-slim` and installs the packages listed
below. The base-image tag and APT packages are not pinned to immutable versions, so
their exact versions depend on the image and package repositories at build time.
The default Codex version is set in [generator.py](skill2env/generator.py) and can be
overridden with `--codex-version`.

| Component / version | Copyright holder, where available | License | Source | License file / documentation |
| --- | --- | --- | --- | --- |
| `node:22-bookworm-slim` image build scripts | Joyent, Inc.; Node.js contributors | MIT for the image build scripts; image contents have their own licenses | [Node image Dockerfile](https://github.com/nodejs/docker-node/blob/main/22/bookworm-slim/Dockerfile) | [Image repository LICENSE](https://raw.githubusercontent.com/nodejs/docker-node/main/LICENSE) |
| Debian 12 (Bookworm) base-system packages | Respective package authors and contributors, recorded in each package's copyright file | Multiple licenses, including GPL, LGPL, BSD, and MIT; per-package terms apply | [Debian Bookworm packages and sources](https://packages.debian.org/bookworm/) | [Debian license information](https://www.debian.org/legal/licenses/); `/usr/share/doc/<package>/copyright` in the image |
| Node.js 22.x | Node.js contributors; Joyent, Inc. and other Node contributors | MIT, with bundled third-party licenses | [Node.js](https://github.com/nodejs/node/tree/v22.x) | [LICENSE including bundled components](https://raw.githubusercontent.com/nodejs/node/v22.x/LICENSE) |
| npm (bundled with Node.js) | npm, Inc. and contributors | Artistic-2.0; dependencies retain their own licenses | [npm CLI](https://github.com/npm/cli) | [LICENSE in Node.js 22.x](https://raw.githubusercontent.com/nodejs/node/v22.x/deps/npm/LICENSE) |
| Yarn Classic (bundled by the base image; currently 1.22.22) | Yarn Contributors | BSD-2-Clause | [Yarn](https://github.com/yarnpkg/yarn/tree/v1.22.22) | [LICENSE](https://raw.githubusercontent.com/yarnpkg/yarn/v1.22.22/LICENSE) |
| `@openai/codex` (default 0.146.0) | OpenAI (2025); additional holders in NOTICE | Apache-2.0; MIT for code attributed in NOTICE | [Codex](https://github.com/openai/codex/tree/rust-v0.146.0) | [LICENSE](https://raw.githubusercontent.com/openai/codex/rust-v0.146.0/LICENSE), [NOTICE](https://raw.githubusercontent.com/openai/codex/rust-v0.146.0/NOTICE) |

The following are all packages explicitly installed by the Dockerfile's `apt-get
install` command. The linked Debian copyright records identify upstream sources,
additional copyright holders, and file-specific licenses. For the exact installed
versions and their dependencies, consult `/usr/share/doc/<package>/copyright` and
`/usr/share/common-licenses/` in the built image.

| Component | Copyright holder, where available | Main license / additional terms | Source | License file / documentation |
| --- | --- | --- | --- | --- |
| bash | Free Software Foundation, Inc. and other contributors | GPL-3.0-or-later; file-specific terms in copyright record | [Debian bash](https://packages.debian.org/bookworm/bash) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/b/bash/bash_5.2.15-2_copyright) |
| ca-certificates | Fumitoshi UKAI; Philipp Kern; Michael Shuler; Debian and Mozilla contributors | GPL-2.0-or-later for scripts; MPL-2.0 for Mozilla certificate data | [Debian ca-certificates](https://packages.debian.org/bookworm/ca-certificates) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/c/ca-certificates/ca-certificates_20250419_copyright) |
| curl | Daniel Stenberg and other contributors | curl license; file-specific terms in copyright record | [Debian curl](https://packages.debian.org/bookworm/curl) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/c/curl/curl_7.88.1-10+deb12u15_copyright) |
| file | Ian F. Darwin; Christos Zoulas; other contributors | BSD-2-Clause-like license with a copyright-placement condition; other file-specific terms | [Debian file](https://packages.debian.org/bookworm/file) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/f/file/file_5.44-3_copyright) |
| gh (GitHub CLI) | GitHub Inc.; other holders in copyright record | MIT (Expat); BSD-3-Clause for some bundled code | [Debian gh](https://packages.debian.org/bookworm/gh) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/g/gh/gh_2.23.0+dfsg1-1_copyright) |
| git | Linus Torvalds and other contributors | GPL-2.0-only; bundled code has additional terms | [Debian git](https://packages.debian.org/bookworm/git) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/g/git/git_2.39.5-0+deb12u3_copyright) |
| git-lfs | GitHub, Inc. and Git LFS contributors | MIT (Expat) | [Debian git-lfs](https://packages.debian.org/bookworm/git-lfs) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/g/git-lfs/git-lfs_3.3.0-1+deb12u1_copyright) |
| jq | Stephen Dolan; other holders in copyright record | MIT for jq; CC-BY-3.0 for documentation; other file-specific terms | [Debian jq](https://packages.debian.org/bookworm/jq) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/j/jq/jq_1.6-2.1+deb12u2_copyright) |
| tar | Free Software Foundation, Inc.; other contributors | GPL-3.0-or-later; file-specific terms in copyright record | [Debian tar](https://packages.debian.org/bookworm/tar) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/t/tar/tar_1.34+dfsg-1.2+deb12u1_copyright) |
| unzip | Info-ZIP (1990–2009) | Info-ZIP license (2009-Jan-02) | [Debian unzip](https://packages.debian.org/bookworm/unzip) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/u/unzip/unzip_6.0-28_copyright) |
| wget | Free Software Foundation, Inc. | GPL-3.0-or-later with an OpenSSL linking exception; GNU FDL for documentation | [Debian wget](https://packages.debian.org/bookworm/wget) | [Copyright](https://metadata.ftp-master.debian.org/changelogs/main/w/wget/wget_1.21.3-1+deb12u1_copyright) |

## SkillHub material

The collected skills have a separate [source and license inventory](SkillHub/skillhub_source_licenses.csv)
and [preserved license files](SkillHub/licenses/). See the [SkillHub README](SkillHub/README.md)
for details.
