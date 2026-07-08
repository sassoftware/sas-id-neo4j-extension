---
sidebar_position: 22
---

# Decision Node - Neo4j Generate Cypher

The **Neo4j Generate Cypher** node converts natural-language requests into valid [Cypher](https://neo4j.com/docs/getting-started/cypher/) query statements against a connected Neo4j database.

For example, a user can provide a request such as:

> "Show me the 10 most sold products between January and June last year."

The node uses a Large Language Model (LLM) to analyze the request and generate the corresponding Cypher query.

### Features

- Converts natural-language questions into Cypher query statements
- Designed for data retrieval and analysis scenarios
- Integrates with a connected Neo4j graph database
- Uses an LLM to generate Cypher automatically

### Limitations

- Only **read/query operations** are supported
- **CREATE**, **UPDATE**, and **DELETE** statements are not generated

> ❗**Note:** The current release supports only **Azure OpenAI** models.

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
