SKILL_ALIASES = {
    "react":              ["reactjs", "react.js", "react js", "react native"],
    "node.js":            ["nodejs", "node js", "node", "express.js", "expressjs"],
    "javascript":         ["js", "es6", "es2015", "es2016", "ecmascript"],
    "typescript":         ["ts"],
    "python":             ["py", "python3", "python2"],
    "machine learning":   ["ml", "machine-learning", "machinelearning"],
    "postgresql":         ["postgres", "psql", "pg"],
    "mongodb":            ["mongo", "mongo db"],
    "kubernetes":         ["k8s", "k8"],
    "aws":                ["amazon web services", "amazon aws"],
    "gcp":                ["google cloud", "google cloud platform"],
    "azure":              ["microsoft azure", "azure cloud"],
    "ci/cd":              ["cicd", "ci cd", "continuous integration", "continuous deployment"],
    "docker":             ["containerization", "containers"],
    "git":                ["github", "gitlab", "bitbucket"],
    "rest":               ["restful", "rest api", "restful api"],
    "sql":                ["structured query language"],
    "html":               ["html5"],
    "css":                ["css3"],
    "linux":              ["unix", "ubuntu", "debian", "bash", "shell scripting"],
    "terraform":          ["iac", "infrastructure as code"],
    "scikit-learn":       ["sklearn", "scikit learn"],
    "tensorflow":         ["tf", "tensor flow"],
    "pytorch":            ["torch"],
    "fastapi":            ["fast api"],
    "django":             ["django rest framework", "drf"],
}

_REVERSE_MAP: dict = {}
for canonical, aliases in SKILL_ALIASES.items():
    _REVERSE_MAP[canonical] = canonical
    for alias in aliases:
        _REVERSE_MAP[alias] = canonical


def normalize_skill(skill: str) -> str:
    return _REVERSE_MAP.get(skill.lower().strip(), skill.lower().strip())


def get_all_forms(skill: str) -> list:
    canonical = normalize_skill(skill)
    return [canonical] + SKILL_ALIASES.get(canonical, [])


def skills_match(skill_a: str, skill_b: str) -> bool:
    return normalize_skill(skill_a) == normalize_skill(skill_b)


def extract_skills_rule_based(text: str, all_skills: dict) -> list:
    found = []
    text_lower = text.lower()
    for category_skills in all_skills.values():
        for skill in category_skills:
            all_forms = get_all_forms(skill)
            if any(form in text_lower for form in all_forms):
                if skill not in found:
                    found.append(skill)
    return found


def normalize_skills_list(skills: list) -> list:
    seen_canonical = set()
    result = []
    for skill in skills:
        canonical = normalize_skill(skill)
        if canonical not in seen_canonical:
            seen_canonical.add(canonical)
            result.append(skill)
    return result


def analyze_gap_normalized(user_skills: list, role_data: list) -> tuple:
    user_canonical = {normalize_skill(s) for s in user_skills}
    job_skills = [item["skill"] for item in role_data]
    present = [s for s in user_skills
               if normalize_skill(s) in {normalize_skill(j) for j in job_skills}]
    missing = [s for s in job_skills
               if normalize_skill(s) not in user_canonical]
    return present, missing