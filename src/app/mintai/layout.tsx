import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "MintAi | Predict Your Next Exam",
  description: "Chat with our custom AI to get instant, accurate answers about your syllabus, exams, and predict your paper.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
