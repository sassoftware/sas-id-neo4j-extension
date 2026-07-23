---
sidebar_position: 200
---

## Delete Sample Database in Neo4j

To delete the sample database Northwind in Neo4j run the folloing commands from the Neo4j browser UI.

```
MATCH (n)
DETACH DELETE n;
```
Create commands to drop constraints:
```
SHOW CONSTRAINTS YIELD name
RETURN "DROP CONSTRAINT " + name + ";" AS cmd;
```
Run the generated drop constraint commands:
```
DROP CONSTRAINT Category_categoryID;
DROP CONSTRAINT Customer_customerID;
DROP CONSTRAINT Order_orderID;
DROP CONSTRAINT Product_productID;
DROP CONSTRAINT Supplier_supplierID;
```
Create commands to drop indexes:
```
SHOW INDEXES YIELD name
RETURN "DROP INDEX " + name + ";" AS cmd;
```
Run the generated drop index commands:
```
DROP INDEX Category_categoryID;
DROP INDEX Customer_customerID;
DROP INDEX Order_orderID;
DROP INDEX Product_productID;
DROP INDEX Supplier_supplierID;
```
Run command to check that the database is empty:
```
MATCH (n)
RETURN n;
```
