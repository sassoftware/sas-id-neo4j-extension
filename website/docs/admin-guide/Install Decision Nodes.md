---
sidebar_position: 500
---

To install the Neo4j nodes into Intelligent Decisioning folow instructions below.

* Run command from ```~/id-neo4j-dnt/scripts```

    ```
    ./createDNT.sh <server> <user> <password>
    ```

    | Parameter | Comment |
    | --- | --- |
    | server | Viya server URL. If running from a jump server, ensure connectivity.
    | user | Viya admin user id |
    | password | Viya user password |


**Example:**
```
./createDNT.sh myserver.sas.com viyaUser mypassword
```
