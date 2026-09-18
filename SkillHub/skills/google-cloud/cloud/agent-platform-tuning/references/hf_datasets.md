# Huggingface Dataset References

This document provides references for various datasets used in Agent Platform
Tuning.

## How to use datasets

When using a dataset for tuning, it is recommended to first analyze the dataset to understand its structure and content. For more information on data preparation and formatting, please refer to [Data Preparation for Tuning](data_prep.md).

To download the entire dataset, the following script can be used:

```python
from datasets import load_dataset
dataset = load_dataset("username/dataset_name")
```

To load a specific split, the following script can be used:

```python
from datasets import load_dataset
dataset = load_dataset("username/dataset_name", split="split_name")
```

For larger datasets, it might be helpful to subset the dataset and use only
portions of the dataset as required by the specific task requested. Either use
the splits defined in the huggingface website (ex. `default`) or offer to
partition the dataset for the user. Ensure that the user can see some examples
of the dataset before proceeding.

[!IMPORTANT]
**CRITICAL: Ask for Confirmation and Column Selection.**
Do not proceed with dataset preparation or upload until you perform the
following steps and get user confirmation:
1. **Dataset and Split Confirmation:** Present the dataset and available splits
    to the user and have them confirm which to use. Additionally, show a few
    samples to the user for preview.
2. **Column Selection:** The tuning entrypoint requires mapping source columns to the target format (either `prompt`/`completion` or `messages` format). You must:
    - Provide a list of all available columns in the selected dataset split.
    - Recommend which columns should be mapped to `prompt` (or user message) and `completion` (or assistant response), offering a few reasonable options if applicable.
    - Ask the user to confirm the column mapping or specify which columns to use.

## Datasets List

Each dataset includes a brief description of the dataset type and some usage
hints. The hints are **not** the only way to use these datasets but offer some
suggestions based on the corresponding dataset.

[!IMPORTANT]
Examine the hints since they include some information about the dataset. These
include comments about the contents of the dataset that may be pertinent to the
users request.

### General and Reasoning Tasks

#### Mathematical Reasoning

| Name | Description | Sample Count (Split) | Usage Hints |
|---|---|---|---|
| [open-r1/OpenR1-Math-220k](https://huggingface.co/datasets/open-r1/OpenR1-Math-220k) | A dataset of math problems and solutions. | 93,700 (default) - 220,000 (full) | The main columns are problem and solution. Some other helpful columns are answer, problem_type, question_type, and messages. |
| [AI-MO/NuminaMath-TIR](https://huggingface.co/datasets/AI-MO/NuminaMath-TIR) | A dataset for improving model performance in complex logic and calculations. | N/A | Good choice for mathematical reasoning. |

#### Instruction Following

| Name | Description | Sample Count (Split) | Usage Hints |
|---|---|---|---|
| [argilla/ifeval-like-data](https://huggingface.co/datasets/argilla/ifeval-like-data) | A dataset that involves instruction following. | 550,000 (default), 56,000 (filtered) | There are multiple languages in this dataset. Prompt the user with this dataset if specific languages are expected. Filter accordingly |
| [HuggingFaceTB/smoltalk2](https://huggingface.co/datasets/HuggingFaceTB/smoltalk2) | Enhancing broad instruction-following capabilities. | N/A | This needs to be subsetted. as the initial dataset is very large and covers a wide range of tasks. |

#### Multilingual Support

| Name | Description | Sample Count (Split) | Usage Hints |
|---|---|---|---|
| [CohereForAI/aya_dataset](https://huggingface.co/datasets/CohereForAI/aya_dataset) | Expanding linguistic capabilities across diverse languages. | N/A | Contains multi-language instruction following data. |

### Specialized and Technical Tasks

#### Programming & Coding

| Name | Description | Sample Count (Split) | Usage Hints |
|---|---|---|---|
| [ise-uiuc/Magicoder-Evol-Instruct-110K](https://huggingface.co/datasets/ise-uiuc/Magicoder-Evol-Instruct-110K) | Code generation dataset. | 110,000 | Suitable for advancing coding capabilities. |
| [open-r1/datasets](https://huggingface.co/open-r1/datasets) | Specialized programming & reasoning data. | N/A | General source for open reasoning technical data. |

#### Tool Use & Integration

| Name | Description | Sample Count (Split) | Usage Hints |
|---|---|---|---|
| [gorilla-llm/Berkeley-Function-Calling-Leaderboard](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard) | Adhere to constraints and use external systems. | N/A | High-quality tool usage and function calling data. |
| [Bingguang/HardGen](https://huggingface.co/datasets/Bingguang/HardGen) | Evaluating handling complex tools and constraints. | N/A | Validated for tool use integration tasks. |

