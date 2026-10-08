def analyze_performance(
    response_time,
    html_size
):

    issues = []
    score = 100

    if response_time <= 1:

        response_status = "excellent"

    elif response_time <= 2:

        response_status = "good"

        score -= 10

    elif response_time <= 4:

        response_status = "needs improvement"

        score -= 25

        issues.append(
            "Server response time is high."
        )

    else:

        response_status = "slow"

        score -= 40

        issues.append(
            "Server response time is very slow."
        )

    html_size_kb = round(
        html_size / 1024,
        2
    )

    if html_size_kb > 500:

        score -= 15

        issues.append(
            "HTML document is large."
        )

    return {
        "score": max(score, 0),
        "response_time_seconds": response_time,
        "html_size_kb": html_size_kb,
        "response_status": response_status,
        "issues": issues
    }