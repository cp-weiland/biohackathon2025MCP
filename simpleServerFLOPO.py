import json
from typing import Dict, Any, Optional, Union, List

from loguru import logger

from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from mcp.server.fastmcp import FastMCP


sparql = SPARQLWrapper("https://semantics.senckenberg.de/sparql-endpoint")

sparql.setReturnFormat(JSON)

def sparql_query(query_string: str) -> Dict[str, Any]:
    """Execute a SPARQL query and return the results"""
    try:
        sparql.setQuery(query_string)
        results = sparql.query().convert()
        return results
    except SPARQLExceptions.EndPointNotFound:
        return {"error": f"SPARQL endpoint not found:"}
    except Exception as e:
        return {"error": f"Query error: {str(e)}"}
    
mcp = FastMCP("SPARQL Query Server")
    
query_doc = f"""
FLOPOknb enables queries against flora data to be answered. Execute a SPARQL query via the FLOPOknb SPARQL endpoint using query_string in the 'argument' section below. Use the following query, don't change it:

PREFIX FLOPO: <http://purl.obolibrary.org/obo/FLOPO_>
PREFIX RO: <http://purl.obolibrary.org/obo/RO_>

SELECT DISTINCT ?taxon_uri  ?species_name ?trait
{{    GRAPH <http://semantics.senckenberg.de/wopo> {{
    ?taxon_uri rdfs:label ?species_name ;
    RO:0002200 ?FLOPO_term .
    ?FLOPO_term rdfs:label ?trait .
    }} }} LIMIT 5 
"""

@mcp.tool(description=query_doc)
def sparqlQuery(query_string: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    return sparql_query(query_string)
    
# Run the MCP server
mcp.run(transport="stdio")
