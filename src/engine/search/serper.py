import json
import os

import requests
from dotenv import load_dotenv

from src.views.custom_logger import logger

load_dotenv()


URL = "https://google.serper.dev/search"
API_KEY = os.getenv("SERPER_API_KEY")


def search(query: str):
    payload = json.dumps({"q": query})
    headers = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}

    response = requests.request("POST", URL, headers=headers, data=payload)
    search_results = response.json()
    return search_results


def simplify_search(query: str):
    search_results = search(query)
    search_results = prune_search_result(search_results)

    knowledgeGraph = search_results.get("knowledgeGraph")
    answerBox = search_results.get("answerBox")
    organic = search_results.get("organic")

    if answerBox:
        logger.i("answerBox found in search result")
        return answerBox

    elif knowledgeGraph:
        logger.i("knowledgeGraph found in search result")
        return knowledgeGraph

    return organic


def prune_search_result(search_results):
    if "answerBox" in search_results:
        search_results["answerBox"].pop("snippetHighlighted", None)

    for i in range(len(search_results.get("organic", []))):
        search_results["organic"][i].pop("sitelinks", None)

    return search_results


if __name__ == "__main__":
    search_result = simplify_search("Mass of the Sun?")
