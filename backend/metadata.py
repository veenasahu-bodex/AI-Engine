def analyze_metadata(soup):

    checks = []

    total = 0
    passed = 0

    title = soup.find("title")

    total += 1

    if title and title.get_text(strip=True):

        passed += 1

        checks.append({
            "name": "Title",
            "status": "present",
            "value": title.get_text(strip=True)
        })

    else:

        checks.append({
            "name": "Title",
            "status": "missing"
        })

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    total += 1

    if meta_description and meta_description.get("content"):

        passed += 1

        checks.append({
            "name": "Meta Description",
            "status": "present",
            "value": meta_description.get("content")
        })

    else:

        checks.append({
            "name": "Meta Description",
            "status": "missing"
        })

    robots = soup.find(
        "meta",
        attrs={"name": "robots"}
    )

    total += 1

    if robots:

        passed += 1

        checks.append({
            "name": "Robots",
            "status": "present",
            "value": robots.get("content")
        })

    else:

        checks.append({
            "name": "Robots",
            "status": "missing"
        })

    canonical = soup.find(
        "link",
        attrs={"rel": "canonical"}
    )

    total += 1

    if canonical:

        passed += 1

        checks.append({
            "name": "Canonical",
            "status": "present",
            "value": canonical.get("href")
        })

    else:

        checks.append({
            "name": "Canonical",
            "status": "missing"
        })

    og_title = soup.find(
        "meta",
        attrs={"property": "og:title"}
    )

    total += 1

    if og_title:

        passed += 1

        checks.append({
            "name": "Open Graph Title",
            "status": "present"
        })

    else:

        checks.append({
            "name": "Open Graph Title",
            "status": "missing"
        })

    og_description = soup.find(
        "meta",
        attrs={"property": "og:description"}
    )

    total += 1

    if og_description:

        passed += 1

        checks.append({
            "name": "Open Graph Description",
            "status": "present"
        })

    else:

        checks.append({
            "name": "Open Graph Description",
            "status": "missing"
        })

    score = round(
        (passed / total) * 100
    )

    return {
        "score": score,
        "passed": passed,
        "total": total,
        "checks": checks
    }