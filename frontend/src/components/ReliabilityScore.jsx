import { card, sectionTitle, colors, getReliability } from "../styles/tokens";

export default function ReliabilityScore({ result }) {
  const palette = getReliability(result.reliability_color);

  return (
    <div style={card}>
      <h3 style={sectionTitle}>🎯 Resume Reliability Score</h3>

      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <div style={{ fontSize: "42px", fontWeight: "700", color: palette.main }}>
          {result.reliability_score}%
        </div>
        <span style={{
          padding: "4px 14px",
          borderRadius: "999px",
          fontSize: "13px",
          fontWeight: "700",
          backgroundColor: palette.bg,
          color: palette.text,
        }}>
          {result.reliability_label}
        </span>
      </div>

      <div style={{
        marginTop: "12px",
        height: "10px",
        backgroundColor: colors.bg,
        borderRadius: "999px",
        overflow: "hidden",
      }}>
        <div style={{
          width: `${result.reliability_score}%`,
          height: "100%",
          backgroundColor: palette.main,
          borderRadius: "999px",
          transition: "width 0.5s ease",
        }} />
      </div>

      {result.missing_sections?.length > 0 && (
        <div style={{ marginTop: "16px" }}>
          <p style={{ fontSize: "13px", color: colors.textSecondary, marginBottom: "8px" }}>
            ⚠️ Missing Sections:
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {result.missing_sections.map((s, i) => (
              <span key={i} style={{
                padding: "4px 12px",
                backgroundColor: colors.dangerBg,
                color: colors.dangerText,
                borderRadius: "999px",
                fontSize: "12px",
                textTransform: "capitalize",
              }}>
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {result.improvements?.length > 0 && (
        <div style={{ marginTop: "16px" }}>
          <p style={{ fontSize: "13px", color: colors.textSecondary, marginBottom: "8px" }}>
            📝 Quick Improvements:
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            {result.improvements.map((imp, i) => (
              <div key={i} style={{
                fontSize: "13px",
                color: colors.textBright,
                paddingLeft: "12px",
                borderLeft: `2px solid ${colors.orange}`,
              }}>
                {imp}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
