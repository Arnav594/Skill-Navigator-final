import { card, colors } from "../styles/tokens";

function SkillPanel({ title, skills, emptyText, tone }) {
  const isMissing = tone === "missing";
  const pillBg = isMissing ? "#7f1d1d" : "#166534";
  const pillFg = isMissing ? colors.dangerText : colors.successText;

  return (
    <div style={card}>
      <h3 style={{ margin: "0 0 16px 0", fontSize: "16px" }}>{title}</h3>
      {skills.length === 0 ? (
        <p style={{ color: colors.textMuted, fontSize: "14px" }}>{emptyText}</p>
      ) : (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
          {skills.map((s, i) => (
            <span key={i} style={{
              padding: "4px 12px",
              backgroundColor: pillBg,
              color: pillFg,
              borderRadius: "999px",
              fontSize: "13px",
            }}>
              {s}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default function SkillsList({ skills, missing }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
      <SkillPanel
        title="✅ Your Skills"
        skills={skills}
        emptyText="No skills detected"
        tone="present"
      />
      <SkillPanel
        title="❌ Missing Skills"
        skills={missing}
        emptyText="No missing skills!"
        tone="missing"
      />
    </div>
  );
}
