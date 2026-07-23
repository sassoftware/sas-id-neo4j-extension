---
sidebar_position: 60
---

To uninstall the Neo4j nodes from Intelligent Decisioning folow instructions below.

* Run command from ```~/id-neo4j-dnt/scripts```
    ```
    ./deleteDNT.sh <node name> <server> <user> <password>
    ```

    | Parameter | Comment |
    | --- | --- |
    | node name | Name of the decision node (use quotes if it contains spaces)|
    | server | Viya server URL. If running from a jump server, ensure connectivity. |
    | user | Viya admin user id |
    | password | Viya user password |

**Example**
```
./deleteDNT.sh "my Node" myserver.sas.com viyaUser mypassword
```