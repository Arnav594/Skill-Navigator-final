import { useState } from "react";
import { fetchQuiz } from "../api/client";

export function useQuiz() {
  const [active, setActive] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [finished, setFinished] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const start = async (role) => {
    setLoading(true);
    setActive(true);
    setFinished(false);
    setSelectedAnswers({});
    setCurrentQuestion(0);
    setError(null);

    try {
      const data = await fetchQuiz(role);
      if (data.error) {
        setError(data.error);
        setLoading(false);
        return;
      }
      setQuestions(data.questions || []);
    } catch (err) {
      setError("Could not load quiz questions. Please try again.");
    }
    setLoading(false);
  };

  const exit = () => {
    setActive(false);
    setFinished(false);
    setSelectedAnswers({});
    setCurrentQuestion(0);
    setError(null);
  };

  const answer = (key) => {
    setSelectedAnswers((prev) => ({ ...prev, [currentQuestion]: key }));
  };

  const next = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
    } else {
      setFinished(true);
    }
  };

  const score = () =>
    questions.reduce((acc, q, i) => acc + (selectedAnswers[i] === q.correct ? 1 : 0), 0);

  return {
    active,
    questions,
    currentQuestion,
    selectedAnswers,
    finished,
    loading,
    error,
    start,
    exit,
    answer,
    next,
    score,
  };
}
