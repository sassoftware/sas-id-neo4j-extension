---
sidebar_position: 510
---

# Decision Node - Neo4j Data Query

The **Neo4j Data Query** node executes Cypher statements directly against a Neo4j database.

### Supported Operations

- Query (MATCH/RETURN)
- CREATE
- UPDATE
- DELETE

When executing a **query**, the returned results are displayed in a **data grid** for easy inspection and analysis.

### Use Cases

- Execute Cypher statements
- Create, update, or delete graph data
- Retrieve and explore data stored in Neo4j
- Validate and test Cypher queries


When executing a query, the returned results are displayed in a **data grid** for easy inspection and analysis.

### Limitations

- Query results **must** be returned in a **flat tabular format** suitable for display in the data grid.
- Nested structures such as maps, nested objects, deeply nested collections, or complex graph result structures are not supported and may lead to execution errors.
- Queries should be written to return scalar values or flattened columns.
- Cypher statements used to **modify data (INSERT, UPDATE, DELETE)** must **not return any results**.

**Supported Example**

```cypher
MATCH (p:Product)-[:SOLD_IN]->(r:Region)
RETURN p.name AS Product,
       r.name AS Region,
       p.sales AS Sales
```
**Not Supported Example**
```
MATCH (p:Product)-[:SOLD_IN]->(r:Region)
RETURN p, collect(r)
```


## Input Parameters

| Name        | Type   | Description |
|-------------|--------|-------------|
| `cypher_para` | string | JSON-formatted parameters for filtering data. Example: `{"Name": "A"}` |
| `cypher_stmt` | string | Cypher query to execute. |

## Output Parameters

| Name           | Type       | Description |
|----------------|------------|-------------|
| `neo4j_result`   | data grid  | Query result returned in tabular format. |
| `error_code`     | integer    | Indicates success (`0`) or failure (non-zero). |
| `error_msg`      | string     | Execution message. |
