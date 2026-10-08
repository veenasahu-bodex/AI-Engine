from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
import traceback

from crawler import scan_website
from seo import analyze_seo
from links import check_links
from images import analyze_images
from accessibility import analyze_accessibility
from performance import analyze_performance
from metadata import analyze_metadata
from ai_analyzer import analyze_with_ai


app = FastAPI(
    title="AI Website Audit Engine",
    description="AI-powered Website SEO, Performance and Accessibility Audit API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI Website Audit Engine API is running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "status": "online",
    }


@app.post("/api/scan")
async def scan(request: ScanRequest):

    url = str(request.url)

    print("\n" + "=" * 70)
    print("STARTING WEBSITE AUDIT")
    print("URL:", url)
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. CRAWLER
    # ---------------------------------------------------------

    try:

        print("\n[1/7] Crawling website...")

        website = await scan_website(url)

        print("Crawler completed successfully.")
        print("Status:", website.get("status_code"))
        print("HTML Size:", website.get("html_size"))
        print("Response Time:", website.get("response_time"))

    except Exception as error:

        print("\n" + "=" * 70)
        print("CRAWLER ERROR")
        print("=" * 70)

        print("URL:", url)
        print("Error:", repr(error))

        traceback.print_exc()

        print("=" * 70)

        return JSONResponse(
            status_code=200,
            content={
                "success": False,
                "url": url,
                "error_type": "crawler",
                "message": str(error),
                "overall_score": 0,
                "scores": {},
                "audit": None,
                "ai_analysis": None,
            },
        )

    # ---------------------------------------------------------
    # 2. SEO
    # ---------------------------------------------------------

    try:

        print("\n[2/7] Running SEO analysis...")

        seo_result = analyze_seo(
            website["soup"],
            url
        )

        print("SEO analysis completed.")
        print("SEO Score:", seo_result.get("score", 0))

    except Exception as error:

        print("SEO ERROR:", repr(error))

        seo_result = {
            "score": 0,
            "issues": [
                {
                    "type": "error",
                    "message": str(error)
                }
            ]
        }

    # ---------------------------------------------------------
    # 3. LINKS
    # ---------------------------------------------------------

    try:

        print("\n[3/7] Checking links...")

        link_result = await check_links(
            website["links"],
            url
        )

        print("Link analysis completed.")
        print("Link Score:", link_result.get("score", 0))

    except Exception as error:

        print("LINK ERROR:", repr(error))

        link_result = {
            "score": 0,
            "total_checked": 0,
            "working": 0,
            "broken": 0,
            "issues": [],
            "error": str(error),
        }

    # ---------------------------------------------------------
    # 4. IMAGES
    # ---------------------------------------------------------

    try:

        print("\n[4/7] Checking images...")

        image_result = await analyze_images(
            website["images"],
            url
        )

        print("Image analysis completed.")
        print("Image Score:", image_result.get("score", 0))

    except Exception as error:

        print("IMAGE ERROR:", repr(error))

        image_result = {
            "score": 0,
            "total_checked": 0,
            "working": 0,
            "broken": 0,
            "missing_alt": 0,
            "issues": [],
            "error": str(error),
        }

    # ---------------------------------------------------------
    # 5. ACCESSIBILITY
    # ---------------------------------------------------------

    try:

        print("\n[5/7] Checking accessibility...")

        accessibility_result = analyze_accessibility(
            website["soup"]
        )

        print("Accessibility analysis completed.")
        print(
            "Accessibility Score:",
            accessibility_result.get("score", 0)
        )

    except Exception as error:

        print(
            "ACCESSIBILITY ERROR:",
            repr(error)
        )

        accessibility_result = {
            "score": 0,
            "total_checked": 0,
            "passed": 0,
            "issues": [
                {
                    "type": "error",
                    "message": str(error)
                }
            ],
        }

    # ---------------------------------------------------------
    # 6. PERFORMANCE
    # ---------------------------------------------------------

    try:

        print("\n[6/7] Checking performance...")

        performance_result = analyze_performance(
            website["response_time"],
            website["html_size"]
        )

        print("Performance analysis completed.")
        print(
            "Performance Score:",
            performance_result.get("score", 0)
        )

    except Exception as error:

        print(
            "PERFORMANCE ERROR:",
            repr(error)
        )

        performance_result = {
            "score": 0,
            "response_time": website.get("response_time"),
            "html_size": website.get("html_size"),
            "issues": [
                {
                    "type": "error",
                    "message": str(error)
                }
            ],
        }

    # ---------------------------------------------------------
    # 7. METADATA
    # ---------------------------------------------------------

    try:

        print("\n[7/7] Checking metadata...")

        metadata_result = analyze_metadata(
            website["soup"]
        )

        print("Metadata analysis completed.")
        print(
            "Metadata Score:",
            metadata_result.get("score", 0)
        )

    except Exception as error:

        print(
            "METADATA ERROR:",
            repr(error)
        )

        metadata_result = {
            "score": 0,
            "issues": [
                {
                    "type": "error",
                    "message": str(error)
                }
            ],
        }

    # ---------------------------------------------------------
    # SCORES
    # ---------------------------------------------------------

    scores = {
        "seo": seo_result.get("score", 0),
        "links": link_result.get("score", 0),
        "images": image_result.get("score", 0),
        "accessibility": accessibility_result.get("score", 0),
        "performance": performance_result.get("score", 0),
        "metadata": metadata_result.get("score", 0),
    }

    valid_scores = [
        float(score or 0)
        for score in scores.values()
    ]

    overall_score = (
        round(sum(valid_scores) / len(valid_scores))
        if valid_scores
        else 0
    )

    print("\nOverall Score:", overall_score)

    # ---------------------------------------------------------
    # AUDIT DATA
    # ---------------------------------------------------------

    audit_data = {
        "url": url,
        "overall_score": overall_score,
        "scores": scores,

        "seo": seo_result,

        "broken_links": link_result,

        "images": image_result,

        "accessibility": accessibility_result,

        "performance": performance_result,

        "metadata": metadata_result,
    }

    # ---------------------------------------------------------
    # DEFAULT AI RESPONSE
    # ---------------------------------------------------------

    ai_result = {
        "summary": "AI recommendations are not available.",

        "priority_issues": [],

        "seo_recommendations": [],

        "performance_recommendations": [],

        "accessibility_recommendations": [],

        "metadata_recommendations": [],

        "image_recommendations": [],

        "link_recommendations": [],
    }

    # ---------------------------------------------------------
    # AI ANALYSIS
    # ---------------------------------------------------------

    try:

        print("\nGenerating AI recommendations...")

        ai_result = analyze_with_ai(
            audit_data
        )

        print("AI analysis completed.")

    except Exception as error:

        print(
            "AI ERROR:",
            repr(error)
        )

        ai_result["summary"] = (
            "Website audit completed, but "
            "AI recommendations could not be generated."
        )

    # ---------------------------------------------------------
    # FINAL RESPONSE
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("AUDIT COMPLETED")
    print("Overall Score:", overall_score)
    print("=" * 70)

    return {
        "success": True,

        "url": url,

        "overall_score": overall_score,

        "scores": scores,

        "audit": audit_data,

        "ai_analysis": ai_result,
    }