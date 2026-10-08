from bs4 import BeautifulSoup


def analyze_accessibility(soup):
    """
    Analyze basic website accessibility.

    Accepts either:
    - BeautifulSoup object
    - HTML string
    """

    # If HTML string is passed, convert it to BeautifulSoup
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    # Make sure soup is valid
    if soup is None:
        return {
            "score": 0,
            "total_checked": 0,
            "passed": 0,
            "issues": [
                {
                    "type": "error",
                    "message": "Website HTML could not be analyzed"
                }
            ]
        }

    issues = []
    passed = 0
    total = 0

    # --------------------------------------------------
    # IMAGE ACCESSIBILITY
    # --------------------------------------------------

    images = soup.find_all("img")

    for img in images:
        total += 1

        alt = img.get("alt")

        if alt is None:
            issues.append({
                "type": "image",
                "message": "Image is missing alt attribute",
                "element": str(img)[:200]
            })
        else:
            passed += 1

    # --------------------------------------------------
    # BUTTON ACCESSIBILITY
    # --------------------------------------------------

    buttons = soup.find_all("button")

    for button in buttons:
        total += 1

        text = button.get_text(strip=True)
        aria_label = button.get("aria-label")
        title = button.get("title")

        if text or aria_label or title:
            passed += 1
        else:
            issues.append({
                "type": "button",
                "message": "Button has no accessible name",
                "element": str(button)[:200]
            })

    # --------------------------------------------------
    # LINK ACCESSIBILITY
    # --------------------------------------------------

    links = soup.find_all("a")

    for link in links:
        total += 1

        text = link.get_text(strip=True)
        aria_label = link.get("aria-label")
        title = link.get("title")

        if text or aria_label or title:
            passed += 1
        else:
            issues.append({
                "type": "link",
                "message": "Link has no accessible text",
                "element": str(link)[:200]
            })

    # --------------------------------------------------
    # INPUT ACCESSIBILITY
    # --------------------------------------------------

    inputs = soup.find_all("input")

    for input_tag in inputs:

        input_type = input_tag.get(
            "type",
            "text"
        ).lower()

        # Ignore non-user-input elements
        if input_type in [
            "hidden",
            "submit",
            "button",
            "reset"
        ]:
            continue

        total += 1

        input_id = input_tag.get("id")
        aria_label = input_tag.get("aria-label")
        aria_labelledby = input_tag.get("aria-labelledby")
        placeholder = input_tag.get("placeholder")

        has_label = False

        if input_id:
            label = soup.find(
                "label",
                attrs={
                    "for": input_id
                }
            )

            if label:
                has_label = True

        if (
            has_label
            or aria_label
            or aria_labelledby
            or placeholder
        ):
            passed += 1

        else:
            issues.append({
                "type": "input",
                "message": "Input has no accessible label",
                "element": str(input_tag)[:200]
            })

    # --------------------------------------------------
    # TEXTAREA ACCESSIBILITY
    # --------------------------------------------------

    textareas = soup.find_all("textarea")

    for textarea in textareas:

        total += 1

        textarea_id = textarea.get("id")
        aria_label = textarea.get("aria-label")
        aria_labelledby = textarea.get("aria-labelledby")
        placeholder = textarea.get("placeholder")

        has_label = False

        if textarea_id:

            label = soup.find(
                "label",
                attrs={
                    "for": textarea_id
                }
            )

            if label:
                has_label = True

        if (
            has_label
            or aria_label
            or aria_labelledby
            or placeholder
        ):
            passed += 1

        else:
            issues.append({
                "type": "textarea",
                "message": "Textarea has no accessible label",
                "element": str(textarea)[:200]
            })

    # --------------------------------------------------
    # SELECT ACCESSIBILITY
    # --------------------------------------------------

    selects = soup.find_all("select")

    for select in selects:

        total += 1

        select_id = select.get("id")
        aria_label = select.get("aria-label")
        aria_labelledby = select.get("aria-labelledby")

        has_label = False

        if select_id:

            label = soup.find(
                "label",
                attrs={
                    "for": select_id
                }
            )

            if label:
                has_label = True

        if (
            has_label
            or aria_label
            or aria_labelledby
        ):
            passed += 1

        else:
            issues.append({
                "type": "select",
                "message": "Select element has no accessible label",
                "element": str(select)[:200]
            })

    # --------------------------------------------------
    # SCORE
    # --------------------------------------------------

    if total == 0:
        score = 100
    else:
        score = round(
            (passed / total) * 100
        )

    return {
        "score": score,
        "total_checked": total,
        "passed": passed,
        "issues": issues
    }