---
sidebar_position: 21
---

# Decision Node - Neo4j Generate Cypher

This node generates a Cypher statement based on a user-defined prompt. It reads the Neo4j database schema and combines it with the user input before sending it to a Large Language Model (LLM). The LLM is restricted to generating **read-only Cypher queries**.

> ❗ **Note**: Currently, only Azure OpenAI models are supported.

## Input Parameters

| Name        | Type   | Description |
|-------------|--------|-------------|
| neo4j_db    | string | Name of the Neo4j database to query.If only one database is used in the decision flow, this field can be left empty. If multiple databases are used, this parameter must be specified. |
| user_prompt | string | Prompt describing the data query.Example: *List all customer names with phone numbers that start with "A"* |

## Output Parameters

| Name          | Type    | Description |
|---------------|---------|-------------|
| cypher_para   | string  | JSON-formatted parameters for the Cypher query.Example: `{"Name": "A"}` |
| cypher_stmt   | string  | Generated Cypher query. |
| error_code    | integer | Indicates success (`0`) or failure (non-zero). |
| error_msg     | string  | Error message (empty if successful). |
| llm_metrics   | string  | JSON containing LLM execution details (e.g., elapsed time, input tokens, output tokens). |
