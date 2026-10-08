import httpx
from urllib.parse import urlparse


async def check_links(links, base_url):

    results = []

    base_domain = urlparse(
        base_url
    ).netloc

    unique_links = list(
        set(links)
    )[:100]

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=10.0,
        headers={
            "User-Agent": "AI-Website-Audit-Engine/1.0"
        }
    ) as client:

        for link in unique_links:

            try:

                parsed = urlparse(link)

                if parsed.netloc != base_domain:
                    continue

                response = await client.head(
                    link
                )

                if response.status_code == 405:

                    response = await client.get(
                        link
                    )

                results.append({
                    "url": link,
                    "status_code": response.status_code,
                    "status": (
                        "broken"
                        if response.status_code >= 400
                        else "working"
                    )
                })

            except Exception as error:

                results.append({
                    "url": link,
                    "status_code": None,
                    "status": "broken",
                    "error": str(error)
                })

    broken = [
        item
        for item in results
        if item["status"] == "broken"
    ]

    working = [
        item
        for item in results
        if item["status"] == "working"
    ]

    total = len(results)

    score = (
        round(
            (len(working) / total) * 100
        )
        if total
        else 100
    )

    return {
        "score": score,
        "total_links_checked": total,
        "working_links": len(working),
        "broken_links": len(broken),
        "details": results
    }