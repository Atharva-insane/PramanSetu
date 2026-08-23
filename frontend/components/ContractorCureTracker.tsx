"use client";

import React, { useState } from "react";
import { Clock, AlertCircle, CheckCircle2, ChevronDown, ChevronUp, Send, FileText, Scale } from "lucide-react";

interface ContractorCureTrackerProps {
  dossierId: string;
  contractorName: string;
}

export default function ContractorCureTracker({ dossierId, contractorName }: ContractorCureTrackerProps) {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [rebuttalText, setRebuttalText] = useState(
    "Contractor submits that the photographic coordinates differed due to GPS shadowing under dense foliage; attached certified surveyor certificate claiming physical asphalt completion."
  );
  const [defenseStatus, setDefenseStatus] = useState<"pending" | "submitted" | "reviewed">("pending");
  const [evaluationResult, setEvaluationResult] = useState<string | null>(null);

  // Calculate 7-day statutory deadline from current date
  const now = new Date();
  const cureDeadline = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  const deadlineStr = cureDeadline.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const handleSimulateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setDefenseStatus("submitted");
    setEvaluationResult(
      "CVO EVALUATION: Contractor defense REJECTED. Perceptual frequency hash confirms image was captured in 2023 for Package #102; GPS shadowing cannot alter optical DCT frequency characteristics. Proceeding with GFR 175 Debarment."
    );
  };

  return (
    <div className="civic-card p-5 space-y-4 border-amber-300 bg-amber-50/40">
      
      {/* Top Header & 7-Day Countdown */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start space-x-3">
          <div className="p-2.5 rounded-lg bg-amber-100 text-amber-800 shrink-0">
            <Clock className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-[10px] uppercase tracking-wider font-bold px-1.5 py-0.5 rounded bg-amber-200 text-amber-900">
                Rule 175 GFR 2017
              </span>
              <h4 className="text-sm font-bold text-[#0f2942]">
                7-Day Statutory Cure Period & Natural Justice Tracker
              </h4>
            </div>
            <p className="text-xs text-slate-600 mt-0.5">
              Contractor <span className="font-semibold text-slate-900">{contractorName}</span> has a mandatory 7-day window to submit written defense before GeM debarment.
            </p>
          </div>
        </div>

        {/* Countdown Badge */}
        <div className="p-3 rounded-lg bg-white border border-amber-300 text-center shrink-0 shadow-sm font-mono">
          <span className="text-[9px] uppercase font-sans font-bold text-slate-500 block">
            Statutory Cure Deadline
          </span>
          <span className="text-xs font-bold text-amber-800">
            {deadlineStr} (6d 23h remaining)
          </span>
        </div>
      </div>

      {/* Simulator Toggle Button */}
      <div className="pt-2 border-t border-amber-200">
        <button
          onClick={() => setIsDrawerOpen(!isDrawerOpen)}
          className="w-full flex items-center justify-between text-xs font-bold text-amber-900 hover:text-amber-700"
        >
          <span className="flex items-center space-x-1.5">
            <Scale className="h-4 w-4 text-amber-700" />
            <span>Simulate Contractor Written Defense / Rebuttal Review</span>
          </span>
          {isDrawerOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </button>

        {isDrawerOpen && (
          <form onSubmit={handleSimulateSubmit} className="mt-3 p-4 rounded-lg bg-white border border-slate-200 space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Contractor Formal Written Explanation / Counter-Claim
              </label>
              <textarea
                rows={3}
                value={rebuttalText}
                onChange={(e) => setRebuttalText(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded p-2 text-xs text-slate-900 focus:border-orange-500 focus:outline-none font-sans"
              />
            </div>

            <div className="flex items-center justify-between">
              <span className="text-[11px] text-slate-500 font-medium">
                Simulates receiving formal contractor response via procurement portal.
              </span>

              <button
                type="submit"
                className="px-3.5 py-1.5 rounded bg-amber-700 hover:bg-amber-800 text-white font-bold text-xs flex items-center space-x-1 shadow-sm"
              >
                <Send className="h-3.5 w-3.5" />
                <span>Evaluate Contractor Defense</span>
              </button>
            </div>

            {evaluationResult && (
              <div className="p-3 rounded bg-rose-50 border border-rose-200 text-rose-900 text-xs font-mono leading-relaxed mt-2">
                <span className="font-bold block text-rose-950 font-sans uppercase text-[10px]">
                  Vigilance Evaluation Outcome:
                </span>
                {evaluationResult}
              </div>
            )}
          </form>
        )}
      </div>

    </div>
  );
}
