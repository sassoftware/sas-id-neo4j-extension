# Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import argparse
import requests
import json
import os
 
def createDNT(nodeName, nodeIcon, nodeColor, nodeDescription, dntCodeFile, dntParameterFile, server, token):
    msg= '' 
    server= 'https://' +server
    url= server +"/decisions/decisionNodeTypes"
     
    payload = json.dumps({
      "name": f"{nodeName}",
      "hasProperties": True,
      "hasInputs": True,
      "hasOutputs": True,
      "inputDatagridMappable": False,
      "outputDatagridMappable": False,
      "inputDecisionTermMappable": True,
      "outputDecisionTermMappable": True,
      "hasProperties": True,
      "independentMappings": False,
      "type": "static",
      "themeId": f"{nodeIcon}",
      "color": nodeColor,
      "description": f"{nodeDescription}"
    })
     
    headers= {
      'Authorization': 'Bearer ' +token,
      'Content-Type': 'application/json' 
    }
     
    response= requests.request("POST", url, headers=headers, data=payload)
     
    if response.status_code == 401:
        msg= "Error: httpStatus " +str(response.status_code)
        msg= msg +" | Message: Access token invalid. Restart SAS Studio and try again."
        return msg
    elif response.status_code != 201:
        msg= "Error: httpStatus " +str(response.status_code)
        try:
            msg= msg +" | Message: " +response.json()['message']
        except:
            pass
        return msg
    else:
        dnt_id= response.json()['id']
     
    url= server +f"/decisions/decisionNodeTypes/{dnt_id}/content"
     
    try:
        with open(dntCodeFile, "r") as f:
            dntContent= f.read()
    except Exception as e:
        msg= f"Error reading DNT code file: {e}"
        return msg

    try:
        with open(dntParameterFile, "r") as f:
            dntParamsJSON= f.read()
    except Exception as e:
        msg= f"Error reading DNT parameter file: {e}"
        return msg

    try:
        dntParams= json.loads(dntParamsJSON)
    except Exception as e:
        msg= f"Error parsing DNT parameter file: {e}"
        return msg

    payload= json.dumps({
      "contentType": "DS2",
      "staticContent": dntContent,
      "nodeTypeSignatureTerms": dntParams
    })
     
    headers= {
      'Authorization': 'Bearer ' +token,
      'Content-Type': 'application/json' 
    }
     
    response= requests.request("POST", url, headers=headers, data=payload)
     
    if response.status_code != 201:
        msg= "Error: httpStatus " +str(response.status_code)
        try:
            msg= msg +" | Message: " +response.json()['message']
        except:
            pass
        return msg
    else:
        msg= f"Created Decision Type Node '{nodeName}'"
    return msg    

############################################################################### 
def main():
    parser = argparse.ArgumentParser(description="Create DNT")

    parser.add_argument("--server", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--dntCodeFile", required=True)
    parser.add_argument("--dntParameterFile", required=True)
    parser.add_argument("--nodeName", required=True)
    parser.add_argument("--nodeIcon", required=True)
    parser.add_argument("--nodeColor", required=True)
    parser.add_argument("--nodeDescription", required=True)

    args = parser.parse_args()
    print("Creating DNT with the following parameters:")
    print(f"  Server: {args.server}")
    print(f"  Node Name: {args.nodeName}")
    print(f"  Node Icon: {args.nodeIcon}")
    print(f"  Node Color: {args.nodeColor}")
    print(f"  Node Description: {args.nodeDescription}")
    print(f"  DNT Code File: {args.dntCodeFile}")
    print(f"  DNT Parameter File: {args.dntParameterFile}")

    result= createDNT(args.nodeName, args.nodeIcon, args.nodeColor, args.nodeDescription, args.dntCodeFile, args.dntParameterFile, args.server, args.token)

    print(result)

############################################################################### 
if __name__ == "__main__":
    main()
