import { card, sectionTitle, colors, getMatchColor } from "../styles/tokens";

export default function SkillMatchCard({ matchPercent }) {
  const color = getMatchColor(matchPercent);

  const verdict =
    matchPercent >= 70 ? "🟢 Strong match for this role!" :
    matchPercent >= 40 ? "🟡 Moderate match — some gaps to fill" :
                         "🔴 Low match — significant skills needed";

  return (
    <div style={card}>
      <h3 style={sectionTitle}>📊 Skill Match Score</h3>

      <div style={{ fontSize: "36px", fontWeight: "700", color }}>
        {matchPercent}%
      </div>

      <div style={{
        marginTop: "12px",
        height: "10px",
        backgroundColor: colors.bg,
        borderRadius: "999px",
        overflow: "hidden",
      }}>
        <div style={{
          width: `${matchPercent}%`,
          height: "100%",
          backgroundColor: color,
          borderRadius: "999px",
          transition: "width 0.5s ease",
        }} />
      </div>

      <p style={{ marginTop: "8px", fontSize: "13px", color: colors.textMuted }}>
        {verdict}
      </p>
    </div>
  );
}
