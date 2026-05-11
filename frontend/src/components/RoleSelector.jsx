import { colors } from "../styles/tokens";

export default function RoleSelector({ roles, value, onChange }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{
        padding: "12px 18px",
        fontSize: "15px",
        borderRadius: "10px",
        flex: "1",
        minWidth: "200px",
        backgroundColor: colors.bg,
        color: "white",
        border: `1px solid ${colors.border}`,
        outline: "none",
      }}
    >
      {roles.map((r, index) => (
        <option key={index}>{r}</option>
      ))}
    </select>
  );
}
