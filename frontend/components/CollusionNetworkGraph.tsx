"use client";

import React, { useState } from "react";
import { Share2, Users, FileText, AlertTriangle, ShieldAlert, Link as LinkIcon, Info } from "lucide-react";
import { useLanguage } from "@/context/LanguageContext";

interface NetworkNode {
  id: string;
  label: string;
  type: "contractor" | "tender" | "shared_asset";
  risk?: string;
  flagged_claims?: number;
  amount?: string;
  details?: string;
}

interface NetworkLink {
  source: string;
  target: string;
  relation: string;
  type: "bid" | "fraud_link" | "collusion_ring";
}

interface CollusionNetworkGraphProps {
  nodes: NetworkNode[];
  links: NetworkLink[];
}

export default function CollusionNetworkGraph({ nodes = [], links = [] }: CollusionNetworkGraphProps) {
  const safeNodes = Array.isArray(nodes) ? nodes : [];
  const { language } = useLanguage();
  const [selectedNode, setSelectedNode] = useState<NetworkNode | null>(safeNodes[0] || null);

  const getNode = (id: string, fallbackIdx: number): NetworkNode | null => {
    return safeNodes.find((n) => n.id === id) || safeNodes[fallbackIdx] || safeNodes[0] || null;
  };

  return (
    <div className="space-y-6">
      
      {/* Overview Banner */}
      <div className="p-4 rounded-lg bg-purple-50 border border-purple-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-2 text-purple-900 font-bold">
          <Share2 className="h-4 w-4 text-purple-700 shrink-0" />
          <span>
            {language === "हिंदी"
              ? "निविदाओं के मध्य ठेकेदार सिंडिकेट एवं साक्ष्य पुनर्चक्रण संजाल"
              : language === "தமிழ்"
              ? "ஒப்பந்தக்காரர் சிண்டிகேட் மற்றும் ஆதார மறுபயன்பாட்டு நெட்வொர்க்"
              : "Cross-Tender Contractor Syndicate & Evidence Recycling Network"}
          </span>
        </div>
        <div className="flex items-center space-x-3 text-purple-800 font-mono text-[11px]">
          <span>{language === "हिंदी" ? "सिंडिकेट पकड़े गए: 1" : "Syndicates Detected: 1"}</span>
          <span>&bull;</span>
          <span>{language === "हिंदी" ? "साझा साक्ष्य कड़ियां: 2" : "Shared Asset Links: 2"}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Interactive Node-Link Canvas */}
        <div className="lg:col-span-8 civic-card p-6 bg-slate-900 border-slate-800 text-white relative min-h-[460px] flex flex-col justify-between overflow-hidden shadow-xl">
          
          <div className="absolute inset-0 bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:20px_20px] opacity-30 pointer-events-none" />

          {/* Canvas Header */}
          <div className="relative z-10 flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
              {language === "हिंदी" ? "इंटरैक्टिव बोली संजाल अन्वेषक" : "Interactive Bidding Graph Explorer"}
            </span>
            
            <div className="flex items-center space-x-3 text-[10px] font-mono">
              <span className="flex items-center space-x-1">
                <span className="h-2.5 w-2.5 rounded-full bg-orange-500 inline-block" />
                <span>{language === "हिंदी" ? "ठेकेदार" : "Contractor"}</span>
              </span>
              <span className="flex items-center space-x-1">
                <span className="h-2.5 w-2.5 rounded bg-blue-500 inline-block" />
                <span>{language === "हिंदी" ? "निविदा" : "Tender"}</span>
              </span>
              <span className="flex items-center space-x-1">
                <span className="h-2.5 w-2.5 rounded-full bg-rose-500 inline-block" />
                <span>{language === "हिंदी" ? "साझा फोटो हैश" : "Shared Photo Hash"}</span>
              </span>
            </div>
          </div>

          {/* Graph Visual Canvas */}
          <div className="relative w-full h-[320px] my-4">
            
            {/* SVG Connecting Links */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
              {/* Collusion Ring between C1 and C2 */}
              <line x1="25%" y1="35%" x2="70%" y2="30%" stroke="#dc2626" strokeWidth="2.5" strokeDasharray="6" />
              {/* C1 to Tenders */}
              <line x1="25%" y1="35%" x2="15%" y2="75%" stroke="#64748b" strokeWidth="1.5" />
              <line x1="25%" y1="35%" x2="40%" y2="80%" stroke="#64748b" strokeWidth="1.5" />
              {/* C2 to Tender */}
              <line x1="70%" y1="30%" x2="85%" y2="75%" stroke="#64748b" strokeWidth="1.5" />
              {/* Photo Hash Links */}
              <line x1="25%" y1="35%" x2="48%" y2="50%" stroke="#f43f5e" strokeWidth="2" />
              <line x1="70%" y1="30%" x2="48%" y2="50%" stroke="#f43f5e" strokeWidth="2" />
            </svg>

            {/* Nodes Layout */}
            
            {/* Node 1: Apex Civil */}
            <button
              type="button"
              onClick={() => setSelectedNode(getNode("c1", 0))}
              style={{ top: "35%", left: "25%" }}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 p-3 rounded-full transition-all z-20 ${
                selectedNode?.id === "c1" ? "ring-4 ring-orange-400 bg-orange-600 scale-110" : "bg-orange-700 hover:scale-105"
              }`}
            >
              <Users className="h-5 w-5 text-white" />
              <span className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 rounded bg-black/80 text-[10px] whitespace-nowrap font-mono text-white">
                Apex Civil ({language === "हिंदी" ? "उच्च जोखिम" : "High Risk"})
              </span>
            </button>

            {/* Node 2: Shri Ram Infra */}
            <button
              type="button"
              onClick={() => setSelectedNode(getNode("c2", 1))}
              style={{ top: "30%", left: "70%" }}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 p-3 rounded-full transition-all z-20 ${
                selectedNode?.id === "c2" ? "ring-4 ring-orange-400 bg-orange-600 scale-110" : "bg-orange-700 hover:scale-105"
              }`}
            >
              <Users className="h-5 w-5 text-white" />
              <span className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 rounded bg-black/80 text-[10px] whitespace-nowrap font-mono text-white">
                Shri Ram Infra ({language === "हिंदी" ? "उच्च जोखिम" : "High Risk"})
              </span>
            </button>

            {/* Node 3: Shared Hash Asset */}
            <button
              type="button"
              onClick={() => setSelectedNode(getNode("h1", 4))}
              style={{ top: "50%", left: "48%" }}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 p-2.5 rounded-full transition-all z-20 ${
                selectedNode?.id === "h1" || selectedNode?.id === "hash1" ? "ring-4 ring-rose-400 bg-rose-600 scale-110" : "bg-rose-500 hover:scale-105 animate-pulse"
              }`}
            >
              <LinkIcon className="h-4 w-4 text-white" />
              <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 px-2 py-0.5 rounded bg-rose-950 text-[10px] whitespace-nowrap font-mono text-white border border-rose-800">
                {language === "हिंदी" ? "साझा फोटो हैश (दूरी 0)" : "Shared Photo Hash (Dist 0)"}
              </span>
            </button>

            {/* Node 4: Tender TDR-8819 */}
            <button
              type="button"
              onClick={() => setSelectedNode(getNode("t1", 2))}
              style={{ top: "75%", left: "15%" }}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 p-2.5 rounded transition-all z-20 ${
                selectedNode?.id === "t1" ? "ring-4 ring-blue-400 bg-blue-600 scale-110" : "bg-blue-700 hover:scale-105"
              }`}
            >
              <FileText className="h-4 w-4 text-white" />
              <span className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 rounded bg-black/80 text-[10px] whitespace-nowrap font-mono text-white">
                TDR-8819 (PMGSY)
              </span>
            </button>

            {/* Node 5: Tender TDR-9921 */}
            <button
              type="button"
              onClick={() => setSelectedNode(getNode("t2", 3))}
              style={{ top: "80%", left: "40%" }}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 p-2.5 rounded transition-all z-20 ${
                selectedNode?.id === "t2" ? "ring-4 ring-blue-400 bg-blue-600 scale-110" : "bg-blue-700 hover:scale-105"
              }`}
            >
              <FileText className="h-4 w-4 text-white" />
              <span className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 rounded bg-black/80 text-[10px] whitespace-nowrap font-mono text-white">
                TDR-9921 (JJM)
              </span>
            </button>

            {/* Node 6: Tender TDR-7742 */}
            <button
              type="button"
              onClick={() => setSelectedNode(getNode("t3", 2))}
              style={{ top: "75%", left: "85%" }}
              className="absolute transform -translate-x-1/2 -translate-y-1/2 p-2.5 rounded bg-blue-700 hover:scale-105 transition-all z-20"
            >
              <FileText className="h-4 w-4 text-white" />
              <span className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 rounded bg-black/80 text-[10px] whitespace-nowrap font-mono text-white">
                TDR-7742 (State PWD)
              </span>
            </button>

          </div>

          <div className="relative z-10 flex items-center justify-between text-[10px] font-mono text-slate-400 border-t border-slate-800 pt-2">
            <span>{language === "हिंदी" ? "फोरेंसिक संजाल विश्लेषण: 2 अलग-अलग कंपनियों द्वारा एक ही कार्यस्थल फोटो प्रस्तुत" : "Forensic Link: Duplicate pHash submitted by 2 distinct corporate entities"}</span>
            <span>CVC Alert 2024-CVO-991</span>
          </div>

        </div>

        {/* Right: Selected Node Details & Collusion Insights */}
        <div className="lg:col-span-4 space-y-4">
          {selectedNode ? (
            <div className="civic-card p-6 space-y-4 border-slate-300">
              
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-purple-100 text-purple-800 border border-purple-200">
                  {selectedNode.type}
                </span>
                <span className="text-xs text-slate-500 font-mono">{selectedNode.id}</span>
              </div>

              <div>
                <h3 className="text-sm font-bold text-[#0f2942] leading-snug">
                  {selectedNode.label}
                </h3>
                {selectedNode.risk && (
                  <span className="text-xs text-rose-600 font-bold block mt-0.5">
                    {language === "हिंदी" ? "जोखिम वर्गीकरण: " : "Risk: "}{selectedNode.risk}
                  </span>
                )}
              </div>

              <div className="p-3 bg-slate-50 rounded border border-slate-200 space-y-2 text-xs">
                {selectedNode.flagged_claims !== undefined && (
                  <div className="flex justify-between">
                    <span className="text-slate-500">{language === "हिंदी" ? "ध्वजंकित दावे:" : "Flagged Invoices:"}</span>
                    <span className="font-bold text-rose-600 font-mono">{selectedNode.flagged_claims}</span>
                  </div>
                )}
                {selectedNode.amount && (
                  <div className="flex justify-between">
                    <span className="text-slate-500">{language === "हिंदी" ? "विवादित मूल्य:" : "Disputed Value:"}</span>
                    <span className="font-bold text-slate-900 font-mono">{selectedNode.amount}</span>
                  </div>
                )}
                {selectedNode.details && (
                  <div className="pt-2 border-t border-slate-200 text-slate-600 leading-relaxed">
                    {selectedNode.details}
                  </div>
                )}
              </div>

              <div className="p-3 rounded bg-purple-50/70 border border-purple-200 text-xs text-purple-950 space-y-1">
                <span className="font-bold block text-[10px] uppercase text-purple-800">
                  {language === "हिंदी" ? "सीवीओ विधिक अनुशंसा:" : "CVO Legal Recommendation:"}
                </span>
                <p className="leading-snug">
                  {language === "हिंदी"
                    ? "GFR 2017 नियम 175 के तहत दोनों फर्मों के विरुद्ध संयुक्त कारण बताओ नोटिस एवं GeM पोर्टल पर काली सूची में डालने की संस्तुति।"
                    : "Issue joint show-cause under GFR 2017 Rule 175 for bid manipulation and asset recycling. Recommend joint GeM debarment."}
                </p>
              </div>

            </div>
          ) : (
            <div className="civic-card p-8 text-center text-xs text-slate-500">
              {language === "हिंदी" ? "सिंडिकेट विवरण देखने के लिए किसी भी नोड पर क्लिक करें।" : "Select any node on the graph to inspect collusion details."}
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
