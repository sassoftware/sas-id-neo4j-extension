## Create a new version of the Python Library

#### Update Python code
* Create directory
    ```
    mkdir ~/id-neo4j
    cd ~/id-neo4j
    ```
* Clone git project in directory id-neo4j<br>
It might be convinient to clone project from VS Code if you to change the Python code.

* Build virtual Python environment under ~/id-neo4j
    ```
    cd ~/id-neo4j
    python3 -m venv venv
    ```
* Activate virtual environment
    ```
    source venv/bin/activate
    ```

* Edit Python code<br>
* Check in Python code after changing.

---

#### Build Wheel file
* Change the version in pyproject.toml before creating a new file
    * **The version must correspond to the Tag and Title for the Release!**
* Check in pyproject.toml
* Go to directory where pyproject.toml resides
* Run commands:<br>
    Only for the first build:
    ```
    python -m pip install --upgrade build 
    ```
    Build wheel:
    ```
    python -m build 
    ```
	this creates file:  
	dist/ id_neo4j-\<VERSION\>-py3-none-any.whl<br>
    E.g.: *dist/ id_neo4j-0.1.0-py3-none-any.whl*
	
* Download file to Windows - to import when building the new release in GitHub

---

#### Create Release in GitHub
* Go to GitHub repository
    * https://github.com/sassoftware/sas-id-neo4j-extension
* Go to *Release*
* Click *Draft a new release*
* Set *Tag* and *Title*
    * E.g.: Tag = v0.2.18
    * E.g.: Title = v0.2.18
* Scroll to *Attach binaries by dropping them here or selecting them.*
* Upload wheel file
* Create release
 ---

**!!! IMPORTANT !!!**<br>
When building a new release version you must adjust the version number in files:
* [pipConfMap_Neo4j.yaml](../DNT/publish/pipConfMap_Neo4j.yaml)
* [install-py-lib.md](../../website/docs/admin-guide/install-py-lib.md)
    * Change value in line 18

---

When building a new release version:

* You need to create a new SCR publishing destination.
* You need to add the new version to Python in Viya.

---

To install the new Python library call<br>
```pip install https://github.com/sassoftware/sas-id-neo4j-extension/releases/download/v<VERSION>>/id_neo4j-<VERSION>>-py3-none-any.whl```

**Example:**
```
pip install https://github.com/sassoftware/sas-id-neo4j-extension/releases/download/v0.2.18/id_neo4j-0.2.18-py3-none-any.whl
```