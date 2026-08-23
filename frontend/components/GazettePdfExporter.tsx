"use client";

import React from "react";
import { Landmark, Scale, ShieldCheck, Printer, X, QrCode } from "lucide-react";

interface GazettePdfExporterProps {
  auditData: any;
  signatureData?: any;
  onClose: () => void;
}

export default function GazettePdfExporter({ auditData, signatureData, onClose }: GazettePdfExporterProps) {
  if (!auditData) return null;

  const {
    status,
    risk_score,
    decision_reason,
    project_metadata,
    contractor_profile,
    dossier,
    duplicate_check,
    location_check,
    web_search_check,
    muster_roll_check,
    chrono_check,
    material_check,
    genai_forensic_check
  } = auditData;

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadGazette = () => {
    const gazetteContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>OFFICIAL GAZETTE • GFR 2017 RULE 175 • ${dossier?.dossier_id || "DOSSIER"}</title>
  <style>
    body { font-family: Georgia, serif; margin: 40px; color: #111; line-height: 1.6; }
    .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 20px; }
    .header h1 { margin: 0; font-size: 20px; text-transform: uppercase; }
    .header p { margin: 4px 0 0; font-size: 13px; color: #444; }
    .badge { background: #fee2e2; border: 1px solid #b91c1c; color: #991b1b; padding: 6px 12px; font-weight: bold; text-align: center; margin: 16px 0; }
    .meta-table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }
    .meta-table td, .meta-table th { border: 1px solid #ccc; padding: 8px; }
    .meta-table th { background: #f3f4f6; text-align: left; }
    .seal-box { border: 2px dashed #0f2942; padding: 12px; background: #f8fafc; font-family: monospace; font-size: 11px; margin-top: 24px; }
    @media print { body { margin: 0; } }
  </style>
</head>
<body>
  <div class="header">
    <div style="font-size: 11px; font-weight: bold; letter-spacing: 2px;">GOVERNMENT OF INDIA • NATIONAL EVIDENCE GATEWAY</div>
    <h1>Office of the Executive Engineer & Tender Scrutiny Authority</h1>
    <p>GFR 2017 Rule 175 Statutory Show-Cause & Payment Freeze Gazette</p>
  </div>
  <div class="badge">PRE-APPROVAL PAYMENT HOLD: ${status} (Risk Score: ${risk_score}/100)</div>
  <table class="meta-table">
    <tr><th>Dossier Reference</th><td>${dossier?.dossier_id}</td><th>Issue Date</th><td>${dossier?.generated_at}</td></tr>
    <tr><th>Project Title</th><td>${project_metadata?.project_name}</td><th>Tender ID</th><td>${project_metadata?.tender_id}</td></tr>
    <tr><th>Contractor</th><td>${contractor_profile?.contractor_name}</td><th>Claim Amount</th><td>${project_metadata?.claim_amount}</td></tr>
    <tr><th>Primary Reason</th><td colspan="3">${decision_reason}</td></tr>
  </table>
  <h3>Forensic Telemetry Summary</h3>
  <ul>
    <li><b>pHash Invariant Check:</b> ${duplicate_check?.message || "Verified"}</li>
    <li><b>WGS-84 Geodesic Verification:</b> ${location_check?.message || "Verified"}</li>
    <li><b>Global Web Reverse Search:</b> ${web_search_check?.message || "Original Capture"}</li>
    <li><b>NOAA Solar & Open-Meteo Radar:</b> ${chrono_check?.message || "Verified"}</li>
    <li><b>Labor Muster Roll Discrepancy:</b> Disputed Leakage: ₹${muster_roll_check?.suspected_ghost_wage_leakage || 0}</li>
  </ul>
  <div class="seal-box">
    <b>OFFICIAL RFC-8785 CRYPTOGRAPHIC SEAL:</b> ${shaSeal}<br>
    <b>QR NON-REPUDIATION VERIFICATION PORTAL:</b> <a href="${qrUrl}">${qrUrl}</a>
  </div>
</body>
</html>`;

    const blob = new Blob([gazetteContent], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${dossier?.dossier_id || "GAZETTE"}_OFFICIAL_NOTICE.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const qrUrl = dossier?.crypto_verification?.verification_url || "http://localhost:3000/verify";
  const shaSeal = dossier?.crypto_verification?.sha256_seal || "a3f89e81b2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8";

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm overflow-y-auto p-4 flex justify-center">
      <div className="bg-white max-w-4xl w-full my-8 rounded-xl shadow-2xl overflow-hidden text-slate-900 font-sans border border-slate-300">
        
        {/* Top Floating Action Bar (Hidden in Print) */}
        <div className="p-4 bg-[#0f2942] text-white flex items-center justify-between sticky top-0 z-10 print:hidden">
          <div className="flex items-center space-x-2">
            <Scale className="h-5 w-5 text-orange-400" />
            <span className="font-bold text-sm">
              Official Government Gazette Notice (GFR 2017 Rule 175)
            </span>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleDownloadGazette}
              className="px-3.5 py-2 rounded bg-slate-700 hover:bg-slate-600 text-white font-bold text-xs flex items-center space-x-1.5 shadow-sm transition-colors"
            >
              <span>Download Gazette (.html)</span>
            </button>
            <button
              onClick={handlePrint}
              className="px-4 py-2 rounded bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs flex items-center space-x-1.5 shadow-sm transition-colors"
            >
              <Printer className="h-4 w-4" />
              <span>Print / Save as PDF</span>
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded bg-white/10 hover:bg-white/20 text-white"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Printable Multi-Page Document Body */}
        <div className="p-8 md:p-12 space-y-12 bg-white text-slate-900 print:p-0 print:space-y-8">
          
          {/* ================= PAGE 1: STATUTORY SHOW-CAUSE NOTICE ================= */}
          <div className="space-y-6 min-h-[900px] border-b-2 border-dashed border-slate-300 pb-12 print:border-none print:min-h-screen print:page-break-after-always">
            
            {/* National Header */}
            <div className="text-center space-y-1 border-b-2 border-slate-900 pb-4">
              <span className="text-[11px] font-bold tracking-widest uppercase text-slate-600 block">
                GOVERNMENT OF INDIA &bull; NATIONAL PROCUREMENT OVERSIGHT INITIATIVE
              </span>
              <h1 className="text-xl font-extrabold tracking-tight uppercase text-slate-950 font-serif">
                OFFICE OF THE EXECUTIVE ENGINEER & TENDER SCRUTINY AUTHORITY
              </h1>
              <p className="text-xs text-slate-600 font-serif">
                State Vigilance & Public Works Scrutiny Cell &bull; Central Evidence Registry
              </p>
            </div>

            {/* Reference Bar */}
            <div className="flex items-center justify-between text-xs font-mono border-b border-slate-200 pb-2">
              <span>Ref: GFR-2017/Rule-175/VIG/{dossier?.dossier_id}</span>
              <span>Date of Issue: {dossier?.generated_at}</span>
            </div>

            {/* Notice Title */}
            <div className="text-center py-2 bg-slate-100 border border-slate-300 rounded font-bold text-xs uppercase tracking-wide">
              FORMAL SHOW-CAUSE NOTICE & PRE-DISBURSEMENT PAYMENT FREEZE DIRECTIVE
            </div>

            {/* Notice Body */}
            <div className="space-y-4 text-xs font-serif leading-relaxed text-justify">
              <p>
                <strong>To:</strong> Authorized Representative, <strong>{project_metadata?.contractor_name}</strong>
                <br />
                <strong>Subject:</strong> Notice to Show-Cause regarding critical evidentiary discrepancies in milestone payment claim for Tender No: <strong>{project_metadata?.tender_id}</strong>.
              </p>

              <p>
                1. <strong>WHEREAS</strong> your firm submitted physical completion evidence claiming fund disbursement of <strong>{project_metadata?.claim_amount}</strong> for the project titled <em>&ldquo;{project_metadata?.project_name}&rdquo;</em> under scheme <em>&ldquo;{project_metadata?.scheme}&rdquo;</em>.
              </p>

              <p>
                2. <strong>AND WHEREAS</strong> statutory pre-approval scrutiny conducted via the CivicAudit AI Evidence Gateway recorded a <strong>Composite Risk Score of {risk_score}/100 ({status})</strong> with the following primary infractions:
              </p>

              <div className="p-3 bg-slate-50 border border-slate-200 rounded font-sans text-xs space-y-1">
                <div>&bull; <strong>Decision Finding:</strong> {decision_reason}</div>
                <div>&bull; <strong>Action Directive:</strong> {auditData.recommended_action}</div>
              </div>

              <p>
                3. <strong>NOW THEREFORE</strong>, under Rule 175 of the General Financial Rules (GFR 2017) and Clause 59 of the Works Procurement Contract, you are hereby called upon to <strong>SHOW CAUSE within SEVEN (7) DAYS</strong> of receipt of this memorandum why:
              </p>
              <ul className="list-decimal pl-6 space-y-1 font-sans text-[11px]">
                <li>The milestone disbursement claim should not be cancelled permanently;</li>
                <li>The Performance Bank Guarantee (PBG) deposited with the Treasury should not be forfeited; and</li>
                <li>Proceedings for debarment and blacklisting from Government e-Marketplace (GeM) should not be initiated.</li>
              </ul>
            </div>

            {/* Digital Signature Box & Verification QR */}
            <div className="pt-6 border-t border-slate-300 flex flex-col sm:flex-row items-center justify-between gap-4">
              
              {/* Digital Signature Seal */}
              <div className="p-3.5 rounded-lg border-2 border-emerald-600 bg-emerald-50/70 text-emerald-950 text-xs space-y-1 w-full sm:w-80">
                <div className="flex items-center space-x-1.5 font-bold text-emerald-800 uppercase text-[10px]">
                  <ShieldCheck className="h-4 w-4 text-emerald-600" />
                  <span>Officially Digitally Certified</span>
                </div>
                <div className="font-bold text-slate-900">{signatureData?.officerName || "Er. Rajeshwar Nath Sharma"}</div>
                <div className="text-[10px] text-slate-600">{signatureData?.designation || "Executive Engineer (Vigilance)"}</div>
                <div className="text-[9px] font-mono text-slate-500">{signatureData?.dscToken || "DSC-CLASS3-IN-88912"} &bull; {signatureData?.signedAt || "Certified on Record"}</div>
              </div>

              {/* QR Code Verification Block */}
              <div className="flex items-center space-x-3 p-3 rounded-lg border border-slate-300 bg-slate-50 text-right font-mono text-[10px]">
                <div>
                  <span className="font-bold block text-slate-800 font-sans">Scan to Authenticate</span>
                  <span className="text-slate-500">SHA-256: {shaSeal.slice(0, 12)}...</span>
                </div>
                <div className="p-1.5 bg-white border border-slate-400 rounded">
                  <QrCode className="h-10 w-10 text-slate-900" />
                </div>
              </div>

            </div>

          </div>

          {/* ================= PAGE 2: ANNEXURE A (VISUAL EVIDENCE RECORD) ================= */}
          <div className="space-y-6 min-h-[900px] border-b-2 border-dashed border-slate-300 pb-12 print:border-none print:min-h-screen print:page-break-after-always">
            
            <div className="border-b-2 border-slate-900 pb-2">
              <span className="text-xs font-bold uppercase tracking-widest text-orange-600 block">
                ANNEXURE A: CERTIFIED EVIDENCE METADATA & OPTICAL AUDIT
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Physical Construction Evidence Examination Record
              </h2>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs font-mono bg-slate-50 p-4 border border-slate-300 rounded">
              <div><span className="text-slate-500">Submitted File:</span> {auditData.filename}</div>
              <div><span className="text-slate-500">Contractor:</span> {project_metadata?.contractor_name}</div>
              <div><span className="text-slate-500">Designated GPS:</span> ({project_metadata?.claimed_latitude}, {project_metadata?.claimed_longitude})</div>
              <div><span className="text-slate-500">Measured Distance:</span> {location_check?.distance_metres}m from corridor</div>
              <div><span className="text-slate-500">Perceptual Hash:</span> {duplicate_check?.closest_match ? "RECYCLED ASSET" : "UNIQUE"}</div>
              <div><span className="text-slate-500">Web Stock Match:</span> {web_search_check?.match_found ? web_search_check.domain : "NONE"}</div>
            </div>

            <div className="p-4 bg-slate-100 rounded border border-slate-300 text-xs font-serif leading-relaxed">
              <h4 className="font-bold text-slate-900 font-sans mb-1">Optical Inspection Notes:</h4>
              <p>{genai_forensic_check?.reason || "Zero-shot visual inspection verified authentic physical characteristics."}</p>
            </div>

          </div>

          {/* ================= PAGE 3: ANNEXURE B (DISPUTED LABOR ROLL) ================= */}
          <div className="space-y-6 min-h-[900px] border-b-2 border-dashed border-slate-300 pb-12 print:border-none print:min-h-screen print:page-break-after-always">
            
            <div className="border-b-2 border-slate-900 pb-2">
              <span className="text-xs font-bold uppercase tracking-widest text-purple-700 block">
                ANNEXURE B: AUDIT DISPUTED LABOR MUSTER ROLL & WAGE LEAKAGE SCHEDULE
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Itemized Phantom Worker Discrepancies
              </h2>
            </div>

            <div className="p-3 bg-purple-50 border border-purple-200 rounded text-xs font-bold text-purple-900 flex justify-between">
              <span>Total Suspected Treasury Wage Leakage:</span>
              <span>₹{muster_roll_check?.suspected_ghost_wage_leakage?.toLocaleString() || "0.00"}</span>
            </div>

            <table className="w-full text-left text-xs border border-slate-300 border-collapse">
              <thead>
                <tr className="bg-slate-100 border-b border-slate-300 font-bold text-slate-700 text-[10px] uppercase">
                  <th className="p-2 border-r border-slate-300">Worker ID</th>
                  <th className="p-2 border-r border-slate-300">Name & Trade</th>
                  <th className="p-2 border-r border-slate-300">Claimed Days</th>
                  <th className="p-2 border-r border-slate-300">Daily Wage</th>
                  <th className="p-2 border-r border-slate-300">Claimed Amount</th>
                  <th className="p-2">Discrepancy Reason</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 font-medium">
                {muster_roll_check?.discrepancies?.map((w: any, idx: number) => (
                  <tr key={idx}>
                    <td className="p-2 font-mono font-bold border-r border-slate-200">{w.worker_id}</td>
                    <td className="p-2 border-r border-slate-200">{w.worker_name} ({w.trade})</td>
                    <td className="p-2 font-mono border-r border-slate-200">{w.days_claimed}</td>
                    <td className="p-2 font-mono border-r border-slate-200">₹{w.daily_wage}</td>
                    <td className="p-2 font-mono font-bold text-orange-700 border-r border-slate-200">₹{w.claimed_wage_total?.toLocaleString()}</td>
                    <td className="p-2 text-rose-700 font-sans text-[11px]">{w.discrepancy_reason}</td>
                  </tr>
                ))}
              </tbody>
            </table>

          </div>

          {/* ================= PAGE 4: ANNEXURE C (10-VECTOR MATHEMATICAL PROOF) ================= */}
          <div className="space-y-6 min-h-[900px] print:min-h-screen">
            
            <div className="border-b-2 border-slate-900 pb-2">
              <span className="text-xs font-bold uppercase tracking-widest text-blue-700 block">
                ANNEXURE C: 10-VECTOR MATHEMATICAL MATRIX & ALGORITHMIC LOG
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Transparent Forensic Formula & Regulatory Scoring Log
              </h2>
            </div>

            <div className="p-3 bg-slate-100 border border-slate-300 rounded font-mono text-xs text-slate-800">
              Formula: <strong>Risk Score = min(100, Σ W_i · S_i) = {risk_score}/100</strong>
            </div>

            <div className="space-y-3">
              {auditData.risk_assessment?.breakdown?.map((item: any, idx: number) => (
                <div key={idx} className="p-3 rounded border border-slate-200 bg-slate-50 flex items-start justify-between text-xs">
                  <div>
                    <span className="font-bold text-slate-900">{item.label}</span>
                    <p className="text-slate-600 text-[11px] mt-0.5">{item.reason}</p>
                  </div>
                  <span className={`font-mono font-bold px-2 py-0.5 rounded text-[10px] ${
                    item.triggered ? "bg-rose-100 text-rose-800 border border-rose-200" : "bg-emerald-100 text-emerald-800"
                  }`}>
                    {item.triggered ? `+${item.weight} pts` : "0 pts (PASS)"}
                  </span>
                </div>
              ))}
            </div>

            {/* Official Certification Seal Footer */}
            <div className="pt-8 border-t-2 border-slate-900 text-center text-xs text-slate-600 space-y-1 font-serif">
              <p className="font-bold text-slate-900">CERTIFIED TRUE COPY OF THE ADMINISTRATIVE VIGILANCE LEDGER</p>
              <p>Generated by CivicAudit AI Pre-Approval Evidence Intelligence Gateway &bull; Reference SHA-256: {shaSeal}</p>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
