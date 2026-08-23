"use client";

import React, { useState } from "react";
import {
  Shield,
  Upload,
  FileSpreadsheet,
  Cpu,
  Sparkles,
  AlertCircle,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Clock,
  ArrowRight,
  Layers,
  MapPin,
  FileText,
  Landmark,
  Scale,
  Zap,
  ChevronDown,
  ChevronUp,
  Eye,
  Sliders
} from "lucide-react";
import { runMilestoneAudit } from "@/lib/api";
import ForensicMatrixGrid from "@/components/ForensicMatrixGrid";
import LegalDossierViewer from "@/components/LegalDossierViewer";
import { useLanguage } from "@/context/LanguageContext";

export default function GatekeeperIntakePage() {
  const { t } = useLanguage();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [musterFile, setMusterFile] = useState<File | null>(null);

  // Form Inputs
  const [scheme, setScheme] = useState("Pradhan Mantri Gram Sadak Yojana (PMGSY)");
  const [projectName, setProjectName] = useState("Rural Bituminous Connectivity Road - Package 402");
  const [contractorName, setContractorName] = useState("M/s Apex Civil Constructions Ltd.");
  const [tenderId, setTenderId] = useState("TDR-2024-UP-8819");
  const [claimAmount, setClaimAmount] = useState("₹45,00,000");
  const [claimedLat, setClaimedLat] = useState<number>(25.3176);
  const [claimedLon, setClaimedLon] = useState<number>(82.9739);
  const [claimedMaterial, setClaimedMaterial] = useState("Finished Bituminous Asphalt");
  const [claimedTimestamp, setClaimedTimestamp] = useState("2024-07-15 14:00");

  // Audit State
  const [isScanning, setIsScanning] = useState(false);
  const [scanStep, setScanStep] = useState(0);
  const [auditResult, setAuditResult] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<"simple" | "detailed">("simple");

  const scanSteps = [
    "Stage 1/7: Checking for duplicate past photos (pHash DCT)...",
    "Stage 2/7: Cross-checking public stock photo databases...",
    "Stage 3/7: Verifying GPS location with Haversine formula...",
    "Stage 4/7: Checking satellite ground-truth anomaly zones...",
    "Stage 5/7: Calculating labor muster roll wage leakage...",
    "Stage 6/7: Analyzing physical material with computer vision...",
    "Stage 7/7: Generating official verdict & GFR 175 legal notices...",
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setAuditResult(null);
      setErrorMessage(null);
    }
  };

  const handleMusterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setMusterFile(e.target.files[0]);
    }
  };

  // Quick 1-Click Signature Presets
  const handleLoadSample = (scenario: "clean" | "fraud" | "reset") => {
    if (scenario === "reset") {
      setSelectedFile(null);
      setPreviewUrl(null);
      setMusterFile(null);
      setProjectName("");
      setScheme("Pradhan Mantri Gram Sadak Yojana (PMGSY)");
      setContractorName("");
      setTenderId("");
      setClaimAmount("");
      setClaimedLat(25.3176);
      setClaimedLon(82.9739);
      setClaimedMaterial("Finished Bituminous Asphalt");
      setClaimedTimestamp("2024-07-15 14:00");
      setAuditResult(null);
      setErrorMessage(null);
      return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = 640;
    canvas.height = 480;
    const ctx = canvas.getContext("2d");

    let fileName = "demo1_clean_road.jpg";
    let pName = "Rural Bituminous Connectivity Road - Sector 4";
    let sch = "PMGSY 2024";
    let cont = "Varanasi Highway Developers Ltd.";
    let tId = "TDR-2024-VAR-402";
    let claim = "₹50,00,000";
    let lat = 25.3176;
    let lon = 82.9739;
    let mat = "Finished Bituminous Asphalt";
    let ts = "2024-07-15 11:30";
    let color = "#14532d";

    if (scenario === "fraud") {
      fileName = "demo2_fraud_pipeline.jpg";
      pName = "Drinking Water Pipeline Network Scheme";
      sch = "Jal Jeevan Mission 2024";
      cont = "M/s Apex Civil Constructions Ltd.";
      tId = "TDR-2024-PRY-881";
      claim = "₹45,00,000";
      lat = 25.4358;
      lon = 81.8463;
      mat = "Drinking Water Pipeline";
      ts = "2024-07-15 14:00";
      color = "#1e3a8a";
    }

    if (ctx) {
      ctx.fillStyle = color;
      ctx.fillRect(0, 0, 640, 480);
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 18px monospace";
      ctx.fillText(`PRESET: ${scenario.toUpperCase()}`, 20, 50);
      ctx.fillText(`Project: ${pName}`, 20, 90);
      ctx.fillText(`Contractor: ${cont}`, 20, 130);
      ctx.fillText(`Tender Claim: ${claim}`, 20, 170);
    }

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], fileName, { type: "image/jpeg" });
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
        setProjectName(pName);
        setScheme(sch);
        setContractorName(cont);
        setTenderId(tId);
        setClaimAmount(claim);
        setClaimedLat(lat);
        setClaimedLon(lon);
        setClaimedMaterial(mat);
        setClaimedTimestamp(ts);
        setAuditResult(null);
        setErrorMessage(null);

        if (scenario === "fraud") {
          const sampleCsv = `worker_id,name,trade,days_worked,daily_wage\nW-2001,Ramesh Kumar,Mason,26,550\nW-2002,Suresh Yadav,Helper,26,450\nW-2003,Dinesh Verma,Helper,26,450\nW-2004,GHOST-901,Phantom Worker,26,500\nW-2005,GHOST-902,Phantom Worker,26,500\nW-2001,Ramesh Kumar,Mason,26,550\nW-2006,Mahesh Chand,Operator,45,700\n`;
          const mFile = new File([new Blob([sampleCsv], { type: "text/csv" })], "demo2_ghost_muster.csv", { type: "text/csv" });
          setMusterFile(mFile);
        } else {
          const sampleCsv = `worker_id,name,trade,days_worked,daily_wage\nW-1001,Ramesh Kumar,Mason,26,550\nW-1002,Suresh Yadav,Helper,26,450\nW-1003,Dinesh Verma,Helper,26,450\nW-1004,Aakash Singh,Helper,26,450\nW-1005,Vikram Patel,Supervisor,26,700\n`;
          const mFile = new File([new Blob([sampleCsv], { type: "text/csv" })], "demo1_clean_muster.csv", { type: "text/csv" });
          setMusterFile(mFile);
        }
      }
    }, "image/jpeg");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setErrorMessage("Please attach physical photographic evidence to begin.");
      return;
    }

    setIsScanning(true);
    setErrorMessage(null);
    setAuditResult(null);

    const stepInterval = setInterval(() => {
      setScanStep((prev) => (prev < scanSteps.length - 1 ? prev + 1 : prev));
    }, 280);

    try {
      const result = await runMilestoneAudit({
        image: selectedFile,
        claimed_latitude: Number(claimedLat),
        claimed_longitude: Number(claimedLon),
        project_name: projectName,
        scheme,
        contractor_name: contractorName,
        tender_id: tenderId,
        claim_amount: claimAmount,
        claimed_material: claimedMaterial,
        claimed_timestamp: claimedTimestamp,
        muster_roll_file: musterFile,
      });

      clearInterval(stepInterval);
      setAuditResult(result);
    } catch (err: any) {
      clearInterval(stepInterval);
      setErrorMessage(err.message || "Failed to process pre-disbursement audit.");
    } finally {
      setIsScanning(false);
      setScanStep(0);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header Banner with Friendly Subtitle */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center">
            <span className="text-[10px] font-bold tracking-widest uppercase text-orange-600 bg-orange-50 px-2 py-0.5 rounded border border-orange-200">
              {t.gatekeeper}
            </span>
            <h1 className="text-2xl font-extrabold text-[#0f2942] tracking-tight">
              {t.intakeTitle}
            </h1>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            {t.intakeSubtitle}
          </p>
        </div>
      </div>

      {/* Friendly 1-Click Sample Preset Bar */}
      <div className="p-4 rounded-xl bg-orange-50/70 border border-orange-200 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-orange-950 flex items-center space-x-1.5">
            <Zap className="h-4 w-4 text-orange-600" />
            <span>{t.quickPresetsTitle}:</span>
          </span>
          <span className="text-[11px] text-slate-500 hidden sm:inline font-medium">
            1-Click Benchmark Demonstrations or Upload Custom Evidence Below
          </span>
        </div>

        <div className="flex flex-wrap gap-2 pt-1">
          <button
            type="button"
            onClick={() => handleLoadSample("clean")}
            className="px-3.5 py-1.5 rounded-md bg-white hover:bg-emerald-50 text-emerald-800 border border-emerald-300 text-xs font-semibold shadow-xs transition-colors"
          >
            🟢 {t.preset1Label}
          </button>
          <button
            type="button"
            onClick={() => handleLoadSample("fraud")}
            className="px-3.5 py-1.5 rounded-md bg-white hover:bg-rose-50 text-rose-800 border border-rose-300 text-xs font-semibold shadow-xs transition-colors"
          >
            🔴 {t.preset2Label}
          </button>
          <button
            type="button"
            onClick={() => handleLoadSample("reset")}
            className="px-3.5 py-1.5 rounded-md bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 text-xs font-semibold shadow-xs transition-colors flex items-center space-x-1"
          >
            <RotateCcw className="h-3 w-3 text-slate-500" />
            <span>{t.preset4Label}</span>
          </button>
        </div>
      </div>

      {/* Main Intake Form Grid */}
      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Upload Evidence */}
        <div className="lg:col-span-5 space-y-4">
          <div className="civic-card p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-orange-700 flex items-center space-x-1.5">
                <Upload className="h-4 w-4" />
                <span>Step 1: Physical Photographic Evidence</span>
              </h3>
            </div>

            <label className="relative border-2 border-dashed border-slate-300 hover:border-orange-500 rounded-lg p-5 flex flex-col items-center justify-center cursor-pointer transition-colors bg-slate-50 group overflow-hidden min-h-[220px]">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="hidden"
              />

              {previewUrl ? (
                <div className="relative w-full h-48 rounded overflow-hidden flex items-center justify-center bg-slate-900">
                  <img
                    src={previewUrl}
                    alt="Milestone Evidence Preview"
                    className="max-h-full max-w-full object-contain"
                  />
                  <div className="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/80 text-[10px] text-white font-mono">
                    {selectedFile?.name}
                  </div>
                </div>
              ) : (
                <div className="text-center space-y-2">
                  <div className="p-3 rounded-full bg-orange-100 inline-block text-orange-700">
                    <Upload className="h-6 w-6" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-800">
                      Drop On-Site Photo Here or Browse
                    </p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      JPEG, PNG captured at worksite
                    </p>
                  </div>
                </div>
              )}
            </label>

            {/* Optional Muster Roll */}
            <div className="pt-2 border-t border-slate-100">
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Supplementary Labor Muster Roll (Optional)</span>
                {musterFile && <span className="text-emerald-700 font-mono text-[10px]">Attached</span>}
              </div>
              <input
                type="file"
                accept=".csv,.json"
                onChange={handleMusterChange}
                className="w-full text-xs text-slate-500 file:mr-2 file:py-1 file:px-2.5 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-orange-700 hover:file:bg-orange-100"
              />
            </div>
          </div>
        </div>

        {/* Right Column: Tender Details */}
        <div className="lg:col-span-7 space-y-4">
          <div className="civic-card p-6 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-orange-700 flex items-center space-x-1.5">
              <FileText className="h-4 w-4" />
              <span>Step 2: Tender Details & Claim Parameters</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Sanction Scheme</label>
                <input
                  type="text"
                  value={scheme}
                  onChange={(e) => setScheme(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Tender / Sanction ID</label>
                <input
                  type="text"
                  value={tenderId}
                  onChange={(e) => setTenderId(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 font-mono focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-700 mb-1">Project Name</label>
                <input
                  type="text"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Contractor Name</label>
                <input
                  type="text"
                  value={contractorName}
                  onChange={(e) => setContractorName(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Claim Amount in ₹</label>
                <input
                  type="text"
                  value={claimAmount}
                  onChange={(e) => setClaimAmount(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-orange-700 font-bold font-mono focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Worksite GPS Coordinates</label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    step="any"
                    value={claimedLat}
                    onChange={(e) => setClaimedLat(parseFloat(e.target.value))}
                    className="w-full bg-white border border-slate-300 rounded px-2.5 py-2 text-xs font-mono"
                    placeholder="Lat"
                  />
                  <input
                    type="number"
                    step="any"
                    value={claimedLon}
                    onChange={(e) => setClaimedLon(parseFloat(e.target.value))}
                    className="w-full bg-white border border-slate-300 rounded px-2.5 py-2 text-xs font-mono"
                    placeholder="Lon"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Sanctioned Milestone Material</label>
                <input
                  type="text"
                  value={claimedMaterial}
                  onChange={(e) => setClaimedMaterial(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none"
                />
              </div>
            </div>

            {errorMessage && (
              <p className="text-xs text-rose-600 font-semibold">{errorMessage}</p>
            )}

            <button
              type="submit"
              disabled={isScanning}
              className="w-full py-3 rounded-md font-bold text-xs uppercase tracking-wider bg-orange-600 hover:bg-orange-700 text-white shadow-xs transition-all flex items-center justify-center space-x-2"
            >
              {isScanning ? (
                <span>Screening Evidence Across 10 Forensic Engines...</span>
              ) : (
                <span>Step 3: Run Automated Pre-Approval Audit</span>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Animated Live Examination Progress Bar */}
      {isScanning && (
        <div className="civic-card p-6 border-orange-300 bg-orange-50/50 space-y-3 animate-in fade-in duration-200">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-orange-950 flex items-center space-x-2">
              <span className="h-2.5 w-2.5 rounded-full bg-orange-600 animate-ping inline-block" />
              <span>{scanSteps[scanStep]}</span>
            </span>
            <span className="font-mono text-orange-700 font-bold">
              {Math.round(((scanStep + 1) / scanSteps.length) * 100)}%
            </span>
          </div>

          <div className="w-full bg-orange-200 rounded-full h-2 overflow-hidden">
            <div
              className="bg-orange-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((scanStep + 1) / scanSteps.length) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Scrutiny Results Cockpit */}
      {auditResult && (
        <div className="space-y-8 pt-4 border-t border-slate-200 animate-in fade-in duration-300">
          
          {/* Big Friendly Verdict Banner */}
          <div
            className={`p-6 rounded-xl border shadow-sm ${
              auditResult.status === "FLAGGED"
                ? "bg-rose-50 border-rose-200 text-rose-950"
                : auditResult.status === "REVIEW"
                ? "bg-amber-50 border-amber-200 text-amber-950"
                : "bg-emerald-50 border-emerald-200 text-emerald-950"
            }`}
          >
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
              
              <div className="space-y-2">
                <div className="flex items-center space-x-2.5">
                  <span
                    className={`text-xs uppercase tracking-wider font-extrabold px-3 py-1 rounded border ${
                      auditResult.status === "FLAGGED"
                        ? "bg-rose-600 text-white border-rose-600"
                        : auditResult.status === "REVIEW"
                        ? "bg-amber-500 text-white border-amber-500"
                        : "bg-emerald-600 text-white border-emerald-600"
                    }`}
                  >
                    VERDICT: {auditResult.status === "CLEAR" ? "SAFE TO DISBURSE (CLEAR)" : auditResult.status === "FLAGGED" ? "HOLD DISBURSEMENT (FLAGGED)" : "MANUAL REVIEW REQUIRED"}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">
                    Tender: {auditResult.project_metadata?.tender_id}
                  </span>
                </div>

                <h2 className="text-xl font-bold text-slate-900">
                  {auditResult.decision_reason}
                </h2>

                <p className="text-xs text-slate-700 font-medium">
                  <span className="text-slate-900 font-bold">Action Directive:</span> {auditResult.recommended_action}
                </p>
              </div>

              {/* Composite Score Pill */}
              <div className="flex items-center space-x-6 p-4 rounded-lg bg-white border border-slate-200 shrink-0 font-mono shadow-xs">
                <div className="text-center">
                  <span className="text-[10px] text-slate-500 uppercase font-bold font-sans block">
                    Composite Risk Score
                  </span>
                  <div className="text-3xl font-black mt-1">
                    <span
                      className={
                        auditResult.risk_score >= 60
                          ? "text-rose-600"
                          : auditResult.risk_score >= 25
                          ? "text-amber-600"
                          : "text-emerald-600"
                      }
                    >
                      {auditResult.risk_score}
                    </span>
                    <span className="text-slate-400 text-sm">/100</span>
                  </div>
                </div>

                <div className="h-8 w-[1px] bg-slate-200" />

                <div>
                  <span className="text-[10px] text-slate-500 uppercase font-bold font-sans block">
                    Contractor Trust
                  </span>
                  <div className="flex items-center space-x-1 mt-1 text-sm font-bold text-amber-600">
                    <span>{auditResult.contractor_profile?.star_rating || 4.0} ★</span>
                    <span className="text-[10px] text-slate-500 font-normal">
                      ({auditResult.contractor_profile?.integrity_score || 80}/100)
                    </span>
                  </div>
                </div>
              </div>

            </div>
          </div>

          {/* Friendly View Mode Switcher */}
          <div className="flex items-center justify-between p-3 bg-slate-100 rounded-lg border border-slate-200 text-xs">
            <div className="flex items-center space-x-2 text-slate-700 font-semibold">
              <Sliders className="h-4 w-4 text-slate-500" />
              <span>Inspection View Mode:</span>
            </div>

            <div className="flex gap-1.5">
              <button
                type="button"
                onClick={() => setViewMode("simple")}
                className={`px-3 py-1 rounded text-xs font-bold transition-all ${
                  viewMode === "simple"
                    ? "bg-white text-orange-700 shadow-xs border border-slate-300"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Executive Notice View
              </button>
              <button
                type="button"
                onClick={() => setViewMode("detailed")}
                className={`px-3 py-1 rounded text-xs font-bold transition-all ${
                  viewMode === "detailed"
                    ? "bg-white text-orange-700 shadow-xs border border-slate-300"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                10-Vector Mathematical Telemetry
              </button>
            </div>
          </div>

          {/* Detailed 10-Vector Mathematical Matrix Grid */}
          {viewMode === "detailed" && (
            <ForensicMatrixGrid auditData={auditResult} />
          )}

          {/* Legal Dossier & Court-Admissible Gazette Viewer */}
          <LegalDossierViewer
            dossier={auditResult.dossier}
            riskScore={auditResult.risk_score}
            verdict={auditResult.status}
            auditData={auditResult}
          />

        </div>
      )}

    </div>
  );
}
