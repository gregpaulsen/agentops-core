"use client";
import React from "react";
export class ErrorBoundary extends React.Component<any,{error?:Error}>{
  state = { error: undefined as Error|undefined };
  static getDerivedStateFromError(error: Error){ return { error }; }
  render(){
    if(this.state.error) return <div className="p-6 text-red-600">Something went wrong.</div>;
    return this.props.children;
  }
}


