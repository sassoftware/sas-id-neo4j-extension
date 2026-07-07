---
sidebar_position: 10
---

# Decision Node - Neo4j Data Query

This node executes a Cypher statement. When performing data queries, the results are returned in a tabular (data grid) format.

<details>
<summary><strong>Cypher Restrictions</strong></summary>

- Cypher statements used to **retrieve data (SELECT)** must return results in a **flat table structure**.
- Queries that produce nested or complex data structures may lead to execution errors.
- Cypher statements used to **modify data (INSERT, UPDATE, DELETE)** must **not return any results**.

</details>


## Input Parameters

| Name        | Type   | Description |
|-------------|--------|-------------|
| cypher_para | string | JSON-formatted parameters for filtering data.Example: `{"Name": "A"}` |
| cypher_stmt | string | Cypher query to execute. |

## Output Parameters

| Name           | Type       | Description |
|----------------|------------|-------------|
| neo4j_result   | data grid  | Query result returned in tabular format. |
| error_code     | integer    | Indicates success (`0`) or failure (non-zero). |
| error_msg      | string     | Error message (empty if successful). |
