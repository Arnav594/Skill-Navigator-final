import { colors } from "../styles/tokens";
import RoleSelector from "./RoleSelector";

export default function ResumeUpload({
  message, setMessage,
  fileName, onFileUpload,
  roles, role, setRole,
  loading, onAnalyze,
  onStartQuiz,
}) {
  return (
    <div style={{
      backgroundColor: colors.surface,
      borderRadius: "16px",
      padding: "24px",
      marginBottom: "24px",
      border: `1px solid ${colors.border}`,
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
            backgroundColor: colors.bg,
            color: "white",
            border: `1px solid ${colors.border}`,
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
            backgroundColor: colors.surface,
            border: `1px solid ${colors.primary}`,
            borderRadius: "8px",
            cursor: "pointer",
            color: colors.primary,
            fontSize: "12px",
          }}>
            📁 Upload Resume
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={onFileUpload}
              style={{ display: "none" }}
            />
          </label>
          {fileName && (
            <span style={{ fontSize: "12px", color: colors.textSecondary }}>
              ✅ {fileName}
            </span>
          )}
        </div>
      </div>

      <div style={{
        display: "flex",
        gap: "12px",
        marginTop: "16px",
        alignItems: "center",
        flexWrap: "wrap",
      }}>
        <RoleSelector roles={roles} value={role} onChange={setRole} />

        <button
          onClick={onAnalyze}
          disabled={loading}
          style={{
            padding: "12px 30px",
            fontSize: "15px",
            borderRadius: "10px",
            cursor: loading ? "not-allowed" : "pointer",
            backgroundColor: loading ? colors.primaryDark : colors.primary,
            color: "white",
            border: "none",
            fontWeight: "600",
          }}
        >
          {loading ? "⏳ Analyzing..." : "🔍 Analyze"}
        </button>

        <button
          onClick={onStartQuiz}
          style={{
            padding: "12px 20px",
            fontSize: "15px",
            borderRadius: "10px",
            cursor: "pointer",
            backgroundColor: colors.bg,
            color: colors.success,
            border: `2px solid ${colors.success}`,
            fontWeight: "600",
          }}
        >
          🎯 Take Quiz
        </button>
      </div>
    </div>
  );
}
