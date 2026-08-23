"use client";

import React, { useState, useEffect } from "react";
import {
  BarChart3,
  ShieldAlert,
  ShieldCheck,
  Award,
  AlertTriangle,
  Search,
  Filter,
  DollarSign,
  Users,
  CheckCircle2,
  TrendingDown,
  Scale,
  Landmark,
  FileText
} from "lucide-react";
import { fetchContractors, fetchAuditLedger } from "@/lib/api";
import { escapeCsvCell } from "@/lib/bundleExporter";
import { useLanguage } from "@/context/LanguageContext";

export default function VigilanceDashboardPage() {
  const { t } = useLanguage();
  const [contractors, setContractors] = useState<any[]>([]);
  const [filterScheme, setFilterScheme] = useState("ALL");
  const [filterRisk, setFilterRisk] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [liveAudits, setLiveAudits] = useState<any[]>([]);

  useEffect(() => {
    async function loadData() {
      const contData = await fetchContractors();
      if (contData && contData.contractors) {
        setContractors(contData.contractors);
      }

      const auditData = await fetchAuditLedger();
      if (auditData && auditData.audits && auditData.audits.length > 0) {
        const mapped = auditData.audits.map((a: any) => ({
          id: a.dossier_id || `AUD-${a.tender_id}`,
          date: a.created_at_utc ? a.created_at_utc.slice(0, 10) : new Date().toISOString().slice(0, 10),
          scheme: a.scheme || "PMGSY",
          project: a.project_name || "Infrastructure Milestone",
          contractor: a.contractor_name || "Contractor",
          claim: a.claim_amount || "₹0",
          riskScore: a.risk_score || 0,
          verdict: a.verdict || "CLEAR",
          primaryAnomaly: a.decision_reason || "Pre-approval audit complete",
          action: a.recommended_action || "Disbursement Verified"
        }));
        setLiveAudits(mapped);
      }
    }
    loadData();
  }, []);

  const auditLedger = [
    {
      id: "DOSSIER-2024-VAR-402",
      date: "2024-07-15",
      scheme: "PMGSY 2024",
      project: "Rural Bituminous Connectivity Road - Sector 4",
      contractor: "Varanasi Highway Developers Ltd.",
      claim: "₹50,00,000",
      riskScore: 5,
      verdict: "CLEAR",
      primaryAnomaly: "None (All 10 Forensic Vectors Verified Clean)",
      action: "Clearance Certificate Issued • Treasury Sanctioned"
    },
    {
      id: "DOSSIER-2024-PRY-881",
      date: "2024-07-15",
      scheme: "Jal Jeevan Mission 2024",
      project: "Drinking Water Pipeline Network Scheme",
      contractor: "M/s Apex Civil Constructions Ltd.",
      claim: "₹45,00,000",
      riskScore: 92,
      verdict: "FLAGGED",
      primaryAnomaly: "Multi-Vector: Asset Recycling (pHash 0) + Ghost Labor (₹3.15L Leakage)",
      action: "Show-Cause Notice Issued (GFR 175) • Payment Freeze"
    }
  ];

  const effectiveLedger = liveAudits.length > 0 ? [...liveAudits, ...auditLedger] : auditLedger;

  const filteredLedger = effectiveLedger.filter((item) => {
    const matchesScheme = filterScheme === "ALL" || item.scheme.includes(filterScheme);
    const matchesRisk = filterRisk === "ALL" || item.verdict === filterRisk;
    const matchesSearch =
      searchQuery === "" ||
      item.project.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.contractor.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesScheme && matchesRisk && matchesSearch;
  });

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs uppercase font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-700 border border-blue-200">
              State Vigilance & Financial Directorate
            </span>
            <h1 className="text-2xl font-extrabold text-[#0f2942] tracking-tight">
              Vigilance Intelligence & Contractor Risk Ledger
            </h1>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            Centralized macro oversight of public infrastructure disbursements, repeat contractor risk ratings, and fraud mitigation.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => {
              const headers = "Dossier ID,Date,Scheme,Project,Contractor,Claim Amount,Risk Score,Verdict,Primary Anomaly,Vigilance Action\n";
              const rows = filteredLedger.map((r) =>
                `${escapeCsvCell(r.id)},${escapeCsvCell(r.date)},${escapeCsvCell(r.scheme)},${escapeCsvCell(r.project)},${escapeCsvCell(r.contractor)},${escapeCsvCell(r.claim)},${Number(r.riskScore) || 0},${escapeCsvCell(r.verdict)},${escapeCsvCell(r.primaryAnomaly)},${escapeCsvCell(r.action)}`
              ).join("\n");
              const blob = new Blob([headers + rows], { type: "text/csv;charset=utf-8;" });
              const url = URL.createObjectURL(blob);
              const link = document.createElement("a");
              link.href = url;
              link.setAttribute("download", `pramansetu_vigilance_ledger_${new Date().toISOString().slice(0, 10)}.csv`);
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            }}
            className="px-3 py-1.5 rounded bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold border border-slate-300 shadow-xs flex items-center space-x-1.5 transition-colors"
          >
            <FileText className="h-3.5 w-3.5 text-orange-600" />
            <span>Export Ledger CSV</span>
          </button>
          <div className="p-2 rounded bg-white border border-slate-200 font-mono text-xs text-slate-700 shadow-xs">
            Financial Year 2024–2025
          </div>
        </div>
      </div>

      {/* Macro Key Performance Indicators (Clean White Cards) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="civic-card p-5 space-y-2">
          <span className="text-xs text-slate-500 font-semibold uppercase">Total Claims Screened</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-[#0f2942] font-mono">62</span>
            <span className="text-xs text-emerald-700 font-bold bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">100% Pre-Approval</span>
          </div>
          <p className="text-[11px] text-slate-500">Across 5 National & State Schemes</p>
        </div>

        <div className="civic-card p-5 space-y-2">
          <span className="text-xs text-slate-500 font-semibold uppercase">Pre-Disbursement Savings</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-orange-600 font-mono">₹5.42 Cr</span>
            <span className="text-xs text-slate-600 font-semibold">Protected</span>
          </div>
          <p className="text-[11px] text-slate-500">Prevented before treasury release</p>
        </div>

        <div className="civic-card p-5 space-y-2">
          <span className="text-xs text-slate-500 font-semibold uppercase">High-Risk Interception</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-rose-600 font-mono">16.1%</span>
            <span className="text-xs text-rose-700 font-bold bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200">10 Flagged</span>
          </div>
          <p className="text-[11px] text-slate-500">Show-Cause notices served</p>
        </div>

        <div className="civic-card p-5 space-y-2">
          <span className="text-xs text-slate-500 font-semibold uppercase">Ghost Labor Prevented</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-purple-700 font-mono">₹18.9 L</span>
            <span className="text-xs text-purple-700 font-bold bg-purple-50 px-1.5 py-0.5 rounded border border-purple-200">42 Workers</span>
          </div>
          <p className="text-[11px] text-slate-500">Phantom muster entries caught</p>
        </div>
      </div>

      {/* Contractor Integrity Scorecards */}
      <div className="civic-card p-6 space-y-4">
        <div>
          <h3 className="text-base font-bold text-[#0f2942] flex items-center space-x-2">
            <Award className="h-5 w-5 text-orange-600" />
            <span>Contractor Integrity Risk Scorecards & Repeat Offender Ledger</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Tracks historical compliance across tenders, flagging habitual offenders for debarment on GeM.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {contractors.map((c) => (
            <div
              key={c.contractor_id}
              className={`p-4 rounded-lg border space-y-3 ${
                c.risk_tier === "HIGH_RISK"
                  ? "bg-rose-50/60 border-rose-200"
                  : "bg-slate-50/60 border-slate-200"
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-xs font-bold text-[#0f2942]">{c.contractor_name}</h4>
                  <span className="text-[10px] text-slate-500 font-mono">{c.registration_no}</span>
                </div>
                <span
                  className={`text-[9px] uppercase font-bold px-2 py-0.5 rounded border ${
                    c.risk_tier === "HIGH_RISK"
                      ? "bg-rose-100 text-rose-800 border-rose-300"
                      : "bg-emerald-100 text-emerald-800 border-emerald-300"
                  }`}
                >
                  {c.risk_tier}
                </span>
              </div>

              <div className="flex items-center justify-between text-xs font-mono pt-2 border-t border-slate-200">
                <div>
                  <span className="text-slate-500 block text-[9px] font-sans">Integrity Score</span>
                  <span className="text-xs font-bold text-slate-900">{c.integrity_score}/100</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[9px] font-sans">Trust Rating</span>
                  <span className="text-xs font-bold text-orange-600">{c.star_rating} ★</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[9px] font-sans">Flags Logged</span>
                  <span className={`text-xs font-bold ${c.flags_recorded > 0 ? "text-rose-600" : "text-slate-600"}`}>
                    {c.flags_recorded}
                  </span>
                </div>
              </div>

              <p className="text-[11px] text-slate-600 leading-snug pt-1">
                {c.cvo_recommendation}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Central Pre-Approval Audit Ledger Table */}
      <div className="civic-card p-6 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h3 className="text-base font-bold text-[#0f2942] flex items-center space-x-2">
              <Scale className="h-5 w-5 text-orange-600" />
              <span>{t.dashboardTitle}</span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              {t.dashboardSubtitle}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <div className="relative">
              <Search className="h-3.5 w-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder={t.searchPlaceholder}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-white border border-slate-300 rounded pl-8 pr-3 py-1.5 text-xs text-slate-900 focus:border-orange-500 focus:outline-none w-56 font-medium"
              />
            </div>

            <select
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
              className="bg-white border border-slate-300 rounded px-2.5 py-1.5 text-xs text-slate-900 focus:border-orange-500 focus:outline-none font-medium"
            >
              <option value="ALL">{t.filterAllRisk}</option>
              <option value="FLAGGED">FLAGGED (High)</option>
              <option value="REVIEW">REVIEW (Medium)</option>
              <option value="CLEAR">CLEAR (Low)</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider text-[10px] bg-slate-50">
                <th className="py-2.5 px-3">{t.colDossierId} / {t.colDate}</th>
                <th className="py-2.5 px-3">{t.colProject}</th>
                <th className="py-2.5 px-3">{t.colContractor}</th>
                <th className="py-2.5 px-3">{t.colClaimAmount}</th>
                <th className="py-2.5 px-3">{t.colRiskScore}</th>
                <th className="py-2.5 px-3">{t.colVerdict}</th>
                <th className="py-2.5 px-3">{t.colAction}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 font-medium text-slate-700">
              {filteredLedger.map((row) => (
                <tr key={row.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-3">
                    <span className="font-mono text-orange-700 font-bold block">{row.id}</span>
                    <span className="text-[10px] text-slate-500">{row.date}</span>
                  </td>
                  <td className="py-3 px-3">
                    <span className="text-slate-900 font-bold block">{row.project}</span>
                    <span className="text-[10px] text-slate-500">{row.scheme}</span>
                  </td>
                  <td className="py-3 px-3 text-slate-800">{row.contractor}</td>
                  <td className="py-3 px-3 font-mono font-bold text-orange-700">{row.claim}</td>
                  <td className="py-3 px-3">
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold border ${
                        row.riskScore >= 60
                          ? "bg-rose-100 text-rose-800 border-rose-200"
                          : row.riskScore >= 25
                          ? "bg-amber-100 text-amber-800 border-amber-200"
                          : "bg-emerald-100 text-emerald-800 border-emerald-200"
                      }`}
                    >
                      {row.riskScore}/100 ({row.verdict})
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-700">{row.primaryAnomaly}</td>
                  <td className="py-3 px-3">
                    <span className="text-[11px] font-semibold text-slate-700 px-2 py-0.5 rounded bg-slate-100 border border-slate-200 block text-center">
                      {row.action}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
