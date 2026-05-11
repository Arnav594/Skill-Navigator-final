import { colors } from "../styles/tokens";

export default function Header() {
  return (
    <div style={{ textAlign: "center", marginBottom: "40px" }}>
      <h1 style={{ fontSize: "32px", fontWeight: "700", color: colors.primary }}>
        🧭 Skill Navigator
      </h1>
      <p style={{ color: colors.textSecondary, fontSize: "15px", marginTop: "8px" }}>
        Upload your resume, pick a role, and get AI-powered career insights
      </p>
    </div>
  );
}
