"use client";

import { motion } from "framer-motion";

export default function Template({ children }: { children: React.ReactNode }) {
  // We don't use AnimatePresence mode="wait" here because Next.js App Router 
  // currently doesn't unmount the old template immediately, which causes layout jumps.
  // Instead, we just trigger an entrance animation on route change.
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
