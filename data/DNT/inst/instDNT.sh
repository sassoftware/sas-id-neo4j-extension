#!/usr/bin/env bash
# Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
cd ~
if [ ! -d "~/id-neo4j-dnt" ]; then
    mkdir -p ~/id-neo4j-dnt
fi
cd id-neo4j-dnt
wget https://github.com/sassoftware/sas-id-neo4j-extension/archive/refs/heads/main.zip
unzip main.zip "sas-id-neo4j-extension-main/data/DNT/scripts/*"
mv sas-id-neo4j-extension-main/data/DNT/* ./
rm -rf sas-id-neo4j-extension-main
rm main.zip
cd ~/id-neo4j-dnt/scripts
chmod +x *.sh
