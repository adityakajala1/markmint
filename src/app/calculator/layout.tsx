import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mint+ GPA Calculator | MarkMint",
  description: "Calculate your exact GPA across 40+ engineering branches with automated course fetching.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
