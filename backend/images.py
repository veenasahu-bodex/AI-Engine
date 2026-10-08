import httpx


async def analyze_images(images, base_url):

    issues = []
    working = 0

    async with httpx.AsyncClient(
        timeout=10.0,
        follow_redirects=True
    ) as client:

        for image in images:

            image_url = image["url"]

            try:

                response = await client.head(
                    image_url
                )

                if response.status_code >= 400:

                    issues.append({
                        "url": image_url,
                        "issue": "Broken image"
                    })

                else:

                    working += 1

            except Exception:

                issues.append({
                    "url": image_url,
                    "issue": "Image could not be loaded"
                })

            if image.get("alt") is None:

                issues.append({
                    "url": image_url,
                    "issue": "Missing ALT attribute"
                })

            elif image.get("alt") == "":

                issues.append({
                    "url": image_url,
                    "issue": "Empty ALT attribute"
                })

    total = len(images)

    issue_count = len(issues)

    if total == 0:

        score = 100

    else:

        score = max(
            0,
            round(
                100 -
                (
                    issue_count /
                    (total * 2)
                ) * 100
            )
        )

    return {
        "score": score,
        "total_images": total,
        "working_images": working,
        "issues_count": issue_count,
        "issues": issues
    }