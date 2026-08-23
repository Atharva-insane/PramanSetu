"use client";

import React, { useState } from "react";
import { MapPin, ShieldAlert, ShieldCheck, AlertTriangle, Eye, Filter, ArrowUpRight, Layers } from "lucide-react";
import { useLanguage } from "@/context/LanguageContext";

interface ProjectPin {
  id: string;
  name: string;
  scheme: string;
  contractor: string;
  latitude: number;
  longitude: number;
  location_name: string;
  risk_score: number;
  status: "CLEAR" | "REVIEW" | "FLAGGED";
  claim_amount: string;
  protected_amount: string;
  discrepancy: string;
}

interface GeoRiskHeatmapProps {
  projects: ProjectPin[];
}

export default function GeoRiskHeatmap({ projects = [] }: GeoRiskHeatmapProps) {
  const safeProjects = Array.isArray(projects) ? projects : [];
  const { language } = useLanguage();
  const [selectedScheme, setSelectedScheme] = useState<string>("ALL");
  const [selectedStatus, setSelectedStatus] = useState<string>("ALL");
  const [activeProject, setActiveProject] = useState<ProjectPin | null>(
    safeProjects.length > 1 ? safeProjects[1] : (safeProjects[0] || null)
  );

  const filteredProjects = safeProjects.filter((p) => {
    const schemeMatch = selectedScheme === "ALL" || (p?.scheme || "").toLowerCase().includes(selectedScheme.toLowerCase());
    const statusMatch = selectedStatus === "ALL" || p?.status === selectedStatus;
    return schemeMatch && statusMatch;
  });

  // Normalized map coordinates for northern/central India cluster (25N-28N, 80E-86E)
  const getMapPosition = (lat: number, lon: number) => {
    const minLat = 24.5;
    const maxLat = 27.5;
    const minLon = 79.5;
    const maxLon = 86.0;

    const x = ((lon - minLon) / (maxLon - minLon)) * 100;
    const y = (1 - (lat - minLat) / (maxLat - minLat)) * 100;
    return { left: `${Math.max(8, Math.min(92, x))}%`, top: `${Math.max(12, Math.min(88, y))}%` };
  };

  return (
    <div className="space-y-4">
      
      {/* Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 bg-slate-50 border border-slate-200 rounded-lg text-xs">
        <div className="flex items-center space-x-2">
          <Filter className="h-4 w-4 text-slate-500" />
          <span className="font-bold text-slate-800">
            {language === "हिंदी" ? "भू-स्थानिक जोखिम फ़िल्टर करें:" : language === "தமிழ்" ? "வரைபட வடிகட்டி:" : "Filter Geographic Heatmap:"}
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <select
            value={selectedScheme}
            onChange={(e) => setSelectedScheme(e.target.value)}
            className="bg-white border border-slate-300 rounded px-2.5 py-1 text-xs text-slate-800 font-medium focus:outline-none focus:border-orange-500"
          >
            <option value="ALL">{language === "हिंदी" ? "सभी योजनाएं" : language === "தமிழ்" ? "அனைத்து திட்டங்கள்" : "All Schemes"}</option>
            <option value="PMGSY">PMGSY Rural Roads</option>
            <option value="Jal Jeevan">Jal Jeevan Mission</option>
            <option value="Smart Cities">Smart Cities Mission</option>
            <option value="NHAI">NHAI Highways</option>
          </select>

          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="bg-white border border-slate-300 rounded px-2.5 py-1 text-xs text-slate-800 font-medium focus:outline-none focus:border-orange-500"
          >
            <option value="ALL">{language === "हिंदी" ? "सभी जोखिम स्थितियां" : language === "தமிழ்" ? "அனைத்து நிலைகள்" : "All Risk Statuses"}</option>
            <option value="FLAGGED">{language === "हिंदी" ? "ध्वजंकित (जोखिम ≥ 60)" : "Flagged (Risk ≥ 60)"}</option>
            <option value="REVIEW">{language === "हिंदी" ? "समीक्षा (जोखिम 25-59)" : "Review (Risk 25-59)"}</option>
            <option value="CLEAR">{language === "हिंदी" ? "स्पष्ट (जोखिम < 25)" : "Clear (Risk < 25)"}</option>
          </select>

          <span className="text-[11px] text-slate-500 font-mono pl-2">
            {language === "हिंदी"
              ? `${safeProjects.length} में से ${filteredProjects.length} नोड प्रदर्शित`
              : `Showing ${filteredProjects.length} of ${safeProjects.length} nodes`}
          </span>
        </div>
      </div>

      {/* Main Map & Detail Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Interactive Regional Map Canvas */}
        <div className="lg:col-span-8 civic-card p-6 bg-slate-900 border-slate-800 text-white relative min-h-[440px] flex flex-col justify-between overflow-hidden shadow-xl">
          
          {/* Map Grid Background Texture */}
          <div className="absolute inset-0 bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:24px_24px] opacity-40 pointer-events-none" />

          {/* Map Header */}
          <div className="relative z-10 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Layers className="h-4 w-4 text-orange-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
                {language === "हिंदी"
                  ? "उत्तर क्षेत्रीय सार्वजनिक निर्माण गलियारा (उ.प्र. • बिहार)"
                  : "Northern Regional Public Works Corridor (UP • Bihar)"}
              </span>
            </div>

            {/* Map Legend */}
            <div className="flex items-center space-x-3 text-[10px] font-mono">
              <span className="flex items-center space-x-1">
                <span className="h-2 w-2 rounded-full bg-rose-500 inline-block" />
                <span>{language === "हिंदी" ? "ध्वजंकित (उच्च)" : "Flagged"}</span>
              </span>
              <span className="flex items-center space-x-1">
                <span className="h-2 w-2 rounded-full bg-amber-400 inline-block" />
                <span>{language === "हिंदी" ? "समीक्षा (मध्यम)" : "Review"}</span>
              </span>
              <span className="flex items-center space-x-1">
                <span className="h-2 w-2 rounded-full bg-emerald-400 inline-block" />
                <span>{language === "हिंदी" ? "स्पष्ट (निम्न)" : "Clear"}</span>
              </span>
            </div>
          </div>

          {/* Regional Reference Labels */}
          <div className="relative z-0 my-auto h-64 w-full">
            
            <div className="absolute top-4 left-8 text-slate-600 font-mono text-[10px] uppercase tracking-widest pointer-events-none">
              UTTAR PRADESH CORRIDOR
            </div>
            <div className="absolute bottom-6 right-8 text-slate-600 font-mono text-[10px] uppercase tracking-widest pointer-events-none">
              EASTERN / BIHAR CORRIDOR
            </div>

            {/* SVG Connecting Risk Lines */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
              <line x1="25%" y1="40%" x2="48%" y2="55%" stroke="#475569" strokeWidth="1" strokeDasharray="3 3" />
              <line x1="48%" y1="55%" x2="72%" y2="45%" stroke="#475569" strokeWidth="1" strokeDasharray="3 3" />
              <line x1="72%" y1="45%" x2="85%" y2="70%" stroke="#475569" strokeWidth="1" strokeDasharray="3 3" />
            </svg>

            {/* Interactive Project Pins */}
            {filteredProjects.map((p) => {
              const pos = getMapPosition(p.latitude, p.longitude);
              const isSelected = activeProject?.id === p.id;

              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setActiveProject(p)}
                  style={{ left: pos.left, top: pos.top }}
                  className={`absolute transform -translate-x-1/2 -translate-y-1/2 group transition-all z-20 ${
                    isSelected ? "scale-125 z-30" : "hover:scale-110"
                  }`}
                >
                  <div className="relative flex items-center justify-center">
                    {isSelected && (
                      <span className="absolute -inset-2 rounded-full bg-orange-500/30 animate-ping pointer-events-none" />
                    )}
                    
                    <div
                      className={`h-4 w-4 rounded-full border-2 border-slate-900 shadow-md flex items-center justify-center ${
                        p.status === "FLAGGED"
                          ? "bg-rose-500 ring-2 ring-rose-400/50"
                          : p.status === "REVIEW"
                          ? "bg-amber-400 ring-2 ring-amber-300/50"
                          : "bg-emerald-400 ring-2 ring-emerald-300/50"
                      }`}
                    />
                  </div>

                  {/* Pin Tooltip */}
                  <div className="absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-black/90 text-[10px] text-white font-mono whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none shadow-lg border border-slate-700">
                    {p.name.slice(0, 22)}...
                  </div>
                </button>
              );
            })}

          </div>

          {/* Map Footer Technical Strip */}
          <div className="relative z-10 flex items-center justify-between text-[10px] font-mono text-slate-400 border-t border-slate-800 pt-2">
            <span>Projection: EPSG:4326 WGS84 Datum</span>
            <span>Geospatial Coverage: 12 Districts Monitored</span>
          </div>

        </div>

        {/* Right: Selected Project Inspector Card */}
        <div className="lg:col-span-4 space-y-4">
          {activeProject ? (
            <div className="civic-card p-6 space-y-4 border-slate-300">
              
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <span
                  className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded border ${
                    activeProject.status === "FLAGGED"
                      ? "bg-rose-100 text-rose-800 border-rose-200"
                      : activeProject.status === "REVIEW"
                      ? "bg-amber-100 text-amber-800 border-amber-200"
                      : "bg-emerald-100 text-emerald-800 border-emerald-200"
                  }`}
                >
                  {activeProject.status} &bull; {language === "हिंदी" ? "जोखिम" : "RISK"} {activeProject.risk_score}/100
                </span>

                <span className="text-xs text-slate-500 font-mono">{activeProject.id}</span>
              </div>

              <div>
                <h3 className="text-sm font-bold text-[#0f2942] leading-snug">
                  {activeProject.name}
                </h3>
                <span className="text-xs text-slate-500 font-medium">{activeProject.scheme}</span>
              </div>

              <div className="space-y-2 text-xs font-mono bg-slate-50 p-3 rounded border border-slate-200">
                <div>
                  <span className="text-slate-500 font-sans block text-[10px]">
                    {language === "हिंदी" ? "स्थान:" : "Location:"}
                  </span>
                  <span className="text-slate-900 font-semibold">{activeProject.location_name}</span>
                </div>
                <div>
                  <span className="text-slate-500 font-sans block text-[10px]">
                    {language === "हिंदी" ? "ठेकेदार:" : "Contractor:"}
                  </span>
                  <span className="text-slate-900 font-semibold">{activeProject.contractor}</span>
                </div>
                <div className="flex justify-between pt-1 border-t border-slate-200">
                  <div>
                    <span className="text-slate-500 font-sans block text-[10px]">
                      {language === "हिंदी" ? "दावा:" : "Claimed:"}
                    </span>
                    <span className="text-slate-900 font-bold">{activeProject.claim_amount}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 font-sans block text-[10px]">
                      {language === "हिंदी" ? "सुरक्षित:" : "Protected:"}
                    </span>
                    <span className="text-emerald-700 font-bold">{activeProject.protected_amount}</span>
                  </div>
                </div>
              </div>

              <div className="p-3 rounded bg-slate-100 border border-slate-200 text-xs text-slate-800 leading-relaxed">
                <span className="font-bold block text-[10px] uppercase text-slate-600 mb-0.5">
                  {language === "हिंदी" ? "फोरेंसिक निष्कर्ष:" : "Forensic Finding:"}
                </span>
                {activeProject.discrepancy}
              </div>

              <a
                href="/intake"
                className="w-full py-2.5 rounded bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs uppercase tracking-wider flex items-center justify-center space-x-1.5 shadow-sm transition-all"
              >
                <span>
                  {language === "हिंदी" ? "पूर्ण डोसियर संवीक्षा करें" : "Scrutinize Full Milestone Voucher"}
                </span>
                <ArrowUpRight className="h-3.5 w-3.5" />
              </a>

            </div>
          ) : (
            <div className="civic-card p-8 text-center text-xs text-slate-500">
              {language === "हिंदी" ? "वास्तविक समय के साक्ष्य देखने के लिए किसी भी मैप मार्कर पर क्लिक करें।" : "Click any map marker to inspect real-time project forensics."}
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
