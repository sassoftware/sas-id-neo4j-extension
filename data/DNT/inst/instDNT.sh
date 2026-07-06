#!/usr/bin/env bash
cd ~
if [ ! -d "~/id-neo4j-dnt" ]; then
    mkdir -p ~/id-neo4j-dnt
fi
cd id-neo4j-dnt
wget https://github.com/sukckn/id-neo4j/archive/refs/heads/main.zip
unzip main.zip "id-neo4j-main/data/DNT/*"
mv id-neo4j-main/data/DNT/* ./
rm -rf id-neo4j-main
rm main.zip
cd ~/id-neo4j-dnt/scripts
chmod +x *.sh
