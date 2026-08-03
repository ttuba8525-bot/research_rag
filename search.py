import time
import arxiv
from duckduckgo_search import DDGS

# ---------------------------------------------------------
# Search arXiv Papers
# ---------------------------------------------------------

def search_arxiv_papers(query, max_results=3):

    client = arxiv.Client(
        page_size=10,
        delay_seconds=3,
        num_retries=3
    )

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    try:

        for paper in client.results(search):

            papers.append(
                {
                    "title": paper.title,
                    "summary": paper.summary[:300].replace("\n", " ") + "...",
                    "url": paper.pdf_url,
                    "published": str(paper.published.date())
                }
            )

            time.sleep(1)

    except Exception as e:

        print("arXiv Error:", e)

    return papers


# ---------------------------------------------------------
# DuckDuckGo Search
# ---------------------------------------------------------

def search_similar_online_papers(query):

    results = []

    try:

        with DDGS() as ddgs:

            search_query = (
                f"site:arxiv.org "
                f"OR site:openreview.net "
                f"{query} research paper"
            )

            for item in ddgs.text(
                search_query,
                max_results=5
            ):

                results.append(
                    {
                        "title": item.get("title", "Untitled"),
                        "link": item.get("href", "#"),
                        "snippet": item.get("body", "")
                    }
                )

    except Exception as e:

        print("DuckDuckGo Error:", e)

    return results


# ---------------------------------------------------------
# Combine Results
# ---------------------------------------------------------

def discover_papers(topic):

    arxiv_results = search_arxiv_papers(topic)

    web_results = search_similar_online_papers(topic)

    output = "# 📚 Similar Papers\n\n"

    output += "## arXiv Results\n\n"

    if arxiv_results:

        for paper in arxiv_results:

            output += (
                f"### {paper['title']}\n"
                f"**Published:** {paper['published']}\n\n"
                f"{paper['summary']}\n\n"
                f"PDF: {paper['url']}\n\n"
                "---\n\n"
            )

    else:

        output += "No arXiv papers found.\n\n"

    output += "\n## Web Results\n\n"

    if web_results:

        for paper in web_results:

            output += (
                f"### {paper['title']}\n"
                f"{paper['snippet']}\n\n"
                f"{paper['link']}\n\n"
                "---\n\n"
            )

    else:

        output += "No web search results found."

    return output
