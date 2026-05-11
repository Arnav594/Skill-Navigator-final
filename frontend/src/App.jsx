// Top-level orchestrator. All state lives in hooks; this file just wires
// hooks → pages and decides whether to show the home view or the quiz view.

import { useState, useEffect } from "react";

import Header from "./components/Header";
import ErrorBanner from "./components/ErrorBanner";
import Quiz from "./components/Quiz";
import HomePage from "./pages/HomePage";

import { useRoles } from "./hooks/useRoles";
import { useResumeAnalysis } from "./hooks/useResumeAnalysis";
import { useQuiz } from "./hooks/useQuiz";

import { colors } from "./styles/tokens";

function App() {
  const { roles, selectedRole, setSelectedRole, error: rolesError } = useRoles();
  const analysis = useResumeAnalysis();
  const quiz = useQuiz();

  // Surface roles-loading error through the analysis error channel
  const [bootError, setBootError] = useState(null);
  useEffect(() => {
    if (rolesError) setBootError(rolesError);
  }, [rolesError]);

  const displayedError = analysis.error || bootError;
  const dismissError = () => {
    analysis.setError(null);
    setBootError(null);
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: colors.bg,
      color: "white",
      fontFamily: "'Segoe UI', sans-serif",
      padding: "40px 20px",
    }}>
      <div style={{ maxWidth: "800px", margin: "0 auto" }}>
        <Header />

        <ErrorBanner message={displayedError} onDismiss={dismissError} />

        {quiz.active ? (
          <Quiz role={selectedRole} quiz={quiz} onExit={quiz.exit} />
        ) : (
          <HomePage
            roles={roles}
            role={selectedRole}
            setRole={setSelectedRole}
            analysis={analysis}
            onStartQuiz={() => quiz.start(selectedRole)}
          />
        )}
      </div>
    </div>
  );
}

export default App;
