"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FileText, HelpCircle, BookOpen, Target } from "lucide-react";

import {
  getDashboardStats,
  getTopicFrequencies,
  getMarksDistribution,
  getUnitDistribution,
  getQuestionTypes,
} from "@/lib/api";
import {
  DashboardStats,
  TopicFrequency,
  MarksDistribution,
  UnitDistribution,
  QuestionTypeStats,
} from "@/lib/types";

import { StatCard } from "@/components/ui/stat-card";
import { ChartCard } from "@/components/ui/chart-card";
import { SkeletonStatCard, SkeletonChart } from "@/components/ui/skeleton-loader";
import { ErrorState } from "@/components/ui/error-state";
import { TopicFrequencyChart } from "@/components/charts/topic-frequency-chart";
import { MarksDistributionChart } from "@/components/charts/marks-distribution-chart";
import { UnitDistributionChart } from "@/components/charts/unit-distribution-chart";
import { QuestionTypeChart } from "@/components/charts/question-type-chart";
import { PageHeader } from "@/components/layout/page-header";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [topicFrequencies, setTopicFrequencies] = useState<TopicFrequency[]>([]);
  const [marksDistribution, setMarksDistribution] = useState<MarksDistribution[]>([]);
  const [unitDistribution, setUnitDistribution] = useState<UnitDistribution[]>([]);
  const [questionTypes, setQuestionTypes] = useState<QuestionTypeStats[]>([]);
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [
        statsData,
        topicData,
        marksData,
        unitData,
        typesData,
      ] = await Promise.all([
        getDashboardStats(),
        getTopicFrequencies(),
        getMarksDistribution(),
        getUnitDistribution(),
        getQuestionTypes(),
      ]);

      setStats(statsData);
      setTopicFrequencies(topicData);
      setMarksDistribution(marksData);
      setUnitDistribution(unitData);
      setQuestionTypes(typesData);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("An unknown error occurred"));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (error) {
    return (
      <div className="flex h-full items-center justify-center py-10">
        <ErrorState
          title="Failed to load dashboard data"
          message={error.message}
          onRetry={fetchData}
        />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Dashboard"
        description="Overview of exam pattern analysis"
      />

      {isLoading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <SkeletonStatCard key={`stat-skeleton-${i}`} />
          ))}
        </div>
      ) : stats && (
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4"
        >
          <motion.div variants={item}>
            <StatCard
              title="Papers Analyzed"
              value={stats.papersAnalyzed}
              icon={<FileText className="h-5 w-5" />}
              description="Total previous year papers"
            />
          </motion.div>
          <motion.div variants={item}>
            <StatCard
              title="Total Questions"
              value={stats.totalQuestions}
              icon={<HelpCircle className="h-5 w-5" />}
              description="Questions extracted"
            />
          </motion.div>
          <motion.div variants={item}>
            <StatCard
              title="Topics Detected"
              value={stats.topicsDetected}
              icon={<BookOpen className="h-5 w-5" />}
              description="Unique sub-topics found"
            />
          </motion.div>
          <motion.div variants={item}>
            <StatCard
              title="Prediction Confidence"
              value={`${stats.predictionConfidence}%`}
              icon={<Target className="h-5 w-5" />}
              description="Based on historical accuracy"
            />
          </motion.div>
        </motion.div>
      )}

      {isLoading ? (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <SkeletonChart key={`chart-skeleton-${i}`} />
          ))}
        </div>
      ) : (
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 gap-6 lg:grid-cols-2"
        >
          <motion.div variants={item}>
            <ChartCard
              title="Topic Frequency"
              description="How often each topic appears"
            >
              <TopicFrequencyChart data={topicFrequencies} />
            </ChartCard>
          </motion.div>
          <motion.div variants={item}>
            <ChartCard
              title="Marks Distribution"
              description="Breakdown by marks"
            >
              <MarksDistributionChart data={marksDistribution} />
            </ChartCard>
          </motion.div>
          <motion.div variants={item}>
            <ChartCard
              title="Unit Distribution"
              description="Weight of each unit"
            >
              <UnitDistributionChart data={unitDistribution} />
            </ChartCard>
          </motion.div>
          <motion.div variants={item}>
            <ChartCard
              title="Question Types"
              description="Breakdown by type"
            >
              <QuestionTypeChart data={questionTypes} />
            </ChartCard>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}
