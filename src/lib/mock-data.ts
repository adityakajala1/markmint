import {
  DashboardStats,
  CourseInfo,
  TopicStat,
  Question,
  Prediction,
  TopicFrequency,
  MarksDistribution,
  UnitDistribution,
  QuestionTypeBreakdown,
  HeatmapCell,
  HistoricalTrend,
  MarksPattern,
  UnitWeight,
  ConfidenceGroup,
  QuestionFamily,
  StudyPlan
} from './types';

export const mockDashboardStats: DashboardStats = {
  papersAnalyzed: 12,
  totalQuestions: 487,
  topicsDetected: 34,
  predictionConfidence: 78
};

export const mockCourseInfo: CourseInfo = {
  id: 'CS301',
  name: 'Data Structures & Algorithms',
  code: 'CS301',
  semester: 4,
  examType: 'End Semester',
  academicYear: '2023-2024',
  department: 'Computer Science and Engineering'
};

export const mockTopicStats: TopicStat[] = [
  { topic: 'Binary Trees', frequency: 45, confidence: 92, unit: 3 },
  { topic: 'Graph Traversal', frequency: 38, confidence: 88, unit: 4 },
  { topic: 'Sorting Algorithms', frequency: 35, confidence: 85, unit: 2 },
  { topic: 'Dynamic Programming', frequency: 32, confidence: 80, unit: 5 },
  { topic: 'Hashing', frequency: 28, confidence: 75, unit: 2 },
  { topic: 'Linked Lists', frequency: 26, confidence: 90, unit: 1 },
  { topic: 'Stacks & Queues', frequency: 24, confidence: 86, unit: 1 },
  { topic: 'Greedy Algorithms', frequency: 22, confidence: 72, unit: 5 },
  { topic: 'Searching', frequency: 20, confidence: 78, unit: 2 },
  { topic: 'Heaps', frequency: 18, confidence: 65, unit: 3 },
  { topic: 'String Matching', frequency: 15, confidence: 60, unit: 4 },
  { topic: 'Complexity Analysis', frequency: 12, confidence: 55, unit: 1 }
];

export const mockQuestions: Question[] = [
  { id: 'q1', text: 'Explain the working of Quick Sort with an example. What is its time complexity in the worst case?', topic: 'Sorting Algorithms', unit: 2, marks: 10, year: 2023, type: ['Theory', 'Analysis'], difficulty: 3, confidence: 85, source: '2023-Q4' },
  { id: 'q2', text: 'Write a non-recursive function to traverse a binary tree in post-order.', topic: 'Binary Trees', unit: 3, marks: 15, year: 2022, type: ['Implementation'], difficulty: 4, confidence: 92, source: '2022-Q5' },
  { id: 'q3', text: 'Define a B-Tree. Construct a B-Tree of order 3 for the following data: 10, 20, 30, 40, 50, 60, 70, 80, 90.', topic: 'Binary Trees', unit: 3, marks: 10, year: 2024, type: ['Application'], difficulty: 3, confidence: 75, source: '2024-Q3' },
  { id: 'q4', text: 'Compare Adjacency Matrix and Adjacency List representations of a graph.', topic: 'Graph Traversal', unit: 4, marks: 5, year: 2023, type: ['Theory'], difficulty: 2, confidence: 88, source: '2023-Q6' },
  { id: 'q5', text: "Find the minimum spanning tree of the given graph using Kruskal's algorithm.", topic: 'Greedy Algorithms', unit: 5, marks: 10, year: 2021, type: ['Application'], difficulty: 3, confidence: 72, source: '2021-Q7' },
  { id: 'q6', text: "Solve the 0/1 Knapsack problem for the following items using Dynamic Programming: W=50, w={10,20,30}, v={60,100,120}.", topic: 'Dynamic Programming', unit: 5, marks: 15, year: 2023, type: ['Application', 'Implementation'], difficulty: 4, confidence: 80, source: '2023-Q8' },
  { id: 'q7', text: "What is a Hash Collision? Explain linear probing and quadratic probing with examples.", topic: 'Hashing', unit: 2, marks: 10, year: 2022, type: ['Theory'], difficulty: 2, confidence: 75, source: '2022-Q2' },
  { id: 'q8', text: "Write a C function to reverse a singly linked list in-place.", topic: 'Linked Lists', unit: 1, marks: 10, year: 2024, type: ['Implementation'], difficulty: 3, confidence: 90, source: '2024-Q1' },
  { id: 'q9', text: "Evaluate the following postfix expression using a stack: 5 3 + 8 2 - *", topic: 'Stacks & Queues', unit: 1, marks: 5, year: 2020, type: ['Application'], difficulty: 1, confidence: 86, source: '2020-Q2' },
  { id: 'q10', text: "Explain Dijkstra's shortest path algorithm. Trace it on a sample graph.", topic: 'Graph Traversal', unit: 4, marks: 15, year: 2024, type: ['Theory', 'Application'], difficulty: 3, confidence: 95, source: '2024-Q6' },
  { id: 'q11', text: 'Define asymptotic notations: Big-O, Omega, and Theta.', topic: 'Complexity Analysis', unit: 1, marks: 5, year: 2021, type: ['Theory'], difficulty: 2, confidence: 55, source: '2021-Q1' },
  { id: 'q12', text: 'Implement a circular queue using arrays.', topic: 'Stacks & Queues', unit: 1, marks: 10, year: 2022, type: ['Implementation'], difficulty: 3, confidence: 80, source: '2022-Q1' },
  { id: 'q13', text: 'How does binary search work? Write its recursive algorithm and find its time complexity.', topic: 'Searching', unit: 2, marks: 10, year: 2023, type: ['Implementation', 'Analysis'], difficulty: 2, confidence: 88, source: '2023-Q3' },
  { id: 'q14', text: 'What is a Max-Heap? Build a max-heap from the array: {4, 10, 3, 5, 1}.', topic: 'Heaps', unit: 3, marks: 10, year: 2020, type: ['Application'], difficulty: 3, confidence: 65, source: '2020-Q5' },
  { id: 'q15', text: 'Explain the KMP string matching algorithm. How does it improve upon the naive approach?', topic: 'String Matching', unit: 4, marks: 15, year: 2021, type: ['Theory', 'Analysis'], difficulty: 4, confidence: 60, source: '2021-Q8' },
  { id: 'q16', text: 'What is tail recursion? How is it different from normal recursion?', topic: 'Complexity Analysis', unit: 1, marks: 5, year: 2024, type: ['Theory'], difficulty: 2, confidence: 45, source: '2024-Q2' },
  { id: 'q17', text: 'Write an algorithm for deleting a node from a Binary Search Tree.', topic: 'Binary Trees', unit: 3, marks: 15, year: 2023, type: ['Implementation'], difficulty: 4, confidence: 92, source: '2023-Q5' },
  { id: 'q18', text: 'State the difference between DFS and BFS.', topic: 'Graph Traversal', unit: 4, marks: 5, year: 2022, type: ['Theory'], difficulty: 1, confidence: 95, source: '2022-Q7' },
  { id: 'q19', text: 'Explain Matrix Chain Multiplication using Dynamic Programming.', topic: 'Dynamic Programming', unit: 5, marks: 15, year: 2024, type: ['Theory', 'Application'], difficulty: 4, confidence: 85, source: '2024-Q9' },
  { id: 'q20', text: 'Find the optimal Huffman code for the given characters and frequencies: a(5), b(9), c(12), d(13), e(16), f(45).', topic: 'Greedy Algorithms', unit: 5, marks: 10, year: 2022, type: ['Application'], difficulty: 3, confidence: 75, source: '2022-Q9' }
];

export const mockPredictions: Prediction[] = [
  { topic: 'Binary Trees', probability: 92, confidence: 88, evidence: { papers_present: 11, total_papers: 12, long_answer_count: 8 }, historicalAppearances: [1, 2, 1, 3, 2] },
  { topic: 'Graph Traversal', probability: 85, confidence: 82, evidence: { papers_present: 10, total_papers: 12, long_answer_count: 5 }, historicalAppearances: [1, 1, 2, 1, 2] },
  { topic: 'Dynamic Programming', probability: 78, confidence: 75, evidence: { papers_present: 8, total_papers: 12, long_answer_count: 6 }, historicalAppearances: [0, 1, 1, 2, 1] },
  { topic: 'Sorting Algorithms', probability: 72, confidence: 80, evidence: { papers_present: 9, total_papers: 12, long_answer_count: 4 }, historicalAppearances: [2, 1, 0, 1, 1] },
  { topic: 'Hashing', probability: 65, confidence: 70, evidence: { papers_present: 7, total_papers: 12, long_answer_count: 2 }, historicalAppearances: [1, 0, 1, 0, 1] },
  { topic: 'Linked Lists', probability: 60, confidence: 75, evidence: { papers_present: 8, total_papers: 12, long_answer_count: 3 }, historicalAppearances: [1, 1, 0, 1, 1] },
  { topic: 'Stacks & Queues', probability: 55, confidence: 65, evidence: { papers_present: 6, total_papers: 12, long_answer_count: 1 }, historicalAppearances: [1, 0, 1, 1, 0] },
  { topic: 'Greedy Algorithms', probability: 50, confidence: 60, evidence: { papers_present: 5, total_papers: 12, long_answer_count: 3 }, historicalAppearances: [0, 1, 0, 1, 0] },
  { topic: 'Searching', probability: 45, confidence: 55, evidence: { papers_present: 6, total_papers: 12, long_answer_count: 1 }, historicalAppearances: [1, 0, 1, 0, 0] },
  { topic: 'Heaps', probability: 40, confidence: 50, evidence: { papers_present: 4, total_papers: 12, long_answer_count: 1 }, historicalAppearances: [1, 0, 0, 1, 0] }
];

export const mockTopicFrequencies: TopicFrequency[] = [
  { topic: 'Binary Trees', frequency: 45 },
  { topic: 'Graph Traversal', frequency: 38 },
  { topic: 'Sorting', frequency: 35 },
  { topic: 'DP', frequency: 32 },
  { topic: 'Hashing', frequency: 28 },
  { topic: 'Linked Lists', frequency: 26 },
  { topic: 'Stacks/Queues', frequency: 24 },
  { topic: 'Greedy', frequency: 22 }
];

export const mockMarksDistribution: MarksDistribution[] = [
  { marks: 2, count: 120, label: '2 Marks (Short)' },
  { marks: 5, count: 150, label: '5 Marks (Medium)' },
  { marks: 10, count: 140, label: '10 Marks (Long)' },
  { marks: 15, count: 77, label: '15 Marks (Very Long)' }
];

export const mockUnitDistribution: UnitDistribution[] = [
  { unit: 1, name: 'Basic Data Structures', weight: 15, questionCount: 95 },
  { unit: 2, name: 'Advanced Data Structures & Hashing', weight: 20, questionCount: 110 },
  { unit: 3, name: 'Trees & Heaps', weight: 25, questionCount: 125 },
  { unit: 4, name: 'Graphs & String Matching', weight: 20, questionCount: 90 },
  { unit: 5, name: 'Algorithm Design Techniques', weight: 20, questionCount: 67 }
];

export const mockQuestionTypes: QuestionTypeBreakdown[] = [
  { type: 'Theory', count: 180, percentage: 37 },
  { type: 'Implementation', count: 120, percentage: 25 },
  { type: 'Application', count: 100, percentage: 20 },
  { type: 'Analysis', count: 50, percentage: 10 },
  { type: 'Design', count: 37, percentage: 8 }
];

export const mockHeatmapData: HeatmapCell[] = [
  // 2020
  { topic: 'Binary Trees', year: 2020, frequency: 3 },
  { topic: 'Graph Traversal', year: 2020, frequency: 2 },
  { topic: 'Sorting', year: 2020, frequency: 4 },
  { topic: 'DP', year: 2020, frequency: 1 },
  { topic: 'Hashing', year: 2020, frequency: 2 },
  { topic: 'Linked Lists', year: 2020, frequency: 3 },
  { topic: 'Stacks/Queues', year: 2020, frequency: 3 },
  { topic: 'Greedy', year: 2020, frequency: 1 },
  // 2021
  { topic: 'Binary Trees', year: 2021, frequency: 4 },
  { topic: 'Graph Traversal', year: 2021, frequency: 3 },
  { topic: 'Sorting', year: 2021, frequency: 2 },
  { topic: 'DP', year: 2021, frequency: 2 },
  { topic: 'Hashing', year: 2021, frequency: 1 },
  { topic: 'Linked Lists', year: 2021, frequency: 2 },
  { topic: 'Stacks/Queues', year: 2021, frequency: 1 },
  { topic: 'Greedy', year: 2021, frequency: 2 },
  // 2022
  { topic: 'Binary Trees', year: 2022, frequency: 3 },
  { topic: 'Graph Traversal', year: 2022, frequency: 4 },
  { topic: 'Sorting', year: 2022, frequency: 3 },
  { topic: 'DP', year: 2022, frequency: 3 },
  { topic: 'Hashing', year: 2022, frequency: 3 },
  { topic: 'Linked Lists', year: 2022, frequency: 2 },
  { topic: 'Stacks/Queues', year: 2022, frequency: 2 },
  { topic: 'Greedy', year: 2022, frequency: 1 },
  // 2023
  { topic: 'Binary Trees', year: 2023, frequency: 5 },
  { topic: 'Graph Traversal', year: 2023, frequency: 3 },
  { topic: 'Sorting', year: 2023, frequency: 4 },
  { topic: 'DP', year: 2023, frequency: 4 },
  { topic: 'Hashing', year: 2023, frequency: 2 },
  { topic: 'Linked Lists', year: 2023, frequency: 3 },
  { topic: 'Stacks/Queues', year: 2023, frequency: 1 },
  { topic: 'Greedy', year: 2023, frequency: 3 },
  // 2024
  { topic: 'Binary Trees', year: 2024, frequency: 4 },
  { topic: 'Graph Traversal', year: 2024, frequency: 5 },
  { topic: 'Sorting', year: 2024, frequency: 2 },
  { topic: 'DP', year: 2024, frequency: 5 },
  { topic: 'Hashing', year: 2024, frequency: 3 },
  { topic: 'Linked Lists', year: 2024, frequency: 4 },
  { topic: 'Stacks/Queues', year: 2024, frequency: 2 },
  { topic: 'Greedy', year: 2024, frequency: 2 }
];

export const mockHistoricalTrends: HistoricalTrend[] = [
  { year: 2020, 'Binary Trees': 3, 'Graph Traversal': 2, 'DP': 1, 'Sorting': 4 },
  { year: 2021, 'Binary Trees': 4, 'Graph Traversal': 3, 'DP': 2, 'Sorting': 2 },
  { year: 2022, 'Binary Trees': 3, 'Graph Traversal': 4, 'DP': 3, 'Sorting': 3 },
  { year: 2023, 'Binary Trees': 5, 'Graph Traversal': 3, 'DP': 4, 'Sorting': 4 },
  { year: 2024, 'Binary Trees': 4, 'Graph Traversal': 5, 'DP': 5, 'Sorting': 2 }
];

export const mockMarksPattern: MarksPattern[] = [
  { year: 2020, '2marks': 20, '5marks': 30, '10marks': 25, '15marks': 10 },
  { year: 2021, '2marks': 22, '5marks': 28, '10marks': 28, '15marks': 12 },
  { year: 2022, '2marks': 25, '5marks': 32, '10marks': 26, '15marks': 15 },
  { year: 2023, '2marks': 24, '5marks': 29, '10marks': 30, '15marks': 18 },
  { year: 2024, '2marks': 29, '5marks': 31, '10marks': 31, '15marks': 22 }
];

export const mockUnitWeights: UnitWeight[] = [
  { unit: 1, name: 'Basic DS', weight: 15, topicCount: 4 },
  { unit: 2, name: 'Adv DS & Hashing', weight: 20, topicCount: 5 },
  { unit: 3, name: 'Trees & Heaps', weight: 25, topicCount: 3 },
  { unit: 4, name: 'Graphs & Strings', weight: 20, topicCount: 4 },
  { unit: 5, name: 'Algorithm Design', weight: 20, topicCount: 4 }
];

export const mockConfidenceGroups: ConfidenceGroup[] = [
  { level: 'high', topics: ['Binary Trees', 'Graph Traversal', 'Linked Lists'], evidenceCount: 45, description: 'Almost certain to appear. Very consistent history.' },
  { level: 'medium', topics: ['Dynamic Programming', 'Sorting Algorithms', 'Hashing'], evidenceCount: 28, description: 'Highly likely. Appears in most recent papers.' },
  { level: 'low', topics: ['Heaps', 'String Matching', 'Complexity Analysis'], evidenceCount: 12, description: 'Possible but inconsistent. Study if time permits.' }
];

export const mockQuestionFamilies: QuestionFamily = {
  id: 'root',
  label: 'Data Structures & Algorithms',
  type: 'root',
  children: [
    {
      id: 'graphs',
      label: 'Graph Traversal',
      type: 'topic',
      children: [
        {
          id: 'bfs',
          label: 'BFS',
          type: 'subtopic',
          children: [
            { id: 'bfs-theory', label: 'Theory', type: 'question-type' },
            { id: 'bfs-impl', label: 'Implementation', type: 'question-type' }
          ]
        },
        {
          id: 'dfs',
          label: 'DFS',
          type: 'subtopic',
          children: [
            { id: 'dfs-app', label: 'Application', type: 'question-type' }
          ]
        },
        {
          id: 'dijkstra',
          label: 'Dijkstra',
          type: 'subtopic',
          children: [
            { id: 'dijkstra-theory', label: 'Theory', type: 'question-type' },
            { id: 'dijkstra-impl', label: 'Implementation', type: 'question-type' }
          ]
        }
      ]
    },
    {
      id: 'trees',
      label: 'Binary Trees',
      type: 'topic',
      children: [
        { id: 'bst', label: 'Binary Search Tree', type: 'subtopic' },
        { id: 'avl', label: 'AVL Tree', type: 'subtopic' }
      ]
    }
  ]
};

export const mockStudyPlan: StudyPlan = {
  totalDays: 7,
  totalHours: 28,
  recommendations: [
    'Focus heavily on Binary Trees and Graphs early on.',
    'Practice Dynamic Programming code daily.',
    'Review theory questions for Hashing and Complexity Analysis.'
  ],
  days: [
    {
      day: 1,
      tasks: [
        { topic: 'Binary Trees (Theory & Traversals)', hours: 2, type: 'study', priority: 'high' },
        { topic: 'Binary Trees (Coding)', hours: 2, type: 'practice', priority: 'high' }
      ]
    },
    {
      day: 2,
      tasks: [
        { topic: 'Graph Traversal (BFS/DFS)', hours: 2, type: 'study', priority: 'high' },
        { topic: 'Shortest Path Algorithms', hours: 2, type: 'practice', priority: 'high' }
      ]
    },
    {
      day: 3,
      tasks: [
        { topic: 'Sorting Algorithms', hours: 2, type: 'revision', priority: 'medium' },
        { topic: 'Hashing Concepts', hours: 2, type: 'study', priority: 'medium' }
      ]
    },
    {
      day: 4,
      tasks: [
        { topic: 'Dynamic Programming (Knapsack, Matrix Chain)', hours: 3, type: 'study', priority: 'high' },
        { topic: 'DP Problems', hours: 1, type: 'practice', priority: 'high' }
      ]
    },
    {
      day: 5,
      tasks: [
        { topic: 'Linked Lists & Stacks/Queues', hours: 3, type: 'revision', priority: 'low' },
        { topic: 'Greedy Algorithms', hours: 1, type: 'study', priority: 'medium' }
      ]
    },
    {
      day: 6,
      tasks: [
        { topic: 'Heaps & String Matching', hours: 2, type: 'study', priority: 'low' },
        { topic: 'Previous Year Questions (2023, 2024)', hours: 2, type: 'mock-test', priority: 'high' }
      ]
    },
    {
      day: 7,
      tasks: [
        { topic: 'Full Mock Test', hours: 3, type: 'mock-test', priority: 'high' },
        { topic: 'Review Mistakes & Formulas', hours: 1, type: 'revision', priority: 'high' }
      ]
    }
  ]
};
