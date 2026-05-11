import ResumeUpload from "../components/ResumeUpload";
import ReliabilityScore from "../components/ReliabilityScore";
import SkillMatchCard from "../components/SkillMatchCard";
import SkillsList from "../components/SkillsList";
import Suggestions from "../components/Suggestions";
import Roadmap from "../components/Roadmap";
import { colors } from "../styles/tokens";

export default function HomePage({ roles, role, setRole, analysis, onStartQuiz }) {
  const {
    message, setMessage,
    fileName, handleFileUpload,
    result, loading,
    showRoadmap, setShowRoadmap,
    matchPercent,
    handleSubmit,
  } = analysis;

  return (
    <div>
      <ResumeUpload
        message={message}
        setMessage={setMessage}
        fileName={fileName}
        onFileUpload={handleFileUpload}
        roles={roles}
        role={role}
        setRole={setRole}
        loading={loading}
        onAnalyze={() => handleSubmit(role)}
        onStartQuiz={onStartQuiz}
      />

      {/* AI source indicator */}
      {result?.ai_used !== undefined && (
        <div style={{
          textAlign: "right",
          fontSize: "12px",
          color: result.ai_used ? colors.success : colors.orange,
          marginBottom: "8px",
        }}>
          {result.ai_used ? "✨ AI-powered results" : "⚡ Rule-based fallback results"}
        </div>
      )}

      {result && (
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <ReliabilityScore result={result} />
          <SkillMatchCard matchPercent={matchPercent} />
          <SkillsList skills={result.skills} missing={result.missing} />

          {!result.roadmap_requested && (
            <Suggestions raw={result.suggestions} />
          )}

          {!showRoadmap && (
            <button
              onClick={() => setShowRoadmap(true)}
              style={{
                padding: "14px",
                fontSize: "15px",
                borderRadius: "12px",
                cursor: "pointer",
                backgroundColor: colors.bg,
                color: colors.primary,
                border: `2px solid ${colors.primary}`,
                fontWeight: "600",
                width: "100%",
              }}
            >
              🗺️ View Learning Roadmap
            </button>
          )}

          {showRoadmap && result.roadmap && <Roadmap raw={result.roadmap} />}
        </div>
      )}
    </div>
  );
}
