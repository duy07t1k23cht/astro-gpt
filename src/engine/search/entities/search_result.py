import os
from typing import List


class SearchResult:
    def __init__(
        self,
        kind: str = None,
        title: str = None,
        htmlTitle: str = None,
        link: str = None,
        displayLink: str = None,
        snippet: str = None,
        htmlSnippet: str = None,
        cacheId: str = None,
        formattedUrl: str = None,
        htmlFormattedUrl: str = None,
        pagemap: dict = None,
        mime: str = None,
        fileFormat: str = None,
        image: dict = None,
        labels: List[dict] = [],
    ) -> None:
        self.kind = kind
        self.title = title
        self.htmlTitle = htmlTitle
        self.link = link
        self.displayLink = displayLink
        self.snippet = snippet
        self.htmlSnippet = htmlSnippet
        self.cacheId = cacheId
        self.formattedUrl = formattedUrl
        self.htmlFormattedUrl = htmlFormattedUrl
        self.pagemap = pagemap
        self.mime = mime
        self.fileFormat = fileFormat
        self.image = image
        self.labels = labels

    def summary(self, title: bool = True, snippet: bool = True, source: bool = False):
        title_text = f"Title: {self.title}\n" if title and self.title else ""
        snippet_text = f"Snippet: {self.snippet}\n" if snippet and self.snippet else ""
        source_text = f"Source: {self.link}" if source and self.link else ""

        return f"{title_text}{snippet_text}{source_text}".strip()
