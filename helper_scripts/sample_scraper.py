import os
import sys
import requests

def get_response(search_request : str) -> str:
    resp = requests.get(" https://search.rcsb.org/rcsbsearch/v2/query?json=" +search_request)
    """https://files.rcsb.org/download/1ABC.pdb.gz url for requesting 1ABC.pdb.gz"""
    return resp

def get_gzipped_pdb(pdb_id: str) -> int:
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb.gz"
    resp = requests.get(url)
    if not resp.status_code == 200:
        print(f"response code was not 200, please check (PDB ID: {pdb_id})")
        return -1
    f = open(f"{pdb_id}.pdb.gz", 'wb')
    f.write(resp.content)
    f.close()
    return 0

def main():
    f = open("sample_query.json", 'r')
    search_request = f.read()
    f.close()
    response = get_response(search_request)
    print(response)
