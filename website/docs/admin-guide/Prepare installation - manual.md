---
sidebar_position: 3
---

To manually copy the resources from the Git repository follow the steps below.

* Go to the Linux server home directory
* Create the required directories:

    ```
    cd ~
    mkdir -p id-neo4j-dnt/scripts
    mkdir -p id-neo4j-dnt/src
    ```

* Copy files from Git repository to the respective Linux derectory:
    * [data/DNT/scripts](../../../data/DNT/scripts/) → ~/id-neo4j-dnt/scripts
    * [data/DNT/src](../../../data/DNT/src/) → ~/id-neo4j-dnt/src
* Make the scripts files executable:

    ```
    cd ~/id-neo4j-dnt/scripts
    chmod +x createDNT.sh
    chmod +x deleteDNT.sh
    ```