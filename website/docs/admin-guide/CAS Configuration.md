---
sidebar_position: 130
---

## CAS Configuration
To run scroring tests in Intelligent Decisioning you need to set variables for CAS.
* Open **Viya Environment Manager**
* Navigate to:
    * Configuration → All Services
* Select 
    * cas-shared-default
* Select (right have pane) 
    * sas.cas.instance.config:config
* Edit instance (click on pencil)
* In field *contents* set set variable *NEO4J_CONOPTS*. 
* Add **env.** in front of the variable name.

    **Example:**
	```
	env.NEO4J_CONOPTS = 'db=neo4j;server=10.0.0.4;PORT=8089;uid=neo4j;pwd=Orion123;protocol=neo4j;limit=0;'
    env.NEO4J_GENERATE_CYPHER='model=gpt-4.1-mini;version=2024-12-01-preview;endpoint=https://sgerabc-gpt-mini.openai.azure.com;limit=0;regenmax=3;key=<API_KEY>;'
    env.NEO4J_SYS_PROMPT_ADD = '- If a date field in the database is a STRING, treat it as a string when filtering or comparing these fields.'
	```
