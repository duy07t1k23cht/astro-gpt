from typing import List
import os
import requests
import json

from src.engine.search.entities.search_result import SearchResult

URL = "https://www.googleapis.com/customsearch/v1"


class SearchEngine:
    def __init__(self) -> None:
        self.__api_key = os.getenv("SEARCH_ENGINE_API_KEY")
        self.__engine_id = os.getenv("SEARCH_ENGINE_ID")

    def search(self, query: str) -> List[SearchResult]:
        params = {
            "key": self.__api_key,
            "cx": self.__engine_id,
            "q": query,
        }

        response = requests.get(URL, params=params)

        data = response.json()
        search_results = []
        results = data.get("items", [])
        for result in results:
            search_result = SearchResult(**result)
            search_results.append(search_result)

        return search_results


if __name__ == "__main__":
    search_engine = SearchEngine()

    search_results = search_engine.search("What is the next fixture of Champion League?")
    for result in search_results:
        print(result.summary(source=True))
        print()
