"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { ShieldCheck, Search, CheckCircle2, XCircle, AlertTriangle, Lock, Scale, Landmark, FileText, QrCode } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

function VerifyContent() {
  const searchParams = useSearchParams();
  const queryDossier = searchParams.get("dossier_id") || searchParams.get("dossier") || "";

  const [searchId, setSearchId] = useState(queryDossier);
  const [isVerifying, setIsVerifying] = useState(false);
  const [verifiedRecord, setVerifiedRecord] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [notFound, setNotFound] = useState<boolean>(false);
  const [tampered, setTampered] = useState<boolean>(false);

  const executeVerification = async (dossierId: string) => {
    const cleanId = dossierId.trim();
    if (!cleanId) {
      setErrorMessage("Please enter a valid Dossier Reference ID.");
      setVerifiedRecord(null);
      setNotFound(false);
      setTampered(false);
      return;
    }

    setIsVerifying(true);
    setErrorMessage(null);
    setNotFound(false);
    setTampered(false);
    setVerifiedRecord(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/verify/${encodeURIComponent(cleanId)}`);
      
      if (response.status === 404) {
        setNotFound(true);
        setErrorMessage(`Dossier '${cleanId}' not found in the central vigilance ledger. Cryptographic authenticity cannot be verified.`);
        setIsVerifying(false);
        return;
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        setErrorMessage(errorData.detail || `Verification failed with status code ${response.status}`);
        setIsVerifying(false);
        return;
      }

      const data = await response.json();
      setVerifiedRecord(data);

      if (data.status === "INTEGRITY_CHECK_FAILED" || !data.verified) {
        setTampered(true);
      }
    } catch (err: any) {
      setErrorMessage("Unable to connect to verification server. Please verify the backend service is running on port 8002.");
    } finally {
      setIsVerifying(false);
    }
  };

  useEffect(() => {
    if (queryDossier) {
      setSearchId(queryDossier);
      executeVerification(queryDossier);
    }
  }, [queryDossier]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    executeVerification(searchId);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8 py-4">
      
      {/* Header */}
      <div className="text-center space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded bg-orange-100 text-orange-800 text-xs font-bold uppercase tracking-wider">
          <ShieldCheck className="h-4 w-4 text-orange-600" />
          <span>Public Evidentiary Verification Portal</span>
        </div>
        <h1 className="text-2xl md:text-3xl font-extrabold text-[#0f2942] tracking-tight">
          Cryptographic Evidence Ledger & QR Verification
        </h1>
        <p className="text-xs text-slate-600 max-w-xl mx-auto">
          Authenticate printed Government Gazette notices, payment hold directives, and electronic evidence records against the central statutory ledger via recomputed SHA-256 validation.
        </p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="civic-card p-4 flex gap-2">
        <div className="relative flex-1">
          <Search className="h-4 w-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            required
            placeholder="Enter Dossier Reference ID (e.g. DOSSIER-202407-8819A)..."
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            className="w-full bg-slate-50 border border-slate-300 rounded pl-9 pr-3 py-2 text-xs text-slate-900 font-mono focus:border-orange-500 focus:outline-none"
          />
        </div>

        <button
          type="submit"
          disabled={isVerifying}
          className="px-5 py-2 rounded bg-orange-600 hover:bg-orange-700 disabled:opacity-50 text-white font-bold text-xs uppercase tracking-wider shadow-sm transition-all"
        >
          {isVerifying ? "Verifying..." : "Verify Record"}
        </button>
      </form>

      {/* State 1: Record Not Found (404) */}
      {notFound && (
        <div className="civic-card p-6 border-rose-300 bg-rose-50/70 space-y-3 text-rose-900">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-full bg-rose-200 text-rose-700">
              <XCircle className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-sm font-bold">Dossier Record Not Found (404)</h3>
              <p className="text-xs text-rose-700">{errorMessage}</p>
            </div>
          </div>
          <div className="p-3 bg-white rounded border border-rose-200 text-xs text-slate-700 leading-relaxed font-mono">
            <strong>Security Notice:</strong> The supplied identifier does not correspond to any registered audit dossier in the central ledger. Non-repudiation and legal authenticity cannot be established.
          </div>
        </div>
      )}

      {/* State 2: Tampered / Hash Mismatch */}
      {tampered && verifiedRecord && (
        <div className="civic-card p-6 border-rose-500 bg-rose-50 space-y-4 text-rose-950">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-full bg-rose-600 text-white">
              <AlertTriangle className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-sm font-extrabold text-rose-800 uppercase tracking-wide">
                Integrity Check Failed — Evidence Tampering Detected
              </h3>
              <p className="text-xs text-rose-700">
                The database record values for this dossier do not match the original SHA-256 seal.
              </p>
            </div>
          </div>

          <div className="p-4 bg-white rounded border border-rose-300 text-xs font-mono space-y-2">
            <div><span className="text-slate-500">Dossier ID:</span> <span className="font-bold">{verifiedRecord.dossier_id}</span></div>
            <div><span className="text-slate-500">Stored Seal:</span> <span className="text-rose-700 font-bold break-all">{verifiedRecord.sha256_seal}</span></div>
            <div><span className="text-slate-500">Recomputed Digest:</span> <span className="text-amber-700 font-bold break-all">{verifiedRecord.recomputed_seal}</span></div>
            <div><span className="text-slate-500">Status:</span> <span className="text-rose-700 font-bold">{verifiedRecord.ledger_integrity}</span></div>
          </div>
        </div>
      )}

      {/* State 3: Authentic Verified Record */}
      {verifiedRecord && verifiedRecord.verified && !tampered && (
        <div className="civic-card p-8 border-emerald-300 bg-white space-y-6 shadow-lg relative overflow-hidden">
          
          <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-50 rounded-full blur-2xl pointer-events-none" />

          {/* Verification Badge */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200">
            <div className="flex items-center space-x-3">
              <div className="p-3 rounded-full bg-emerald-100 text-emerald-700">
                <CheckCircle2 className="h-6 w-6" />
              </div>
              <div>
                <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-700 block">
                  Official Cryptographic Certificate
                </span>
                <h3 className="text-base font-bold text-[#0f2942]">
                  Authentic Statutory Record Verified
                </h3>
              </div>
            </div>

            <div className="px-3 py-1 rounded bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-mono font-bold">
              Status: {verifiedRecord.ledger_integrity} (SHA-256 Match)
            </div>
          </div>

          {/* Details Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono bg-slate-50 p-5 rounded-lg border border-slate-200">
            <div>
              <span className="text-slate-500 block text-[10px] font-sans font-semibold">Dossier Reference ID:</span>
              <span className="font-bold text-slate-900">{verifiedRecord.dossier_id}</span>
            </div>

            <div>
              <span className="text-slate-500 block text-[10px] font-sans font-semibold">Project Name:</span>
              <span className="font-bold text-slate-900">{verifiedRecord.project_name || "N/A"}</span>
            </div>

            <div>
              <span className="text-slate-500 block text-[10px] font-sans font-semibold">Contractor Name:</span>
              <span className="text-slate-800 font-sans font-medium">{verifiedRecord.contractor_name || "N/A"}</span>
            </div>

            <div>
              <span className="text-slate-500 block text-[10px] font-sans font-semibold">Recorded Verdict:</span>
              <span className={`font-bold ${verifiedRecord.verdict === "FLAGGED" ? "text-rose-700" : "text-emerald-700"}`}>
                {verifiedRecord.verdict} (Risk: {verifiedRecord.risk_score}/100)
              </span>
            </div>

            <div className="sm:col-span-2">
              <span className="text-slate-500 block text-[10px] font-sans font-semibold">Verified SHA-256 Cryptographic Seal:</span>
              <span className="text-emerald-800 font-bold break-all">{verifiedRecord.sha256_seal}</span>
            </div>

            <div className="sm:col-span-2">
              <span className="text-slate-500 block text-[10px] font-sans font-semibold">Verification Timestamp:</span>
              <span className="text-slate-800">{verifiedRecord.verified_at_utc}</span>
            </div>
          </div>

          {/* Legal Footnote */}
          <div className="p-3 rounded bg-slate-100 border border-slate-200 text-slate-600 text-[11px] leading-relaxed">
            <strong>Admissibility Note:</strong> Recomputed SHA-256 hash confirms complete cryptographic equivalence with the original central ledger record under General Financial Rules (GFR 2017) Rule 175.
          </div>

        </div>
      )}

      {/* General Error Message */}
      {errorMessage && !notFound && !tampered && (
        <div className="civic-card p-4 border-amber-300 bg-amber-50 text-amber-900 text-xs">
          {errorMessage}
        </div>
      )}

    </div>
  );
}

export default function PublicVerificationPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs text-slate-500">Loading verification portal...</div>}>
      <VerifyContent />
    </Suspense>
  );
}
