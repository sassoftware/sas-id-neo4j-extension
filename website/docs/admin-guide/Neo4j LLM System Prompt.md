---
sidebar_position: 110
---

## Neo4j LLM System Prompt
If the node *Neo4j Generate Cypher* does not generate the expected result, you can "fine-tune" the LLM system prompt by adding additional rules. These rules are submitted via the environment variable *NEO4J_SYS_PROMPT_ADD*.

**Example:**

For database *Northwind*, date fields have the format STRING. To generate correct Cypher, we can add an additional rule:
```
NEO4J_SYS_PROMPT_ADD = '- If a date field in the database is a STRING, treat it as a string when filtering or comparing these fields.'
```
>💡 **Tip:** Each rule should start with a hyphen (-) for the LLM to recognize individual rules.
