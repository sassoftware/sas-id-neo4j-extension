---
sidebar_position: 100
---

> ❗ **Note**: Currently, only Azure OpenAI models are supported.

## Neo4j LLM Parameters
The node Neo4j Generate Cypher uses an LLM to generate Cypher queries. Configure the node via environment variable *NEO4J_GENERATE_CYPHER*.

| Parameter | Comment |
| --- | --- |
| model | LLM model (e.g. gpt-4.1-mini) |
| version | Model version. E.g. *2024-12-01-preview*|
| endpoint | API endpoint URL. E.g. https://sgerabc-gpt-mini.openai.azure.com |
| limit | Optional limit on returned records. |
| regenmax | Number of retries if syntax correction is required (default: 3) |
| key | API key. |

Parameters are separated by semicolons (;).

**Example**
```
NEO4J_GENERATE_CYPHER='model=gpt-4.1-mini;version=2024-12-01-preview;endpoint=https://sgerabc-gpt-mini.openai.azure.com;limit=0;regenmax=3;key=<API_KEY>;'

```
>❗**Important**: Variable name 'NEO4J_GENERATE_CYPHER' must be in upper case!
