import { useState } from "react";
import { analyzeResume } from "../api/client";
import { wantsRoadmap } from "../api/parsers";

export function useResumeAnalysis() {
  const [message, setMessage] = useState("");
  const [fileName, setFileName] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showRoadmap, setShowRoadmap] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    setUploadedFile(file);
  };

  const handleSubmit = async (role) => {
    if (!uploadedFile && !message) {
      setError("Please upload a resume or type a message.");
      return;
    }
    setLoading(true);
    setShowRoadmap(false);
    setResult(null);
    setError(null);

    const roadmapRequested = wantsRoadmap(message);

    try {
      const data = await analyzeResume({
        file: uploadedFile,
        message,
        role,
        roadmapRequested,
      });
      if (data.error) {
        setError(data.error);
        setLoading(false);
        return;
      }
      setResult(data);
      if (roadmapRequested) setShowRoadmap(true);
    } catch (err) {
      setError("Could not connect to the server. Please check your connection and try again.");
    }
    setLoading(false);
  };

  // Skill match % derived from result
  const matchPercent = (() => {
    if (!result) return 0;
    const total = result.skills.length + result.missing.length;
    if (total === 0) return 0;
    return Math.round((result.skills.length / total) * 100);
  })();

  return {
    // form state
    message, setMessage,
    fileName, uploadedFile, handleFileUpload,
    // result state
    result, loading, error, setError,
    showRoadmap, setShowRoadmap,
    matchPercent,
    // actions
    handleSubmit,
  };
}
