#!/bin/bash
# Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
PY_EXEC=$(which python3)
if [ -z "$PY_EXEC" ]; then
  echo "Python3 is not installed or not in PATH. Please install Python3 and try again."
  exit 1
fi

SERVER=$1
USER=$2
PASSWORD=$3

export BEARER_TOKEN=$(curl -sk -X POST "https://${SERVER}/SASLogon/oauth/token" \
  -u "sas.cli:" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=${USER}&password=${PASSWORD}" \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

$PY_EXEC ./createDNT.py \
  --server "$SERVER" \
  --token "$BEARER_TOKEN" \
  --dntCodeFile "../src/neo4j_generateCypher.sas" \
  --dntParameterFile "../src/neo4j_generateCypher_parameters.sas" \
  --nodeName "Neo4j Generate Cypher" \
  --nodeIcon "DNT_THEME3" \
  --nodeColor "5" \
  --nodeDescription "Generate Neo4j Cypher statement for the input user prompt."

echo "---------------------------------------------"

$PY_EXEC ./createDNT.py \
  --server "$SERVER" \
  --token "$BEARER_TOKEN" \
  --dntCodeFile "../src/neo4j_dataQuery.sas" \
  --dntParameterFile "../src/neo4j_dataQuery_parameters.sas" \
  --nodeName "Neo4j Data Query" \
  --nodeIcon "DNT_THEME3" \
  --nodeColor "5" \
  --nodeDescription "Retrieve data from neo4j database."

