---
sidebar_position: 15
---

## SCR Configuration

If you run the decision flow in SAS Container Runtime (SCR) set variable *NEO4J_CONOPTS* as environment variable.

**Example:**
```
NEO4J_CONOPTS= db=neo4j;server=10.0.0.4;PORT=8089;uid=neo4j;pwd=Orion123;protocol=neo4j;limit=0;
NEO4J_GENERATE_CYPHER= model= gpt-4.1-mini; version= 2024-12-01-preview; endpoint= https://sgerabc-gpt-mini.openai.azure.com; limit= 0; regenmax=3;key= <API_KEY>;
NEO4J_SYS_PROMPT_ADD = '- If a date field in the database is a STRING, treat it as a string when filtering or comparing these fields.'
```