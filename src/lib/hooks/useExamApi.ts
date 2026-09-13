"use client";
import { useState, useEffect, useCallback } from "react";
import { getCourse, getExamQuestions, getExamDNA, getExamPredictions } from "@/lib/api";

export function useExamApi(id: string | number) {
  const [course, setCourse] = useState<any>(null);
  const [questions, setQuestions] = useState<any>(null);
  const [dna, setDNA] = useState<any>(null);
  const [predictions, setPredictions] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [c, q, d, p] = await Promise.all([
        getCourse(id),
        getExamQuestions(id, 1, 50),
        getExamDNA(id),
        getExamPredictions(id)
      ]);
      setCourse(c); setQuestions(q); setDNA(d); setPredictions(p);
    } catch (e: any) {
      setError(e.message || "Failed to load exam data");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  return { course, questions, dna, predictions, loading, error, retry: fetchAll };
}
