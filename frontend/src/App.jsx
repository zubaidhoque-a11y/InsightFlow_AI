
import { useRef, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const fileInput = useRef(null);
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState(
    "Analyze this dataset, summarize its key patterns, and identify important insights."
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyzeDataset(event) {
    event.preventDefault();

    if (!file) {
      setError("Please select a CSV file before starting the analysis.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question about your dataset.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question.trim());

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "The backend could not analyze this dataset."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot reach FastAPI. Make sure your backend is running on port 8000."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  function handleFile(selectedFile) {
    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Please upload a CSV file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError("");
    setResult(null);
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#home">
          <span className="brand-mark">✳</span>
          <span>
            InsightFlow<span className="brand-ai"> AI</span>
          </span>
        </a>

        <div className="sidebar-label">WORKSPACE</div>

        <a className="nav-link selected" href="#analyze">
          <span>◈</span> Data Analysis
        </a>

        <a className="nav-link" href="#results">
          <span>▥</span> Visualizations
        </a>

        <div className="sidebar-label workflow-label">
          YOUR WORKFLOW
        </div>

        <div className="workflow-item">
          <span className="workflow-number">01</span>
          <div>
            <strong>Upload</strong>
            <small>Choose a CSV dataset</small>
          </div>
        </div>

        <div className="workflow-item">
          <span className="workflow-number">02</span>
          <div>
            <strong>Analyze</strong>
            <small>Ask your AI assistant</small>
          </div>
        </div>

        <div className="workflow-item">
          <span className="workflow-number">03</span>
          <div>
            <strong>Discover</strong>
            <small>Explore results and charts</small>
          </div>
        </div>

        <div className="sidebar-footer">
          <span className="online-dot" />
          <div>
            <strong>Local API</strong>
            <small>FastAPI connection</small>
          </div>
        </div>
      </aside>

      <main className="main-content" id="home">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> Data analysis
          </div>
          <div className="topbar-badge">
            <span /> AI workspace
          </div>
        </header>

        <section className="hero">
          <div className="eyebrow">
            <span>✦</span> YOUR INTELLIGENT DATA ASSISTANT
          </div>

          <h1>
            Make your data
            <br />
            <span>tell its story.</span>
          </h1>

          <p>
            Explore datasets, uncover meaningful patterns, and generate
            visual insights with your AI-powered analysis workflow.
          </p>

          <div className="hero-tags">
            <span>✳ LangGraph workflow</span>
            <span>⌁ Automated charts</span>
            <span>◈ CSV analysis</span>
          </div>
        </section>

        <section className="workspace-grid" id="analyze">
          <form
            className="panel upload-panel"
            onSubmit={analyzeDataset}
          >
            <div className="panel-heading">
              <div>
                <div className="step-label">STEP 01 / INPUT</div>
                <h2>Start your analysis</h2>
                <p>
                  Choose a dataset and tell the AI what to explore.
                </p>
              </div>
              <span className="heading-icon">↗</span>
            </div>

            <label
              className={`dropzone ${file ? "file-selected" : ""}`}
              onDragOver={(event) => event.preventDefault()}
              onDrop={(event) => {
                event.preventDefault();
                handleFile(event.dataTransfer.files[0]);
              }}
            >
              <input
                ref={fileInput}
                type="file"
                accept=".csv,text/csv"
                onChange={(event) =>
                  handleFile(event.target.files[0])
                }
              />

              <span className="upload-icon">
                {file ? "✓" : "↑"}
              </span>

              <strong>
                {file ? file.name : "Drop your CSV file here"}
              </strong>

              <span className="drop-description">
                {file
                  ? "Your dataset is ready to analyze"
                  : "or click to browse files"}
              </span>

              <span className="csv-pill">CSV FORMAT</span>
            </label>

            <div className="field-header">
              <label htmlFor="analysis-question">
                What would you like to know?
              </label>
              <span>AI PROMPT</span>
            </div>

            <textarea
              id="analysis-question"
              rows={4}
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Example: Find missing values, key trends, and unusual patterns..."
            />

            {error && (
              <div className="error-box">⚠ {error}</div>
            )}

            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  Analyzing dataset...
                </>
              ) : (
                <>
                  ✦ &nbsp; Analyze dataset <span>→</span>
                </>
              )}
            </button>

            <div className="secure-note">
              ⌑ &nbsp; Processed through your local backend
            </div>
          </form>

          <aside className="panel process-panel">
            <div className="step-label">HOW IT WORKS</div>

            <h2>
              From raw data
              <br />
              to real insights.
            </h2>

            <p className="process-intro">
              Your request flows through your AI-powered analysis pipeline.
            </p>

            <div className="pipeline">
              <div className="pipeline-step">
                <span className="pipeline-icon purple">⇧</span>
                <div>
                  <strong>Dataset ingestion</strong>
                  <small>Upload and inspect your CSV</small>
                </div>
                <span className="pipeline-check">01</span>
              </div>

              <div className="pipeline-line" />

              <div className="pipeline-step">
                <span className="pipeline-icon blue">✳</span>
                <div>
                  <strong>AI reasoning</strong>
                  <small>LangGraph-powered workflow</small>
                </div>
                <span className="pipeline-check">02</span>
              </div>

              <div className="pipeline-line" />

              <div className="pipeline-step">
                <span className="pipeline-icon green">▥</span>
                <div>
                  <strong>Visual discovery</strong>
                  <small>Generate data visualizations</small>
                </div>
                <span className="pipeline-check">03</span>
              </div>
            </div>

            <div className="tip-card">
              <span>✧</span>
              <div>
                <strong>Pro tip</strong>
                <p>
                  Ask a specific question for more useful, focused insights.
                </p>
              </div>
            </div>
          </aside>
        </section>

        {loading && (
          <div className="loading-panel">
            <span className="loading-orb">✳</span>
            <div>
              <strong>Your analysis is in progress</strong>
              <p>
                The AI workflow is processing your dataset.
                Larger files may take longer.
              </p>
            </div>
          </div>
        )}

        {result && (
          <section className="results-section" id="results">
            <div className="results-heading">
              <div>
                <div className="eyebrow">✦ ANALYSIS RESULTS</div>
                <h2>Your data, at a glance.</h2>
                <p>
                  Analysis for{" "}
                  <strong>{result.filename || file?.name}</strong>
                </p>
              </div>

              <span className="success-pill">✓ Complete</span>
            </div>

            <div className="metrics-grid">
              <Metric
                label="Total rows"
                value={result.rows ?? "—"}
                icon="▤"
              />
              <Metric
                label="Total columns"
                value={result.columns ?? "—"}
                icon="▥"
              />
              <Metric
                label="Visualizations"
                value={result.charts?.length ?? 0}
                icon="◫"
              />
            </div>

            <div className="panel result-panel">
              <div className="result-title">
                <span className="result-icon">✳</span>
                <div>
                  <h3>AI-generated insights</h3>
                  <p>Results from your analysis workflow</p>
                </div>
              </div>

              <div className="answer-text">
                {result.answer ||
                  "The workflow returned no analysis text."}
              </div>
            </div>

            <div className="panel result-panel">
              <div className="result-title">
                <span className="result-icon">▤</span>
                <div>
                  <h3>Dataset columns</h3>
                  <p>
                    {result.column_names?.length ?? 0} fields detected
                  </p>
                </div>
              </div>

              <div className="column-chips">
                {(result.column_names || []).map((column) => (
                  <span key={column}>{column}</span>
                ))}
              </div>
            </div>

            {result.charts?.length > 0 && (
              <div className="visualizations">
                <div className="visualizations-heading">
                  <div>
                    <div className="eyebrow">DATA EXPLORATION</div>
                    <h2>Generated visualizations</h2>
                  </div>
                </div>

                <div className="charts-grid">
                  {result.charts.map((chart, index) => (
                    <article
                      className="panel chart-panel"
                      key={`${chart}-${index}`}
                    >
                      <h3>Visualization {index + 1}</h3>
                      <img
                        src={chart.startsWith("http") ? chart : `${API_URL}/${chart.replace(/^\/+/, "")}`}
                        alt={`Dataset visualization ${index + 1}`}
                      />
                    </article>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {/* Footer with developer credit */}
        <footer className="footer">
          <span>✳ InsightFlow AI</span>

          <span>
            Intelligent analysis · Powered by your AI workflow
          </span>

          <div className="developer-credit">
            <p>
              Built by{" "}
              <span className="developer-name">
                Jubaid Hoque Choudhury
              </span>
            </p>

            <span className="footer-caption">
              InsightFlow AI · Agentic Data Analysis
            </span>
          </div>
        </footer>
      </main>
    </div>
  );
}

function Metric({ label, value, icon }) {
  return (
    <div className="panel metric-card">
      <div className="metric-top">
        <span>{label}</span>
        <span className="metric-icon">{icon}</span>
      </div>

      <strong>
        {typeof value === "number"
          ? value.toLocaleString()
          : value}
      </strong>

      <small>From current dataset</small>
    </div>
  );
}

export default App;

