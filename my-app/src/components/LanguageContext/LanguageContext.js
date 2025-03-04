import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('ru');

  useEffect(() => {
    const savedLang = localStorage.getItem('language') || 'ru';
    setLanguage(savedLang);
  }, []);

  const toggleLanguage = async () => {
    const newLang = language === 'ru' ? 'en' : 'ru';
    try {
      await axios.post('http://127.0.0.1:5000/api/set_language', { language: newLang });
      setLanguage(newLang);
      localStorage.setItem('language', newLang);
    } catch (error) {
      console.error('Language change failed:', error);
    }
  };

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};