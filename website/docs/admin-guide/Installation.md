---
sidebar_position: 20
---

To install the ID-Neo4j nodes in SAS Intelligent Decisioning, follow the steps below. You can perform the installation either from a Linux server or directly through SAS Studio.

## Option 1: Install from a Linux Server

### 1. Prepare the Installation Environment

Before installing the ID-Neo4j nodes, copy the installation resources to a Linux server. This can be either:

- The SAS Viya server, or
- A jump server with network connectivity to the SAS Viya environment.

You can obtain the installation resources using one of the following methods:

- [**Manual Preparation**](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Prepare%20installation%20-%20manual
)  
  Copy the required files directly from the Git repository.  

- [**Automated Preparation**](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Prepare%20installation%20-%20automated)

  Use the provided installation script to download the required resources automatically.  

### 2. Install the ID-Neo4j Nodes

[Deploy the ID-Neo4j nodes](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Install%20Decision%20Nodes) to SAS Intelligent Decisioning.

---

## Option 2: Install Through SAS Studio

### 1. Install the Nodes Using SAS Studio

Use the provided custom steps within a SAS Studio flow to [install the ID-Neo4j nodes](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Install%20via%20SAS%20Studio).

---

## Post-Installation Tasks

### 3. Install the Required Python Library

[Install the Python library](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/install-py-lib) that provides the runtime functionality for the Neo4j nodes. 

### 4. Configure Connection Parameters

Configure the parameters required to [connect to Neo4j](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Neo4j%20Database%20Parameters) and the [Large Language Model (LLM)](https://sassoftware.github.io/sas-id-neo4j-extension/admin-guide/Neo4j%20LLM%20Parameters). 

