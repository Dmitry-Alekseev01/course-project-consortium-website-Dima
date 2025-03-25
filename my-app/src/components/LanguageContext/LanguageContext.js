import React, { createContext, useState, useEffect } from 'react';

export const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('ru');

  useEffect(() => {
    const savedLang = localStorage.getItem('language');
    const validLang = ['ru', 'en'].includes(savedLang) ? savedLang : 'ru';
    setLanguage(validLang);
    localStorage.setItem('language', validLang);
  }, []);

  const toggleLanguage = () => {
    const newLang = language === 'ru' ? 'en' : 'ru';
    setLanguage(newLang);
    localStorage.setItem('language', newLang);
  };

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};

// // LanguageContext.js
// import React, { createContext, useState, useEffect } from 'react';

// export const LanguageContext = createContext();

// export const LanguageProvider = ({ children }) => {
//   const [language, setLanguage] = useState(() => {
//     // Инициализация из localStorage сразу при создании
//     const savedLang = localStorage.getItem('language');
//     return ['ru', 'en'].includes(savedLang) ? savedLang : 'ru';
//   });

//   useEffect(() => {
//     // Синхронизация при изменении языка
//     localStorage.setItem('language', language);
//   }, [language]);

//   const toggleLanguage = () => {
//     setLanguage(prev => (prev === 'ru' ? 'en' : 'ru'));
//   };

//   return (
//     <LanguageContext.Provider value={{ 
//       language,
//       toggleLanguage 
//     }}>
//       {children}
//     </LanguageContext.Provider>
//   );
// };

// import React, { createContext, useState, useEffect } from 'react';

// export const LanguageContext = createContext();

// export const LanguageProvider = ({ children }) => {
//   const [language, setLanguage] = useState(() => {
//     const savedLang = localStorage.getItem('language');
//     return ['ru', 'en'].includes(savedLang) ? savedLang : 'ru';
//   });

//   const toggleLanguage = () => {
//     setLanguage(prevLang => {
//       const newLang = prevLang === 'ru' ? 'en' : 'ru';
//       localStorage.setItem('language', newLang);
//       return newLang;
//     });
//   };

//   return (
//     <LanguageContext.Provider value={{ language, toggleLanguage }}>
//       {children}
//     </LanguageContext.Provider>
//   );
// };