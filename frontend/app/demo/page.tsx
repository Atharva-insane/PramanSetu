"use client";

import React, { useState } from "react";
import {
  PlayCircle,
  ShieldCheck,
  ShieldAlert,
  Binary,
  MapPin,
  Users,
  Layers,
  Sun,
  Search,
  Cpu,
  Sparkles,
  ArrowRight,
  Scale,
  Landmark,
  FileCheck2,
  FileSpreadsheet,
  AlertTriangle,
  RotateCcw,
  CheckCircle2,
  Lock
} from "lucide-react";
import { runMilestoneAudit } from "@/lib/api";
import ForensicMatrixGrid from "@/components/ForensicMatrixGrid";
import LegalDossierViewer from "@/components/LegalDossierViewer";
import { useLanguage } from "@/context/LanguageContext";

export default function JudgeBenchmarkDemoPage() {
  const { t, language } = useLanguage();
  const [activeCaseId, setActiveCaseId] = useState<string>("case-1");
  const [isRunning, setIsRunning] = useState(false);
  const [auditResult, setAuditResult] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const benchmarkCases = [
    {
      id: "case-1",
      badge: language === "हिंदी" ? "मानक 1: प्रामाणिक निर्माण कार्य" : language === "தமிழ்" ? "சான்று 1: உண்மையான பணி" : "Signature Demo 1: Authentic Infrastructure Works",
      title: language === "हिंदी" ? "स्वच्छ व प्रमाणित अवसंरचना मील का पत्थर (PASS)" : language === "தமிழ்" ? "முழுமையாக அங்கீகரிக்கப்பட்ட உள்கட்டமைப்பு" : "Compliant Gold Standard Milestone (PASS / CLEAR)",
      scheme: "PMGSY 2024",
      project: "Rural Bituminous Connectivity Road - Sector 4",
      contractor: "Varanasi Highway Developers Ltd.",
      tenderId: "TDR-2024-VAR-402",
      claim: "₹50,00,000",
      expectedScore: "0 – 10 (CLEAR)",
      expectedBadge: "bg-emerald-100 text-emerald-800 border-emerald-200",
      icon: ShieldCheck,
      desc: language === "हिंदी"
        ? "कार्यस्थल के वास्तविक जीपीएस निर्देशांक (25.3176° N, 82.9739° E), सत्यापित 25 मजदूरों का मस्टर रोल और प्रामाणिक डामर निर्माण कार्य का साक्ष्य।"
        : language === "தமிழ்"
        ? "உண்மையான ஜிபிஎஸ் ஒருங்கிணைப்புகள் (25.3176° N, 82.9739° E), 25 தொழிலாளர் பட்டியல் மற்றும் உண்மையான தார் சாலை சான்று."
        : "Genuine road construction evidence with matching EXIF GPS coordinates (25.3176° N, 82.9739° E), verified 25-worker muster roll, and pristine physical asphalt compaction.",
      highlights: [
        { label: "GPS Hardware EXIF", value: "Exact 25.3176° N, 82.9739° E (0m error)", status: "pass" },
        { label: "Past Asset pHash", value: "Unique visual signature (Zero prior reuse)", status: "pass" },
        { label: "Muster Roll Telemetry", value: "25 Active verified workers (0 Ghost IDs)", status: "pass" },
        { label: "Material & Chrono", value: "Finished compacted asphalt, consistent dry weather", status: "pass" }
      ],
      lat: 25.3176,
      lon: 82.9739,
      material: "Finished Bituminous Asphalt",
      timestamp: "2024-07-15 11:30",
      imageName: "demo1_clean_road.jpg",
      musterType: "clean",
      color: "#14532d"
    },
    {
      id: "case-2",
      badge: language === "हिंदी" ? "मानक 2: बहु-आयामी फोरेंसिक धोखाधड़ी" : language === "தமிழ்" ? "சான்று 2: பலதரப்பு மோசடி கண்டறிதல்" : "Signature Demo 2: Multi-Vector Forensic Flag",
      title: language === "हिंदी" ? "सिंडिकेट फ्रॉड, फोटो रीसाइक्लिंग व फर्जी लेबर (FLAGGED)" : language === "தமிழ்" ? "பழைய புகைப்படம் & போலி தொழிலாளர் மோசடி" : "Recycled Asset, Ghost Labor & Satellite Anomaly (FLAGGED)",
      scheme: "Jal Jeevan Mission 2024",
      project: "Drinking Water Pipeline Network Scheme",
      contractor: "M/s Apex Civil Constructions Ltd.",
      tenderId: "TDR-2024-PRY-881",
      claim: "₹45,00,000",
      expectedScore: "88 – 95 (FLAGGED)",
      expectedBadge: "bg-rose-100 text-rose-800 border-rose-200",
      icon: ShieldAlert,
      desc: language === "हिंदी"
        ? "ठेकेदार ने 2023 की पुरानी पाइपलाइन फोटो को 2024 के नए भुगतान के लिए पुनः प्रस्तुत किया (pHash मैच)। मस्टर रोल में फर्जी मजदूर (₹3.15L लीकेज) व सैटेलाइट ग्राउंड-ट्रुथ विसंगति पाई गई।"
        : language === "தமிழ்"
        ? "2023 ஆம் ஆண்டின் பழைய புகைப்படத்தை மீண்டும் சமர்ப்பித்தல் (pHash பொருத்தம்), போலி தொழிலாளர்கள் (₹3.15L கசிவு) மற்றும் செயற்கைக்கோள் முரண்பாடு கண்டறியப்பட்டது."
        : "Contractor re-submitted a 2023 completed pipeline voucher (pHash Hamming Distance 0 against ASSET-UP-2023-001), phantom ghost workers in muster roll (₹3,15,000 leakage), and satellite terrain anomaly.",
      highlights: [
        { label: "Perceptual Hashing (pHash)", value: "Matches ASSET-UP-2023-001 (Hamming Dist 0)", status: "fail" },
        { label: "Ghost Labor Muster Roll", value: "2 Phantom IDs + Duplicate Worker (₹3.15L leak)", status: "fail" },
        { label: "Satellite Ground Truth", value: "Zero physical earthwork in Prayagraj Zone", status: "fail" },
        { label: "Chrono Weather Cross-check", value: "Dry sunny photo vs 112mm recorded monsoon", status: "fail" }
      ],
      lat: 25.4358,
      lon: 81.8463,
      material: "Drinking Water Pipeline",
      timestamp: "2024-07-15 14:00",
      imageName: "demo2_fraud_pipeline.jpg",
      musterType: "ghost",
      color: "#1e3a8a"
    }
  ];

  const activeCase = benchmarkCases.find((c) => c.id === activeCaseId) || benchmarkCases[0];

  const handleRunCase = async (c: typeof benchmarkCases[0]) => {
    setIsRunning(true);
    setAuditResult(null);
    setErrorMessage(null);

    // Deterministic canvas simulation payload
    const canvas = document.createElement("canvas");
    canvas.width = 640;
    canvas.height = 480;
    const ctx = canvas.getContext("2d");
    if (ctx) {
      ctx.fillStyle = c.color;
      ctx.fillRect(0, 0, 640, 480);
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 18px monospace";
      ctx.fillText(`SIGNATURE BENCHMARK: ${c.id.toUpperCase()}`, 20, 50);
      ctx.fillText(`SCHEME: ${c.scheme}`, 20, 90);
      ctx.fillText(`TENDER ID: ${c.tenderId}`, 20, 130);
      ctx.fillText(`CONTRACTOR: ${c.contractor}`, 20, 170);
      ctx.fillText(`CLAIM: ${c.claim}`, 20, 210);
      ctx.fillText(`STATUTORY BASIS: GFR 2017 RULE 175`, 20, 250);
    }

    const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, "image/jpeg"));
    if (!blob) {
      setIsRunning(false);
      return;
    }

    const dummyFile = new File([blob], c.imageName, { type: "image/jpeg" });

    // Optional muster CSV sample attachment
    let musterBlob: File | undefined = undefined;
    if (c.musterType === "ghost") {
      const csvContent =
        "worker_id,name,trade,days_worked,daily_wage\n" +
        "W-2001,Ramesh Kumar,Mason,26,550\n" +
        "W-2002,Suresh Yadav,Helper,26,450\n" +
        "W-2003,Dinesh Verma,Helper,26,450\n" +
        "W-2004,GHOST-901,Phantom Worker,26,500\n" +
        "W-2005,GHOST-902,Phantom Worker,26,500\n" +
        "W-2001,Ramesh Kumar,Mason,26,550\n" +
        "W-2006,Mahesh Chand,Operator,45,700\n";
      musterBlob = new File([new Blob([csvContent], { type: "text/csv" })], "demo2_ghost_muster.csv");
    } else {
      const csvContent =
        "worker_id,name,trade,days_worked,daily_wage\n" +
        "W-1001,Ramesh Kumar,Mason,26,550\n" +
        "W-1002,Suresh Yadav,Helper,26,450\n" +
        "W-1003,Dinesh Verma,Helper,26,450\n" +
        "W-1004,Aakash Singh,Helper,26,450\n" +
        "W-1005,Vikram Patel,Supervisor,26,700\n";
      musterBlob = new File([new Blob([csvContent], { type: "text/csv" })], "demo1_clean_muster.csv");
    }

    try {
      const result = await runMilestoneAudit({
        image: dummyFile,
        scheme: c.scheme,
        project_name: c.project,
        contractor_name: c.contractor,
        tender_id: c.tenderId,
        claim_amount: c.claim,
        claimed_latitude: c.lat,
        claimed_longitude: c.lon,
        claimed_material: c.material,
        claimed_timestamp: c.timestamp,
        muster_roll_file: musterBlob,
        is_demo: true
      });

      setAuditResult(result);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to execute benchmark demonstration");
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-bold tracking-widest uppercase text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 flex items-center space-x-1">
              <Sparkles className="h-3 w-3" />
              <span>{language === "हिंदी" ? "फोरेंसिक प्रयोगशाला" : "Evaluation Benchmark"}</span>
            </span>
            <h1 className="text-2xl font-extrabold text-[#0f2942] tracking-tight">
              {language === "हिंदी" ? "हस्ताक्षर डेमो व फोरेंसिक बेंचमार्क केंद्र" : language === "தமிழ்" ? "முக்கிய செயல்விளக்க ஆய்வகம்" : "Signature Demo & Forensic Benchmark Lab"}
            </h1>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            {language === "हिंदी"
              ? "दो विस्तृत एवं गहन परिदृश्यों के माध्यम से 10-वेक्टर फोरेंसिक इंजन, विधिक अनुपालन एवं धोखाधड़ी रोकथाम का प्रत्यक्ष परीक्षण करें।"
              : "Experience the complete 10-vector forensic verification pipeline through two high-fidelity signature demonstrations."}
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 flex items-center space-x-1.5">
            <Lock className="h-3.5 w-3.5 text-slate-400" />
            <span>GFR 2017 Rule 175 Calibrated</span>
          </span>
        </div>
      </div>

      {/* Two Signature Demo Selector Tabs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {benchmarkCases.map((c) => {
          const isSelected = activeCaseId === c.id;
          const Icon = c.icon;
          const isPass = c.id === "case-1";

          return (
            <div
              key={c.id}
              onClick={() => {
                setActiveCaseId(c.id);
                setAuditResult(null);
                setErrorMessage(null);
              }}
              className={`cursor-pointer rounded-xl border p-5 transition-all relative overflow-hidden ${
                isSelected
                  ? isPass
                    ? "border-emerald-500 bg-emerald-50/40 shadow-md ring-2 ring-emerald-500/20"
                    : "border-rose-500 bg-rose-50/40 shadow-md ring-2 ring-rose-500/20"
                  : "border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <div className={`p-2 rounded-lg ${isPass ? "bg-emerald-100 text-emerald-800" : "bg-rose-100 text-rose-800"}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-500">
                      {c.badge}
                    </span>
                    <h3 className="text-sm font-bold text-slate-900 leading-snug">
                      {c.title}
                    </h3>
                  </div>
                </div>
                <span className={`text-[10px] font-extrabold uppercase px-2 py-0.5 rounded border ${c.expectedBadge}`}>
                  {c.expectedScore}
                </span>
              </div>

              <p className="text-xs text-slate-600 mt-3 line-clamp-2">
                {c.desc}
              </p>

              <div className="mt-4 pt-3 border-t border-slate-200/60 flex items-center justify-between text-xs text-slate-500">
                <div className="flex items-center space-x-1 font-mono">
                  <span className="font-semibold text-slate-700">{c.contractor.split(" ")[0]}</span>
                  <span>•</span>
                  <span>{c.claim}</span>
                </div>
                <span className="text-xs font-bold text-blue-600 flex items-center space-x-1">
                  <span>{isSelected ? (language === "हिंदी" ? "सक्रिय चुना गया" : "Selected") : (language === "हिंदी" ? "चुनें" : "Select")}</span>
                  <ArrowRight className="h-3 w-3" />
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Active Selected Demo In-Depth Control Panel */}
      <div className="civic-card p-6 border-slate-300 bg-white space-y-6">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase border ${activeCase.expectedBadge}`}>
                {activeCase.expectedScore}
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                {activeCase.title}
              </h2>
            </div>
            <p className="text-xs text-slate-600">
              {activeCase.desc}
            </p>
          </div>

          <button
            onClick={() => handleRunCase(activeCase)}
            disabled={isRunning}
            className={`px-5 py-2.5 rounded-lg text-sm font-bold text-white shadow-sm flex items-center space-x-2 transition-all shrink-0 ${
              isRunning
                ? "bg-slate-400 cursor-not-allowed"
                : activeCase.id === "case-1"
                ? "bg-emerald-600 hover:bg-emerald-700 active:scale-[0.98]"
                : "bg-rose-600 hover:bg-rose-700 active:scale-[0.98]"
            }`}
          >
            {isRunning ? (
              <>
                <Cpu className="h-4 w-4 animate-spin" />
                <span>{language === "हिंदी" ? "फोरेंसिक स्कैनिंग जारी..." : "Executing Live Audit..."}</span>
              </>
            ) : (
              <>
                <PlayCircle className="h-4 w-4" />
                <span>{language === "हिंदी" ? "लाइव फोरेंसिक परीक्षण चलाएं" : "Run Live Forensic Audit"}</span>
              </>
            )}
          </button>
        </div>

        {/* Project Parameters Matrix */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-slate-50 p-4 rounded-lg border border-slate-200">
          <div>
            <span className="text-[10px] uppercase font-bold text-slate-500">Government Scheme</span>
            <div className="text-xs font-bold text-slate-800 mt-0.5">{activeCase.scheme}</div>
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold text-slate-500">Project / Tender ID</span>
            <div className="text-xs font-bold text-slate-800 mt-0.5">{activeCase.tenderId}</div>
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold text-slate-500">Claimed Contractor</span>
            <div className="text-xs font-bold text-slate-800 mt-0.5">{activeCase.contractor}</div>
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold text-slate-500">Milestone Claim Value</span>
            <div className="text-xs font-bold text-slate-800 font-mono mt-0.5">{activeCase.claim}</div>
          </div>
        </div>

        {/* Forensic Highlights Under Scrutiny */}
        <div>
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">
            {language === "हिंदी" ? "परीक्षण के प्रमुख फोरेंसिक पैरामीटर" : "Forensic Scrutiny Vectors Under Test"}
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {activeCase.highlights.map((h, i) => (
              <div
                key={i}
                className={`p-3 rounded-lg border flex items-start space-x-3 text-xs ${
                  h.status === "pass"
                    ? "bg-emerald-50/50 border-emerald-200 text-emerald-950"
                    : "bg-rose-50/50 border-rose-200 text-rose-950"
                }`}
              >
                <div className="mt-0.5">
                  {h.status === "pass" ? (
                    <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                  ) : (
                    <AlertTriangle className="h-4 w-4 text-rose-600" />
                  )}
                </div>
                <div>
                  <span className="font-bold">{h.label}: </span>
                  <span className="text-slate-700">{h.value}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Error Message */}
      {errorMessage && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-800 rounded-lg text-xs flex items-center space-x-2">
          <AlertTriangle className="h-4 w-4 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Live Scanning Animation */}
      {isRunning && (
        <div className="civic-card p-8 text-center space-y-4 border-blue-300 bg-blue-50/40 animate-pulse">
          <div className="inline-flex p-3 rounded-full bg-blue-100 text-blue-700">
            <Cpu className="h-8 w-8 animate-spin" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-blue-900">
              {language === "हिंदी" ? "10-वेक्टर फोरेंसिक सत्यापन प्रक्रिया सक्रिय है..." : "10-Vector Multi-Layer Forensic Verification Active..."}
            </h3>
            <p className="text-xs text-blue-700 mt-1 max-w-md mx-auto">
              Scanning pHash DCT, Google Cloud Web Search, Haversine Hardware GPS, Satellite Ground-Truth, and Muster Roll CSV wage tables...
            </p>
          </div>
        </div>
      )}

      {/* Render Results when complete */}
      {auditResult && (
        <div className="space-y-8 animate-in fade-in duration-300">
          
          {/* Top Result Banner */}
          <div
            className={`p-6 rounded-xl border flex flex-col md:flex-row md:items-center justify-between gap-4 ${
              auditResult.status === "CLEAR"
                ? "bg-emerald-50 border-emerald-300 text-emerald-950"
                : "bg-rose-50 border-rose-300 text-rose-950"
            }`}
          >
            <div className="flex items-center space-x-4">
              <div
                className={`p-3 rounded-full ${
                  auditResult.status === "CLEAR" ? "bg-emerald-200 text-emerald-800" : "bg-rose-200 text-rose-800"
                }`}
              >
                {auditResult.status === "CLEAR" ? (
                  <ShieldCheck className="h-8 w-8" />
                ) : (
                  <ShieldAlert className="h-8 w-8" />
                )}
              </div>
              <div>
                <span className="text-[10px] font-extrabold uppercase tracking-wider opacity-75">
                  Official Statutory Verdict
                </span>
                <h2 className="text-xl font-black tracking-tight">
                  {auditResult.status === "CLEAR" ? "AUDIT CLEARANCE CERTIFICATE ISSUED" : "PRE-APPROVAL DISBURSEMENT PAYMENT FREEZE"}
                </h2>
                <p className="text-xs mt-1 max-w-2xl font-medium">
                  {auditResult.decision_reason}
                </p>
              </div>
            </div>

            <div className="text-right shrink-0">
              <span className="text-[10px] font-extrabold uppercase tracking-wider block opacity-75">
                Composite Risk Score
              </span>
              <span
                className={`text-3xl font-black font-mono ${
                  auditResult.status === "CLEAR" ? "text-emerald-700" : "text-rose-700"
                }`}
              >
                {auditResult.risk_score} / 100
              </span>
            </div>
          </div>

          {/* 10-Vector Forensic Matrix Grid */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center space-x-2">
                <Cpu className="h-4 w-4 text-blue-600" />
                <span>Forensic Matrix Verification Breakdown (10 Vectors)</span>
              </h3>
            </div>
            <ForensicMatrixGrid auditData={auditResult} />
          </div>

          {/* Legal Dossier & Statutory Remediation Notice */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center space-x-2">
                <Scale className="h-4 w-4 text-blue-600" />
                <span>Statutory Remediation & GFR 175 Legal Notice Dossier</span>
              </h3>
            </div>
            <LegalDossierViewer
              dossier={auditResult.dossier}
              riskScore={auditResult.risk_score}
              verdict={auditResult.status}
              auditData={auditResult}
            />
          </div>

        </div>
      )}

    </div>
  );
}
