"use client";

import React, { useState, useEffect } from "react";
import {
  Globe,
  Share2,
  TrendingUp,
  Scale,
  ShieldAlert,
  ShieldCheck,
  Building,
  Landmark,
  Layers,
  ArrowUpRight,
  Download
} from "lucide-react";
import GeoRiskHeatmap from "@/components/GeoRiskHeatmap";
import CollusionNetworkGraph from "@/components/CollusionNetworkGraph";
import TemporalAnomalyChart from "@/components/TemporalAnomalyChart";
import { useLanguage } from "@/context/LanguageContext";
import { API_BASE_URL } from "@/lib/api";

export default function MacroAnalyticsPage() {
  const { t, language } = useLanguage();
  const [activeTab, setActiveTab] = useState<"geo" | "collusion" | "temporal" | "pipeline">("geo");
  const [geoData, setGeoData] = useState<any>(null);
  const [collusionData, setCollusionData] = useState<any>(null);
  const [temporalData, setTemporalData] = useState<any>(null);
  const [pipelineData, setPipelineData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchAnalytics() {
      try {
        const fetchSafe = async (endpoint: string) => {
          try {
            const res = await fetch(`${API_BASE_URL}${endpoint}`);
            if (res.ok) return await res.json();
            return null;
          } catch (e) {
            return null;
          }
        };

        const [geoRes, colRes, tempRes, pipeRes] = await Promise.all([
          fetchSafe("/api/analytics/geo-heatmap"),
          fetchSafe("/api/analytics/collusion-network"),
          fetchSafe("/api/analytics/temporal-trends"),
          fetchSafe("/api/analytics/enforcement-pipeline"),
        ]);
        if (geoRes) setGeoData(geoRes);
        if (colRes) setCollusionData(colRes);
        if (tempRes) setTemporalData(tempRes);
        if (pipeRes) setPipelineData(pipeRes);
      } catch (err) {
        console.error("Failed to load analytics data from API, fallback to default", err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchAnalytics();
  }, []);

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-bold tracking-widest uppercase text-orange-600 bg-orange-50 px-2 py-0.5 rounded border border-orange-200">
              {t.analytics}
            </span>
            <h1 className="text-2xl font-extrabold text-[#0f2942] tracking-tight">
              {t.analyticsTitle}
            </h1>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            {t.analyticsSubtitle}
          </p>
        </div>

        <button
          onClick={() => window.print()}
          className="px-3.5 py-1.5 rounded bg-white hover:bg-slate-50 text-xs font-bold text-slate-700 border border-slate-300 shadow-sm transition-colors flex items-center space-x-1.5"
        >
          <Download className="h-3.5 w-3.5" />
          <span>
            {language === "हिंदी" ? "कार्यकारी रिपोर्ट निर्यात करें" : language === "தமிழ்" ? "அறிக்கை பதிவிறக்கம்" : "Export Executive Report"}
          </span>
        </button>
      </div>

      {/* Top Macro KPI Ticker Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="civic-card p-5 space-y-1 border-emerald-200 bg-emerald-50/40">
          <span className="text-[10px] uppercase font-bold text-emerald-800 tracking-wider">
            {language === "हिंदी" ? "सुरक्षित सार्वजनिक धनराशि" : language === "தமிழ்" ? "பாதுகாக்கப்பட்ட பொது நிதி" : "Treasury Funds Protected"}
          </span>
          <div className="text-2xl font-extrabold text-emerald-700 font-mono">
            ₹{temporalData?.cumulative_protected_cr || "9.52"} Cr
          </div>
          <span className="text-[11px] text-slate-500 font-medium">
            {language === "हिंदी" ? "ट्रेजरी भुगतान से पूर्व रोकी गई" : "Intercepted prior to PFMS release"}
          </span>
        </div>

        <div className="civic-card p-5 space-y-1 border-rose-200 bg-rose-50/40">
          <span className="text-[10px] uppercase font-bold text-rose-800 tracking-wider">
            {language === "हिंदी" ? "उच्च-जोखिम परियोजना हॉटस्पॉट" : language === "தமிழ்" ? "அதிக ஆபத்து பகுதிகள்" : "High-Risk Project Hotspots"}
          </span>
          <div className="text-2xl font-extrabold text-rose-700 font-mono">
            {geoData?.flagged_count || 4} {language === "हिंदी" ? "जिले" : "Districts"}
          </div>
          <span className="text-[11px] text-slate-500 font-medium">
            {language === "हिंदी" ? "सक्रिय भुगतान रोक निर्देश" : "Active payment hold directives"}
          </span>
        </div>

        <div className="civic-card p-5 space-y-1 border-purple-200 bg-purple-50/40">
          <span className="text-[10px] uppercase font-bold text-purple-800 tracking-wider">
            {language === "हिंदी" ? "ठेकेदार मिलीभगत सिंडिकेट" : language === "தமிழ்" ? "ஒப்பந்தக்காரர் கூட்டு மோசடி" : "Collusion Syndicates Detected"}
          </span>
          <div className="text-2xl font-extrabold text-purple-700 font-mono">
            {collusionData?.syndicates_detected || 1} {language === "हिंदी" ? "सिंडिकेट" : "Rings"}
          </div>
          <span className="text-[11px] text-slate-500 font-medium">
            {language === "हिंदी" ? "निविदाओं के मध्य फोटो पुनर्चक्रण" : "Cross-tender reused photo links"}
          </span>
        </div>

        <div className="civic-card p-5 space-y-1 border-amber-200 bg-amber-50/40">
          <span className="text-[10px] uppercase font-bold text-amber-800 tracking-wider">
            {language === "हिंदी" ? "जब्त बैंक गारंटी" : language === "தமிழ்" ? "பறிமுதல் செய்யப்பட்ட வங்கி உத்தரவாதம்" : "Bank Guarantees Seized"}
          </span>
          <div className="text-2xl font-extrabold text-amber-700 font-mono">
            {pipelineData?.total_pbg_seized || "₹16,55,000"}
          </div>
          <span className="text-[11px] text-slate-500 font-medium">
            {language === "हिंदी" ? "GFR 2017 नियम 175 के तहत जब्त" : "Forfeited under GFR 2017 Rule 175"}
          </span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-3">
        <button
          onClick={() => setActiveTab("geo")}
          className={`flex items-center space-x-1.5 px-3.5 py-2 rounded text-xs font-bold transition-all ${
            activeTab === "geo"
              ? "bg-[#0f2942] text-white shadow-sm"
              : "bg-white text-slate-700 hover:bg-slate-100 border border-slate-200"
          }`}
        >
          <Globe className="h-4 w-4 text-orange-400" />
          <span>1. {t.tabHeatmap}</span>
        </button>

        <button
          onClick={() => setActiveTab("collusion")}
          className={`flex items-center space-x-1.5 px-3.5 py-2 rounded text-xs font-bold transition-all ${
            activeTab === "collusion"
              ? "bg-[#0f2942] text-white shadow-sm"
              : "bg-white text-slate-700 hover:bg-slate-100 border border-slate-200"
          }`}
        >
          <Share2 className="h-4 w-4 text-purple-400" />
          <span>2. {t.tabCollusion}</span>
        </button>

        <button
          onClick={() => setActiveTab("temporal")}
          className={`flex items-center space-x-1.5 px-3.5 py-2 rounded text-xs font-bold transition-all ${
            activeTab === "temporal"
              ? "bg-[#0f2942] text-white shadow-sm"
              : "bg-white text-slate-700 hover:bg-slate-100 border border-slate-200"
          }`}
        >
          <TrendingUp className="h-4 w-4 text-emerald-400" />
          <span>3. {t.tabTemporal}</span>
        </button>

        <button
          onClick={() => setActiveTab("pipeline")}
          className={`flex items-center space-x-1.5 px-3.5 py-2 rounded text-xs font-bold transition-all ${
            activeTab === "pipeline"
              ? "bg-[#0f2942] text-white shadow-sm"
              : "bg-white text-slate-700 hover:bg-slate-100 border border-slate-200"
          }`}
        >
          <Scale className="h-4 w-4 text-rose-400" />
          <span>4. {t.tabDebarment}</span>
        </button>
      </div>

      {/* Main Tab Content Display */}
      {activeTab === "geo" && (
        <GeoRiskHeatmap projects={geoData?.projects || []} />
      )}

      {activeTab === "collusion" && (
        <CollusionNetworkGraph nodes={collusionData?.nodes || []} links={collusionData?.links || []} />
      )}

      {activeTab === "temporal" && (
        <TemporalAnomalyChart
          monthlySeries={temporalData?.monthly_series || []}
          cumulativeProtected={temporalData?.cumulative_protected_cr || 9.52}
        />
      )}

      {activeTab === "pipeline" && (
        <div className="civic-card p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-200">
            <div>
              <h3 className="text-base font-bold text-[#0f2942]">
                Inter-Departmental Anti-Corruption & Debarment Pipeline
              </h3>
              <p className="text-xs text-slate-500">
                Live case tracking from GFR 175 Show-Cause notice to Bank Guarantee forfeiture and GeM blacklisting.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-slate-200 border-collapse">
              <thead>
                <tr className="bg-slate-100 border-b border-slate-300 font-bold text-slate-700 uppercase text-[10px]">
                  <th className="p-3 border-r border-slate-200">Case Ref</th>
                  <th className="p-3 border-r border-slate-200">Contractor & Scheme</th>
                  <th className="p-3 border-r border-slate-200">Disputed Amount</th>
                  <th className="p-3 border-r border-slate-200">Primary Infraction</th>
                  <th className="p-3 border-r border-slate-200">Current Enforcement Stage</th>
                  <th className="p-3 border-r border-slate-200">PBG Recovery</th>
                  <th className="p-3">GeM Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 font-medium">
                {pipelineData.cases.map((c: any, idx: number) => (
                  <tr key={idx} className="hover:bg-slate-50">
                    <td className="p-3 font-mono font-bold text-slate-900 border-r border-slate-200">{c.case_id}</td>
                    <td className="p-3 border-r border-slate-200">
                      <div className="font-bold text-slate-900">{c.contractor}</div>
                      <div className="text-slate-500 text-[11px]">{c.scheme}</div>
                    </td>
                    <td className="p-3 font-mono font-bold text-orange-700 border-r border-slate-200">{c.disputed_amount}</td>
                    <td className="p-3 border-r border-slate-200 text-rose-700 text-[11px]">{c.infraction}</td>
                    <td className="p-3 border-r border-slate-200">
                      <span className="px-2 py-0.5 rounded font-bold text-[10px] bg-amber-100 text-amber-900 border border-amber-200">
                        Stage {c.stage_step}/4: {c.current_stage}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-emerald-700 font-bold border-r border-slate-200">{c.pbg_status}</td>
                    <td className="p-3 font-bold text-slate-800 text-[11px]">{c.gem_debarment}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
}
