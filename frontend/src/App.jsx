import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/scan";

const metrics = [
  {
    key: "seo",
    name: "SEO Score",
    icon: "S",
  },
  {
    key: "performance",
    name: "Performance",
    icon: "P",
  },
  {
    key: "accessibility",
    name: "Accessibility",
    icon: "A",
  },
  {
    key: "metadata",
    name: "Metadata",
    icon: "M",
  },
  {
    key: "links",
    name: "Broken Links",
    icon: "L",
  },
  {
    key: "images",
    name: "Images",
    icon: "I",
  },
];

function normalizeUrl(url) {
  const value = url.trim();

  if (!value) {
    return "";
  }

  if (!value.startsWith("http://") && !value.startsWith("https://")) {
    return `https://${value}`;
  }

  return value;
}

function getScoreClass(score) {
  if (score >= 80) {
    return "good";
  }

  if (score >= 60) {
    return "medium";
  }

  return "low";
}

function getScoreLabel(score) {
  if (score >= 80) {
    return "Good";
  }

  if (score >= 60) {
    return "Needs Improvement";
  }

  return "Needs Attention";
}

function createMockAudit(url) {
  const mockScores = {
    seo: 82,
    performance: 74,
    accessibility: 88,
    metadata: 79,
    links: 91,
    images: 68,
  };

  const overallScore = Math.round(
    Object.values(mockScores).reduce(
      (total, score) => total + score,
      0
    ) / Object.values(mockScores).length
  );

  return {
    success: true,
    mock: true,
    url,
    overall_score: overallScore,
    scores: mockScores,

    audit: {
      url,
      overall_score: overallScore,

      scores: mockScores,

      seo: {
        score: 82,
        issues: [
          {
            type: "seo",
            message: "Some pages may need improved heading structure.",
          },
          {
            type: "seo",
            message: "Consider adding more descriptive internal links.",
          },
        ],
      },

      broken_links: {
        score: 91,
        total_checked: 24,
        working: 22,
        broken: 2,
        issues: [
          {
            type: "link",
            message: "2 links returned unsuccessful responses.",
          },
        ],
      },

      images: {
        score: 68,
        total_checked: 18,
        working: 17,
        broken: 1,
        missing_alt: 4,
        issues: [
          {
            type: "image",
            message: "4 images are missing alt text.",
          },
          {
            type: "image",
            message: "1 image could not be loaded.",
          },
        ],
      },

      accessibility: {
        score: 88,
        total_checked: 25,
        passed: 22,
        issues: [
          {
            type: "accessibility",
            message: "Some interactive elements need better accessible labels.",
          },
        ],
      },

      performance: {
        score: 74,
        response_time: 1.42,
        html_size: 184520,
        issues: [
          {
            type: "performance",
            message: "Initial response time can be improved.",
          },
          {
            type: "performance",
            message: "HTML payload could be reduced.",
          },
        ],
      },

      metadata: {
        score: 79,
        issues: [
          {
            type: "metadata",
            message: "Some metadata fields can be improved for search engines.",
          },
        ],
      },
    },

    ai_analysis: {
      summary:
        "The website has a solid overall foundation, but image optimization, performance, and metadata improvements can increase its technical quality and search visibility.",

      priority_issues: [
        {
          category: "Images",
          issue: "Several images are missing alternative text.",
          impact: "This can affect accessibility and image search visibility.",
          recommendation:
            "Add meaningful alt text to all informative images.",
        },
        {
          category: "Performance",
          issue: "The initial response time can be improved.",
          impact: "Slower responses can affect user experience.",
          recommendation:
            "Optimize server response time, caching, and page resources.",
        },
        {
          category: "Metadata",
          issue: "Some metadata fields need improvement.",
          impact:
            "Better metadata can help search engines understand the page.",
          recommendation:
            "Review title, description, canonical and social metadata.",
        },
      ],

      seo_recommendations: [
        "Improve heading hierarchy and make headings descriptive.",
        "Use descriptive internal links between related pages.",
      ],

      performance_recommendations: [
        "Reduce unnecessary HTML and page resources.",
        "Improve server response time and caching.",
      ],

      accessibility_recommendations: [
        "Add accessible names to interactive elements.",
        "Make sure all important images have useful alt text.",
      ],

      metadata_recommendations: [
        "Review page title and meta description.",
        "Check canonical and social sharing metadata.",
      ],

      image_recommendations: [
        "Add descriptive alt text to missing images.",
        "Compress and optimize large image files.",
      ],

      link_recommendations: [
        "Review the broken links and replace or remove invalid URLs.",
        "Check internal links regularly.",
      ],
    },
  };
}

function App() {
  const [url, setUrl] = useState("https://bodex.io/");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const scanWebsite = async (event) => {
    event.preventDefault();

    const normalizedUrl = normalizeUrl(url);

    if (!normalizedUrl) {
      setError("Please enter a website URL.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      console.log("Starting website scan:", normalizedUrl);

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: normalizedUrl,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
        return;
      }

      console.warn(
        "Real website scan failed. Using mock scan.",
        data.message
      );

      const mockResult = createMockAudit(normalizedUrl);

      setResult(mockResult);
    } catch (scanError) {
      console.warn(
        "Real website scan unavailable. Using mock scan.",
        scanError
      );

      const mockResult = createMockAudit(normalizedUrl);

      setResult(mockResult);
    } finally {
      setLoading(false);
    }
  };

  const scores = result?.scores || {};

  const audit = result?.audit || {};

  const aiAnalysis = result?.ai_analysis || {};

  const overallScore = result?.overall_score || 0;

  const getIssues = () => {
    const allIssues = [];

    const auditSections = [
      {
        name: "SEO",
        data: audit.seo,
      },
      {
        name: "Broken Links",
        data: audit.broken_links,
      },
      {
        name: "Images",
        data: audit.images,
      },
      {
        name: "Accessibility",
        data: audit.accessibility,
      },
      {
        name: "Performance",
        data: audit.performance,
      },
      {
        name: "Metadata",
        data: audit.metadata,
      },
    ];

    auditSections.forEach((section) => {
      if (!section.data?.issues) {
        return;
      }

      section.data.issues.forEach((issue) => {
        allIssues.push({
          ...issue,
          category: section.name,
        });
      });
    });

    return allIssues;
  };

  const getAIRecommendations = () => {
    const recommendations = [];

    const recommendationSections = [
      {
        category: "SEO",
        items: aiAnalysis.seo_recommendations,
      },
      {
        category: "Performance",
        items: aiAnalysis.performance_recommendations,
      },
      {
        category: "Accessibility",
        items: aiAnalysis.accessibility_recommendations,
      },
      {
        category: "Metadata",
        items: aiAnalysis.metadata_recommendations,
      },
      {
        category: "Images",
        items: aiAnalysis.image_recommendations,
      },
      {
        category: "Links",
        items: aiAnalysis.link_recommendations,
      },
    ];

    recommendationSections.forEach((section) => {
      if (!Array.isArray(section.items)) {
        return;
      }

      section.items.forEach((item) => {
        if (!item) {
          return;
        }

        recommendations.push({
          category: section.category,
          text:
            typeof item === "string"
              ? item
              : item.recommendation || item.message || "",
        });
      });
    });

    return recommendations.filter((item) => item.text);
  };

  const issues = getIssues();

  const recommendations = getAIRecommendations();

  return (
    <div className="app">
      {/* ================= HEADER ================= */}

      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">AI</div>

          <div>
            <h1>AI Website Audit</h1>
            <p>SEO & Performance Intelligence</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Audit Engine Online
        </div>
      </header>

      {/* ================= MAIN ================= */}

      <main>
        <div className="container">

          {/* ================= HERO ================= */}

          <section className="hero">
            <div className="hero-content">
              <span className="eyebrow">
                AI-POWERED WEBSITE ANALYSIS
              </span>

              <h2>
                Understand your website
                <br />
                before your users do.
              </h2>

              <p>
                Scan any public website for SEO, performance,
                accessibility, metadata, images and broken links.
                Get practical AI-powered recommendations in seconds.
              </p>

              <form
                className="scan-form"
                onSubmit={scanWebsite}
              >
                <input
                  type="text"
                  value={url}
                  onChange={(event) =>
                    setUrl(event.target.value)
                  }
                  placeholder="Enter website URL..."
                  disabled={loading}
                />

                <button
                  type="submit"
                  disabled={loading}
                >
                  {loading ? "Scanning..." : "Scan Website"}
                </button>
              </form>

              {error && (
                <div className="error-box">
                  <strong>Scan Error</strong>
                  <span>{error}</span>
                </div>
              )}
            </div>
          </section>

          {/* ================= LOADING ================= */}

          {loading && (
            <div className="loading-card">
              <div className="loader"></div>

              <div>
                <h3>Analyzing website...</h3>

                <p>
                  Checking SEO, links, images,
                  accessibility, performance and metadata.
                </p>
              </div>
            </div>
          )}

          {/* ================= RESULTS ================= */}

          {result && !loading && (
            <section className="results">

              {/* Website URL */}

              <div className="website-bar">
                <div>
                  <span className="small-label">
                    WEBSITE ANALYZED
                  </span>

                  <h3>{result.url}</h3>
                </div>

                <div className="scan-success">
                  {result.mock
                    ? "Demo Scan"
                    : "Scan Completed"}
                </div>
              </div>

              {/* ================= OVERVIEW ================= */}

              <div className="overview-grid">

                <div className="score-card">
                  <div className="score-heading">
                    <span>Overall Website Score</span>

                    <span
                      className={`score-status ${getScoreClass(
                        overallScore
                      )}`}
                    >
                      {getScoreLabel(overallScore)}
                    </span>
                  </div>

                  <div className="score-circle">
                    <div className="score-number">
                      {overallScore}
                      <small>/100</small>
                    </div>
                  </div>

                  <p>
                    Combined score across all website
                    audit categories.
                  </p>
                </div>

                <div className="summary-card">
                  <span className="small-label">
                    AI AUDIT SUMMARY
                  </span>

                  <h3>Website Overview</h3>

                  <p>
                    {aiAnalysis.summary ||
                      "No AI summary available."}
                  </p>
                </div>
              </div>

              {/* ================= METRICS ================= */}

              <div className="section-heading">
                <span className="small-label">
                  AUDIT CATEGORIES
                </span>

                <h2>Website Health</h2>
              </div>

              <div className="metrics-grid">
                {metrics.map((metric) => {
                  const score = scores[metric.key] || 0;

                  return (
                    <div
                      className="metric-card"
                      key={metric.key}
                    >
                      <div className="metric-top">
                        <div className="metric-icon">
                          {metric.icon}
                        </div>

                        <span
                          className={`metric-score ${getScoreClass(
                            score
                          )}`}
                        >
                          {score}
                        </span>
                      </div>

                      <h3>{metric.name}</h3>

                      <div className="progress">
                        <div
                          className={`progress-fill ${getScoreClass(
                            score
                          )}`}
                          style={{
                            width: `${score}%`,
                          }}
                        ></div>
                      </div>

                      <span className="metric-label">
                        {getScoreLabel(score)}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* ================= TECHNICAL DATA ================= */}

              <div className="section-heading">
                <span className="small-label">
                  TECHNICAL DETAILS
                </span>

                <h2>Website Data</h2>
              </div>

              <div className="technical-grid">

                <div className="technical-card">
                  <span>Response Time</span>

                  <strong>
                    {audit.performance?.response_time
                      ? `${audit.performance.response_time}s`
                      : "N/A"}
                  </strong>
                </div>

                <div className="technical-card">
                  <span>HTML Size</span>

                  <strong>
                    {audit.performance?.html_size
                      ? `${Math.round(
                          audit.performance.html_size / 1024
                        )} KB`
                      : "N/A"}
                  </strong>
                </div>

                <div className="technical-card">
                  <span>Links Checked</span>

                  <strong>
                    {audit.broken_links?.total_checked ?? "N/A"}
                  </strong>
                </div>

                <div className="technical-card">
                  <span>Working Links</span>

                  <strong>
                    {audit.broken_links?.working ?? "N/A"}
                  </strong>
                </div>

                <div className="technical-card">
                  <span>Images Checked</span>

                  <strong>
                    {audit.images?.total_checked ?? "N/A"}
                  </strong>
                </div>

                <div className="technical-card">
                  <span>Missing Alt Text</span>

                  <strong>
                    {audit.images?.missing_alt ?? "N/A"}
                  </strong>
                </div>

              </div>

              {/* ================= ISSUES + AI ================= */}

              <div className="content-grid">

                {/* ISSUES */}

                <div className="panel">
                  <div className="panel-header">
                    <div>
                      <span className="small-label">
                        TECHNICAL FINDINGS
                      </span>

                      <h2>Issues Found</h2>
                    </div>

                    <div className="count-badge">
                      {issues.length}
                    </div>
                  </div>

                  {issues.length > 0 ? (
                    <div className="issue-list">
                      {issues.map((issue, index) => (
                        <div
                          className="issue-item"
                          key={`${issue.category}-${index}`}
                        >
                          <div className="issue-number">
                            {index + 1}
                          </div>

                          <div>
                            <span className="issue-category">
                              {issue.category}
                            </span>

                            <p>
                              {issue.message ||
                                issue.issue ||
                                "Issue detected"}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="empty-state">
                      <div className="empty-icon">
                        ✓
                      </div>

                      <h3>
                        No major issues found
                      </h3>

                      <p>
                        The website passed the available
                        audit checks.
                      </p>
                    </div>
                  )}
                </div>

                {/* AI RECOMMENDATIONS */}

                <div className="panel ai-panel">
                  <div className="panel-header">
                    <div>
                      <span className="small-label">
                        AI ANALYSIS
                      </span>

                      <h2>
                        Recommendations
                      </h2>
                    </div>

                    <div className="ai-badge">
                      AI
                    </div>
                  </div>

                  {recommendations.length > 0 ? (
                    <div className="recommendation-list">
                      {recommendations.map(
                        (recommendation, index) => (
                          <div
                            className="recommendation-item"
                            key={`${recommendation.category}-${index}`}
                          >
                            <div className="recommendation-icon">
                              ✦
                            </div>

                            <div>
                              <span className="recommendation-category">
                                {recommendation.category}
                              </span>

                              <p>
                                {recommendation.text}
                              </p>
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  ) : (
                    <div className="empty-state">
                      <div className="empty-icon">
                        AI
                      </div>

                      <h3>
                        No recommendations available
                      </h3>

                      <p>
                        AI recommendations will appear
                        after the audit.
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* ================= PRIORITY ISSUES ================= */}

              {Array.isArray(
                aiAnalysis.priority_issues
              ) &&
                aiAnalysis.priority_issues.length > 0 && (
                  <div className="priority-section">

                    <div className="section-heading">
                      <span className="small-label">
                        AI PRIORITY ANALYSIS
                      </span>

                      <h2>
                        Priority Issues
                      </h2>
                    </div>

                    <div className="priority-grid">
                      {aiAnalysis.priority_issues.map(
                        (item, index) => (
                          <div
                            className="priority-card"
                            key={index}
                          >
                            <div className="priority-top">
                              <span className="priority-category">
                                {item.category ||
                                  "General"}
                              </span>

                              <span className="priority-number">
                                {index + 1}
                              </span>
                            </div>

                            <h3>
                              {item.issue ||
                                "Issue detected"}
                            </h3>

                            {item.impact && (
                              <p>
                                <strong>
                                  Impact:
                                </strong>{" "}
                                {item.impact}
                              </p>
                            )}

                            {item.recommendation && (
                              <p>
                                <strong>
                                  Recommendation:
                                </strong>{" "}
                                {item.recommendation}
                              </p>
                            )}
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}
            </section>
          )}

          {/* ================= INITIAL STATE ================= */}

          {!result && !loading && (
            <div className="empty-dashboard">

              <div className="empty-dashboard-icon">
                ◈
              </div>

              <h2>
                Ready to analyze your website
              </h2>

              <p>
                Enter a public website URL above to
                start a complete technical audit.
              </p>

            </div>
          )}
        </div>
      </main>

      {/* ================= FOOTER ================= */}

      <footer className="footer">
        <p>
          AI Website Audit Engine
        </p>

        <span>•</span>

        <span>
          SEO · Performance · Accessibility · AI
        </span>
      </footer>
    </div>
  );
}

export default App;