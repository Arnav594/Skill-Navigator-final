// Centralized style tokens. The original App.jsx hard-coded these everywhere;
// pulling them out here makes future theming (e.g. light mode) a one-file change.

export const colors = {
  bg:           "#0f172a",
  surface:      "#1e293b",
  border:       "#334155",
  primary:      "#3b82f6",
  primaryDark:  "#1e40af",
  primaryBg:    "#1e3a5f",

  success:      "#22c55e",
  successBg:    "#14532d",
  successText:  "#86efac",

  warning:      "#facc15",
  warningBg:    "#713f12",
  warningText:  "#fde047",

  orange:       "#f97316",
  orangeBg:     "#7c2d12",
  orangeText:   "#fdba74",

  danger:       "#ef4444",
  dangerBg:     "#7f1d1d",
  dangerText:   "#fca5a5",

  textPrimary:  "#e2e8f0",
  textSecondary:"#94a3b8",
  textMuted:    "#64748b",
  textSubtle:   "#475569",
  textBright:   "#cbd5e1",
};

// Reusable card style used by every result section
export const card = {
  backgroundColor: colors.surface,
  borderRadius: "16px",
  padding: "24px",
  border: `1px solid ${colors.border}`,
};

export const sectionTitle = {
  margin: "0 0 16px 0",
  fontSize: "16px",
  color: colors.textSecondary,
};

// Score color helpers (preserve original logic exactly)
export const getMatchColor = (percent) => {
  if (percent >= 70) return colors.success;
  if (percent >= 40) return colors.warning;
  return colors.danger;
};

export const reliabilityColors = {
  green:  { main: colors.success, bg: colors.successBg, text: colors.successText },
  yellow: { main: colors.warning, bg: colors.warningBg, text: colors.warningText },
  orange: { main: colors.orange,  bg: colors.orangeBg,  text: colors.orangeText  },
  red:    { main: colors.danger,  bg: colors.dangerBg,  text: colors.dangerText  },
};

export const getReliability = (color) =>
  reliabilityColors[color] || reliabilityColors.red;
