import { card, colors } from "../styles/tokens";
import { parseSuggestions } from "../api/parsers";

export default function Suggestions({ raw }) {
  const suggestions = parseSuggestions(raw);

  return (
    <div style={card}>
      <h3 style={{ margin: "0 0 16px 0", fontSize: "16px" }}>💡 AI Suggestions</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        {suggestions.map((s, i) => (
          <div key={i} style={{
            borderLeft: `3px solid ${colors.primary}`,
            paddingLeft: "16px",
            display: "flex",
            gap: "12px",
            alignItems: "flex-start",
          }}>
            <span style={{
              backgroundColor: colors.primaryBg,
              color: colors.primary,
              borderRadius: "999px",
              padding: "2px 10px",
              fontSize: "12px",
              fontWeight: "700",
              whiteSpace: "nowrap",
              marginTop: "2px",
            }}>
              {i + 1}
            </span>
            <div>
              {s.title && (
                <div style={{
                  fontWeight: "700",
                  fontSize: "15px",
                  color: colors.textPrimary,
                  marginBottom: "4px",
                }}>
                  {s.title}
                </div>
              )}
              <div style={{
                fontSize: "14px",
                color: colors.textSecondary,
                lineHeight: "1.6",
              }}>
                {s.description}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
