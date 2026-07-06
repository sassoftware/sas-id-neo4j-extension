import os
import json
import re
from typing import Dict, Any, Tuple, List
from neo4j import GraphDatabase
from neo4j.time import Date, DateTime, Time
from neo4j.spatial import CartesianPoint, WGS84Point
import logging

class idNeo4j:
    def __init__(self, neo4j_db:str=''):
#        logging.basicConfig(level=logging.DEBUG)
        self.logger= logging.getLogger("idNeo4j")
        self.logger.info(f'Execute idNeo4j')
        ###########################################################
        # Get all nodes in the database
        ###########################################################
        self.SCHEMA_NODE_QUERY= """
        CALL db.schema.nodeTypeProperties()
        YIELD nodeLabels, propertyName, propertyTypes, mandatory
        RETURN nodeLabels, propertyName, propertyTypes, mandatory
        ORDER BY nodeLabels, propertyName
        """
        ###########################################################
        # Show ALL relationships, including types with zero properties,
        # and report: relType, propertyName, propertyTypes, mandatory,
        #             sourceNodeLabels, targetNodeLabels
        ###########################################################
        self.SCHEMA_REL_QUERY= """
        MATCH (a)-[r]->(b)
        WITH
        type(r)   AS relType,
        labels(a) AS sourceNodeLabels,
        labels(b) AS targetNodeLabels,
        collect(r) AS rels,
        count(*)   AS totalObservations
        
        // Collect all observed property keys across the group
        WITH
        relType, sourceNodeLabels, targetNodeLabels, rels, totalObservations,
        [x IN reduce(acc = [], rel IN rels | acc + keys(rel)) | x] AS flattenedKeys
        
        // De-duplicate keys without APOC
        WITH
        relType, sourceNodeLabels, targetNodeLabels, rels, totalObservations,
        reduce(s = [], k IN flattenedKeys | CASE WHEN k IN s THEN s ELSE s + k END) AS propNames
        
        // Ensure a row even if there are NO properties at all
        UNWIND (CASE WHEN size(propNames) = 0 THEN [NULL] ELSE propNames END) AS propertyName
        
        // Compute observed types (skip NULLs), and "mandatory" flag
        WITH
        relType, sourceNodeLabels, targetNodeLabels, rels, totalObservations, propertyName,
        // Collect raw type strings for non-null values of this property across the group
        [v IN [rel IN rels | CASE WHEN propertyName IS NOT NULL THEN rel[propertyName] ELSE NULL END]
            WHERE v IS NOT NULL
            | valueType(v)                      // built-in, no APOC
        ] AS rawTypes,
        size([
            rel IN rels
            WHERE propertyName IS NOT NULL AND rel[propertyName] IS NOT NULL
            | 1
        ]) AS propertyObservations
        
        // Normalize "… NOT NULL" suffix and de-duplicate types
        WITH
        relType, sourceNodeLabels, targetNodeLabels, propertyName, totalObservations, propertyObservations,
        [t IN rawTypes | replace(t, ' NOT NULL', '')] AS nnTypes
        WITH
        relType, sourceNodeLabels, targetNodeLabels, propertyName, totalObservations, propertyObservations,
        reduce(s = [], t IN nnTypes | CASE WHEN t IN s THEN s ELSE s + t END) AS propertyTypes
        
        RETURN
        relType,
        propertyName,
        propertyTypes,                                     // e.g. ["INTEGER","STRING","LIST<INTEGER>","BOOLEAN","ZONED DATETIME"]
        CASE
            WHEN propertyName IS NULL THEN false             // type had no properties at all
            ELSE propertyObservations = totalObservations    // property present on every relationship in the group
        END AS mandatory,
        sourceNodeLabels,
        targetNodeLabels
        ORDER BY relType, propertyName;
        """
        
        ###########################################################
        # Neo4j connection settings
        ###########################################################
        conopts_keys=['db', 'server', 'port', 'uid', 'pwd', 'protocol']

        if neo4j_db:
            self.neo4j_conopts_name= "NEO4J_CONOPTS_" +neo4j_db.upper()
        else:
            self.neo4j_conopts_name= "NEO4J_CONOPTS"

        # read the connection parameters from environment variable
        NEO4J_CONOPTS=os.environ.get(self.neo4j_conopts_name, '')
        #if NEO4J_CONOPTS is empty (not set) we try to read it from the file casconfig_usermods.lua assuming we are 
        # running in ID test mode where environment variables are not set but parameters are stored in the casconfig_usermods.lua file
        if not NEO4J_CONOPTS:
            NEO4J_CONOPTS= self.get_var_from_usermods(self.neo4j_conopts_name)

        # parse connection parameters 
        neo4j_conopts= self.parse_parameters(NEO4J_CONOPTS)

        # check if parameters are missing
        self.conopts_keys_missing= []
        for k in conopts_keys:
            if k not in list(neo4j_conopts):
                self.conopts_keys_missing.append(k)
    
        try:
            neo4j_protocol= neo4j_conopts['protocol']
        except:
            neo4j_protocol= ''
        try:
            neo4j_server= neo4j_conopts['server']
        except:
            neo4j_server= ''
        try:
            neo4j_port= neo4j_conopts['port']
        except:
            neo4j_port= None
        self.NEO4J_URL= f"{neo4j_protocol}://{neo4j_server}:{neo4j_port}"
        
        try:
            self.NEO4J_USER= neo4j_conopts['uid']
        except:
            self.NEO4J_USER= None
        try:
            self.NEO4J_PASSWORD= neo4j_conopts['pwd']
        except:
            self.NEO4J_PASSWORD= None
        try:
            self.NEO4J_DATABASE= neo4j_conopts['db']
        except:
            self.NEO4J_DATABASE= None    
        try:
            self.NEO4J_LIMIT= int(neo4j_conopts['limit'])
        except:
            self.NEO4J_LIMIT= 0
            
        if self.NEO4J_LIMIT < 0:
            self.NEO4J_LIMIT= 0

        self.logger.debug(f"Neo4j Connection URL: {self.NEO4J_URL}, User: {self.NEO4J_USER}, Database: {self.NEO4J_DATABASE}, Limit: {self.NEO4J_LIMIT}")
    ##############################################################################################
    # Load parameters CAS config usermods file. 
    # This is used when running in ID where environment variables are not set but parameters are stored in the casconfig_usermods.lua file
    ##############################################################################################
    def get_var_from_usermods(self, var_name):
        var_name= 'env.' + var_name.strip()
        try:
            with open('/cas/config/casconfig_usermods.lua', 'r') as file:
                for line in file:
                    line= line.strip()
                    if line[:2] == '--':
                        continue
                    pattern= rf"{var_name}\s*=\s*'([^']*)'"
                    match= re.search(pattern, line)
                    if match:
                        return match.group(1)
        except:
            pass
        return ''

    ###########################################################
    # parse the neo4j connection parameters that come in via 
    # environment variable
    ###########################################################
    def parse_parameters(self, para_string: str) -> dict:
        # Remove optional surrounding parentheses if present
        para_string= para_string.strip().strip('()')
    
        # Replace ":" (used like separator) with ";"
        para_string= re.sub(r':(?=\s*\w+\s*=)', ';', para_string)
    
        # Extract key=value pairs
        pattern= re.compile(r'(\w+)\s*=\s*([^;]+)')
    
        parameters= {}
        for key, value in pattern.findall(para_string):
            key = key.strip().lower() # enforce lowercase keys
            value= value.strip()
    
            # Optional cleanup: remove trailing ":" if still present
            value= value.rstrip(':')
            parameters[key]= value
        return parameters
        
    ###########################################################
    # return if all the Neo4j parameters haver a value
    ###########################################################
    def neo4j_parameters_ok(self):
        # check that all connection parameters have a value.
        if self.conopts_keys_missing:
            return f"Neo4j connection parameter(s) not set for environment variable '{self.neo4j_conopts_name}'. Missing parameters: {', '.join(self.conopts_keys_missing)}. Check environment variable settings!"
        return ''
    
    ###########################################################
    # get schema from the database
    # fetch nodes and relationships from the database
    ###########################################################
    def fetch_schema(self, tx) -> Dict[str, Any]:
        node_rows= list(tx.run(self.SCHEMA_NODE_QUERY))
        rel_rows= list(tx.run(self.SCHEMA_REL_QUERY))
        return {"nodes": node_rows, "rels": rel_rows}

    ###########################################################
    # takes the schema information from the database and 
    # puts it into a format which is better understandable for 
    # the LLM when creating the user prompt
    ###########################################################
    def schema_to_prompt(self, schema: Dict[str, Any]) -> str:
        # Compact, deterministic schema text for the LLM
        lines: List[str]= []
        lines.append("NODES (label-set -> propertyName: propertyTypes [mandatory?])")
        for r in schema["nodes"]:
            labels= ":".join(r["nodeLabels"])  # label sets, e.g., "Person" or "Person:Customer"
            ptypes= "|".join(r["propertyTypes"])
            mand= "mandatory" if r["mandatory"] else "optional"
            lines.append(f"- {labels} -> {r['propertyName']}: {ptypes} [{mand}]")

        lines.append("")
        lines.append("RELATIONSHIPS (source -[:TYPE]-> target -> propertyName: propertyTypes [mandatory?])")
        for r in schema["rels"]:
            src = ":".join(r["sourceNodeLabels"])
            tgt = ":".join(r["targetNodeLabels"])
            ptypes = "|".join(r["propertyTypes"]) if r["propertyTypes"] else ""
            mand = "mandatory" if r["mandatory"] else "optional"
            # Some rels have no properties; keep it readable
            if r["propertyName"]:
                lines.append(f"- ({src})-[:{r['relType']}]->({tgt}) -> {r['propertyName']}: {ptypes} [{mand}]")
            else:
                lines.append(f"- ({src})-[:{r['relType']}]->({tgt})")
        return "\n".join(lines)

    ###########################################################
    # Check with Neo4j if the cypher syntax is correct
    ###########################################################
    def check_cypher(self, session, cypher: str, params: Dict[str, Any]) -> Tuple[int, List]:
        try:
            result= session.run("EXPLAIN " + cypher, params)
        except Exception as e:
            chunks= re.findall(r'\{(.*?)\}', str(e), flags=re.DOTALL)
            result= {}        
            for chunk in chunks:
                # Split only on the first colon to keep colons inside the message
                if ':' in chunk:
                    key, value = chunk.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    result[key] = value 
            if len(chunks) == 0:
                return (-2, str(e)) 
            else:
                return (-2, result['neo4j_code'] +" | " +result['message'].replace("\'", "")) 

        summary= result.consume()
        notifs= getattr(summary, "gql_status_objects", []) or []

        if notifs[0].gql_status == '00001':
            return (0, '')    

        return (-1, notifs)

    ###########################################################
    # convert the data that come back from the database 
    # so we can put it into a datagrid
    ###########################################################
    def to_dg_value(self, value: Any) -> Any:
        # Boolean
        if isinstance(value, bool) == True:
            # Convert to 1 or 0
            if value:
                py= int(1)
            else:
                py= int(0)
            return py
        
        # Temporal
        if isinstance(value, DateTime):
            # Convert to Python datetime and format as 'YYYY-MM-DD HH:MM:SS'
            py= value.to_native()              # -> datetime.datetime
            return py.strftime('%Y-%m-%d %H:%M:%S.%f')
        if isinstance(value, Date):
            # Convert to Python datetime and format as 'YYYY-MM-DD'
            py= value.to_native()              # -> datetime.date
            return py.strftime('%Y-%m-%d')
        if isinstance(value, Time):
            py= value.to_native()              # -> datetime.time
            return py.strftime('%H:%M:%S.%f')

        # Spatial
        if isinstance(value, CartesianPoint):
            return json.dumps({"type": "Point", "crs": "cartesian", "srid": value.srid, "x": value.x, "y": value.y, **({"z": value.z} if hasattr(value, "z") else {})})
        if isinstance(value, WGS84Point):
            return json.dumps({"type": "Point", "crs": "wgs-84", "srid": value.srid, "longitude": value.x, "latitude": value.y, **({"height": value.z} if hasattr(value, "z") else {})})

        # Collections: convert recursively
        if isinstance(value, (list, tuple)):
            lst= [self.to_dg_value(v) for v in value]
            return json.dumps(lst)
        if isinstance(value, dict):
            dic= {k: self.to_dg_value(v) for k, v in value.items()}
            return json.dumps(dic)
        
        # Fallback: leave as-is for primitives or other already-serializable types
        return value

    ###########################################################
    # move the data that comes back from the database into a 
    # datagrid
    ###########################################################
    def move_to_dg(self, rows: list[Dict[str, Any]], type: str) -> Tuple[List, str]:
        dg= []
        dg_meta= {"metadata": []}
        dg_data= {"data": []}
        msg= ''
        
        self.logger.debug(f"Processed Cypher. Type: {type}. Processed rows: {len(rows)}")
        
        # if no data was returned from Neo4j set appropreate message and return
        if len(rows) == 0:
            msg= "No changes, no records."

        else:
            if type != 'read': 
                if len(rows) == 1:
                    msg= "1 record affected."
                else:
                    msg= f"{len(rows)} records affected."
            else:
                if len(rows) == 1:
                    msg= "Selected 1 record."
                else:
                    msg= f"Selected {len(rows)} records."

            # if dummy data returned don't create dom't put data in a datagrid
            if list(rows[0].keys())[0] == "__OK__":
                pass
                
            # if data was returned put data in a datagrid 
            else:
                # loop through first row to declare dg columns with data type
                for c in rows[0].keys():
                    col= {}
                    if isinstance(rows[0][c], bool):
                        col[c]= "bool"
                    elif isinstance(rows[0][c], int):
                        col[c]= "long"
                    elif isinstance(rows[0][c], float):
                        col[c]= "double"
                    else:
                        col[c]= "string"
                    dg_meta["metadata"].append(col.copy())
            
                # loop through all rows / columns to move data to the datagrid
                for row in rows:
                    colValues= []
                    # loop through columns in single row
                    for col in row.keys():
                        # convert data for dg if necessary
                        data= self.to_dg_value(row[col])
                        colValues.append(data)
                    dg_data['data'].append(colValues)

        # set metadata and data for datagrid
        dg.append(dg_meta)
        dg.append(dg_data)

        return dg, msg

    ###########################################################
    # check if the generated cypher is using the LIMIT clause
    ###########################################################
    def has_limit(self, cypher: str) -> bool:
        # naive check; encourages small result sets
        return re.search(r"(?i)\blimit\s+\d+\b", cypher) is not None	

    ###########################################################
    # read data from the database using the generated cypher
    ###########################################################
    def run_read_query(self, session, cypher: str, params: Dict[str, Any]):
        result= session.run(cypher, params)
        records= list(result)
        keys= result.keys()
        rows= [ {k: r.get(k) for k in keys} for r in records ]
        return keys, rows

    ###########################################################
    # function to retrieve the Neo4j schema
    ###########################################################
    def neo4jSchema(self):
        self.logger.info(f'Execute neo4jSchema()')
        neo4j_schema= error_msg= ""

        # check if are Neo4j parameters have values
        error_msg= self.neo4j_parameters_ok()
        if error_msg:
            error_code= -1
            self.logger.error(error_msg)
            return neo4j_schema,error_msg,error_code            

        neo4jConn= GraphDatabase.driver(self.NEO4J_URL, auth=(self.NEO4J_USER, self.NEO4J_PASSWORD), max_transaction_retry_time=0)
        with neo4jConn.session(database=self.NEO4J_DATABASE) as session:
            neo4j_schema= error_msg= ""
            error_code= 0
            # get database meta information and prepare for llm
            try:
                with session.begin_transaction() as neo:
                    schema= self.fetch_schema(neo)
            except Exception as e:
                error_code= -1
                error_msg= f"Error: {e} -> NEO4J_URL: {self.NEO4J_URL}"
                self.logger.error(error_msg)
                return neo4j_schema,error_msg,error_code
                
            neo4j_schema= self.schema_to_prompt(schema)

        self.logger.debug(f"Neo4j Schema: {neo4j_schema}")
        self.logger.debug(f"Error Message: {error_msg}")
        self.logger.debug(f"Error Code: {error_code}")
        return neo4j_schema,error_msg,error_code

    ###########################################################
    # Check with cypher syntax
    ###########################################################
    def validateCypher(self, cypher,params):
        self.logger.info(f'Execute validateCypher()')
        error_code= 0
        error_msg= ''

        self.logger.debug(f"Cypher to Validate: {cypher}")
        self.logger.debug(f"Parameters: {params}")

        # check if are Neo4j parameters have values
        error_msg= self.neo4j_parameters_ok()
        if error_msg:
            error_code= -1
            self.logger.error(error_msg)
            return error_msg,error_code            

        try:
            paramsDic= json.loads(params)
        except Exception as e:
            error_code= -1
            error_msg= f"Error in parameter 'params': {e}"
            self.logger.error(error_msg)
            return error_code,error_msg

        neo4jConn= GraphDatabase.driver(self.NEO4J_URL, auth=(self.NEO4J_USER, self.NEO4J_PASSWORD), max_transaction_retry_time=0)
        with neo4jConn.session(database=self.NEO4J_DATABASE) as session:
            error_code, msg= self.check_cypher(session, cypher, paramsDic)
            if error_code == 0:
                error_msg= ''
            elif error_code == -1:
                error_msg= msg[0].status_description
                self.logger.error(error_msg)
            elif error_code == -2:
                error_code= -1
                error_msg= msg  
                self.logger.error(error_msg)

        self.logger.debug(f"Error Message: {error_msg}")
        self.logger.debug(f"Error Code: {error_code}")
        return error_code,error_msg

    ###########################################################
    # check the cypher statement how we have to proceed with it (read, write, unknown)
    ###########################################################
    def classify_cypher(self, cypher: str) -> str:
        q = cypher.strip().lower()

        # keywords indicating writes anywhere in the query
        write_keywords = ["create", "merge", "set", "delete", "detach delete", "remove"]

        # if any write keyword appears → WRITE
        if any(k in q for k in write_keywords):
            return "write"

        # detect CALL separately
        if q.startswith("call"):
            if any(k in q for k in ["apoc.create", "apoc.merge", "apoc.do"]):
                return "write"
            return "read"

        # otherwise assume read if MATCH / RETURN present
        if q.startswith("match") or q.startswith("return") or " return " in q:
            return "read"

        # WITH queries (pure projection / filtering)
        if q.startswith("with"):
            return "read"

        return "unknown"

    ###########################################################
    # Query data from Neo4j for the passed in Cypher command
    ###########################################################
    def queryData(self, cypher,params):
        self.logger.info(f'Execute queryData()')
        self.logger.debug(f"Cypher to Execute: {cypher}")
        self.logger.debug(f"Parameters: {params}")

        dgOut= [{"metadata": []}, {"data": []}]
        neo4jResult= []
        error_code= 0

        # check if are Neo4j parameters have values
        error_msg= self.neo4j_parameters_ok()
        if error_msg:
            error_code= -1
            self.logger.error(error_msg)            
            return dgOut, error_code, error_msg
        
        neo4jConn= GraphDatabase.driver(self.NEO4J_URL, auth=(self.NEO4J_USER, self.NEO4J_PASSWORD), max_transaction_retry_time=0)    
        with neo4jConn.session(database=self.NEO4J_DATABASE) as session:
            # optional gentle cap (if model forgot LIMIT)
            if self.NEO4J_LIMIT > 0:
                if " return " in cypher.lower() and not self.has_limit(cypher):
                    cypher= cypher.rstrip(";") + f" LIMIT {self.NEO4J_LIMIT}"

            # execute - read data from the database
            if not params:
                params= '{}'
            # find out how to proceed with the query
            query_type = self.classify_cypher(cypher)

            if query_type == "read":
                self.logger.debug("Process Cypher with neo4j.execute_read().")
                try:
                    keys, rows= session.execute_read(lambda tx: self.run_read_query(tx, cypher, json.loads(params)))
                except Exception as e:
                    error_msg= f"Error Neo4j (cypher or parameters): {e}"
                    error_code= -1
                    self.logger.error(error_msg)            
                    return dgOut, error_code, error_msg
            elif query_type == "write":
                self.logger.debug("Process Cypher with neo4j.execute_write().")
                
                # we add a RETURN clause if no there yet to check later if records got updated
                q= cypher.strip().lower()                
                if " return " not in q:
                    if cypher.strip()[len(q)-1] == ';':
                        cypher= cypher_stmt.strip()[:len(q)-1]
                    cypher+=  ' RETURN "OK" AS __OK__'
                
                try:
                    keys, rows= session.execute_write(lambda tx: self.run_read_query(tx, cypher, json.loads(params)))
                except Exception as e:
                    error_msg= f"Error Neo4j (cypher or parameters): {e}"
                    error_code= -1
                    self.logger.error(error_msg)            
                    return dgOut, error_code, error_msg
            else:
                self.logger.debug("Process Cypher with neo4j.run().")
                try:
                    rows= session.run(cypher, json.loads(params))
                except Exception as e:
                    error_msg= f"Error Neo4j (cypher or parameters): {e}"
                    error_code= -1
                    self.logger.error(error_msg)            
                    return dgOut, error_code, error_msg

        neo4jResult, error_msg= self.move_to_dg(rows, query_type)

        self.logger.debug(f"Neo4j Result: {neo4jResult}")
        self.logger.debug(f"Error Message: {error_msg}")
        self.logger.debug(f"Error Code: {error_code}")
        return neo4jResult, error_code, error_msg
