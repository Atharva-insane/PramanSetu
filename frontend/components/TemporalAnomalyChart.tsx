"use client";

import React from "react";
import { TrendingUp, AlertTriangle, ShieldCheck, DollarSign, Calendar } from "lucide-react";
import { useLanguage } from "@/context/LanguageContext";

interface MonthlyData {
  month: string;
  claimed_cr: number;
  approved_cr: number;
  intercepted_cr: number;
  is_march_rush: boolean;
}

interface TemporalAnomalyChartProps {
  monthlySeries: MonthlyData[];
  cumulativeProtected: number;
}

export default function TemporalAnomalyChart({ monthlySeries = [], cumulativeProtected = 9.52 }: TemporalAnomalyChartProps) {
  const { language } = useLanguage();
  const safeSeries = Array.isArray(monthlySeries) ? monthlySeries : [];
  const maxClaimed = safeSeries.length > 0 ? Math.max(...safeSeries.map((m) => m.claimed_cr), 1) : 1;

  return (
    <div className="space-y-6">
      
      {/* Top Banner */}
      <div className="p-4 rounded-lg bg-orange-50 border border-orange-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-orange-100 text-orange-700">
            <TrendingUp className="h-5 w-5" />
          </div>
          <div>
            <h4 className="font-bold text-orange-950 text-sm">
              {language === "हिंदी"
                ? "वित्तीय गति एवं 'मार्च-रश' विसंगति पहचान"
                : language === "தமிழ்"
                ? "நிதி வேகம் மற்றும் 'மார்ச் ரஷ்' முரண்பாடு கண்டறிதல்"
                : "Temporal Fund Velocity & “March Rush” Anomaly Detection"}
            </h4>
            <p className="text-slate-600 mt-0.5">
              {language === "हिंदी"
                ? "ऐतिहासिक विश्लेषण दर्शाता है कि वित्तीय वर्ष के अंत (मार्च) में फर्जी बिलों की संख्या में 3.8 गुना वृद्धि होती है।"
                : language === "தமிழ்"
                ? "நிதி ஆண்டின் இறுதியில் (மார்ச்) போலி பில்களில் 3.8 மடங்கு அதிகரிப்பு ஏற்படுவதை தரவு காட்டுகிறது."
                : "Historical analysis reveals a 3.8x surge in fraudulent milestone submissions during the financial year-end (March)."}
            </p>
          </div>
        </div>

        <div className="p-2.5 rounded-lg bg-white border border-orange-300 font-mono text-right shrink-0 shadow-sm">
          <span className="text-[9px] uppercase font-sans font-bold text-slate-500 block">
            {language === "हिंदी" ? "कुल सुरक्षित धनराशि" : "Cumulative Funds Protected"}
          </span>
          <span className="text-sm font-extrabold text-emerald-600">₹{cumulativeProtected} {language === "हिंदी" ? "करोड़" : "Crores"}</span>
        </div>
      </div>

      {/* Monthly Velocity Bar Chart */}
      <div className="civic-card p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <h3 className="text-sm font-bold text-[#0f2942]">
            {language === "हिंदी"
              ? "माह-दर-माह दावा राशि बनाम रोकी गई फर्जी राशि (₹ करोड़ में)"
              : "Month-over-Month Milestone Claim Volume vs. Interceptions (₹ in Crores)"}
          </h3>
          
          <div className="flex items-center space-x-4 text-xs font-mono">
            <div className="flex items-center space-x-1.5">
              <span className="h-3 w-3 rounded bg-slate-300 inline-block" />
              <span className="text-slate-600">{language === "हिंदी" ? "दावा राशि (₹ करोड़)" : "Claimed (₹ Cr)"}</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="h-3 w-3 rounded bg-emerald-500 inline-block" />
              <span className="text-emerald-700">{language === "हिंदी" ? "स्वीकृत राशि (₹ करोड़)" : "Approved (₹ Cr)"}</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="h-3 w-3 rounded bg-rose-500 inline-block" />
              <span className="text-rose-700">{language === "हिंदी" ? "रोकी गई राशि (₹ करोड़)" : "Intercepted (₹ Cr)"}</span>
            </div>
          </div>
        </div>

        {/* CSS Flex Bar Graph */}
        <div className="flex items-end justify-between gap-3 h-64 pt-6">
          {safeSeries.map((m) => {
            const heightPercent = (m.claimed_cr / maxClaimed) * 100;
            const approvedPercent = (m.approved_cr / m.claimed_cr) * 100;
            const interceptedPercent = (m.intercepted_cr / m.claimed_cr) * 100;

            return (
              <div key={m.month} className="flex-1 flex flex-col items-center gap-2 group relative">
                
                {/* Tooltip */}
                <div className="absolute bottom-full mb-2 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-900 text-white text-[10px] rounded p-2 pointer-events-none whitespace-nowrap shadow-xl z-20 font-mono">
                  <div className="font-bold border-b border-slate-700 pb-1 mb-1">{m.month} 2024</div>
                  <div>Claimed: ₹{m.claimed_cr} Cr</div>
                  <div className="text-emerald-400">Approved: ₹{m.approved_cr} Cr</div>
                  <div className="text-rose-400">Intercepted: ₹{m.intercepted_cr} Cr</div>
                  {m.is_march_rush && (
                    <div className="text-orange-400 font-bold mt-1">
                      {language === "हिंदी" ? "चेतावनी: मार्च-रश विसंगति" : "Alert: March-Rush Spike"}
                    </div>
                  )}
                </div>

                {/* Vertical Stacked Bar */}
                <div
                  style={{ height: `${heightPercent}%` }}
                  className={`w-full max-w-[48px] rounded-t flex flex-col justify-end overflow-hidden transition-all shadow-sm ${
                    m.is_march_rush ? "ring-2 ring-orange-500 ring-offset-2" : "bg-slate-200"
                  }`}
                >
                  <div style={{ height: `${interceptedPercent}%` }} className="bg-rose-500 w-full" />
                  <div style={{ height: `${approvedPercent}%` }} className="bg-emerald-500 w-full" />
                </div>

                {/* Month Label */}
                <div className="text-center font-mono text-xs">
                  <span className={`block font-bold ${m.is_march_rush ? "text-orange-700" : "text-slate-700"}`}>
                    {m.month}
                  </span>
                  {m.is_march_rush && (
                    <span className="text-[9px] font-bold text-orange-600 bg-orange-100 px-1 py-0.2 rounded mt-0.5 inline-block">
                      {language === "हिंदी" ? "मार्च-रश" : "RUSH"}
                    </span>
                  )}
                </div>

              </div>
            );
          })}
        </div>

      </div>

    </div>
  );
}
