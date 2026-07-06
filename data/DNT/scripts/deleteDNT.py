import argparse
import requests
import json
import os
 
def deleteDNT(nodeName, server, token):
    msg= '' 
     
    server= 'https://' +server    
    url= server +f"/decisions/decisionNodeTypes?name={nodeName}"
 
    payload = ""
    headers= {
      'Authorization': 'Bearer ' +token,
      'Content-Type': 'application/json' 
    }
 
    response= requests.request("GET", url, headers=headers, data=payload)
     
    if response.status_code == 401:
        msg= "Error: httpStatus " +str(response.status_code)
        msg= msg +" | Message: Access token invalid. Restart SAS Studio and try again."
        return msg
    elif response.status_code != 200:
        msg= "Error: httpStatus = " +str(response.status_code)
        try:
            msg= msg +" Message: " +response.json()['message']
        except:
            pass
        return msg
    else:
        nodeName_count= response.json()['count']
      
    if nodeName_count != 1:
        msg= f"Could not find Decision Node Type '{nodeName}'"
        return msg
    else:
        nodeName_id= response.json()['items'][0]['id']
    
    url= server +f"/decisions/decisionNodeTypes/{nodeName_id}"
 
    payload = ""
    headers= {
      'Authorization': 'Bearer ' +token,
      'Content-Type': 'application/json' 
    }
 
    response= requests.request("DELETE", url, headers=headers, data=payload)
 
    if response.status_code != 204:
        msg= "Error: httpStatus = " +str(response.status_code)
        try:
            msg= msg +" Message: " +response.json()['message']
        except:
            pass
        return msg
    else:
        msg= f"Deleted Decision Node Type '{nodeName}'"
    return msg

############################################################################### 
def main():
    parser = argparse.ArgumentParser(description="Delete DNT")

    parser.add_argument("--server", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--nodeName", required=True)

    args = parser.parse_args()
    print("Deleting DNT with the following parameters:")
    print(f"  Server: {args.server}")
    print(f"  Node Name: {args.nodeName}")

    result= deleteDNT(args.nodeName, args.server, args.token)

    print(result)

############################################################################### 
if __name__ == "__main__":
    main()
