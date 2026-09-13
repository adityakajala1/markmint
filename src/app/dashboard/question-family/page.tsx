"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { getQuestionFamilies } from "@/lib/api";
import { QuestionFamily, Question } from "@/lib/types";
import { Loader2, X, Target, Clock, Filter, AlertTriangle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Panel,
  useNodesState,
  useEdgesState,
  Handle,
  Position,
  MarkerType,
  NodeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

// --- Custom Node Component ---
const CustomNode = ({ data }: NodeProps) => {
  const isRoot = data.type === "root";
  const isTopic = data.type === "topic";
  const isSubtopic = data.type === "subtopic";
  const isQuestionType = data.type === "question-type";

  return (
    <div
      className={cn(
        "relative flex flex-col items-center justify-center min-w-[150px] p-3 rounded-xl border transition-all duration-300",
        "bg-card/40 backdrop-blur-md hover:shadow-lg",
        isRoot && "border-primary/50 hover:shadow-primary/20",
        isTopic && "border-accent/50 hover:shadow-accent/20",
        isSubtopic && "border-success/50 hover:shadow-success/20",
        isQuestionType && "border-warning/50 hover:shadow-warning/20",
        !isRoot && !isTopic && !isSubtopic && !isQuestionType && "border-border hover:shadow-primary/20"
      )}
    >
      <Handle type="target" position={Position.Top} className="w-2 h-2 !bg-muted-foreground border-none" />
      <div className="flex flex-col items-center gap-1 text-center">
        <span className="font-semibold text-sm text-foreground">{data.label as string}</span>
        <span
          className={cn(
            "text-[10px] px-2 py-0.5 rounded-full font-medium uppercase tracking-wider",
            isRoot && "bg-primary/20 text-primary",
            isTopic && "bg-accent/20 text-accent",
            isSubtopic && "bg-success/20 text-success",
            isQuestionType && "bg-warning/20 text-warning",
            !isRoot && !isTopic && !isSubtopic && !isQuestionType && "bg-muted text-muted-foreground"
          )}
        >
          {data.type as string}
        </span>
      </div>
      <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-muted-foreground border-none" />
    </div>
  );
};

const nodeTypes = {
  custom: CustomNode,
};

// --- Helper functions for layout ---
const buildGraphFromFamilies = (families: QuestionFamily[]) => {
  const nodes: any[] = [];
  const edges: any[] = [];

  const rootId = "root";
  nodes.push({
    id: rootId,
    type: "custom",
    position: { x: 400, y: 0 },
    data: { label: "Subject", type: "root" },
  });

  // Calculate layout parameters
  const level1Y = 150;
  const level2Y = 300;
  const level3Y = 450;
  
  let currentTopicX = 0;

  families.forEach((family, fIndex) => {
    const topicId = `topic-${family.id}`;
    const xPos = currentTopicX + fIndex * 300;
    
    nodes.push({
      id: topicId,
      type: "custom",
      position: { x: xPos, y: level1Y },
      data: { 
        label: family.topic, 
        type: "topic",
        familyData: family
      },
    });

    edges.push({
      id: `e-${rootId}-${topicId}`,
      source: rootId,
      target: topicId,
      animated: true,
      style: { stroke: "#a78bfa" },
      markerEnd: { type: MarkerType.ArrowClosed, color: "#a78bfa" },
    });

    // Subtopics
    family.children?.forEach((child, cIndex) => {
      const subtopicId = `subtopic-${child.id}`;
      const subXPos = xPos + (cIndex - (family.children!.length - 1) / 2) * 200;

      nodes.push({
        id: subtopicId,
        type: "custom",
        position: { x: subXPos, y: level2Y },
        data: { 
          label: child.topic, 
          type: "subtopic",
          familyData: child
        },
      });

      edges.push({
        id: `e-${topicId}-${subtopicId}`,
        source: topicId,
        target: subtopicId,
        animated: true,
        style: { stroke: "#6366f1" },
        markerEnd: { type: MarkerType.ArrowClosed, color: "#6366f1" },
      });

      // Questions Types
      child.children?.forEach((leaf, lIndex) => {
        const leafId = `leaf-${leaf.id}`;
        const leafXPos = subXPos + (lIndex - (child.children!.length - 1) / 2) * 120;
        
        nodes.push({
          id: leafId,
          type: "custom",
          position: { x: leafXPos, y: level3Y },
          data: { 
            label: leaf.topic, 
            type: "question-type",
            familyData: leaf
          },
        });

        edges.push({
          id: `e-${subtopicId}-${leafId}`,
          source: subtopicId,
          target: leafId,
          animated: true,
          style: { stroke: "#22c55e" },
          markerEnd: { type: MarkerType.ArrowClosed, color: "#22c55e" },
        });
      });
    });
  });

  return { nodes, edges };
};

export default function QuestionFamilyPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [selectedNodeData, setSelectedNodeData] = useState<any | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const families = await getQuestionFamilies();
        const { nodes: initialNodes, edges: initialEdges } = buildGraphFromFamilies(families);
        
        // Simple centering logic
        const centeredNodes = initialNodes.map(n => ({ ...n, position: { x: n.position.x + 200, y: n.position.y + 50 } }));
        
        setNodes(centeredNodes);
        setEdges(initialEdges);
      } catch (error) {
        console.error("Failed to load question families", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [setNodes, setEdges]);

  const onNodeClick = useCallback((event: React.MouseEvent, node: any) => {
    if (node.data.type !== "root") {
      setSelectedNodeData(node.data);
    } else {
      setSelectedNodeData(null);
    }
  }, []);

  const closePanel = () => setSelectedNodeData(null);

  if (loading) {
    return (
      <div className="flex h-[calc(100vh-10rem)] items-center justify-center space-x-2">
        <Loader2 className="h-6 w-6 animate-spin text-primary" />
        <span className="text-muted-foreground">Loading families...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Question Families" 
        description="Explore how questions relate and evolve" 
      />

      <div className="relative h-[600px] w-full rounded-2xl overflow-hidden border border-border bg-card">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          fitView
          minZoom={0.2}
          maxZoom={2}
          className="bg-card"
        >
          <Background gap={16} size={1} color="#27272a" />
          <Controls className="!bg-card/50 !border-border fill-foreground" />
          <MiniMap 
            nodeBorderRadius={8} 
            nodeColor={(n) => {
              switch (n.data?.type) {
                case 'root': return '#a78bfa';
                case 'topic': return '#6366f1';
                case 'subtopic': return '#22c55e';
                case 'question-type': return '#f59e0b';
                default: return '#3f3f46';
              }
            }}
            maskColor="rgba(9, 9, 11, 0.8)"
            className="!bg-card !border-border rounded-xl" 
          />
        </ReactFlow>

        <AnimatePresence>
          {selectedNodeData && (
            <motion.div
              initial={{ opacity: 0, x: 100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 100 }}
              className="absolute top-0 right-0 h-full w-80 glass border-l border-border/50 p-6 shadow-2xl overflow-y-auto z-10 flex flex-col"
            >
              <div className="flex items-start justify-between mb-6">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className={cn(
                      "text-xs px-2 py-0.5 rounded-full font-medium uppercase tracking-wider",
                      selectedNodeData.type === "topic" && "bg-accent/20 text-accent",
                      selectedNodeData.type === "subtopic" && "bg-success/20 text-success",
                      selectedNodeData.type === "question-type" && "bg-warning/20 text-warning"
                    )}>
                      {selectedNodeData.type}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-foreground">{selectedNodeData.label}</h3>
                </div>
                <button 
                  onClick={closePanel}
                  className="p-1 rounded-md hover:bg-muted text-muted-foreground transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {selectedNodeData.familyData?.questions && selectedNodeData.familyData.questions.length > 0 ? (
                <div className="space-y-4 flex-1">
                  <h4 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
                    <Target className="w-4 h-4" /> Related Questions
                  </h4>
                  <div className="space-y-3">
                    {selectedNodeData.familyData.questions.map((q: Question) => (
                      <div key={q.id} className="p-3 rounded-xl bg-background/50 border border-border hover:border-primary/30 transition-colors">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-xs bg-primary/20 text-primary px-2 py-0.5 rounded-full">
                            {q.marks} Marks
                          </span>
                          <span className="text-xs flex items-center gap-1 text-muted-foreground">
                            <Clock className="w-3 h-3" /> {q.year}
                          </span>
                        </div>
                        <p className="text-sm text-foreground line-clamp-3">
                          {q.text}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center text-center opacity-50">
                  <Filter className="w-8 h-8 mb-2" />
                  <p className="text-sm">No direct questions in this node.</p>
                  <p className="text-xs">Explore sub-nodes to find specific questions.</p>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
