"use client";

import React, { useState } from "react";
import {
  FileText,
  Copy,
  Check,
  AlertTriangle,
  Download,
  Scale,
  Users,
  ShieldAlert,
  Landmark,
  ShieldCheck,
  Clock,
  Printer,
  Archive,
  QrCode
} from "lucide-react";
import DigitalSignatureModal from "./DigitalSignatureModal";
import ContractorCureTracker from "./ContractorCureTracker";
import GazettePdfExporter from "./GazettePdfExporter";
import { exportVigilanceCaseBundle } from "@/lib/bundleExporter";
import { useLanguage } from "@/context/LanguageContext";

interface LegalDossierViewerProps {
  dossier: any;
  riskScore: number;
  verdict: string;
  auditData?: any;
}

export default function LegalDossierViewer({ dossier, riskScore, verdict, auditData }: LegalDossierViewerProps) {
  const { t, language } = useLanguage();
  const [activeTab, setActiveTab] = useState<"showcause" | "hold" | "vigilance" | "labor">("showcause");
  const [copied, setCopied] = useState(false);
  const [isSignModalOpen, setIsSignModalOpen] = useState(false);
  const [isPdfModalOpen, setIsPdfModalOpen] = useState(false);
  const [signatureData, setSignatureData] = useState<{
    officerName: string;
    designation: string;
    department: string;
    dscToken: string;
    signedAt: string;
  } | null>(null);

  if (!dossier) return null;

  const { hold_alert, show_cause_notice, vigilance_memo, annexure_b_labor_muster, watermark, dossier_id, generated_at, crypto_verification } = dossier;

  const getTextToCopy = () => {
    if (activeTab === "hold") return hold_alert?.directive || "";
    if (activeTab === "showcause") return show_cause_notice?.notice_text || "";
    if (activeTab === "vigilance") return vigilance_memo?.memo_text || "";
    if (activeTab === "labor") {
      return `ANNEXURE B: DISPUTED LABOR MUSTER ROLL\nTotal Suspected Leakage: ${annexure_b_labor_muster?.total_suspected_leakage}\n` +
        JSON.stringify(annexure_b_labor_muster?.flagged_workers || [], null, 2);
    }
    return "";
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(getTextToCopy());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadBundle = () => {
    exportVigilanceCaseBundle(auditData || { dossier, risk_score: riskScore, status: verdict }, signatureData);
  };

  return (
    <div className="civic-card p-6 space-y-6">
      
      {/* Modals */}
      <DigitalSignatureModal
        isOpen={isSignModalOpen}
        onClose={() => setIsSignModalOpen(false)}
        onSignSuccess={(sig) => setSignatureData(sig)}
      />

      {isPdfModalOpen && (
        <GazettePdfExporter
          auditData={auditData || { dossier, risk_score: riskScore, status: verdict, decision_reason: "Milestone integrity violation", project_metadata: {} }}
          signatureData={signatureData}
          onClose={() => setIsPdfModalOpen(false)}
        />
      )}

      {/* Top Watermark & QR Security Banner */}
      <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center space-x-2 text-amber-800 text-xs font-bold">
          <AlertTriangle className="h-4 w-4 text-amber-600 shrink-0" />
          <span>{watermark || "AI-GENERATED DRAFT — REQUIRES AUTHORIZED HUMAN REVIEW"}</span>
        </div>
        <div className="flex items-center space-x-3 text-[11px] font-mono text-slate-600 font-semibold">
          <span>Ref: {dossier_id}</span>
          <span className="hidden md:inline">&bull;</span>
          <a
            href={crypto_verification?.verification_url || `/verify?dossier_id=${dossier_id}`}
            target="_blank"
            rel="noreferrer"
            className="text-orange-700 hover:underline flex items-center space-x-1"
          >
            <QrCode className="h-3.5 w-3.5" />
            <span>Verify QR Seal</span>
          </a>
        </div>
      </div>

      {/* Header and Quick Action Buttons */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-3 border-b border-slate-200">
        <div>
          <h3 className="text-base font-bold text-[#0f2942] flex items-center space-x-2">
            <Scale className="h-4 w-4 text-orange-600" />
            <span>
              {language === "हिंदी"
                ? "प्रशासनिक विधिक डोसियर एवं वैधानिक नोटिस"
                : language === "தமிழ்"
                ? "சட்ட ஆவணம் மற்றும் அறிவிப்பு ஜெனரேட்டர்"
                : "Administrative Legal Dossier & Statutory Notice Generator"}
            </span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            {language === "हिंदी"
              ? "सामान्य वित्तीय नियम (GFR 2017) नियम 175 के तहत स्वतः जनित विधिक प्रारूप।"
              : language === "தமிழ்"
              ? "GFR 2017 விதி 175 இன் கீழ் தானாக உருவாக்கப்பட்ட சட்ட ஆவணம்."
              : "Auto-generated administrative drafts citing General Financial Rules (GFR 2017) Rule 175."}
          </p>
        </div>

        {/* Action Button Bar */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setIsSignModalOpen(true)}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded text-xs font-bold transition-all ${
              signatureData
                ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                : "bg-orange-50 text-orange-700 border border-orange-200 hover:bg-orange-100"
            }`}
          >
            <ShieldCheck className="h-3.5 w-3.5" />
            <span>
              {signatureData
                ? language === "हिंदी"
                  ? "DSC सिमुलेशन लागू ✓"
                  : "DSC Simulation Applied ✓"
                : language === "हिंदी"
                ? "DSC सिमुलेशन लागू करें"
                : "Simulate DSC Seal"}
            </span>
          </button>

          <button
            onClick={() => setIsPdfModalOpen(true)}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-orange-600 hover:bg-orange-700 text-white text-xs font-bold shadow-sm transition-all"
          >
            <Printer className="h-3.5 w-3.5" />
            <span>
              {language === "हिंदी" ? "राजपत्र PDF डाउनलोड" : "Export Gazette PDF"}
            </span>
          </button>

          <button
            onClick={handleDownloadBundle}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold shadow-sm transition-all"
          >
            <Archive className="h-3.5 w-3.5" />
            <span>
              {language === "हिंदी" ? "केस बंडल (.zip)" : "Case Bundle"}
            </span>
          </button>

          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold border border-slate-300 shadow-sm transition-colors"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5 text-slate-500" />}
            <span>{copied ? (language === "हिंदी" ? "कॉपी हो गया" : "Copied") : (language === "हिंदी" ? "टेक्स्ट कॉपी करें" : "Copy Text")}</span>
          </button>
        </div>
      </div>

      {/* 7-Day Statutory Cure Period Tracker */}
      {verdict === "FLAGGED" && (
        <ContractorCureTracker
          dossierId={dossier_id}
          contractorName={auditData?.project_metadata?.contractor_name || "M/s Apex Civil Constructions Ltd."}
        />
      )}

      {/* Document Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-3">
        {show_cause_notice && (
          <button
            onClick={() => setActiveTab("showcause")}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded text-xs font-bold transition-all ${
              activeTab === "showcause"
                ? "bg-rose-100 text-rose-800 border border-rose-300"
                : "text-slate-600 hover:text-slate-900 bg-slate-100"
            }`}
          >
            <FileText className="h-3.5 w-3.5" />
            <span>
              {language === "हिंदी"
                ? "कारण बताओ नोटिस (GFR 175)"
                : "Draft Show-Cause Notice (GFR 175)"}
            </span>
          </button>
        )}

        {hold_alert && (
          <button
            onClick={() => setActiveTab("hold")}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded text-xs font-bold transition-all ${
              activeTab === "hold"
                ? "bg-amber-100 text-amber-800 border border-amber-300"
                : "text-slate-600 hover:text-slate-900 bg-slate-100"
            }`}
          >
            <ShieldAlert className="h-3.5 w-3.5" />
            <span>
              {language === "हिंदी"
                ? "भुगतान रोक निर्देश (DDO)"
                : "Payment Hold Directive (DDO)"}
            </span>
          </button>
        )}

        {vigilance_memo && (
          <button
            onClick={() => setActiveTab("vigilance")}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded text-xs font-bold transition-all ${
              activeTab === "vigilance"
                ? "bg-blue-100 text-blue-800 border border-blue-300"
                : "text-slate-600 hover:text-slate-900 bg-slate-100"
            }`}
          >
            <Landmark className="h-3.5 w-3.5" />
            <span>
              {language === "हिंदी"
                ? "सतर्कता शाखा गोपनीय ज्ञापन"
                : "Confidential Vigilance Memo"}
            </span>
          </button>
        )}

        {annexure_b_labor_muster && (
          <button
            onClick={() => setActiveTab("labor")}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded text-xs font-bold transition-all ${
              activeTab === "labor"
                ? "bg-purple-100 text-purple-800 border border-purple-300"
                : "text-slate-600 hover:text-slate-900 bg-slate-100"
            }`}
          >
            <Users className="h-3.5 w-3.5" />
            <span>
              {language === "हिंदी"
                ? "अनुलग्नक ख: फर्जी श्रमिक विवरण"
                : "Annexure B: Disputed Labor Roll"}
            </span>
          </button>
        )}
      </div>

      {/* Document Content Display (Gazette Font) */}
      <div className="p-5 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-900 whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto gazette-font">
        {activeTab === "showcause" && show_cause_notice && (
          <div className="space-y-4">
            <div>{show_cause_notice.notice_text}</div>

            {/* Render Digital Signature Block in Notice if signed */}
            {signatureData && (
              <div className="mt-4 p-3 rounded bg-emerald-50 border border-emerald-300 text-emerald-950 font-sans text-xs flex items-center justify-between">
                <div>
                  <span className="font-bold block text-emerald-900 uppercase text-[10px]">Simulated Digital Certification (Prototype Stamp):</span>
                  <span className="font-bold text-slate-900">{signatureData.officerName}</span> ({signatureData.designation})
                  <span className="text-[10px] text-slate-500 block font-mono mt-0.5">Simulated Token: {signatureData.dscToken} &bull; {signatureData.signedAt}</span>
                </div>
                <ShieldCheck className="h-6 w-6 text-emerald-600 shrink-0" />
              </div>
            )}
          </div>
        )}

        {activeTab === "hold" && hold_alert && (
          <div className="space-y-3 font-sans">
            <div className="p-3 rounded bg-rose-100 border border-rose-200 text-rose-900 font-bold">
              {hold_alert.title}
            </div>
            <div><span className="text-slate-500 font-semibold">Recipient:</span> {hold_alert.recipient}</div>
            <div><span className="text-slate-500 font-semibold">Directive:</span> {hold_alert.directive}</div>
            <div><span className="text-slate-500 font-semibold">PBG Action:</span> {hold_alert.pbg_action}</div>
          </div>
        )}

        {activeTab === "vigilance" && vigilance_memo && (
          <div>{vigilance_memo.memo_text}</div>
        )}

        {activeTab === "labor" && annexure_b_labor_muster && (
          <div className="space-y-3 font-sans">
            <div className="p-3 rounded bg-purple-100 border border-purple-200 text-purple-900 font-bold flex justify-between">
              <span>{annexure_b_labor_muster.title}</span>
              <span>Total Suspected Leakage: {annexure_b_labor_muster.total_suspected_leakage}</span>
            </div>

            <div className="space-y-2">
              {annexure_b_labor_muster.flagged_workers?.map((w: any, idx: number) => (
                <div key={idx} className="p-3 rounded bg-white border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between text-xs gap-1.5 shadow-sm">
                  <div>
                    <span className="font-bold text-slate-900">{w.worker_id} - {w.worker_name}</span> ({w.trade})
                    <p className="text-rose-600 text-[11px] mt-0.5 font-medium">{w.discrepancy_reason}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-slate-500">{w.days_claimed} days @ ₹{w.daily_wage}/day</span>
                    <p className="text-orange-700 font-bold">Claimed: ₹{w.claimed_wage_total?.toLocaleString()}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

    </div>
  );
}
