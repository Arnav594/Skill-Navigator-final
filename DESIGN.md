# Skill Navigator – Design Documentation

**Candidate Name:** Arnav  
**Scenario:** Skill-Bridge Career Navigator  
**Tech Stack:** Python (Flask), React, Groq API (LLaMA 3.1), CSV-based data, JSON schema  

---

## 1. Problem Understanding

Students and early-career professionals often struggle to understand how well their current skills align with job requirements. Existing tools either provide generic suggestions or lack personalized evaluation.

This project addresses that gap by building an AI-powered system that evaluates a user’s resume against a selected role and provides a measurable reliability score along with actionable insights.

---

## 2. Solution Overview

The system allows users to:
- Upload a resume (PDF or DOCX)
- Select a target role (e.g., Backend Developer)
- Receive:
  - Reliability score (job readiness)
  - Skill gap analysis
  - Personalized suggestions
  - Learning roadmap
  - Interactive quiz for skill validation

---

## 3. System Architecture

### Frontend (React)
- Handles user interaction
- Resume upload and role selection
- Displays:
  - Scores
  - Skills and gaps
  - Suggestions and roadmap
  - Quiz interface

### Backend (Flask)
- Processes resume input
- Extracts skills
- Compares against role benchmarks
- Generates analysis using AI + fallback

### AI Layer (Groq – LLaMA 3.1)
- Skill extraction
- Suggestion generation
- Roadmap generation

### Data Layer
- CSV files:
  - `skills.csv` → role-based skill benchmarks
  - `questions.csv` → quiz questions

---

## 4. Data Flow

1. User uploads resume + selects role  
2. Resume is parsed (PDF/DOCX → text)  
3. Skills are extracted (AI + fallback)  
4. Skills are compared with role benchmarks (CSV)  
5. Resume is evaluated for structure and quality  
6. AI generates:
   - Suggestions
   - Learning roadmap  
7. Results are returned and displayed in UI  

---

## 5. AI Integration

### Model Used:
- Groq (LLaMA 3.1 8B)

### Approach:
- Hybrid system:
  - AI-based processing (primary)
  - Rule-based fallback (secondary)
- Structured prompting ensures consistent output format
- Resume + role + missing skills are embedded into prompts

### Structured Data Grounding:
- A CSV-based schema acts as a benchmark for each role
- The model compares user skills against this structured data
- This improves consistency and reduces randomness

### Why not full RAG?
A full Retrieval-Augmented Generation (RAG) pipeline (with embeddings and vector databases) was not implemented due to time and complexity constraints. Instead, structured data grounding using CSV-based role definitions was used to simulate retrieval in a lightweight way.

### Fallback Mechanism:
- If AI fails:
  - Rule-based skill extraction is used
  - Predefined suggestions and roadmaps are returned
- Ensures system reliability

---

## 6. Core Features

### 1. Resume Analysis
- Extracts skills from resume
- Computes reliability score
- Identifies missing sections

### 2. Skill Gap Analysis
- Compares user skills vs role requirements
- Outputs:
  - Present skills
  - Missing skills

### 3. AI Suggestions
- Provides structured improvement suggestions
- Uses prompt-controlled formatting

### 4. Learning Roadmap
- Step-by-step guidance for skill development
- AI-generated with fallback support

### 5. Quiz System
- Role-based quiz from CSV dataset
- Evaluates knowledge and provides explanations

---

## 7. Design Decisions & Tradeoffs

### Decision 1: Hybrid AI + Rule-Based System
- Ensures reliability even if AI fails
- Tradeoff: Slight increase in code complexity

### Decision 2: Structured CSV Data instead of Full RAG
- Simpler and faster implementation
- Tradeoff: Less dynamic retrieval compared to full RAG

### Decision 3: Prompt-Based Scoring
- Flexible and adaptable
- Tradeoff: Less deterministic than rule-based scoring

### Decision 4: Choice of LLM Provider
- Groq (LLaMA 3.1) selected for:
  - Low latency
  - Cost efficiency
- Tradeoff: Less ecosystem maturity compared to OpenAI

---

## 8. Testing & Validation

- Manual testing performed for:
  - Resume upload (PDF/DOCX)
  - Empty input handling
  - API failure scenarios
- Validation includes:
  - Output consistency
  - Correct formatting
  - Edge case handling

---

## 9. Limitations

- Scoring depends on prompt quality
- No persistent user data storage
- Limited dataset (CSV-based)
- No advanced resume parsing (e.g., NLP entity extraction)

---

## 10. Future Improvements

- Implement full RAG (vector database + embeddings)
- Add advanced resume parsing (NER-based)
- Improve scoring transparency
- Add user profiles and progress tracking
- Integrate real job descriptions dynamically

---