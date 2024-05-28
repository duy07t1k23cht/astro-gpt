import json
import os
from typing import List

import requests

from src.engine.search.entities.search_result import SearchResult

URL = "https://www.googleapis.com/customsearch/v1"
SEARCH_ENGINE_API_KEY = os.getenv("SEARCH_ENGINE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


def search(query: str) -> dict:
    params = {
        "key": SEARCH_ENGINE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
    }

    response = requests.get(URL, params=params)

    return response.json()


if __name__ == "__main__":
    search_results = search("What is the next fixture of Champion League?")
    for result in search_results:
        print(result.summary(source=True))
        print()
