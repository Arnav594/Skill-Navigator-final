import { colors } from "../styles/tokens";
import { parseRoadmap, buildRoadmapTree } from "../api/parsers";

// Single roadmap node — circle with step number + title + description card.
// Kept inline because it has no use outside Roadmap.
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
        backgroundColor: colors.successBg,
        border: `3px solid ${colors.success}`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontWeight: "700",
        fontSize: "14px",
        color: "#fff",
        boxShadow: `0 0 12px ${colors.success}55`,
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
        color: colors.textPrimary,
        textAlign: "center",
        maxWidth: "160px",
      }}>
        {step}
      </div>

      {/* Description */}
      <div style={{
        marginTop: "10px",
        backgroundColor: colors.bg,
        border: `1px solid ${colors.success}44`,
        borderRadius: "10px",
        padding: "12px",
        fontSize: "12px",
        color: colors.textSecondary,
        lineHeight: "1.6",
        maxWidth: "160px",
        textAlign: "center",
      }}>
        {how}
      </div>
    </div>
  );
}

// Shared connector styles
const horizontalConnector = {
  width: "100%",
  height: "3px",
  backgroundColor: colors.success,
  opacity: 0.6,
  borderRadius: "999px",
};

const verticalConnector = {
  width: "3px",
  height: "40px",
  backgroundColor: colors.success,
  opacity: 0.6,
  borderRadius: "999px",
};

export default function Roadmap({ raw }) {
  const steps = parseRoadmap(raw);
  const rows = buildRoadmapTree(steps);
  let stepCounter = 0;

  return (
    <div style={{
      backgroundColor: colors.surface,
      borderRadius: "16px",
      padding: "32px 24px",
      border: `1px solid ${colors.border}`,
    }}>
      <h3 style={{ margin: "0 0 8px 0", fontSize: "16px", textAlign: "center" }}>
        🗺️ Learning Roadmap
      </h3>
      <p style={{
        textAlign: "center",
        fontSize: "12px",
        color: colors.textMuted,
        marginBottom: "32px",
      }}>
        Your personalized step-by-step learning path
      </p>

      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        {rows.map((row, rowIndex) => {
          const isLast = rowIndex === rows.length - 1;

          if (row.type === "branch") {
            const leftNum = ++stepCounter;
            const rightNum = ++stepCounter;
            return (
              <div key={rowIndex} style={{ width: "100%" }}>
                <div style={{
                  display: "flex",
                  alignItems: "flex-start",
                  justifyContent: "center",
                  width: "100%",
                }}>
                  <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <RoadmapNode number={leftNum} step={row.left.step} how={row.left.how} />
                  </div>

                  <div style={{
                    paddingTop: "22px",
                    width: "60px",
                    flexShrink: 0,
                    display: "flex",
                    alignItems: "flex-start",
                  }}>
                    <div style={horizontalConnector} />
                  </div>

                  <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <RoadmapNode number={rightNum} step={row.right.step} how={row.right.how} />
                  </div>
                </div>

                {!isLast && (
                  <div style={{ display: "flex", justifyContent: "center", margin: "4px 0" }}>
                    <div style={verticalConnector} />
                  </div>
                )}
              </div>
            );
          }

          // center row (single trailing step)
          const centerNum = ++stepCounter;
          return (
            <div key={rowIndex} style={{
              width: "100%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}>
              <div style={{ display: "flex", justifyContent: "center", width: "40%" }}>
                <RoadmapNode number={centerNum} step={row.node.step} how={row.node.how} />
              </div>
              {!isLast && (
                <div style={{ margin: "4px 0" }}>
                  <div style={verticalConnector} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
