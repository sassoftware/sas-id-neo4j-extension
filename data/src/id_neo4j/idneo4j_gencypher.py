# Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from openai import AzureOpenAI
import os
import tiktoken
import json
import time
from datetime import datetime
import logging
import re
import httpx

class idNeo4j_genCypher:
    def __init__(self):
#        logging.basicConfig(level=logging.DEBUG)
        self.resource= 'Generate Cypher'
        self.logger= logging.getLogger("idNeo4j")
        self.logger.info(f'Execute idNeo4j_genCypher')
        ##############################################################################################
        # Set LLM model to use and LLM options
        ##############################################################################################
        self.version= '1.0'
        self.temperature= 0
        self.top_p= 1
        self.n= 1
        self.presence_penalty= 0
        self.frequency_penalty= 0

        ##############################################################################################
        # Set the system prompt for the LLM model
        ##############################################################################################
        self.SYSTEM_PROMPT= """
        You are an expert Neo4j Cypher query generator.
        
        Your task is to generate ONLY valid, executable Cypher queries.
        
        ====================
        OUTPUT REQUIREMENTS
        ====================
        
        - Always return a single JSON object with exactly two keys:
          - "cypher": string
          - "params": object
        
        - Do NOT include any explanations, comments, or markdown.
        - Do NOT wrap the output in code fences.
        
        ====================
        QUERY CONSTRAINTS
        ====================
        
        - Generate strictly READ-ONLY Cypher:
          - Forbidden clauses: MERGE, CREATE, DELETE, DETACH DELETE, SET, REMOVE, DROP, LOAD CSV
          - Forbidden procedures: any APOC or custom procedure that modifies data
        
        - Use parameters for ALL user-provided values (e.g., names, IDs, dates).
          - Never hardcode literals originating from the user
        
        - {limit}
        
        ====================
        RESULT STRUCTURE
        ====================
        
        - The query MUST return a flat, tabular structure.
        - NEVER return:
          - nodes (e.g., RETURN n)
          - relationships
          - paths
          - maps (e.g., { ... })
          - full property objects (e.g., properties(n))
          - collections (e.g., collect(...))
        
        - ALWAYS:
          - Project scalar properties explicitly
          - Use clear snake_case aliases
          - Ensure every column is a primitive value:
            string, number, boolean, or date
        
        - Valid RETURN examples:
          RETURN c.name AS customer_name
          RETURN o.id AS order_id, o.total_price AS total_price
        
        - Invalid RETURN examples:
          RETURN c
          RETURN o
          RETURN properties(c)
          RETURN collect(o)
          RETURN { ... }
        
        - If arrays exist:
          - Flatten them using UNWIND
          - Still return only primitive values
        
        - Do NOT aggregate related entities into arrays or maps
        - Return one row per entity or relationship combination
        
        ====================
        FALLBACK BEHAVIOR
        ====================
        
        - If the request is unclear or required data cannot be determined, return:
          RETURN 'No Data Found' AS message
        - If the request is to insert or update data in the database, return:
          RETURN 'Only reading data is supported!' AS message
        ====================
        GENERAL GUIDELINES
        ====================
        
        - Prefer explicit patterns over implicit assumptions
        - Use meaningful variable names
        - Ensure the query is syntactically correct and executable in Neo4j
        ====================
        IMPORTANT IMFORMATION
        You must obey rules in this section.
        ====================
        
        {additional_rules}
        """

        # We can overwrite the default system prompt via an environment variable.
        # This can be useful if the default system prompt does not deliver the expected Cypher.
        NEO4J_SYS_PROMPT= os.environ.get('NEO4J_SYS_PROMPT', '')
        if not NEO4J_SYS_PROMPT:
            NEO4J_SYS_PROMPT= self.get_var_from_usermods('NEO4J_SYS_PROMPT')
        if NEO4J_SYS_PROMPT:
            self.SYSTEM_PROMPT= NEO4J_SYS_PROMPT
            self.logger.debug(f"New System Prompt:\n{NEO4J_SYS_PROMPT}")

        # We can set additional rules to the system prompt via an environment variable.
        # This can be useful to fine tune the system prompt for a particular database 
        # if the generated Cypher is not correct
        NEO4J_SYS_PROMPT_ADD= os.environ.get('NEO4J_SYS_PROMPT_ADD', '')
        if not NEO4J_SYS_PROMPT_ADD:
            NEO4J_SYS_PROMPT_ADD= self.get_var_from_usermods('NEO4J_SYS_PROMPT_ADD')
        if NEO4J_SYS_PROMPT_ADD:
            self.SYSTEM_PROMPT= self.SYSTEM_PROMPT.replace("{additional_rules}", NEO4J_SYS_PROMPT_ADD)
            self.logger.debug(f"Additional System Prompt Rules:\n{NEO4J_SYS_PROMPT_ADD}")
        else:
            self.SYSTEM_PROMPT= self.SYSTEM_PROMPT.replace("{additional_rules}", "")
        
        
        ##############################################################################################
        # Set the user prompt template to generate Cypher. 
        ##############################################################################################
        self.USER_PROMPT_TEMPLATE_GEN= """Schema:
        {schema}
        
        Question:
        {question}
        
        Return JSON with "cypher" and "params".
        """

        ##############################################################################################
        # Set the user prompt template to re-generate Cypher 
        ##############################################################################################
        self.USER_PROMPT_TEMPLATE_RE_GEN= """
        Schema:
        {schema}
        
        Original Question:
        {question}
        
        The following Cypher failed EXPLAIN or guardrails:
        {cypher}
        
        Error:
        {error_msg}
        
        Fix the query while obeying the rules:
        - read-only only
        - use provided schema only
        - parameterize literals
        - {limit}
        
        Return ONLY JSON with "cypher" and "params".
        """

        #Load llm parameters from environment variable
        self.loadParameters()

    ##############################################################################################
    # parse the open AI parameters that come in via environment variable
    ##############################################################################################
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

    ##############################################################################################
    # Load llm parameters from environment variable
    ##############################################################################################
    def loadParameters(self):
        conopts_keys=['model', 'version', 'endpoint', 'key']
        # read the connection parameters
        NEO4J_GENERATE_CYPHER= os.environ.get('NEO4J_GENERATE_CYPHER', '')
        #if NEO4J_GENERATE_CYPHER is empty (not set) we try to read it from the file casconfig_usermods.lua assuming we are 
        # running in ID test mode where environment variables are not set but parameters are stored in the casconfig_usermods.lua file
        if not NEO4J_GENERATE_CYPHER:
            NEO4J_GENERATE_CYPHER= self.get_var_from_usermods('NEO4J_GENERATE_CYPHER')

        # parse connection parameters
        open_ai_para= self.parse_parameters(NEO4J_GENERATE_CYPHER)
        
        # check if parameters are missing
        self.missing_keys= []
        for k in conopts_keys:
        	if k not in list(open_ai_para):
        		self.missing_keys.append(k)
        try:
        	self.llmModel= open_ai_para['model']
        except:
        	self.llmModel= ''
        try:
        	self.neo4j_limit= int(open_ai_para['limit'])
        except:
        	self.neo4j_limit= 0
        try:
        	self.api_key= open_ai_para['key']
        except:
        	self.api_key= ''
        try:
        	self.api_version= open_ai_para['version']
        except:
        	self.api_version= ''
        try:
        	self.llm_endpoint= open_ai_para['endpoint']
        except:
        	self.llm_endpoint= ''
        try:
        	self.regenmax= int(open_ai_para['regen_max'])
        except:
        	self.regenmax= 3 #set to default value of 3 if not set or invalid
        if self.regenmax < 0:
            self.regenmax= 3 #set to default value of 3 if invalid

        self.logger.debug(f"LLM Model: {self.llmModel}, API Version: {self.api_version}, Endpoint: {self.llm_endpoint}, Regen Max: {self.regenmax}")
        return

    ##############################################################################################
    # Get a str value for a key from a json dictionary
    ##############################################################################################
    def getKeyValueStr(self, jsonDic:str, key:str):
        msg= ''
        value= ''
     
        try:
            pyDic= json.loads(jsonDic)
        except json.JSONDecodeError as e:
            msg= f"Error: Invalid JSON format: {e}"
            # Return a default value or re-raise the exception as appropriate
            return "", msg
        except TypeError as e:
            msg= f"Error: Invalid input type for json.loads(): {e}"
            return "", msg
        except Exception as e:
            msg= "Error: " +str(e)
            return "", msg
        try:
            value= pyDic[key]
        except KeyError  as e:
            msg= f"Error: Missing key: {e}"
            return "", msg
        except Exception as e:
            msg= f"Error: {e}"
            return "", msg

        if isinstance(value, (dict, list)):
            value= json.dumps(value)
        else:
            value= str(value)
     
        return value, msg

    ##############################################################################################
    # Get the maximum number of times to re-generate Cypher in case of failed Cypher execution before giving up. 
    ##############################################################################################
    def regen_max(self):
        return self.regenmax

    ##############################################################################################
    # Execute LLM and return cypher statement and cypher parameters as well as some metrics
    ##############################################################################################
    def genCypher(self, userPrompt:str, neo4j_schema:str, cypher_stmt:str='', error_msg:str=''):
        "Output: cypher_stmt,cypher_para,llmMetrics,error_msg,error_code"
    
        self.logger.info(f'Execute genCypher()')

        callDate= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metricsDic={"call_date": callDate, "system_length": 0, "prompt_length": 0, "output_length": 0, "elapsed": 0, "llm": '', "resource": self.resource, "version": self.version}
        llmMetrics= json.dumps(metricsDic)
        error_code= 0
        cypher_para= ''
        response= ""

        #check if any of the required parameters for the LLM call are missing and if yes return error message and code
        if self.missing_keys:
            error_code= -1
            error_msg= f"Neo4j LLM connection parameter(s) not set: {', '.join(self.missing_keys)}. Check environment variable settings!"
            self.logger.error(error_msg)
            return '','',metricsDic,error_msg,error_code
    
        # set the llm model in llmMetrics structure
        metricsDic['llm']= self.llmModel

        # Set up the httpx client with a timeout configuration
        http_client= httpx.Client(
            timeout=httpx.Timeout(
                connect=5.0,
                read=10.0,
                write=10.0,
                pool=5.0
            )
        )

        # Set up the AzureOpenAI client
        client= AzureOpenAI(
            api_key= self.api_key,
            api_version= self.api_version,
            azure_endpoint= self.llm_endpoint,
            http_client= http_client # Pass the http_client to the AzureOpenAI client
        )
    
        # set the user prompt with schema info and user question (userPrompt) depending on wheather generate or re-regerate cypher
        if not cypher_stmt and not error_msg:
            userPrompt= self.USER_PROMPT_TEMPLATE_GEN.format(schema=neo4j_schema, question=userPrompt)
        # re-generate Cypher based on failed Cypher statement and error message from EXPLAIN or guardrails
        else:
            if self.neo4j_limit > 0:
                userPrompt= self.USER_PROMPT_TEMPLATE_RE_GEN.format(schema=neo4j_schema, question=userPrompt, cypher=cypher_stmt, error_msg=error_msg, limit= f"If possible, include a LIMIT <= {self.neo4j_limit}.")
            else:
                userPrompt= self.USER_PROMPT_TEMPLATE_RE_GEN.format(schema=neo4j_schema, question=userPrompt, cypher=cypher_stmt, error_msg=error_msg, limit= f"Do not set LIMIT if not necessary.")

        if self.neo4j_limit > 0:
            systemPrompt= self.SYSTEM_PROMPT.replace("{limit}", f"If possible, include a LIMIT <= {self.neo4j_limit}.")
        else:
            systemPrompt= self.SYSTEM_PROMPT.replace("{limit}", f"Do not set LIMIT if not necessary.")
       
        self.logger.debug(f"System Prompt: {systemPrompt}")
        self.logger.debug(f"User Prompt: {userPrompt}")

        start= time.time()
        # Define the model and messages
        self.logger.debug(f"Calling LLM with model: {self.llmModel}. Timeout settings: {http_client.timeout}")
        try:
            response= client.chat.completions.create(
                model=self.llmModel,
                temperature= self.temperature,
                top_p= self.top_p,
                n= self.n,
                presence_penalty= self.presence_penalty,
                frequency_penalty= self.frequency_penalty,
                max_completion_tokens= 10000,
                messages=[
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": userPrompt},
                ]
            )
        except Exception as e:
            error_msg= f"Error calling LLM: {e}"
            error_code= -1
            self.logger.error(error_msg)
            return '','',metricsDic,error_msg,error_code

        elapsed= time.time() - start

        response= response.choices[0].message.content
        self.logger.debug(f"LLM Response: {response}")
#########################################################################

        i= 0
        self.logger.debug(f"NEXT {i}")
        try:
            encoding= tiktoken.encoding_for_model(self.llmModel)
        except KeyError:
            encoding= tiktoken.get_encoding("cl100k_base")
        i+=1
        self.logger.debug(f"NEXT {i}")
        system_length= len(encoding.encode(systemPrompt))
        i+=1
        self.logger.debug(f"NEXT {i}")
        prompt_length= len(encoding.encode(userPrompt))
        i+=1
        self.logger.debug(f"NEXT {i}")
        output_length= len(encoding.encode(response))
    
        # set metrics
        i+=1
        self.logger.debug(f"NEXT {i}")
        metricsDic={
            "call_date": callDate,
            "system_length": system_length,
            "prompt_length": prompt_length,
            "output_length": output_length,
            "elapsed": elapsed,
            "llm": self.llmModel,
            "resource": self.resource,
            "version": self.version
            }
    
        # get cypher statement from llm response
        i+=1
        self.logger.debug(f"NEXT {i}")
        cypher_stmt, error_msg= self.getKeyValueStr(response, 'cypher')
        if error_msg:
            error_code= -1
            self.logger.error(error_msg)
            return cypher_stmt,cypher_para,metricsDic,error_msg,error_code

        self.logger.debug(f"NEXT {i}")
        cypher_para, error_msg= self.getKeyValueStr(response, 'params')
        if error_msg:
            error_code= -1
            self.logger.error(error_msg)
            return cypher_stmt,cypher_para,metricsDic,error_msg,error_code

        # reset connections (close underlying httpx.Client and pool)
        client.close()

        self.logger.debug(f"Cypher Statement: {cypher_stmt}")
        self.logger.debug(f"Cypher Parameters: {cypher_para}")
        self.logger.debug(f"Metrics: {metricsDic}")
        self.logger.debug(f"Error Message: {error_msg}")
        self.logger.debug(f"Error Code: {error_code}")
        return cypher_stmt,cypher_para,metricsDic,error_msg,error_code
