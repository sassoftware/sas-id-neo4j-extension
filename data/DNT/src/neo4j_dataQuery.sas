package "${PACKAGE_NAME}" / inline;
	dcl package pymas py;
	dcl double pystop;
	dcl package logger logr('App.tk.SID.Neo4j_dataQuery');
	
	method checkMasPy();
		dcl nvarchar(10485760) pypgm;
		dcl double rc;
		dcl double revision;
		if null(py) and pystop ^= 1 then do;
			py= _new_ pymas();
			if inmas() then do;
				rc= py.useModule('"neo4j_data_query_1_0"', 1);
			end;
			else do;
				rc= 1;
			end;
			if rc then do;
				py.appendSrcLine('from id_neo4j import idNeo4j');
				py.appendSrcLine('import json');
				py.appendSrcLine('');
				py.appendSrcLine('def execute (neo4j_db,cypher_stmt,cypher_para):');
				py.appendSrcLine('    ''Output:neo4j_result,error_code,error_msg''');
				py.appendSrcLine('    id_neo= idNeo4j(neo4j_db)');
				py.appendSrcLine('');
				py.appendSrcLine('    if cypher_para:');
				py.appendSrcLine('        cypher_para= cypher_para.replace("''", ''"'')');
				py.appendSrcLine('    else:');
				py.appendSrcLine('        cypher_para= ''{}''');
				py.appendSrcLine('    dg, error_code, error_msg= id_neo.queryData(cypher_stmt,cypher_para)');
				py.appendSrcLine('    try:');
				py.appendSrcLine('        neo4j_result= json.dumps(dg)');
				py.appendSrcLine('    except Exception as e:');
				py.appendSrcLine('        error_msg= f"Error generating Neo4j result data grid! -> {e} -> The Cypher statement must return data in a flat table structure!"');
				py.appendSrcLine('        error_code= -1');
				py.appendSrcLine('        return str(dg), error_code, error_msg    ');
				py.appendSrcLine('    return neo4j_result,error_code,error_msg');
				pypgm= py.getSource();
				revision= py.publish(pypgm, '"neo4j_data_query_1_0"');
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
		varchar(50) neo4j_db
		, varchar(128000) cypher_stmt
		, varchar(5000) cypher_para
		, in_out package datagrid neo4j_result
		, in_out double error_code
		, in_out varchar error_msg
		);
		dcl double rc;
        dcl varchar(10485760) neo4j_resultJSON;
		
		checkMasPy();
		
		if pystop ^= 1 then do;
			rc= py.setString ('neo4j_db', neo4j_db);
			if rc then do;
				logr.log( 'e', 'set neo4j_db rc=$s', rc );
				return;
			end;
			rc= py.setString ('cypher_stmt', cypher_stmt);
			if rc then do;
				logr.log( 'e', 'set cypher_stmt rc=$s', rc );
				return;
			end;
			rc= py.setString ('cypher_para', cypher_para);
			if rc then do;
				logr.log( 'e', 'set cypher_para rc=$s', rc );
				return;
			end;
			rc= py.execute();
			if rc then do;
				logr.log( 'd', 'execute rc=$s', rc );
				return;
			end;
			neo4j_resultJSON= py.getString('neo4j_result');
			error_code= py.getInt('error_code');
			error_msg= py.getString('error_msg');
            if error_code = 0 then do;
                dataGrid_create(neo4j_result, neo4j_resultJSON);
            end;
		end;
	end;
endpackage;
