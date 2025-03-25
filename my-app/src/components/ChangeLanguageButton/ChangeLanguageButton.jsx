import React, { useContext, useEffect, useState } from 'react';
import { LanguageContext } from '../../components/LanguageContext/LanguageContext';
import './ChangeLanguageButton.css';

const LanguageToggleButton = () => {
  const { language, toggleLanguage } = useContext(LanguageContext);
  const [isFlipped, setIsFlipped] = useState(language === 'en');

  useEffect(() => {
    setIsFlipped(language === 'en');
  }, [language]);

  const handleClick = () => {
    toggleLanguage();
  };

  return (
    <div className={`language-toggle-button ${isFlipped ? 'flipped' : ''}`} onClick={handleClick}>
      <div className="language-toggle-button-inner">
        <div className="language-toggle-button-front">
          {language === 'eng' ? 'ENG' : 'RU'}
        </div>
        <div className="language-toggle-button-back">
          {language === 'ru' ? 'RU' : 'ENG'}
        </div>
      </div>
    </div>
  );
};

export default LanguageToggleButton;