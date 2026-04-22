import requests
import time
from xml.etree import ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def search_pubmed(topic, max_results=20):
    """Step 1: Get PMIDs for a topic."""
    url = f"{BASE_URL}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": topic,
        "retmax": max_results,
        "retmode": "json",
        # "api_key": "YOUR_KEY",   # optional, raises rate limit
        # "email": "you@example.com"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["esearchresult"]["idlist"]

def fetch_abstracts(pmids):
    """Step 2: Fetch abstracts for a list of PMIDs."""
    if not pmids:
        return []
    url = f"{BASE_URL}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "abstract",
        "retmode": "xml",
    }
    r = requests.get(url, params=params)
    r.raise_for_status()

    root = ET.fromstring(r.content)
    results = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        # Abstracts can have multiple sections (Background, Methods, etc.)
        abstract_parts = [
            (t.get("Label", "") + ": " if t.get("Label") else "") + (t.text or "")
            for t in article.findall(".//Abstract/AbstractText")
        ]
        results.append({
            "pmid": pmid,
            "title": title,
            "abstract": "\n".join(abstract_parts),
        })
    return results

# Usage
pmids = search_pubmed("AI AGENTs COVID", max_results=50)
time.sleep(0.34)  # be polite to the API
articles = fetch_abstracts(pmids)

for a in articles:
    print(f"PMID: {a['pmid']}\n{a['title']}\n{a['abstract']}\n{'-'*60}")