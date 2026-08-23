"use client";

import React, { useState } from "react";
import {
  Users,
  Upload,
  FileText,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Copy,
  Check,
  Printer,
  Scale,
  Sparkles,
  HelpCircle,
  Landmark,
  Zap,
  ArrowRight
} from "lucide-react";
import { runCitizenAudit } from "@/lib/api";
import { useLanguage } from "@/context/LanguageContext";

export default function CitizenSocialAuditPage() {
  const { t } = useLanguage();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [projectId, setProjectId] = useState("PROJ-2024-RURAL-089");
  const [projectName, setProjectName] = useState("Gram Sadak Asphalt Paving - Phase 2");
  const [claimedCompletion, setClaimedCompletion] = useState<number>(100);
  const [citizenNotes, setCitizenNotes] = useState("The contractor claims the road is fully asphalted and finished, but ground reality shows unpaved mud gravel with zero drainage.");
  const [latitude, setLatitude] = useState<number>(25.4358);
  const [longitude, setLongitude] = useState<number>(81.8463);

  const [isLoading, setIsLoading] = useState(false);
  const [citizenResult, setCitizenResult] = useState<any>(null);
  const [copiedRti, setCopiedRti] = useState(false);
  const [copiedGrievance, setCopiedGrievance] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setCitizenResult(null);
      setErrorMessage(null);
    }
  };

  const handleLoadSample = () => {
    const canvas = document.createElement("canvas");
    canvas.width = 640;
    canvas.height = 480;
    const ctx = canvas.getContext("2d");
    if (ctx) {
      ctx.fillStyle = "#854d0e";
      ctx.fillRect(0, 0, 640, 480);
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 18px monospace";
      ctx.fillText("CITIZEN GROUND EVIDENCE: UNPAVED MUD TRACK", 20, 50);
      ctx.fillText("PROJECT: GRAM SADAK PAVING", 20, 90);
    }
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], "citizen_unpaved_road.jpg", { type: "image/jpeg" });
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
        setCitizenResult(null);
        setErrorMessage(null);
      }
    }, "image/jpeg");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setErrorMessage("Please attach physical on-site evidence.");
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const result = await runCitizenAudit({
        image: selectedFile,
        project_id: projectId,
        project_name: projectName,
        claimed_completion_percentage: Number(claimedCompletion),
        citizen_notes: citizenNotes,
        claimed_latitude: Number(latitude),
        claimed_longitude: Number(longitude),
      });
      setCitizenResult(result);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to process citizen social audit report.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-bold tracking-widest uppercase text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              {t.citizen}
            </span>
            <h1 className="text-2xl font-extrabold text-[#0f2942] tracking-tight">
              {t.citizenTitle}
            </h1>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            {t.citizenSubtitle}
          </p>
        </div>

        <button
          type="button"
          onClick={handleLoadSample}
          className="px-3.5 py-1.5 rounded bg-white hover:bg-slate-50 text-xs font-bold text-emerald-700 border border-slate-300 shadow-xs transition-colors flex items-center space-x-1.5"
        >
          <Zap className="h-3.5 w-3.5 text-emerald-600" />
          <span>{t.btnLoadSampleProof}</span>
        </button>
      </div>

      {/* Friendly Citizen Guidance Banner */}
      <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-950 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-emerald-100 text-emerald-700">
            <HelpCircle className="h-5 w-5" />
          </div>
          <div>
            <h4 className="font-bold text-sm">How Citizen Social Auditing Works:</h4>
            <p className="text-slate-600 mt-0.5">
              1. Take a photo of an incomplete road/pipe &bull; 2. Our AI translates discrepancies into plain language &bull; 3. Auto-generate a legal RTI Form A petition to demand official records.
            </p>
          </div>
        </div>
      </div>

      {/* Intake Grid */}
      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Upload */}
        <div className="lg:col-span-5 space-y-4">
          <div className="civic-card p-6 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-700 flex items-center space-x-1.5">
              <Upload className="h-4 w-4" />
              <span>Step 1: On-Site Ground Photograph</span>
            </h3>

            <label className="relative border-2 border-dashed border-slate-300 hover:border-emerald-500 rounded-lg p-5 flex flex-col items-center justify-center cursor-pointer transition-colors bg-slate-50 group overflow-hidden min-h-[220px]">
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
                    alt="Citizen Upload Preview"
                    className="max-h-full max-w-full object-contain"
                  />
                  <div className="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/80 text-[10px] text-white font-mono">
                    {selectedFile?.name}
                  </div>
                </div>
              ) : (
                <div className="text-center space-y-2">
                  <div className="p-3 rounded-full bg-emerald-100 inline-block text-emerald-700">
                    <Upload className="h-6 w-6" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-800">Attach Physical On-Site Photo</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">JPEG, PNG captured at public worksite</p>
                  </div>
                </div>
              )}
            </label>
          </div>
        </div>

        {/* Right: Details */}
        <div className="lg:col-span-7 space-y-4">
          <div className="civic-card p-6 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-700 flex items-center space-x-1.5">
              <FileText className="h-4 w-4" />
              <span>Step 2: Project Particulars & Citizen Observation</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Project ID / Sanction Ref</label>
                <input
                  type="text"
                  value={projectId}
                  onChange={(e) => setProjectId(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 font-mono focus:border-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Claimed Completion %</label>
                <div className="flex items-center space-x-2">
                  <input
                    type="number"
                    min={0}
                    max={100}
                    value={claimedCompletion}
                    onChange={(e) => setClaimedCompletion(parseFloat(e.target.value))}
                    className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-orange-700 font-bold font-mono focus:border-emerald-500 focus:outline-none"
                  />
                  <span className="text-xs text-slate-500 font-bold">%</span>
                </div>
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-700 mb-1">Public Project Name</label>
                <input
                  type="text"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-emerald-500 focus:outline-none"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-700 mb-1">Citizen Ground Observation / Site Notes</label>
                <textarea
                  rows={2}
                  value={citizenNotes}
                  onChange={(e) => setCitizenNotes(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-emerald-500 focus:outline-none font-medium"
                />
              </div>
            </div>

            {errorMessage && (
              <p className="text-xs text-rose-600 font-medium">{errorMessage}</p>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 rounded-md font-bold text-xs uppercase tracking-wider bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-all flex items-center justify-center space-x-2"
            >
              {isLoading ? (
                <span>Translating Ground Reality to Legal RTI Petition...</span>
              ) : (
                <span>Step 3: Generate Social Audit & Form A RTI Petition</span>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Citizen Results Screen */}
      {citizenResult && (
        <div className="space-y-6 pt-2 animate-in fade-in duration-300">
          
          {/* Plain Language Summary Card */}
          <div className="civic-card p-6 border-emerald-300 bg-emerald-50/70 space-y-3 shadow-xs">
            <div className="flex items-center space-x-2 text-emerald-800 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="h-4 w-4 text-emerald-600" />
              <span>AI Plain-Language Translation for Citizens & Gram Panchayats</span>
            </div>

            <p className="text-sm font-medium text-slate-900 leading-relaxed">
              {citizenResult.plain_language_summary}
            </p>

            <div className="flex flex-wrap items-center gap-4 pt-2 border-t border-emerald-200 text-xs text-slate-600 font-mono">
              <span>Audit ID: {citizenResult.audit_id}</span>
              <span>&bull;</span>
              <span>Calculated Risk: {citizenResult.risk_score}/100</span>
              <span>&bull;</span>
              <span>Verdict: {citizenResult.verdict}</span>
            </div>
          </div>

          {/* Statutory 30-Day Countdown Clock Tracker */}
          <div className="civic-card p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center space-x-4">
              <div className="p-3 rounded-lg bg-orange-100 text-orange-700">
                <Clock className="h-6 w-6" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-[#0f2942] uppercase tracking-wide">
                  Statutory RTI 30-Day Response Deadline
                </h4>
                <p className="text-xs text-slate-500 mt-0.5">
                  Under Section 7(1) of the RTI Act 2005, the Public Information Officer (PIO) is statutorily mandated to provide certified records within 30 days.
                </p>
              </div>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-center font-mono shrink-0">
              <span className="text-[10px] text-slate-500 uppercase font-sans font-bold block">First Appeal Deadline</span>
              <span className="text-sm font-bold text-orange-600">{citizenResult.first_appeal_date}</span>
            </div>
          </div>

          {/* Form A RTI Application */}
          <div className="civic-card p-6 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-200">
              <div>
                <h3 className="text-base font-bold text-[#0f2942] flex items-center space-x-2">
                  <Scale className="h-4 w-4 text-emerald-600" />
                  <span>{citizenResult.form_a_rti.title}</span>
                </h3>
                <span className="text-xs text-slate-500 font-mono">{citizenResult.form_a_rti.section}</span>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => window.print()}
                  className="flex items-center space-x-1 px-3 py-1.5 rounded bg-white hover:bg-slate-50 text-xs font-semibold text-slate-800 border border-slate-300 shadow-xs"
                >
                  <Printer className="h-3.5 w-3.5" />
                  <span>Print Application</span>
                </button>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(citizenResult.form_a_rti.application_body);
                    setCopiedRti(true);
                    setTimeout(() => setCopiedRti(false), 2000);
                  }}
                  className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-xs transition-colors"
                >
                  {copiedRti ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                  <span>{copiedRti ? "Copied" : "Copy Form A RTI"}</span>
                </button>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 font-mono text-xs text-slate-800 whitespace-pre-wrap leading-relaxed max-h-72 overflow-y-auto">
              {citizenResult.form_a_rti.application_body}
            </div>
          </div>

          {/* CPGRAMS Public Grievance Text */}
          <div className="civic-card p-6 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-200">
              <div>
                <h3 className="text-base font-bold text-[#0f2942]">
                  CPGRAMS Public Grievance Portal Text
                </h3>
                <p className="text-xs text-slate-500">Formatted text ready to copy-paste into Central/State grievance portals.</p>
              </div>

              <button
                onClick={() => {
                  navigator.clipboard.writeText(citizenResult.grievance_text);
                  setCopiedGrievance(true);
                  setTimeout(() => setCopiedGrievance(false), 2000);
                }}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-white hover:bg-slate-50 text-xs font-semibold text-slate-800 border border-slate-300 shadow-xs transition-colors"
              >
                {copiedGrievance ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5 text-slate-600" />}
                <span>{copiedGrievance ? "Copied" : "Copy Grievance"}</span>
              </button>
            </div>

            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 font-mono text-xs text-slate-800 whitespace-pre-wrap leading-relaxed max-h-52 overflow-y-auto">
              {citizenResult.grievance_text}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
