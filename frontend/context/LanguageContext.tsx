"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { SupportedLanguage, TranslationDict, translations } from "@/lib/translations";

interface LanguageContextType {
  language: SupportedLanguage;
  setLanguage: (lang: SupportedLanguage) => void;
  t: TranslationDict;
}

const LanguageContext = createContext<LanguageContextType>({
  language: "English",
  setLanguage: () => {},
  t: translations.English,
});

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<SupportedLanguage>("English");

  useEffect(() => {
    const saved = localStorage.getItem("pramansetu_lang") as SupportedLanguage;
    if (saved && (saved === "English" || saved === "हिंदी" || saved === "தமிழ்")) {
      setLanguageState(saved);
    }
  }, []);

  const setLanguage = (lang: SupportedLanguage) => {
    setLanguageState(lang);
    try {
      localStorage.setItem("pramansetu_lang", lang);
    } catch (e) {
      // Ignore localStorage errors in private mode
    }
  };

  const t = translations[language] || translations.English;

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
