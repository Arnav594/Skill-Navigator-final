import { useState } from "react";

function App() {
  const [resume, setResume] = useState("");
  const [role, setRole] = useState("Cloud Engineer");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!resume.trim()) {
      alert("Please enter your resume");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ resume, role }),
      });

      const data = await res.json();
      setResult(data);
    } catch (error) {
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "auto",
        padding: "20px",
        fontFamily: "Arial",
      }}
    >
      <h2 style={{ textAlign: "center" }}>Skill Navigator</h2>

      <textarea
        rows="6"
        style={{ width: "100%", padding: "10px" }}
        placeholder="Paste your resume here..."
        onChange={(e) => setResume(e.target.value)}
      />

      <br /><br />

      <label><b>Select Role:</b></label>
      <br />

      <select
        style={{ padding: "5px", marginTop: "5px" }}
        onChange={(e) => setRole(e.target.value)}
      >
        <option>Cloud Engineer</option>
        <option>Backend Developer</option>
      </select>

      <br /><br />

      <button
        onClick={handleSubmit}
        style={{
          padding: "8px 16px",
          cursor: "pointer",
        }}
      >
        Analyze
      </button>

      <br /><br />

      {loading && <p>Analyzing...</p>}

      {result && (
        <div>
          <h3>Your Skills</h3>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {result.skills.map((s) => (
              <li key={s}>
                {s} ({result.confidence[s]})
              </li>
            ))}
          </ul>

          <h3>Missing Skills</h3>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {result.missing.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>

          <h3>Suggestions</h3>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {result.suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <h3>Learning Roadmap</h3>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {result.roadmap.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;