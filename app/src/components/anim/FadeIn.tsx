"use client";
import { motion } from "framer-motion";
export const FadeIn = ({ children }: {children: React.ReactNode}) => (
  <motion.div initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} transition={{duration:.25}}>
    {children}
  </motion.div>
);


