# ID-Neo4j

**ID-Neo4j** provides decision nodes for [SAS Intelligent Decisioning](https://go.documentation.sas.com/doc/en/edmcdc/default/edmwn/titlepage.htm) to seamlessly integrate [Neo4j](https://neo4j.com/docs/) into decision flows.

## Neo4j Generate Cypher

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

---

## Neo4j Data Query

The **Neo4j Data Query** node executes Cypher statements directly against a Neo4j database.

### Supported Operations

- Query (MATCH/RETURN)
- CREATE
- UPDATE
- DELETE

When executing a query, the returned results are displayed in a **data grid** for easy inspection and analysis.

### Use Cases

- Execute Cypher statements
- Create, update, or delete graph data
- Retrieve and explore data stored in Neo4j
- Validate and test Cypher queries


When executing a query, the returned results are displayed in a **data grid** for easy inspection and analysis.

### Limitations

- Query results must be returned in a **flat tabular format** suitable for display in the data grid.
- Nested structures such as maps, nested objects, deeply nested collections, or complex graph result structures are not supported.
- Queries should be written to return scalar values or flattened columns.


--- 
### Query Data in Neo4j
![](./static/id-neo4j-nodes.gif)

<details>
<summary>Create data in Neo4j</summary>

![](./static/id-neo4j-create.gif)
</details>
<details>
<summary>Update data in Neo4j</summary>

![](./static/id-neo4j-upd.gif)
</details>
<details>
<summary>Delete data in Neo4j</summary>

![](./static/id-neo4j-delete.gif)
</details>

---

## Documentation

For full documentaion see [ID-Neo4j documentation](https://sassoftware.github.io/sas-id-neo4j-extension/).

---

## License

This project is licensed under the [Apache 2.0 License](LICENSE).
