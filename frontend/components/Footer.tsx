"use client";

import React from "react";
import { useLanguage } from "@/context/LanguageContext";

export default function Footer() {
  const { t, language } = useLanguage();

  const footerText = {
    English: {
      copyright: `PramanSetu (प्रमाण सेतु) © ${new Date().getFullYear()} • National Pre-Approval Public Governance & Anti-Corruption Framework`,
      compliance: "Operational compliance with General Financial Rules (GFR 2017) Rule 175 and Section 6(1) Right to Information Act, 2005.",
    },
    हिंदी: {
      copyright: `प्रमाण सेतु (PramanSetu) © ${new Date().getFullYear()} • राष्ट्रीय भुगतान-पूर्व सार्वजनिक खरीद एवं सतर्कता मंच`,
      compliance: "सामान्य वित्तीय नियम (GFR 2017) नियम 175 एवं सूचना का अधिकार अधिनियम 2005 की धारा 6(1) के अनुरूप।",
    },
    தமிழ்: {
      copyright: `பிரமாண் சேது (PramanSetu) © ${new Date().getFullYear()} • தேசிய முன் அனுமதி பொது நிர்வாகம் மற்றும் ஊழல் தடுப்பு தளம்`,
      compliance: "GFR 2017 விதி 175 மற்றும் தகவல் அறியும் உரிமைச் சட்டம் 2005 பிரிவு 6(1) இன் கீழ் செயல்படுகிறது.",
    }
  }[language] || {
    copyright: `PramanSetu (प्रमाण सेतु) © ${new Date().getFullYear()} • National Pre-Approval Public Governance & Anti-Corruption Framework`,
    compliance: "Operational compliance with General Financial Rules (GFR 2017) Rule 175 and Section 6(1) Right to Information Act, 2005.",
  };

  return (
    <footer className="border-t border-slate-200 bg-white py-8 text-center text-xs text-slate-500">
      <div className="max-w-7xl mx-auto px-4 space-y-2">
        <p className="font-semibold text-slate-700">
          {footerText.copyright}
        </p>
        <p className="text-[11px] text-slate-500">
          {footerText.compliance}
        </p>
      </div>
    </footer>
  );
}
