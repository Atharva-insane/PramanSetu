"use client";

import Link from "next/link";
import {
  ShieldCheck,
  Scale,
  Landmark,
  FileCheck2,
  Users,
  Search,
  ArrowRight,
  TrendingUp,
  Cpu,
  Layers,
  Sparkles,
  Globe,
  Award,
  CheckCircle2,
  HelpCircle,
  Briefcase,
  GraduationCap,
  ChevronRight
} from "lucide-react";

import { useLanguage } from "@/context/LanguageContext";

export default function HomePage() {
  const { t } = useLanguage();

  return (
    <div className="space-y-12 pb-8">
      
      {/* 1. Friendly Monumental Hero Banner */}
      <section className="relative rounded-2xl overflow-hidden shadow-xl border border-slate-300 min-h-[440px] flex items-center bg-[#0f2942]">
        
        <div className="absolute inset-0 bg-[radial-gradient(#1e3a8a_1px,transparent_1px)] [background-size:24px_24px] opacity-25" />
        <div className="absolute top-0 right-0 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-5xl mx-auto px-6 py-12 text-center text-white space-y-6">
          
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/10 border border-white/20 backdrop-blur-sm text-xs font-semibold text-orange-400">
            <Landmark className="h-3.5 w-3.5" />
            <span className="tracking-wide uppercase text-[11px]">
              {t.heroBadge}
            </span>
          </div>

          <div className="hero-frame-box p-6 md:p-8 rounded-xl max-w-3xl mx-auto space-y-3 shadow-2xl">
            <h1 className="text-2xl sm:text-4xl md:text-5xl font-black uppercase tracking-tight leading-tight text-white font-sans">
              {t.heroHeadline}
            </h1>
            <p className="text-xs sm:text-sm text-slate-200 font-medium max-w-xl mx-auto leading-relaxed">
              {t.heroSubtitle}
            </p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <Link
              href="/intake"
              className="px-6 py-3 rounded-lg bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs uppercase tracking-wider flex items-center space-x-2 shadow-lg hover:shadow-orange-600/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <span>{t.btnStartAudit}</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              href="/demo"
              className="px-6 py-3 rounded-lg bg-white/15 hover:bg-white/25 text-white font-bold text-xs uppercase tracking-wider border border-white/30 backdrop-blur-sm transition-all"
            >
              {t.demo}
            </Link>
          </div>

        </div>
      </section>

      {/* 2. "How It Works in 3 Simple Steps" - Friendly Onboarding */}
      <section className="civic-card p-6 md:p-8 space-y-6">
        <div className="text-center max-w-xl mx-auto space-y-1">
          <span className="text-[10px] font-bold uppercase tracking-widest text-orange-600">
            GFR 2017 (Rule 175)
          </span>
          <h2 className="text-xl font-bold text-[#0f2942]">
            {t.howItWorksTitle}
          </h2>
          <p className="text-xs text-slate-500">
            {t.howItWorksSubtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
          
          {/* Step 1 */}
          <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3 text-center relative">
            <div className="h-10 w-10 mx-auto rounded-full bg-orange-100 text-orange-700 font-black text-sm flex items-center justify-center">
              1
            </div>
            <h3 className="text-sm font-bold text-slate-900">{t.step1Title}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.step1Desc}
            </p>
          </div>

          {/* Step 2 */}
          <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3 text-center relative">
            <div className="h-10 w-10 mx-auto rounded-full bg-blue-100 text-blue-700 font-black text-sm flex items-center justify-center">
              2
            </div>
            <h3 className="text-sm font-bold text-slate-900">{t.step2Title}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.step2Desc}
            </p>
          </div>

          {/* Step 3 */}
          <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3 text-center relative">
            <div className="h-10 w-10 mx-auto rounded-full bg-emerald-100 text-emerald-700 font-black text-sm flex items-center justify-center">
              3
            </div>
            <h3 className="text-sm font-bold text-slate-900">{t.step3Title}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.step3Desc}
            </p>
          </div>

        </div>
      </section>

      {/* 3. Persona-Based Guide: "Choose Your Role" */}
      <section className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-[#0f2942]">
              {t.roleSelectTitle}
            </h2>
            <p className="text-xs text-slate-500">
              {t.roleSelectSubtitle}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          {/* Persona 1: Government Officer / Engineer */}
          <Link
            href="/intake"
            className="civic-card p-5 bg-white border-l-4 border-l-orange-500 hover:border-orange-500 space-y-3 group flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="p-2 rounded-lg bg-orange-100 text-orange-700 group-hover:bg-orange-600 group-hover:text-white transition-colors">
                  <Briefcase className="h-5 w-5" />
                </div>
                <span className="text-[10px] font-bold text-orange-700 bg-orange-50 px-2 py-0.5 rounded border border-orange-200">
                  {t.gatekeeper}
                </span>
              </div>
              <h3 className="text-sm font-bold text-[#0f2942]">{t.role1Title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                {t.role1Desc}
              </p>
            </div>

            <div className="pt-2 flex items-center text-xs font-bold text-orange-700 group-hover:text-orange-900">
              <span>{t.role1Btn}</span>
              <ChevronRight className="h-4 w-4 ml-0.5" />
            </div>
          </Link>

          {/* Persona 2: Evaluator / Judge */}
          <Link
            href="/demo"
            className="civic-card p-5 bg-white border-l-4 border-l-purple-500 hover:border-purple-500 space-y-3 group flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="p-2 rounded-lg bg-purple-100 text-purple-700 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                  <GraduationCap className="h-5 w-5" />
                </div>
                <span className="text-[10px] font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                  {t.demo}
                </span>
              </div>
              <h3 className="text-sm font-bold text-[#0f2942]">{t.role2Title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                {t.role2Desc}
              </p>
            </div>

            <div className="pt-2 flex items-center text-xs font-bold text-purple-700 group-hover:text-purple-900">
              <span>{t.role2Btn}</span>
              <ChevronRight className="h-4 w-4 ml-0.5" />
            </div>
          </Link>

          {/* Persona 3: Citizen / Gram Panchayat */}
          <Link
            href="/citizen"
            className="civic-card p-5 bg-white border-l-4 border-l-emerald-500 hover:border-emerald-500 space-y-3 group flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="p-2 rounded-lg bg-emerald-100 text-emerald-700 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                  <Users className="h-5 w-5" />
                </div>
                <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  {t.citizen}
                </span>
              </div>
              <h3 className="text-sm font-bold text-[#0f2942]">{t.role3Title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                {t.role3Desc}
              </p>
            </div>

            <div className="pt-2 flex items-center text-xs font-bold text-emerald-700 group-hover:text-emerald-900">
              <span>{t.role3Btn}</span>
              <ChevronRight className="h-4 w-4 ml-0.5" />
            </div>
          </Link>

          {/* Persona 4: CVO Vigilance Director */}
          <Link
            href="/analytics"
            className="civic-card p-5 bg-white border-l-4 border-l-blue-500 hover:border-l-blue-600 space-y-3 group flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="p-2 rounded-lg bg-blue-100 text-blue-700 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                  <Scale className="h-5 w-5" />
                </div>
                <span className="text-[10px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                  {t.analytics}
                </span>
              </div>
              <h3 className="text-sm font-bold text-[#0f2942]">{t.role4Title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                {t.role4Desc}
              </p>
            </div>

            <div className="pt-2 flex items-center text-xs font-bold text-blue-700 group-hover:text-blue-900">
              <span>{t.role4Btn}</span>
              <ChevronRight className="h-4 w-4 ml-0.5" />
            </div>
          </Link>

        </div>
      </section>

      {/* 4. Macro Vigilance Statistics Counter Strip */}
      <section className="civic-card p-6 md:p-8 bg-[#0f2942] text-white border-slate-800 shadow-xl">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center divide-x-0 md:divide-x divide-slate-700">
          
          <div className="space-y-1">
            <span className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">{t.statTotalAudited}</span>
            <div className="text-3xl md:text-4xl font-black text-white font-mono">62</div>
            <p className="text-[11px] text-slate-400">100% Pre-Approval</p>
          </div>

          <div className="space-y-1">
            <span className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">{t.statPreventedFraud}</span>
            <div className="text-3xl md:text-4xl font-black text-emerald-400 font-mono">₹5.42 Cr</div>
            <p className="text-[11px] text-slate-400">Treasury Protected</p>
          </div>

          <div className="space-y-1">
            <span className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">{t.statAverageSpeed}</span>
            <div className="text-3xl md:text-4xl font-black text-orange-400 font-mono">&lt; 2.5s</div>
            <p className="text-[11px] text-slate-400">10-Vector Scan</p>
          </div>

          <div className="space-y-1">
            <span className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">{t.activeEngines}</span>
            <div className="text-3xl md:text-4xl font-black text-purple-400 font-mono">10 / 10</div>
            <p className="text-[11px] text-slate-400">Live AI & Geodesic</p>
          </div>

        </div>
      </section>

      {/* 5. Institutional Standards & Compliance Footer Strip */}
      <section className="civic-card p-5 bg-white flex flex-wrap items-center justify-between gap-4 text-xs text-slate-600">
        <div className="flex items-center space-x-2">
          <Award className="h-4 w-4 text-orange-600 shrink-0" />
          <span className="font-bold text-slate-800">{t.gfrCompliance}</span>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-[11px] font-mono">
          <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
            GFR 2017 Rule 175
          </span>
          <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
            RTI Act 2005 Section 6(1)
          </span>
          <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
            CVC Guidelines
          </span>
          <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
            Digital India
          </span>
        </div>
      </section>

    </div>
  );
}
