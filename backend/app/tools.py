import requests
import os
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def search_pubmed(query: str):
    """Search PubMed for medical papers."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": "3"}
    response = requests.get(base_url, params=params)
    data = response.json()
    id_list = data.get("esearchresult", {}).get("idlist", [])
    if not id_list:
        return "No papers found."
    return f"Found {len(id_list)} relevant papers. IDs: {', '.join(id_list)}"

@tool
def search_patents(drug_name: str):
    """
    Search for patent information and 'Freedom to Operate' status 
    for a specific drug.
    """
    # This uses the new, non-deprecated class
    search = TavilySearchResults(max_results=3)
    query = f"{drug_name} drug repurposing patent status freedom to operate 2026"
    return search.invoke(query)