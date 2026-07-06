package "${PACKAGE_NAME}" / inline;
	dcl package pymas py;
	dcl double pystop;
	dcl package logger logr('App.tk.SID.Neo4j_genCypher');
	
	method checkMasPy();	
		dcl nvarchar(10485760) pypgm;
		dcl double rc;
		dcl double revision;
		if null(py) and pystop ^= 1 then do;
			py= _new_ pymas();
			if inmas() then do;
				rc= py.useModule('"neo4j_generate_cypher_1_0"', 1);
			end;
			else do;
				rc= 1;
			end;
			if rc then do;
				py.appendSrcLine('import json');
				py.appendSrcLine('from id_neo4j import idNeo4j');
				py.appendSrcLine('from id_neo4j import idNeo4j_genCypher');
				py.appendSrcLine('def execute (user_prompt,neo4j_db):');
				py.appendSrcLine('    ''Output:cypher_stmt,cypher_para,llm_metrics,error_msg,error_code''');
				py.appendSrcLine('    cypher_stmt= ''''');
				py.appendSrcLine('    cypher_para= ''''');
				py.appendSrcLine('    llm_metrics= ''{}''');
				py.appendSrcLine('    error_msg= ''''');
				py.appendSrcLine('    error_code= 0');
				py.appendSrcLine('');
				py.appendSrcLine('    # get neo4j schema information');
				py.appendSrcLine('    id_neo= idNeo4j(neo4j_db)');
				py.appendSrcLine('    neo4j_schema, error_msg, error_code= id_neo.neo4jSchema()');
				py.appendSrcLine('');
				py.appendSrcLine('    # if we did NOT get schema information we leave here!!!');
				py.appendSrcLine('    if error_code != 0:');
				py.appendSrcLine('        return cypher_stmt, cypher_para, llm_metrics, error_msg, error_code');
				py.appendSrcLine('');
				py.appendSrcLine('    # if we got schema information we are going to generate Cypher');
				py.appendSrcLine('    gc= idNeo4j_genCypher()');
				py.appendSrcLine('    regen_max= gc.regen_max()');
				py.appendSrcLine('    # if an error occures in generating Cypher or validating Cypher we are trying up to "regen_max"-times to re-generate Cypher');
				py.appendSrcLine('    for regen_cnt in range(regen_max + 1): # we go at least once through the loop');
				py.appendSrcLine('        cypher_stmt, cypher_para, llm_metrics, error_msg, error_code= gc.genCypher(user_prompt, neo4j_schema, cypher_stmt, error_msg)');
				py.appendSrcLine('        if error_code == 0:');
				py.appendSrcLine('            # we validate the Cypher statement against Neo4j to ensure the statement is correct');
				py.appendSrcLine('            error_code,error_msg= id_neo.validateCypher(cypher_stmt,cypher_para)');
				py.appendSrcLine('            # if Cypher if correct we leave the loop');
				py.appendSrcLine('            if error_code == 0:');
				py.appendSrcLine('                break');
				py.appendSrcLine('    ');
				py.appendSrcLine('    llm_metrics[''regenmax'']= regen_max');
				py.appendSrcLine('    llm_metrics[''regencnt'']= regen_cnt');
				py.appendSrcLine('    llm_metrics= json.dumps(llm_metrics)');
				py.appendSrcLine('    return cypher_stmt,cypher_para,llm_metrics,error_msg,error_code');
				pypgm= py.getSource();
				revision= py.publish(pypgm, '"neo4j_generate_cypher_1_0"');
				if revision < 1 then do;
					pystop= 1;
					logr.log( 'e', 'publish revision=$s', revision );
					return;
				end;
			end;
			else do;
				logr.log( 'd', 'useModule rc=$s', rc );
			end;
			rc= py.useMethod('execute');
			if rc then do;
				pystop= 1;
				logr.log( 'e', 'useMethod rc=$s', rc );
				return;
			end;
		end;
	end;
	
	method execute(
		varchar(32000) user_prompt
		, varchar(100) neo4j_db
		, in_out varchar cypher_stmt
		, in_out varchar cypher_para
		, in_out varchar llm_metrics
		, in_out varchar error_msg
		, in_out double error_code
		);
		dcl double rc;
		
		checkMasPy();
		
		if pystop ^= 1 then do;
			rc= py.setString ('user_prompt', user_prompt);
			if rc then do;
				logr.log( 'e', 'set user_prompt rc=$s', rc );
				return;
			end;
			rc= py.setString ('neo4j_db', neo4j_db);
			if rc then do;
				logr.log( 'e', 'set neo4j_db rc=$s', rc );
				return;
			end;
			rc= py.execute();
			if rc then do;
				logr.log( 'd', 'execute rc=$s', rc );
				return;
			end;
			cypher_stmt= py.getString('cypher_stmt');
			cypher_para= py.getString('cypher_para');
			llm_metrics= py.getString('llm_metrics');
			error_msg= py.getString('error_msg');
			error_code= py.getInt('error_code');
		end;
	end;
endpackage;
