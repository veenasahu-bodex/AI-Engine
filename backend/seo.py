def analyze_seo(soup, url):

    checks = []
    score = 0
    total = 7

    title = soup.find("title")

    if title and title.get_text(strip=True):

        title_text = title.get_text(strip=True)

        if 30 <= len(title_text) <= 60:

            score += 1

            checks.append({
                "name": "Title",
                "status": "good",
                "message": "Title length is good."
            })

        else:

            checks.append({
                "name": "Title",
                "status": "warning",
                "message": "Title exists but length can be improved."
            })

    else:

        checks.append({
            "name": "Title",
            "status": "error",
            "message": "Title tag is missing."
        })

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_description and meta_description.get("content"):

        score += 1

        checks.append({
            "name": "Meta Description",
            "status": "good",
            "message": "Meta description exists."
        })

    else:

        checks.append({
            "name": "Meta Description",
            "status": "error",
            "message": "Meta description is missing."
        })

    h1 = soup.find_all("h1")

    if len(h1) == 1:

        score += 1

        checks.append({
            "name": "H1",
            "status": "good",
            "message": "One H1 heading found."
        })

    elif len(h1) == 0:

        checks.append({
            "name": "H1",
            "status": "error",
            "message": "H1 heading is missing."
        })

    else:

        checks.append({
            "name": "H1",
            "status": "warning",
            "message": "Multiple H1 headings found."
        })

    headings = soup.find_all(
        ["h2", "h3"]
    )

    if headings:

        score += 1

        checks.append({
            "name": "Heading Structure",
            "status": "good",
            "message": "H2/H3 headings found."
        })

    else:

        checks.append({
            "name": "Heading Structure",
            "status": "warning",
            "message": "No H2/H3 headings found."
        })

    canonical = soup.find(
        "link",
        attrs={"rel": "canonical"}
    )

    if canonical:

        score += 1

        checks.append({
            "name": "Canonical",
            "status": "good",
            "message": "Canonical URL exists."
        })

    else:

        checks.append({
            "name": "Canonical",
            "status": "warning",
            "message": "Canonical URL is missing."
        })

    viewport = soup.find(
        "meta",
        attrs={"name": "viewport"}
    )

    if viewport:

        score += 1

        checks.append({
            "name": "Mobile Viewport",
            "status": "good",
            "message": "Viewport meta tag exists."
        })

    else:

        checks.append({
            "name": "Mobile Viewport",
            "status": "error",
            "message": "Viewport meta tag is missing."
        })

    lang = soup.find("html")

    if lang and lang.get("lang"):

        score += 1

        checks.append({
            "name": "HTML Language",
            "status": "good",
            "message": "HTML language attribute exists."
        })

    else:

        checks.append({
            "name": "HTML Language",
            "status": "warning",
            "message": "HTML lang attribute is missing."
        })

    final_score = round(
        (score / total) * 100
    )

    return {
        "score": final_score,
        "checks": checks
    }