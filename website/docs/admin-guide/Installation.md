---
sidebar_position: 20
---

To install the Neo4j nodes in SAS Intelligent Decisioning, complete the following steps:

1. **Prepare the Installation Environment**

    Before installing the Neo4j nodes, copy the installation resources to a Linux server. This can be either:
    * The SAS Viya server, or
    * A jump server with network connectivity to the SAS Viya environment.

    You can obtain the installation resources using one of the following methods:

    * [Manual preparation](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Prepare%20installation%20-%20manual): Copy the required files directly from the Git repository.
    * [Automated preparation](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Prepare%20installation%20-%20automated): Use the provided installation script to download the resources automatically.

2. **Install the Neo4j Nodes**

    [Install the Neo4j nodes](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Install%20Decision%20Nodes) into SAS Intelligent Decisioning.

3. **Install the Required Python Library**
    
    [Install the Python library](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/install-py-lib) that provides the runtime functionality for the Neo4j nodes. 

4. **Configure Connection Parameters**

    [Configure the parameters](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Neo4j%20Database%20Parameters) required to connect to both Neo4j and the Large Language Model (LLM). 
