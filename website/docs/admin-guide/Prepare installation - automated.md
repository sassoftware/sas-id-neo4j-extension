---
sidebar_position: 4
---

To use automated installation script to copy the resources from the Git repository follow the steps below.

* Go to the Linux server home directory
* Run commands to download node installation resources

    ```
    cd ~
    mkdir id-neo4j-dnt && cd id-neo4j-dnt
    wget https://raw.githubusercontent.com/sukckn/id-neo4j/main/data/DNT/inst/instDNT.sh
    chmod +x instDNT.sh && ./instDNT.sh
    rm instDNT.sh
    cd scripts
    ```
