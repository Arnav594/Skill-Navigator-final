// All backend calls live here. Components never touch fetch() directly —
// they go through hooks, and hooks go through this module.

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

export async function fetchRoles() {
  const res = await fetch(`${BASE_URL}/roles`);
  if (!res.ok) throw new Error("Failed to load roles");
  return res.json();
}

export async function analyzeResume({ file, message, role, roadmapRequested }) {
  const formData = new FormData();
  if (file) formData.append("file", file);
  formData.append("message", message);
  formData.append("role", role);
  formData.append("roadmap_requested", roadmapRequested);

  const res = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}

export async function fetchQuiz(role) {
  const res = await fetch(`${BASE_URL}/quiz?role=${encodeURIComponent(role)}`);
  return res.json();
}
