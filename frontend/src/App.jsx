import { useState, useEffect } from "react";

function RoadmapNode({ number, step, how }) {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      flex: "1",
    }}>
      {/* Node circle */}
      <div style={{
        width: "44px",
        height: "44px",
        borderRadius: "50%",
        backgroundColor: "#14532d",
        border: "3px solid #22c55e",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontWeight: "700",
        fontSize: "14px",
        color: "#fff",
        boxShadow: "0 0 12px #22c55e55",
        zIndex: 1,
        flexShrink: 0,
      }}>
        {number}
      </div>

      {/* Step title */}
      <div style={{
        marginTop: "8px",
        fontSize: "13px",
        fontWeight: "700",
        color: "#e2e8f0",
        textAlign: "center",
        maxWidth: "160px",
      }}>
        {step}
      </div>

      {/* Description always visible */}
      <div style={{
        marginTop: "10px",
        backgroundColor: "#0f172a",
        border: "1px solid #22c55e44",
        borderRadius: "10px",
        padding: "12px",
        fontSize: "12px",
        color: "#94a3b8",
        lineHeight: "1.6",
        maxWidth: "160px",
        textAlign: "center",
      }}>
        {how}
      </div>
    </div>
  );
}

function App() {
  const [message, setMessage] = useState("");
  const [role, setRole] = useState("");
  const [roles, setRoles] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);
  const [showRoadmap, setShowRoadmap] = useState(false);
  const [error, setError] = useState(null);

  // 🎯 Quiz states
  const [quizMode, setQuizMode] = useState(false);
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [quizFinished, setQuizFinished] = useState(false);
  const [quizLoading, setQuizLoading] = useState(false);
  const [quizError, setQuizError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/roles")
      .then((res) => res.json())
      .then((data) => {
        setRoles(data);
        if (data.length > 0) setRole(data[0]);
      })
      .catch(() => setError("Could not connect to backend. Please make sure the server is running."));
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    setUploadedFile(file);
    setUploading(false);
  };

  const wantsRoadmap = (text) => {
    const keywords = ["roadmap", "learning path", "guide me", "what should i learn", "how to learn", "study plan"];
    return keywords.some((k) => text.toLowerCase().includes(k));
  };

  const handleSubmit = async () => {
    if (!uploadedFile && !message) {
      setError("Please upload a resume or type a message.");
      return;
    }
    setLoading(true);
    setShowRoadmap(false);
    setResult(null);
    setError(null);

    const roadmapRequested = wantsRoadmap(message);
    const formData = new FormData();
    if (uploadedFile) formData.append("file", uploadedFile);
    formData.append("message", message);
    formData.append("role", role);
    formData.append("roadmap_requested", roadmapRequested);

    try {
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
        setLoading(false);
        return;
      }
      setResult(data);
      if (roadmapRequested) setShowRoadmap(true);
    } catch (err) {
      setError("Could not connect to the server. Please check your connection and try again.");
    }
    setLoading(false);
  };

  const handleStartQuiz = async () => {
    setQuizLoading(true);
    setQuizMode(true);
    setQuizFinished(false);
    setSelectedAnswers({});
    setCurrentQuestion(0);
    setQuizError(null);

    try {
      const res = await fetch(`http://127.0.0.1:5000/quiz?role=${encodeURIComponent(role)}`);
      const data = await res.json();
      if (data.error) {
        setQuizError(data.error);
        setQuizLoading(false);
        return;
      }
      setQuizQuestions(data.questions || []);
    } catch (err) {
      setQuizError("Could not load quiz questions. Please try again.");
    }
    setQuizLoading(false);
  };

  const handleAnswer = (answer) => {
    setSelectedAnswers((prev) => ({ ...prev, [currentQuestion]: answer }));
  };

  const handleNext = () => {
    if (currentQuestion < quizQuestions.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
    } else {
      setQuizFinished(true);
    }
  };

  const calculateScore = () => {
    let correct = 0;
    quizQuestions.forEach((q, i) => {
      if (selectedAnswers[i] === q.correct) correct++;
    });
    return correct;
  };

  const getScoreLabel = (score, total) => {
    const percent = (score / total) * 100;
    if (percent >= 80) return { label: "Excellent! 🌟", color: "#22c55e", bg: "#14532d" };
    if (percent >= 60) return { label: "Good Job! 👍", color: "#facc15", bg: "#713f12" };
    if (percent >= 40) return { label: "Keep Practicing! 📚", color: "#f97316", bg: "#7c2d12" };
    return { label: "Needs Improvement! 💪", color: "#ef4444", bg: "#7f1d1d" };
  };

  const getMatchPercent = () => {
    if (!result) return 0;
    const total = result.skills.length + result.missing.length;
    if (total === 0) return 0;
    return Math.round((result.skills.length / total) * 100);
  };

  const matchPercent = getMatchPercent();

  const getMatchColor = (percent) => {
    if (percent >= 70) return "#22c55e";
    if (percent >= 40) return "#facc15";
    return "#ef4444";
  };

  const getReliabilityColor = (color) => {
    if (color === "green") return "#22c55e";
    if (color === "yellow") return "#facc15";
    if (color === "orange") return "#f97316";
    return "#ef4444";
  };

  const getReliabilityBg = (color) => {
    if (color === "green") return "#14532d";
    if (color === "yellow") return "#713f12";
    if (color === "orange") return "#7c2d12";
    return "#7f1d1d";
  };

  const getReliabilityText = (color) => {
    if (color === "green") return "#86efac";
    if (color === "yellow") return "#fde047";
    if (color === "orange") return "#fdba74";
    return "#fca5a5";
  };

  const parseSuggestions = (raw) => {
    if (!raw) return [];
    const blocks = raw.trim().split(/\n\s*\n/);
    const results = [];
    for (const block of blocks) {
      const lines = block.trim().split("\n");
      let title = "";
      let description = "";
      for (const line of lines) {
        if (line.toUpperCase().startsWith("TITLE:")) {
          title = line.replace(/^TITLE:\s*/i, "").trim();
        } else if (line.toUpperCase().startsWith("DESCRIPTION:")) {
          description = line.replace(/^DESCRIPTION:\s*/i, "").trim();
        }
      }
      if (title && description) results.push({ title, description });
      else if (description && !title) results.push({ title: null, description });
      else if (title && !description) results.push({ title, description: title });
    }
    return results.filter((s) => s.description);
  };

  const parseRoadmap = (raw) => {
    if (!raw) return [];
    const blocks = raw.trim().split(/\n\s*\n/);
    return blocks.map((block) => {
      const stepMatch = block.match(/STEP:\s*(.+)/i);
      const howMatch = block.match(/HOW:\s*(.+)/i);
      return {
        step: stepMatch ? stepMatch[1].trim() : "Step",
        how: howMatch ? howMatch[1].trim() : block.trim(),
      };
    }).filter((s) => s.how);
  };

  const buildRoadmapTree = (steps) => {
    const rows = [];
    let i = 0;
    while (i < steps.length) {
      if (i + 1 < steps.length) {
        rows.push({ type: "branch", left: steps[i], right: steps[i + 1] });
        i += 2;
      } else {
        rows.push({ type: "center", node: steps[i] });
        i += 1;
      }
    }
    return rows;
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#0f172a",
      color: "white",
      fontFamily: "'Segoe UI', sans-serif",
      padding: "40px 20px",
    }}>
      <div style={{ maxWidth: "800px", margin: "0 auto" }}>

        {/* HEADER */}
        <div style={{ textAlign: "center", marginBottom: "40px" }}>
          <h1 style={{ fontSize: "32px", fontWeight: "700", color: "#3b82f6" }}>
            🧭 Skill Navigator
          </h1>
          <p style={{ color: "#94a3b8", fontSize: "15px", marginTop: "8px" }}>
            Upload your resume, pick a role, and get AI-powered career insights
          </p>
        </div>

        {/* ERROR BANNER */}
        {error && (
          <div style={{
            backgroundColor: "#7f1d1d",
            border: "1px solid #ef4444",
            borderRadius: "12px",
            padding: "16px",
            marginBottom: "16px",
            color: "#fca5a5",
            fontSize: "14px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}>
            ⚠️ {error}
            <button onClick={() => setError(null)} style={{
              background: "none", border: "none", color: "#fca5a5", cursor: "pointer", fontSize: "16px",
            }}>✕</button>
          </div>
        )}

        {/* 🎯 QUIZ MODE */}
        {quizMode ? (
          <div>
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "24px",
            }}>
              <h2 style={{ fontSize: "20px", color: "#3b82f6" }}>🎯 {role} Quiz</h2>
              <button
                onClick={() => { setQuizMode(false); setQuizFinished(false); setSelectedAnswers({}); setCurrentQuestion(0); setQuizError(null); }}
                style={{
                  padding: "8px 16px",
                  backgroundColor: "#1e293b",
                  color: "#94a3b8",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontSize: "13px",
                }}
              >✖ Exit Quiz</button>
            </div>

            {quizError ? (
              <div style={{
                backgroundColor: "#1e293b",
                borderRadius: "16px",
                padding: "40px",
                border: "1px solid #334155",
                textAlign: "center",
              }}>
                <div style={{ fontSize: "48px", marginBottom: "16px" }}>⚠️</div>
                <p style={{ color: "#fca5a5", fontSize: "16px", marginBottom: "24px" }}>{quizError}</p>
                <button onClick={handleStartQuiz} style={{
                  padding: "12px 24px",
                  backgroundColor: "#3b82f6",
                  color: "white",
                  border: "none",
                  borderRadius: "10px",
                  cursor: "pointer",
                  fontSize: "14px",
                  fontWeight: "600",
                }}>🔄 Try Again</button>
              </div>

            ) : quizLoading ? (
              <div style={{ textAlign: "center", padding: "60px", color: "#94a3b8" }}>
                ⏳ Loading questions...
              </div>

            ) : quizFinished ? (
              <div style={{
                backgroundColor: "#1e293b",
                borderRadius: "16px",
                padding: "32px",
                border: "1px solid #334155",
              }}>
                <h3 style={{ textAlign: "center", fontSize: "22px", marginBottom: "24px" }}>🏆 Quiz Results</h3>
                {(() => {
                  const score = calculateScore();
                  const total = quizQuestions.length;
                  const scoreInfo = getScoreLabel(score, total);
                  return (
                    <div>
                      <div style={{ textAlign: "center", marginBottom: "24px" }}>
                        <div style={{ fontSize: "64px", fontWeight: "700", color: scoreInfo.color }}>
                          {score}/{total}
                        </div>
                        <span style={{
                          padding: "6px 20px",
                          borderRadius: "999px",
                          fontSize: "15px",
                          fontWeight: "700",
                          backgroundColor: scoreInfo.bg,
                          color: scoreInfo.color,
                        }}>{scoreInfo.label}</span>
                        <div style={{
                          marginTop: "16px",
                          height: "12px",
                          backgroundColor: "#0f172a",
                          borderRadius: "999px",
                          overflow: "hidden",
                        }}>
                          <div style={{
                            width: `${(score / total) * 100}%`,
                            height: "100%",
                            backgroundColor: scoreInfo.color,
                            borderRadius: "999px",
                            transition: "width 0.5s ease",
                          }} />
                        </div>
                      </div>

                      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                        {quizQuestions.map((q, i) => {
                          const userAnswer = selectedAnswers[i];
                          const isCorrect = userAnswer === q.correct;
                          return (
                            <div key={i} style={{
                              backgroundColor: "#0f172a",
                              borderRadius: "12px",
                              padding: "16px",
                              borderLeft: `4px solid ${isCorrect ? "#22c55e" : "#ef4444"}`,
                            }}>
                              <div style={{ fontSize: "14px", fontWeight: "600", color: "#e2e8f0", marginBottom: "8px" }}>
                                Q{i + 1}. {q.question}
                              </div>
                              <div style={{ fontSize: "13px", color: isCorrect ? "#86efac" : "#fca5a5", marginBottom: "4px" }}>
                                {isCorrect ? "✅ Correct!" : `❌ You answered: ${userAnswer} — Correct: ${q.correct}`}
                              </div>
                              <div style={{ fontSize: "13px", color: "#64748b", fontStyle: "italic" }}>
                                💡 {q.explanation}
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      <button onClick={handleStartQuiz} style={{
                        marginTop: "24px",
                        width: "100%",
                        padding: "14px",
                        fontSize: "15px",
                        borderRadius: "12px",
                        cursor: "pointer",
                        backgroundColor: "#3b82f6",
                        color: "white",
                        border: "none",
                        fontWeight: "600",
                      }}>🔄 Retake Quiz</button>
                    </div>
                  );
                })()}
              </div>

            ) : (
              quizQuestions.length > 0 && (
                <div style={{
                  backgroundColor: "#1e293b",
                  borderRadius: "16px",
                  padding: "32px",
                  border: "1px solid #334155",
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                    <span style={{ fontSize: "13px", color: "#94a3b8" }}>Question {currentQuestion + 1} of {quizQuestions.length}</span>
                    <span style={{ fontSize: "13px", color: "#94a3b8" }}>{Object.keys(selectedAnswers).length} answered</span>
                  </div>

                  <div style={{
                    height: "6px",
                    backgroundColor: "#0f172a",
                    borderRadius: "999px",
                    overflow: "hidden",
                    marginBottom: "24px",
                  }}>
                    <div style={{
                      width: `${((currentQuestion + 1) / quizQuestions.length) * 100}%`,
                      height: "100%",
                      backgroundColor: "#3b82f6",
                      borderRadius: "999px",
                      transition: "width 0.3s ease",
                    }} />
                  </div>

                  <div style={{ fontSize: "18px", fontWeight: "600", color: "#e2e8f0", marginBottom: "24px", lineHeight: "1.6" }}>
                    {quizQuestions[currentQuestion].question}
                  </div>

                  <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                    {Object.entries(quizQuestions[currentQuestion].options).map(([key, value]) => (
                      <button
                        key={key}
                        onClick={() => handleAnswer(key)}
                        style={{
                          padding: "14px 20px",
                          borderRadius: "12px",
                          cursor: "pointer",
                          textAlign: "left",
                          fontSize: "14px",
                          fontWeight: selectedAnswers[currentQuestion] === key ? "700" : "400",
                          backgroundColor: selectedAnswers[currentQuestion] === key ? "#1e3a5f" : "#0f172a",
                          color: selectedAnswers[currentQuestion] === key ? "#3b82f6" : "#cbd5e1",
                          border: selectedAnswers[currentQuestion] === key ? "2px solid #3b82f6" : "2px solid #334155",
                          transition: "all 0.2s ease",
                        }}
                      >
                        <span style={{
                          fontWeight: "700",
                          marginRight: "12px",
                          color: selectedAnswers[currentQuestion] === key ? "#3b82f6" : "#64748b",
                        }}>{key}.</span>
                        {value}
                      </button>
                    ))}
                  </div>

                  <button
                    onClick={handleNext}
                    disabled={!selectedAnswers[currentQuestion]}
                    style={{
                      marginTop: "24px",
                      width: "100%",
                      padding: "14px",
                      fontSize: "15px",
                      borderRadius: "12px",
                      cursor: selectedAnswers[currentQuestion] ? "pointer" : "not-allowed",
                      backgroundColor: selectedAnswers[currentQuestion] ? "#3b82f6" : "#1e293b",
                      color: selectedAnswers[currentQuestion] ? "white" : "#475569",
                      border: "none",
                      fontWeight: "600",
                      transition: "all 0.2s ease",
                    }}
                  >
                    {currentQuestion === quizQuestions.length - 1 ? "🏁 Finish Quiz" : "Next Question →"}
                  </button>
                </div>
              )
            )}
          </div>

        ) : (
          <div>
            {/* INPUT CARD */}
            <div style={{
              backgroundColor: "#1e293b",
              borderRadius: "16px",
              padding: "24px",
              marginBottom: "24px",
              border: "1px solid #334155",
            }}>
              <div style={{ position: "relative", width: "100%" }}>
                <textarea
                  rows="6"
                  style={{
                    width: "100%",
                    height: "160px",
                    padding: "16px",
                    paddingBottom: "50px",
                    fontSize: "15px",
                    borderRadius: "12px",
                    resize: "vertical",
                    backgroundColor: "#0f172a",
                    color: "white",
                    border: "1px solid #334155",
                    boxSizing: "border-box",
                    outline: "none",
                    lineHeight: "1.6",
                  }}
                  placeholder={`Type your message here...\n\n💡 Tip: Say 'provide me a roadmap' to also get a learning roadmap!`}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />

                <div style={{
                  position: "absolute",
                  bottom: "10px",
                  left: "10px",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                }}>
                  <label style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "6px",
                    padding: "6px 12px",
                    backgroundColor: "#1e293b",
                    border: "1px solid #3b82f6",
                    borderRadius: "8px",
                    cursor: "pointer",
                    color: "#3b82f6",
                    fontSize: "12px",
                  }}>
                    📁 Upload Resume
                    <input type="file" accept=".pdf,.docx" onChange={handleFileUpload} style={{ display: "none" }} />
                  </label>
                  {uploading && <span style={{ fontSize: "12px", color: "#facc15" }}>⏳ Uploading...</span>}
                  {fileName && !uploading && <span style={{ fontSize: "12px", color: "#94a3b8" }}>✅ {fileName}</span>}
                </div>
              </div>

              <div style={{
                display: "flex",
                gap: "12px",
                marginTop: "16px",
                alignItems: "center",
                flexWrap: "wrap",
              }}>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  style={{
                    padding: "12px 18px",
                    fontSize: "15px",
                    borderRadius: "10px",
                    flex: "1",
                    minWidth: "200px",
                    backgroundColor: "#0f172a",
                    color: "white",
                    border: "1px solid #334155",
                    outline: "none",
                  }}
                >
                  {roles.map((r, index) => (<option key={index}>{r}</option>))}
                </select>

                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  style={{
                    padding: "12px 30px",
                    fontSize: "15px",
                    borderRadius: "10px",
                    cursor: loading ? "not-allowed" : "pointer",
                    backgroundColor: loading ? "#1e40af" : "#3b82f6",
                    color: "white",
                    border: "none",
                    fontWeight: "600",
                  }}
                >
                  {loading ? "⏳ Analyzing..." : "🔍 Analyze"}
                </button>

                <button
                  onClick={handleStartQuiz}
                  style={{
                    padding: "12px 20px",
                    fontSize: "15px",
                    borderRadius: "10px",
                    cursor: "pointer",
                    backgroundColor: "#0f172a",
                    color: "#22c55e",
                    border: "2px solid #22c55e",
                    fontWeight: "600",
                  }}
                >
                  🎯 Take Quiz
                </button>
              </div>
            </div>

            {/* AI source indicator */}
            {result && result.ai_used !== undefined && (
              <div style={{ textAlign: "right", fontSize: "12px", color: result.ai_used ? "#22c55e" : "#f97316", marginBottom: "8px" }}>
                {result.ai_used ? "✨ AI-powered results" : "⚡ Rule-based fallback results"}
              </div>
            )}

            {/* RESULTS */}
            {result && (
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>

                {/* RELIABILITY SCORE */}
                <div style={{ backgroundColor: "#1e293b", borderRadius: "16px", padding: "24px", border: "1px solid #334155" }}>
                  <h3 style={{ margin: "0 0 16px 0", fontSize: "16px", color: "#94a3b8" }}>🎯 Resume Reliability Score</h3>
                  <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                    <div style={{ fontSize: "42px", fontWeight: "700", color: getReliabilityColor(result.reliability_color) }}>
                      {result.reliability_score}%
                    </div>
                    <span style={{
                      padding: "4px 14px",
                      borderRadius: "999px",
                      fontSize: "13px",
                      fontWeight: "700",
                      backgroundColor: getReliabilityBg(result.reliability_color),
                      color: getReliabilityText(result.reliability_color),
                    }}>{result.reliability_label}</span>
                  </div>
                  <div style={{ marginTop: "12px", height: "10px", backgroundColor: "#0f172a", borderRadius: "999px", overflow: "hidden" }}>
                    <div style={{
                      width: `${result.reliability_score}%`,
                      height: "100%",
                      backgroundColor: getReliabilityColor(result.reliability_color),
                      borderRadius: "999px",
                      transition: "width 0.5s ease",
                    }} />
                  </div>
                  {result.missing_sections && result.missing_sections.length > 0 && (
                    <div style={{ marginTop: "16px" }}>
                      <p style={{ fontSize: "13px", color: "#94a3b8", marginBottom: "8px" }}>⚠️ Missing Sections:</p>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                        {result.missing_sections.map((s, i) => (
                          <span key={i} style={{
                            padding: "4px 12px",
                            backgroundColor: "#7f1d1d",
                            color: "#fca5a5",
                            borderRadius: "999px",
                            fontSize: "12px",
                            textTransform: "capitalize",
                          }}>{s}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {result.improvements && result.improvements.length > 0 && (
                    <div style={{ marginTop: "16px" }}>
                      <p style={{ fontSize: "13px", color: "#94a3b8", marginBottom: "8px" }}>📝 Quick Improvements:</p>
                      <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                        {result.improvements.map((imp, i) => (
                          <div key={i} style={{
                            fontSize: "13px",
                            color: "#cbd5e1",
                            paddingLeft: "12px",
                            borderLeft: "2px solid #f97316",
                          }}>{imp}</div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* SKILL MATCH SCORE */}
                <div style={{ backgroundColor: "#1e293b", borderRadius: "16px", padding: "24px", border: "1px solid #334155" }}>
                  <h3 style={{ margin: "0 0 16px 0", fontSize: "16px", color: "#94a3b8" }}>📊 Skill Match Score</h3>
                  <div style={{ fontSize: "36px", fontWeight: "700", color: getMatchColor(matchPercent) }}>{matchPercent}%</div>
                  <div style={{ marginTop: "12px", height: "10px", backgroundColor: "#0f172a", borderRadius: "999px", overflow: "hidden" }}>
                    <div style={{
                      width: `${matchPercent}%`,
                      height: "100%",
                      backgroundColor: getMatchColor(matchPercent),
                      borderRadius: "999px",
                      transition: "width 0.5s ease",
                    }} />
                  </div>
                  <p style={{ marginTop: "8px", fontSize: "13px", color: "#64748b" }}>
                    {matchPercent >= 70 ? "🟢 Strong match for this role!" :
                      matchPercent >= 40 ? "🟡 Moderate match — some gaps to fill" :
                        "🔴 Low match — significant skills needed"}
                  </p>
                </div>

                {/* SKILLS + MISSING */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                  <div style={{ backgroundColor: "#1e293b", borderRadius: "16px", padding: "24px", border: "1px solid #334155" }}>
                    <h3 style={{ margin: "0 0 16px 0", fontSize: "16px" }}>✅ Your Skills</h3>
                    {result.skills.length === 0 ? (
                      <p style={{ color: "#64748b", fontSize: "14px" }}>No skills detected</p>
                    ) : (
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                        {result.skills.map((s, i) => (
                          <span key={i} style={{
                            padding: "4px 12px",
                            backgroundColor: "#166534",
                            color: "#86efac",
                            borderRadius: "999px",
                            fontSize: "13px",
                          }}>{s}</span>
                        ))}
                      </div>
                    )}
                  </div>

                  <div style={{ backgroundColor: "#1e293b", borderRadius: "16px", padding: "24px", border: "1px solid #334155" }}>
                    <h3 style={{ margin: "0 0 16px 0", fontSize: "16px" }}>❌ Missing Skills</h3>
                    {result.missing.length === 0 ? (
                      <p style={{ color: "#64748b", fontSize: "14px" }}>No missing skills!</p>
                    ) : (
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                        {result.missing.map((m, i) => (
                          <span key={i} style={{
                            padding: "4px 12px",
                            backgroundColor: "#7f1d1d",
                            color: "#fca5a5",
                            borderRadius: "999px",
                            fontSize: "13px",
                          }}>{m}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* SUGGESTIONS */}
                {!result.roadmap_requested && (
                  <div style={{ backgroundColor: "#1e293b", borderRadius: "16px", padding: "24px", border: "1px solid #334155" }}>
                    <h3 style={{ margin: "0 0 16px 0", fontSize: "16px" }}>💡 AI Suggestions</h3>
                    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                      {parseSuggestions(result.suggestions).map((s, i) => (
                        <div key={i} style={{
                          borderLeft: "3px solid #3b82f6",
                          paddingLeft: "16px",
                          display: "flex",
                          gap: "12px",
                          alignItems: "flex-start",
                        }}>
                          <span style={{
                            backgroundColor: "#1e3a5f",
                            color: "#3b82f6",
                            borderRadius: "999px",
                            padding: "2px 10px",
                            fontSize: "12px",
                            fontWeight: "700",
                            whiteSpace: "nowrap",
                            marginTop: "2px",
                          }}>{i + 1}</span>
                          <div>
                            {s.title && (
                              <div style={{ fontWeight: "700", fontSize: "15px", color: "#e2e8f0", marginBottom: "4px" }}>
                                {s.title}
                              </div>
                            )}
                            <div style={{ fontSize: "14px", color: "#94a3b8", lineHeight: "1.6" }}>
                              {s.description}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* ROADMAP BUTTON */}
                {!showRoadmap && (
                  <button
                    onClick={() => setShowRoadmap(true)}
                    style={{
                      padding: "14px",
                      fontSize: "15px",
                      borderRadius: "12px",
                      cursor: "pointer",
                      backgroundColor: "#0f172a",
                      color: "#3b82f6",
                      border: "2px solid #3b82f6",
                      fontWeight: "600",
                      width: "100%",
                    }}
                  >🗺️ View Learning Roadmap</button>
                )}

                {/* 🗺️ VISUAL ROADMAP */}
                {showRoadmap && result.roadmap && (() => {
                  const steps = parseRoadmap(result.roadmap);
                  const rows = buildRoadmapTree(steps);
                  let stepCounter = 0;

                  return (
                    <div style={{
                      backgroundColor: "#1e293b",
                      borderRadius: "16px",
                      padding: "32px 24px",
                      border: "1px solid #334155",
                    }}>
                      <h3 style={{ margin: "0 0 8px 0", fontSize: "16px", textAlign: "center" }}>
                        🗺️ Learning Roadmap
                      </h3>
                      <p style={{ textAlign: "center", fontSize: "12px", color: "#64748b", marginBottom: "32px" }}>
                        Your personalized step-by-step learning path
                      </p>

                      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                        {rows.map((row, rowIndex) => {
                          if (row.type === "branch") {
                            const leftNum = ++stepCounter;
                            const rightNum = ++stepCounter;
                            return (
                              <div key={rowIndex} style={{ width: "100%" }}>
                                {/* Branch row */}
                                <div style={{
                                  display: "flex",
                                  alignItems: "flex-start",
                                  justifyContent: "center",
                                  width: "100%",
                                }}>
                                  {/* Left node */}
                                  <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center" }}>
                                    <RoadmapNode number={leftNum} step={row.left.step} how={row.left.how} />
                                  </div>

                                  {/* Horizontal connector aligned to circle center */}
                                  <div style={{
                                    paddingTop: "22px",
                                    width: "60px",
                                    flexShrink: 0,
                                    display: "flex",
                                    alignItems: "flex-start",
                                  }}>
                                    <div style={{
                                      width: "100%",
                                      height: "3px",
                                      backgroundColor: "#22c55e",
                                      opacity: 0.6,
                                      borderRadius: "999px",
                                    }} />
                                  </div>

                                  {/* Right node */}
                                  <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center" }}>
                                    <RoadmapNode number={rightNum} step={row.right.step} how={row.right.how} />
                                  </div>
                                </div>

                                {/* Vertical connector down */}
                                {rowIndex < rows.length - 1 && (
                                  <div style={{ display: "flex", justifyContent: "center", margin: "4px 0" }}>
                                    <div style={{
                                      width: "3px",
                                      height: "40px",
                                      backgroundColor: "#22c55e",
                                      opacity: 0.6,
                                      borderRadius: "999px",
                                    }} />
                                  </div>
                                )}
                              </div>
                            );
                          } else {
                            const centerNum = ++stepCounter;
                            return (
                              <div key={rowIndex} style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
                                {/* Center node */}
                                <div style={{ display: "flex", justifyContent: "center", width: "40%" }}>
                                  <RoadmapNode number={centerNum} step={row.node.step} how={row.node.how} />
                                </div>

                                {/* Vertical connector down */}
                                {rowIndex < rows.length - 1 && (
                                  <div style={{ margin: "4px 0" }}>
                                    <div style={{
                                      width: "3px",
                                      height: "40px",
                                      backgroundColor: "#22c55e",
                                      opacity: 0.6,
                                      borderRadius: "999px",
                                    }} />
                                  </div>
                                )}
                              </div>
                            );
                          }
                        })}
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;