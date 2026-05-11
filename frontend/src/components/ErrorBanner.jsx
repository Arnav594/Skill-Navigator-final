import { colors } from "../styles/tokens";

export default function ErrorBanner({ message, onDismiss }) {
  if (!message) return null;
  return (
    <div style={{
      backgroundColor: colors.dangerBg,
      border: `1px solid ${colors.danger}`,
      borderRadius: "12px",
      padding: "16px",
      marginBottom: "16px",
      color: colors.dangerText,
      fontSize: "14px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    }}>
      ⚠️ {message}
      <button
        onClick={onDismiss}
        style={{
          background: "none",
          border: "none",
          color: colors.dangerText,
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        ✕
      </button>
    </div>
  );
}
