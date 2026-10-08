import time
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/150.0.0.0 Safari/537.36"
)


def get_headers():
    return {
        "User-Agent": USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
    }


def normalize_url(url):
    url = str(url).strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def fetch_website(url):
    """
    Fetch website using synchronous httpx.
    """

    url = normalize_url(url)

    timeout = httpx.Timeout(
        connect=15.0,
        read=30.0,
        write=15.0,
        pool=15.0,
    )

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers=get_headers(),
            verify=True,
        ) as client:

            response = client.get(url)

            response.raise_for_status()

            return response

    except httpx.ConnectError as error:
        raise RuntimeError(
            "Could not connect to the website. "
            "Please check your internet connection or "
            "make sure the website is publicly accessible."
        ) from error

    except httpx.TimeoutException as error:
        raise RuntimeError(
            "Website request timed out. "
            "The website may be slow or temporarily unavailable."
        ) from error

    except httpx.HTTPStatusError as error:
        status = error.response.status_code

        raise RuntimeError(
            f"Website returned HTTP status {status}."
        ) from error

    except httpx.RequestError as error:
        raise RuntimeError(
            f"Website request failed: {error}"
        ) from error


def remove_duplicate_items(items, key_name):
    result = []
    seen = set()

    for item in items:

        value = item.get(key_name)

        if value and value not in seen:

            seen.add(value)
            result.append(item)

    return result


def collect_links(soup, base_url):

    links = []

    for anchor in soup.find_all("a", href=True):

        href = anchor.get("href", "").strip()

        if not href:
            continue

        if href.startswith("#"):
            continue

        if href.startswith("mailto:"):
            continue

        if href.startswith("tel:"):
            continue

        if href.startswith("javascript:"):
            continue

        absolute_url = urljoin(
            base_url,
            href
        )

        parsed = urlparse(absolute_url)

        if parsed.scheme not in ("http", "https"):
            continue

        links.append({
            "url": absolute_url,
            "text": anchor.get_text(
                " ",
                strip=True
            ),
        })

    return remove_duplicate_items(
        links,
        "url"
    )


def collect_images(soup, base_url):

    images = []

    for image in soup.find_all("img"):

        src = (
            image.get("src")
            or image.get("data-src")
            or image.get("data-lazy-src")
        )

        if not src:
            continue

        image_url = urljoin(
            base_url,
            src
        )

        images.append({
            "url": image_url,
            "alt": image.get("alt"),
            "width": image.get("width"),
            "height": image.get("height"),
        })

    return remove_duplicate_items(
        images,
        "url"
    )


async def scan_website(url: str):

    start_time = time.perf_counter()

    url = normalize_url(url)

    print("Fetching:", url)

    response = fetch_website(url)

    response_time = round(
        time.perf_counter() - start_time,
        3
    )

    final_url = str(response.url)

    html = response.text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    parsed_url = urlparse(final_url)

    domain = parsed_url.netloc.lower()

    links = collect_links(
        soup,
        final_url
    )

    images = collect_images(
        soup,
        final_url
    )

    html_size = len(
        response.content
    )

    print("Website fetched successfully.")
    print("Status:", response.status_code)
    print("Final URL:", final_url)
    print("Links:", len(links))
    print("Images:", len(images))
    print("HTML Size:", html_size)
    print("Response Time:", response_time)

    return {
        "url": final_url,
        "status_code": response.status_code,
        "html": html,
        "soup": soup,
        "links": links,
        "images": images,
        "response_time": response_time,
        "html_size": html_size,
        "domain": domain,
    }