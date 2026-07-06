#!/bin/bash
# Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

PY_EXEC=$(which python3)
if [ -z "$PY_EXEC" ]; then
  echo "Python3 is not installed or not in PATH. Please install Python3 and try again."
  exit 1
fi

NODE_NAME=$1
SERVER=$2
USER=$3
PASSWORD=$4

export BEARER_TOKEN=$(curl -sk -X POST "https://${SERVER}/SASLogon/oauth/token" \
  -u "sas.cli:" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=${USER}&password=${PASSWORD}" \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

$PY_EXEC ./deleteDNT.py \
  --server "$SERVER" \
  --token "$BEARER_TOKEN" \
  --nodeName "$NODE_NAME" \
