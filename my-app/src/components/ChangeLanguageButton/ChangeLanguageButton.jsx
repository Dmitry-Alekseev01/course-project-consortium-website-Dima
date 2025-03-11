import React, { useState, useContext } from 'react';
import { LanguageContext } from '../../components/LanguageContext/LanguageContext';
import './ChangeLanguageButton.css';

const LanguageToggleButton = () => {
  const { language, toggleLanguage } = useContext(LanguageContext);
  const [isFlipped, setIsFlipped] = useState(false);

  const handleClick = () => {
    setIsFlipped(!isFlipped);
    toggleLanguage();
  };

  return (
    <div className={`language-toggle-button ${isFlipped ? 'flipped' : ''}`} onClick={handleClick}>
      <div className="language-toggle-button-inner">
        <div className="language-toggle-button-front">
          {language === 'ru' ? 'RU' : 'ENG'}
        </div>
        <div className="language-toggle-button-back">
          {language === 'ru' ? 'ENG' : 'RU'}
        </div>
      </div>
    </div>
  );
};

export default LanguageToggleButton;