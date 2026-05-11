import { colors } from "../styles/tokens";

// Score → label + colors. Preserves original logic exactly.
function getScoreLabel(score, total) {
  const percent = (score / total) * 100;
  if (percent >= 80) return { label: "Excellent! 🌟",       color: colors.success, bg: colors.successBg };
  if (percent >= 60) return { label: "Good Job! 👍",        color: colors.warning, bg: colors.warningBg };
  if (percent >= 40) return { label: "Keep Practicing! 📚", color: colors.orange,  bg: colors.orangeBg  };
  return                    { label: "Needs Improvement! 💪", color: colors.danger,  bg: colors.dangerBg  };
}

// ---------- Sub-views ----------

function QuizErrorView({ error, onRetry }) {
  return (
    <div style={{
      backgroundColor: colors.surface,
      borderRadius: "16px",
      padding: "40px",
      border: `1px solid ${colors.border}`,
      textAlign: "center",
    }}>
      <div style={{ fontSize: "48px", marginBottom: "16px" }}>⚠️</div>
      <p style={{ color: colors.dangerText, fontSize: "16px", marginBottom: "24px" }}>{error}</p>
      <button onClick={onRetry} style={{
        padding: "12px 24px",
        backgroundColor: colors.primary,
        color: "white",
        border: "none",
        borderRadius: "10px",
        cursor: "pointer",
        fontSize: "14px",
        fontWeight: "600",
      }}>
        🔄 Try Again
      </button>
    </div>
  );
}

function QuizLoadingView() {
  return (
    <div style={{ textAlign: "center", padding: "60px", color: colors.textSecondary }}>
      ⏳ Loading questions...
    </div>
  );
}

function QuizResultsView({ questions, selectedAnswers, score, onRetake }) {
  const total = questions.length;
  const scoreValue = score();
  const scoreInfo = getScoreLabel(scoreValue, total);

  return (
    <div style={{
      backgroundColor: colors.surface,
      borderRadius: "16px",
      padding: "32px",
      border: `1px solid ${colors.border}`,
    }}>
      <h3 style={{ textAlign: "center", fontSize: "22px", marginBottom: "24px" }}>
        🏆 Quiz Results
      </h3>

      <div style={{ textAlign: "center", marginBottom: "24px" }}>
        <div style={{ fontSize: "64px", fontWeight: "700", color: scoreInfo.color }}>
          {scoreValue}/{total}
        </div>
        <span style={{
          padding: "6px 20px",
          borderRadius: "999px",
          fontSize: "15px",
          fontWeight: "700",
          backgroundColor: scoreInfo.bg,
          color: scoreInfo.color,
        }}>
          {scoreInfo.label}
        </span>

        <div style={{
          marginTop: "16px",
          height: "12px",
          backgroundColor: colors.bg,
          borderRadius: "999px",
          overflow: "hidden",
        }}>
          <div style={{
            width: `${(scoreValue / total) * 100}%`,
            height: "100%",
            backgroundColor: scoreInfo.color,
            borderRadius: "999px",
            transition: "width 0.5s ease",
          }} />
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        {questions.map((q, i) => {
          const userAnswer = selectedAnswers[i];
          const isCorrect = userAnswer === q.correct;
          return (
            <div key={i} style={{
              backgroundColor: colors.bg,
              borderRadius: "12px",
              padding: "16px",
              borderLeft: `4px solid ${isCorrect ? colors.success : colors.danger}`,
            }}>
              <div style={{
                fontSize: "14px",
                fontWeight: "600",
                color: colors.textPrimary,
                marginBottom: "8px",
              }}>
                Q{i + 1}. {q.question}
              </div>
              <div style={{
                fontSize: "13px",
                color: isCorrect ? colors.successText : colors.dangerText,
                marginBottom: "4px",
              }}>
                {isCorrect
                  ? "✅ Correct!"
                  : `❌ You answered: ${userAnswer} — Correct: ${q.correct}`}
              </div>
              <div style={{ fontSize: "13px", color: colors.textMuted, fontStyle: "italic" }}>
                💡 {q.explanation}
              </div>
            </div>
          );
        })}
      </div>

      <button onClick={onRetake} style={{
        marginTop: "24px",
        width: "100%",
        padding: "14px",
        fontSize: "15px",
        borderRadius: "12px",
        cursor: "pointer",
        backgroundColor: colors.primary,
        color: "white",
        border: "none",
        fontWeight: "600",
      }}>
        🔄 Retake Quiz
      </button>
    </div>
  );
}

function QuizQuestionView({
  questions, currentQuestion, selectedAnswers, onAnswer, onNext,
}) {
  const q = questions[currentQuestion];
  const selected = selectedAnswers[currentQuestion];
  const isLast = currentQuestion === questions.length - 1;

  return (
    <div style={{
      backgroundColor: colors.surface,
      borderRadius: "16px",
      padding: "32px",
      border: `1px solid ${colors.border}`,
    }}>
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "8px",
      }}>
        <span style={{ fontSize: "13px", color: colors.textSecondary }}>
          Question {currentQuestion + 1} of {questions.length}
        </span>
        <span style={{ fontSize: "13px", color: colors.textSecondary }}>
          {Object.keys(selectedAnswers).length} answered
        </span>
      </div>

      <div style={{
        height: "6px",
        backgroundColor: colors.bg,
        borderRadius: "999px",
        overflow: "hidden",
        marginBottom: "24px",
      }}>
        <div style={{
          width: `${((currentQuestion + 1) / questions.length) * 100}%`,
          height: "100%",
          backgroundColor: colors.primary,
          borderRadius: "999px",
          transition: "width 0.3s ease",
        }} />
      </div>

      <div style={{
        fontSize: "18px",
        fontWeight: "600",
        color: colors.textPrimary,
        marginBottom: "24px",
        lineHeight: "1.6",
      }}>
        {q.question}
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        {Object.entries(q.options).map(([key, value]) => {
          const isSelected = selected === key;
          return (
            <button
              key={key}
              onClick={() => onAnswer(key)}
              style={{
                padding: "14px 20px",
                borderRadius: "12px",
                cursor: "pointer",
                textAlign: "left",
                fontSize: "14px",
                fontWeight: isSelected ? "700" : "400",
                backgroundColor: isSelected ? colors.primaryBg : colors.bg,
                color: isSelected ? colors.primary : colors.textBright,
                border: `2px solid ${isSelected ? colors.primary : colors.border}`,
                transition: "all 0.2s ease",
              }}
            >
              <span style={{
                fontWeight: "700",
                marginRight: "12px",
                color: isSelected ? colors.primary : colors.textMuted,
              }}>
                {key}.
              </span>
              {value}
            </button>
          );
        })}
      </div>

      <button
        onClick={onNext}
        disabled={!selected}
        style={{
          marginTop: "24px",
          width: "100%",
          padding: "14px",
          fontSize: "15px",
          borderRadius: "12px",
          cursor: selected ? "pointer" : "not-allowed",
          backgroundColor: selected ? colors.primary : colors.surface,
          color: selected ? "white" : colors.textSubtle,
          border: "none",
          fontWeight: "600",
          transition: "all 0.2s ease",
        }}
      >
        {isLast ? "🏁 Finish Quiz" : "Next Question →"}
      </button>
    </div>
  );
}

// ---------- Top-level Quiz orchestrator ----------

export default function Quiz({ role, quiz, onExit }) {
  return (
    <div>
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "24px",
      }}>
        <h2 style={{ fontSize: "20px", color: colors.primary }}>🎯 {role} Quiz</h2>
        <button
          onClick={onExit}
          style={{
            padding: "8px 16px",
            backgroundColor: colors.surface,
            color: colors.textSecondary,
            border: `1px solid ${colors.border}`,
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "13px",
          }}
        >
          ✖ Exit Quiz
        </button>
      </div>

      {quiz.error ? (
        <QuizErrorView error={quiz.error} onRetry={() => quiz.start(role)} />
      ) : quiz.loading ? (
        <QuizLoadingView />
      ) : quiz.finished ? (
        <QuizResultsView
          questions={quiz.questions}
          selectedAnswers={quiz.selectedAnswers}
          score={quiz.score}
          onRetake={() => quiz.start(role)}
        />
      ) : (
        quiz.questions.length > 0 && (
          <QuizQuestionView
            questions={quiz.questions}
            currentQuestion={quiz.currentQuestion}
            selectedAnswers={quiz.selectedAnswers}
            onAnswer={quiz.answer}
            onNext={quiz.next}
          />
        )
      )}
    </div>
  );
}
