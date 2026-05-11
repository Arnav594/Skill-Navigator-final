// Parsers for the LLM-generated text formats.
// Backend returns suggestions as TITLE:/DESCRIPTION: blocks
// and roadmap as STEP:/HOW: blocks, separated by blank lines.

export function parseSuggestions(raw) {
  if (!raw) return [];
  const blocks = raw.trim().split(/\n\s*\n/);
  const results = [];
  for (const block of blocks) {
    const lines = block.trim().split("\n");
    let title = "";
    let description = "";
    for (const line of lines) {
      if (line.toUpperCase().startsWith("TITLE:")) {
        title = line.replace(/^TITLE:\s*/i, "").trim();
      } else if (line.toUpperCase().startsWith("DESCRIPTION:")) {
        description = line.replace(/^DESCRIPTION:\s*/i, "").trim();
      }
    }
    if (title && description) results.push({ title, description });
    else if (description && !title) results.push({ title: null, description });
    else if (title && !description) results.push({ title, description: title });
  }
  return results.filter((s) => s.description);
}

export function parseRoadmap(raw) {
  if (!raw) return [];
  const blocks = raw.trim().split(/\n\s*\n/);
  return blocks
    .map((block) => {
      const stepMatch = block.match(/STEP:\s*(.+)/i);
      const howMatch = block.match(/HOW:\s*(.+)/i);
      return {
        step: stepMatch ? stepMatch[1].trim() : "Step",
        how: howMatch ? howMatch[1].trim() : block.trim(),
      };
    })
    .filter((s) => s.how);
}

// Build a tree layout from a flat step list:
// pairs become side-by-side branches, lone tail step stays centered.
export function buildRoadmapTree(steps) {
  const rows = [];
  let i = 0;
  while (i < steps.length) {
    if (i + 1 < steps.length) {
      rows.push({ type: "branch", left: steps[i], right: steps[i + 1] });
      i += 2;
    } else {
      rows.push({ type: "center", node: steps[i] });
      i += 1;
    }
  }
  return rows;
}

// Heuristic: does the user's message ask for a roadmap?
export function wantsRoadmap(text) {
  const keywords = [
    "roadmap",
    "learning path",
    "guide me",
    "what should i learn",
    "how to learn",
    "study plan",
  ];
  return keywords.some((k) => text.toLowerCase().includes(k));
}
