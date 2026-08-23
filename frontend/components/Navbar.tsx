"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  Shield,
  BarChart3,
  Users,
  PlayCircle,
  Landmark,
  Scale,
  Search,
  ChevronDown,
  Globe,
  Menu,
  X,
  Activity
} from "lucide-react";
import { fetchHealthDiagnostics } from "@/lib/api";

import { SupportedLanguage } from "@/lib/translations";
import { useLanguage } from "@/context/LanguageContext";

export default function Navbar() {
  const pathname = usePathname();
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const { language, setLanguage, t } = useLanguage();

  useEffect(() => {
    async function checkHealth() {
      const health = await fetchHealthDiagnostics();
      if (health && health.status === "operational") {
        setIsOnline(true);
      } else {
        setIsOnline(false);
      }
    }
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { label: t.home, href: "/" },
    { label: t.gatekeeper, href: "/intake" },
    { label: t.ledger, href: "/dashboard" },
    { label: t.analytics, href: "/analytics" },
    { label: t.citizen, href: "/citizen" },
    { label: t.demo, href: "/demo" },
  ];

  return (
    <header className="sticky top-0 z-50 w-full bg-white border-b border-slate-200 shadow-xs">
      
      {/* Top Institutional Utility Strip */}
      <div className="bg-[#0f2942] text-slate-200 px-4 sm:px-6 lg:px-8 py-1.5 text-xs flex items-center justify-between border-b border-slate-700">
        <div className="flex items-center space-x-2">
          <Landmark className="h-3.5 w-3.5 text-orange-400 shrink-0" />
          <span className="font-semibold tracking-wide uppercase text-[11px] truncate">
            {t.govTitle}
          </span>
        </div>

        <div className="flex items-center space-x-4 text-[11px] shrink-0">
          <span className="hidden md:inline text-slate-300 font-mono">
            {t.gfrCompliance}
          </span>
          <div className="flex items-center space-x-1.5 pl-3 border-l border-slate-600">
            <span className={`h-2 w-2 rounded-full ${isOnline ? "bg-emerald-400 animate-pulse" : "bg-amber-400"}`} />
            <span className="font-medium text-slate-200">
              {isOnline ? t.activeEngines : "Connecting Gateway..."}
            </span>
          </div>
        </div>
      </div>

      {/* Main Clean White Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="h-10 w-10 rounded-lg bg-[#0f2942] flex items-center justify-center shadow-xs group-hover:bg-[#0a1c2e] transition-colors">
            <Scale className="h-5 w-5 text-orange-500" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-xl tracking-tight text-[#0f2942]">
                Praman<span className="text-orange-600">Setu</span>
              </span>
              <span className="text-[9px] uppercase tracking-wider font-bold px-1.5 py-0.5 rounded bg-orange-100 text-orange-700 border border-orange-200">
                प्रमाण सेतु
              </span>
            </div>
            <p className="text-[10px] text-slate-500 font-medium tracking-tight">
              {language === "हिंदी"
                ? "राष्ट्रीय साक्ष्य आसूचना सतर्कता द्वार"
                : language === "தமிழ்"
                ? "தேசிய ஆதார நுண்ணறிவு நுழைவாயில்"
                : "National Evidence Intelligence Gateway"}
            </p>
          </div>
        </Link>

        {/* Navigation Items (Desktop) */}
        <nav className="hidden lg:flex items-center space-x-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`px-3 py-2 rounded-md text-xs font-semibold transition-all ${
                  isActive
                    ? "text-orange-600 bg-orange-50/80 border-b-2 border-orange-600 rounded-b-none"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Right Utility (Diagnostics Badge & Action Button) */}
        <div className="flex items-center space-x-3">
          
          {/* Engine Diagnostics Indicator */}
          <div className="hidden xl:flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-100 border border-slate-200 text-[11px] font-mono">
            <span
              className={`h-2 w-2 rounded-full ${
                isOnline === true
                  ? "bg-emerald-500 animate-pulse"
                  : isOnline === false
                  ? "bg-rose-500"
                  : "bg-amber-400"
              }`}
            />
            <span className="text-slate-700 font-semibold font-sans">
              {isOnline === true
                ? (language === "हिंदी" ? "10/10 इंजन सक्रिय" : language === "தமிழ்" ? "10/10 இயந்திரங்கள் இயங்குகின்றன" : "10/10 Engines Active")
                : isOnline === false
                ? "Engines Offline"
                : "Checking Engines..."}
            </span>
          </div>
          
          {/* Language Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setLangMenuOpen(!langMenuOpen)}
              className="hidden sm:flex items-center space-x-1 px-2.5 py-1.5 rounded-md border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
            >
              <Globe className="h-3.5 w-3.5 text-slate-500" />
              <span>{language}</span>
              <ChevronDown className="h-3 w-3 text-slate-400" />
            </button>

            {langMenuOpen && (
              <div className="absolute right-0 mt-1 w-28 bg-white border border-slate-200 rounded-md shadow-lg py-1 z-50 text-xs font-medium">
                {(["English", "हिंदी", "தமிழ்"] as SupportedLanguage[]).map((lang) => (
                  <button
                    key={lang}
                    onClick={() => {
                      setLanguage(lang);
                      setLangMenuOpen(false);
                    }}
                    className={`w-full text-left px-3 py-1.5 hover:bg-orange-50 hover:text-orange-600 transition-colors ${
                      language === lang ? "text-orange-600 font-bold bg-orange-50/50" : "text-slate-700"
                    }`}
                  >
                    {lang}
                  </button>
                ))}
              </div>
            )}
          </div>

          <Link
            href="/intake"
            className="flex items-center space-x-1.5 bg-orange-600 hover:bg-orange-700 text-white font-bold px-4 py-2 rounded-md text-xs uppercase tracking-wider shadow-xs transition-all hover:shadow hover:-translate-y-0.5 active:translate-y-0"
          >
            <Shield className="h-4 w-4" />
            <span>{t.auditClaim}</span>
          </Link>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 rounded-md text-slate-600 hover:bg-slate-100"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>

        </div>

      </div>

      {/* Mobile Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-slate-200 bg-white p-4 space-y-2 shadow-lg animate-in slide-in-from-top-2 duration-150">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setMobileMenuOpen(false)}
              className={`block px-3 py-2 rounded-md text-xs font-bold ${
                pathname === item.href
                  ? "bg-orange-50 text-orange-600"
                  : "text-slate-700 hover:bg-slate-50"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      )}

    </header>
  );
}
