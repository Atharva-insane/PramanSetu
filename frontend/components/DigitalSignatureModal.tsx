"use client";

import React, { useState } from "react";
import { ShieldCheck, Lock, X, CheckCircle2, Award, Key } from "lucide-react";

interface DigitalSignatureModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSignSuccess: (sigData: { officerName: string; designation: string; department: string; dscToken: string; signedAt: string }) => void;
}

export default function DigitalSignatureModal({ isOpen, onClose, onSignSuccess }: DigitalSignatureModalProps) {
  const [officerName, setOfficerName] = useState("Er. Rajeshwar Nath Sharma");
  const [designation, setDesignation] = useState("Executive Engineer (Vigilance & Quality)");
  const [department, setDepartment] = useState("Public Works Department (PWD), National Infrastructure Cell");
  const [dscToken, setDscToken] = useState("DSC-2024-CLASS3-IN-88912");
  const [pin, setPin] = useState("••••••••");
  const [isSigning, setIsSigning] = useState(false);

  if (!isOpen) return null;

  const handleSign = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSigning(true);

    setTimeout(() => {
      setIsSigning(false);
      onSignSuccess({
        officerName,
        designation,
        department,
        dscToken,
        signedAt: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" }) + " IST",
      });
      onClose();
    }, 800);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="civic-card max-w-lg w-full p-6 space-y-5 bg-white shadow-2xl relative animate-in fade-in zoom-in-95 duration-200">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Header */}
        <div className="flex items-center space-x-3">
          <div className="p-3 rounded-lg bg-orange-100 text-orange-700">
            <Lock className="h-6 w-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-[#0f2942]">
              Simulate Officer Class-3 DSC Stamping
            </h3>
            <p className="text-xs text-slate-500">
              Institutional Demonstration • Class-3 USB Cryptographic Token Simulation
            </p>
          </div>
        </div>

        {/* Prototype Disclaimer Banner */}
        <div className="p-2.5 rounded bg-amber-50 border border-amber-200 text-amber-900 text-[11px] leading-relaxed">
          <strong>Workflow Note:</strong> This interface simulates the officer token signing ceremony. It generates a structured evidence stamp without invoking physical PKCS#11 hardware drivers.
        </div>

        {/* Signing Form */}
        <form onSubmit={handleSign} className="space-y-3.5">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Authorized Signatory Name
            </label>
            <input
              type="text"
              required
              value={officerName}
              onChange={(e) => setOfficerName(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none font-medium"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Official Designation
            </label>
            <input
              type="text"
              required
              value={designation}
              onChange={(e) => setDesignation(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none font-medium"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Department / Directorate
            </label>
            <input
              type="text"
              required
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none font-medium"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                DSC Certificate Token ID
              </label>
              <input
                type="text"
                required
                value={dscToken}
                onChange={(e) => setDscToken(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 font-mono focus:border-orange-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Hardware Token PIN
              </label>
              <input
                type="password"
                required
                value={pin}
                onChange={(e) => setPin(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 font-mono focus:border-orange-500 focus:outline-none"
              />
            </div>
          </div>

          {/* Legal Notice */}
          <div className="p-3 rounded bg-blue-50 border border-blue-200 text-blue-900 text-[11px] leading-relaxed">
            <span className="font-bold">Statutory Certification:</span> Applying this digital signature certifies that the evidence was reviewed under Section 65B of the Indian Evidence Act and GFR 2017 Rule 175.
          </div>

          {/* Submit */}
          <div className="pt-2 flex items-center justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded text-xs font-semibold text-slate-600 hover:bg-slate-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSigning}
              className="px-4 py-2 rounded bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs uppercase tracking-wider flex items-center space-x-1.5 shadow-sm"
            >
              <ShieldCheck className="h-4 w-4" />
              <span>{isSigning ? "Applying Digital Seal..." : "Sign & Seal Document"}</span>
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}
