import requests
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def search_pubmed(query: str):
    """
    Search PubMed for medical papers related to a drug and disease.
    Returns a list of paper titles and summaries.
    """
    # This is a simplified version of the PubMed API call (E-utilities)
    # It searches for the query and returns the IDs of the top 3 papers
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "3"
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    id_list = data.get("esearchresult", {}).get("idlist", [])
    
    if not id_list:
        return "No papers found for this topic."
    
    return f"Found {len(id_list)} relevant papers on PubMed. IDs: {', '.join(id_list)}"


@tool
def search_patents(drug_name: str):
    """
    Search for patent information and 'Freedom to Operate' status 
    for a specific drug.
    """
    search = TavilySearchResults(max_results=3)
    # This query focuses on the legal/commercial aspect
    query = f"{drug_name} drug repurposing patent status freedom to operate 2026"
    return search.invoke(query)