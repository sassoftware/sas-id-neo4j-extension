---
sidebar_position: 9
---

# Configuration
After installing the Neo4j nodes, configure the parameters required to connect to Neo4j and the LLM.

#### Neo4j Database Parameters
Connection parameters are passed via the environment variable *NEO4J_CONOPTS*.

| Parameter | Comment |
| --- | --- |
| db | Name of the Neo4j database (case-sensitive) |
| server | Neo4j host (URL or IP address) |
| port | Neo4j port |
| uid | Neo4j user |
| pwd | Neo4j password |
| protocol | Neo4j protocol (neo4j, neo4j+s, bolt, bolt+s) |
| limit | Maximum number of records returned (0 = unlimited, default = 0) |

Parameters are separated by semicolons (;).

**Example;**
```
NEO4J_CONOPTS='db=neo4j;server=10.0.0.4;PORT=8089;uid=neo4j;pwd=Orion123;protocol=neo4j;limit=0;'
```

>❗**Note**: For multiple databases add the *database name* with an underscore as fuffix to the variable name *NEO4J_CONOPTS*.<br>
E.g. *NEO4J_CONOPTS_MYPRODUCTS*.<br>
In the decision flow set input variable 'neo4j_db' to value 'myproducts'.

>❗**Important**: The variable name 'NEO4J_CONOPTS' (and fuffix database name if set) must be in uppercase!
