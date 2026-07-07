---
sidebar_position: 17
---

## Run Neo4j via Docker Image

To run Neo4j via Docker Image execute the following steps on your Viya server:

### 1. Create the Directory Structure
```
cd ~
mkdir -p neo4j/data neo4j/logs
cd neo4j
```

### 2. Pull the Neo4j Docker Image
```
docker pull neo4j
```

### 3. Start the Neo4j Container
This command will:
* Start a container named id-neo4j
* Expose the HTTP and Bolt ports
* Persist data and logs on the host
* Set the default password for the neo4j user
```
docker run \
  --name id-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -d \
  -v $HOME/neo4j/data:/data \
  -v $HOME/neo4j/logs:/logs \
  --env NEO4J_AUTH=neo4j/Orion123 \
  neo4j:latest
```
❗ Note
Ensure that the configured ports are accessible externally.
If required, adjust the port mappings, for example:
```
-p 8080:7474 -p 8089:7687
```
For additional details, refer to the official [Neo4j documentation](
https://neo4j.com/docs/operations-manual/current/docker/introduction/)
