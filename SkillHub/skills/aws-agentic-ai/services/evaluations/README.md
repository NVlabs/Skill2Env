# Evaluations Service

> **Status**: Available

## Overview

Amazon Bedrock AgentCore Evaluations provides automated assessment tools to measure how well agents perform specific tasks, handle edge cases, and maintain consistency across different inputs and contexts. It uses **LLM-as-a-Judge** techniques to score agent behavior using both built-in and custom evaluators.

AgentCore Evaluations integrates with agent frameworks (**Strands Agents**, **LangGraph**) via instrumentation libraries (**OpenTelemetry**, **OpenInference**). Traces from agents are converted to a unified format and scored automatically.

## Key Concepts

### Evaluators

Resources that define how agent output is assessed. Each evaluator has a unique ARN:

- **Built-in**: `arn:aws:bedrock-agentcore:::evaluator/Builtin.Helpfulness` (public, all users — empty region/account is intentional for AWS-managed evaluators)
- **Custom**: `arn:aws:bedrock-agentcore:<region>:<account>:evaluator/<id>` (private, access-controlled)

### Evaluation Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Online** | Continuously monitors live production traffic | Production quality monitoring |
| **On-demand** | Evaluates specific spans/traces by ID | Debugging, issue investigation, build-time testing |

### Traces and Spans

- **Trace** — complete record of a single agent execution (contains one or more spans)
- **Span** — individual operation within a trace (tool call, model invocation, etc.)
- **Session** — logical grouping of related interactions from a single user/workflow
- **Tool Call** — span representing an agent's invocation of an external function or API

### LLM-as-a-Judge

Evaluation method using a language model to assess output quality. Reference-free — relies on the model's internal knowledge rather than ground-truth data. Enables scalable, consistent, customizable qualitative assessments.

## Built-in Evaluators

Pre-configured evaluators that cannot be modified. Use their ID in format `Builtin.EvaluatorName`:

| Evaluator | Description |
|-----------|-------------|
| `Builtin.Helpfulness` | Assesses how helpful the agent's response is |
| `Builtin.GoalSuccessRate` | Measures end-to-end task completion correctness |

Built-in evaluators support cross-region inference and use optimized prompt templates.

> **Note**: Built-in evaluator configurations (model, prompt template) cannot be modified.

## Custom Evaluators

Define your own evaluator model, evaluation instructions, and scoring schemas tailored to your use cases.

### Create a Custom Evaluator

```bash
aws bedrock-agentcore-control create-evaluator \
  --evaluator-name "my-custom-evaluator" \
  --description "Evaluates response accuracy for domain-specific questions" \
  --region us-east-1
```

### Manage Custom Evaluators

```bash
# List evaluators
aws bedrock-agentcore-control list-evaluators --region us-east-1

# Get evaluator details
aws bedrock-agentcore-control get-evaluator \
  --evaluator-id <EVALUATOR_ID> --region us-east-1

# Update evaluator
aws bedrock-agentcore-control update-evaluator \
  --evaluator-id <EVALUATOR_ID> --region us-east-1

# Delete evaluator
aws bedrock-agentcore-control delete-evaluator \
  --evaluator-id <EVALUATOR_ID> --region us-east-1
```

> **Evaluator locking**: When an enabled online evaluation uses a custom evaluator, the evaluator is automatically locked — no modifications or deletions allowed. Clone a new evaluator if changes are needed.

## Online Evaluation

Continuously monitors deployed agents using live production traffic with configurable sampling and filtering.

### Components

1. **Session sampling and filtering** — percentage-based sampling (e.g., 10%) or conditional filters
2. **Evaluators** — up to 10 per configuration (built-in + custom combined)
3. **Monitoring and analysis** — aggregated scores in dashboards, quality trends, session investigation

### Create with AgentCore CLI

> **Prerequisite**: Install the AgentCore CLI with `npm install -g @aws/agentcore`. See [Runtime Service](../runtime/README.md) for details.

```bash
agentcore add online-eval \
  --name "my_eval_config" \
  --runtime "my_agent_runtime" \
  --evaluator "Builtin.GoalSuccessRate" "Builtin.Helpfulness" \
  --sampling-rate 1.0 \
  --enable-on-create
```

> **Note**: Run from inside an AgentCore project directory (created with `agentcore create`). Then run `agentcore deploy` to create it in your AWS account.

### Create with AWS CLI

```bash
aws bedrock-agentcore-control create-online-evaluation-config \
  --online-evaluation-config-name "my_eval_config" \
  --description "Continuous evaluation of my agent" \
  --rule '{"samplingConfig": {"samplingPercentage": 80.0}}' \
  --data-source-config '{
    "cloudWatchLogs": {
      "logGroupNames": ["/aws/agentcore/my-agent-traces"],
      "serviceNames": ["my_agent.DEFAULT"]
    }
  }' \
  --evaluators '[{"evaluatorId": "Builtin.Helpfulness"}, {"evaluatorId": "Builtin.GoalSuccessRate"}]' \
  --evaluation-execution-role-arn "arn:aws:iam::<ACCOUNT_ID>:role/AgentCoreEvaluationRole" \
  --enable-on-create \
  --region us-east-1
```

### Create with Python SDK

```python
from bedrock_agentcore_starter_toolkit import Evaluation

eval_client = Evaluation()

config = eval_client.create_online_config(
    config_name="my_eval_config",
    agent_id="agent_myagent-ABC123xyz",
    sampling_rate=1.0,
    evaluator_list=["Builtin.GoalSuccessRate", "Builtin.Helpfulness"],
    config_description="Online Evaluation Config",
    auto_create_execution_role=True,
    enable_on_create=True
)

print(f"Config ID: {config['onlineEvaluationConfigId']}")
```

### Execution Control

```bash
# Pause a running evaluation
agentcore pause online-eval "my_eval_config"

# Resume a paused evaluation
agentcore resume online-eval "my_eval_config"
```

Execution states:
- **ENABLED** — actively processing traces and generating results
- **DISABLED** — configuration exists but job is paused

### Manage Online Evaluations

```bash
# List configurations
aws bedrock-agentcore-control list-online-evaluation-configs --region us-east-1

# Get configuration details
aws bedrock-agentcore-control get-online-evaluation-config \
  --online-evaluation-config-id <CONFIG_ID> --region us-east-1

# Update configuration
aws bedrock-agentcore-control update-online-evaluation-config \
  --online-evaluation-config-id <CONFIG_ID> --region us-east-1

# Delete configuration
aws bedrock-agentcore-control delete-online-evaluation-config \
  --online-evaluation-config-id <CONFIG_ID> --region us-east-1
```

## On-Demand Evaluation

Targeted assessment of specific spans or traces at any time. Specify exact span/trace IDs to evaluate.

**Use cases**:
- Investigate specific customer interactions
- Validate fixes for reported issues
- Analyze historical data for quality improvements
- Build-time testing during development

On-demand evaluation supports the same evaluators (built-in and custom) as online evaluation but provides precise control over which interactions to assess.

## Prerequisites

### Required Infrastructure

- AWS account with IAM permissions
- Amazon Bedrock access with model invocation permissions (for custom evaluators)
- Amazon CloudWatch with **Transaction Search** enabled
- ADOT (AWS Distro for OpenTelemetry) SDK instrumenting your agent

### IAM User Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:CreateEvaluator",
        "bedrock-agentcore:GetEvaluator",
        "bedrock-agentcore:ListEvaluators",
        "bedrock-agentcore:UpdateEvaluator",
        "bedrock-agentcore:DeleteEvaluator",
        "bedrock-agentcore:CreateOnlineEvaluationConfig",
        "bedrock-agentcore:GetOnlineEvaluationConfig",
        "bedrock-agentcore:ListOnlineEvaluationConfigs",
        "bedrock-agentcore:UpdateOnlineEvaluationConfig",
        "bedrock-agentcore:DeleteOnlineEvaluationConfig",
        "bedrock-agentcore:Evaluate"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::*:role/AgentCoreEvaluationRole*",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "bedrock-agentcore.amazonaws.com"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:Converse",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ConverseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/*",
        "arn:aws:bedrock:*:*:inference-profile/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:DescribeIndexPolicies",
        "logs:PutIndexPolicy",
        "logs:CreateLogGroup"
      ],
      "Resource": "*"
    }
  ]
}
```

### Service Execution Role

AgentCore Evaluations requires an IAM execution role. Create it automatically (recommended) or manually:

**Automatic** (AgentCore CLI):
```bash
# Role is created automatically during deploy
agentcore deploy
```

**Automatic** (SDK):
```python
eval_client.create_online_config(
    ...,
    auto_create_execution_role=True  # Creates role automatically
)
```

**Manual** — create a role with trust policy for `bedrock-agentcore.amazonaws.com` and permissions for CloudWatch read/write and Bedrock model invocation. See [Prerequisites (AWS Docs)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-prerequisites.html) for the complete policy.

## Limits

| Limit | Value |
|-------|-------|
| Evaluation configurations per region per account | 1,000 |
| Active configurations at any time | 100 |
| Evaluators per configuration | 10 |
| Input/output tokens per minute (large regions) | 1,000,000 |
| Sampling percentage range | 0.01% – 100% |
| Session idle timeout | 1 – 60 minutes (default: 15) |

## Instrumentation Setup

### Strands Agents

Strands Agents includes built-in OpenTelemetry instrumentation. Configure the ADOT exporter:

```python
# Traces are automatically exported when OTEL is configured
# Set environment variables:
# OTEL_EXPORTER_OTLP_ENDPOINT=<your-collector-endpoint>
# OTEL_RESOURCE_ATTRIBUTES=service.name=my_agent.DEFAULT
```

### LangGraph

Use OpenInference instrumentation for LangGraph agents:

```python
# Configure OpenInference instrumentation
# Traces are captured and exported to CloudWatch via ADOT
```

For agents hosted on AgentCore Runtime, follow the [Observability Service](../observability/README.md) setup guide.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No evaluation results | Traces not reaching CloudWatch | Verify ADOT instrumentation and log group configuration |
| Custom evaluator locked | Used by active online evaluation | Pause the evaluation before modifying, or clone the evaluator |
| Permission denied on create | Missing IAM actions | Add `bedrock-agentcore:CreateOnlineEvaluationConfig` and `iam:PassRole` |
| Low sampling coverage | Sampling rate too low | Increase `samplingPercentage` in configuration |
| Model invocation errors | Missing Bedrock permissions | Add `bedrock:InvokeModel` to execution role |

## Related Services

- **[Runtime Service](../runtime/README.md)**: Deploy agents that generate traces for evaluation
- **[Observability Service](../observability/README.md)**: Configure trace collection and monitoring
- **[Gateway Service](../gateway/README.md)**: Evaluate tool invocation accuracy for Gateway targets
- **[Agent Registry](../registry/README.md)**: Discover and catalog evaluated agents

## References

- [AgentCore Evaluations Overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html)
- [How It Works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/how-it-works-evaluations.html)
- [Built-in Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-evaluators-overview.html)
- [Custom Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/custom-evaluators.html)
- [Online Evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/online-evaluations.html)
- [On-demand Evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/on-demand-evaluations.html)
- [Prerequisites](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-prerequisites.html)
