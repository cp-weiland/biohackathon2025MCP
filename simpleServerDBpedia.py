import json
from typing import Dict, Any, Optional, Union, List

from loguru import logger

from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from mcp.server.fastmcp import FastMCP


sparql = SPARQLWrapper("https://dbpedia.org/sparql")

sparql.setReturnFormat(JSON)

def sparql_query(query_string: str) -> Dict[str, Any]:
    """Execute a SPARQL query and return the results"""
    try:
        sparql.setQuery(query_string)
        sparql.query().convert()
        return results
    except SPARQLExceptions.EndPointNotFound:
        return {"error": f"SPARQL endpoint not found:"}
    except Exception as e:
        return {"error": f"Query error: {str(e)}"}
    
mcp = FastMCP("SPARQL Query Server")
    
query_doc = f"""
The DBpedia data set enables queries against Wikipedia data to be answered. Execute a SPARQL query via the DBpedia SPARQL endpoint at http://dbpedia.org/sparql.

Argument:
    query_string: A valid SPARQL query string     
Returns:
    The query results in JSON format
"""

@mcp.tool(description=query_doc)
def sparqlQuery(query_string: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    return sparql_query(query_string)
    
# Run the MCP server
mcp.run(transport="stdio")
