// import React, { useState } from 'react';
// import './ChangeLanguageButton.css';

// const LanguageButton = () => {
//   const [isFlipped, setIsFlipped] = useState(false);

//   const handleClick = () => {
//     setIsFlipped(!isFlipped);
//   };

//   return (
//     <div className={`flip-button ${isFlipped ? 'flipped' : ''}`} onClick={handleClick}>
//       <div className="flip-button-inner">
//         <div className="flip-button-front">RU</div>
//         <div className="flip-button-back">ENG</div>
//       </div>
//     </div>
//   );
// };

// export default LanguageButton;

import React, { useState, useContext } from 'react';
import { LanguageContext } from '../../components/LanguageContext/LanguageContext';
import './ChangeLanguageButton.css';

const LanguageButton = () => {
  const { language, toggleLanguage } = useContext(LanguageContext);
  const [isFlipped, setIsFlipped] = useState(false);

  const handleClick = () => {
    setIsFlipped(!isFlipped);
    toggleLanguage();
  };

  return (
    <div className={`flip-button ${isFlipped ? 'flipped' : ''}`} onClick={handleClick}>
      <div className="flip-button-inner">
        <div className="flip-button-front">{language === 'ru' ? 'RU' : 'ENG'}</div>
        <div className="flip-button-back">{language === 'ru' ? 'ENG' : 'RU'}</div>
      </div>
    </div>
  );
};

export default LanguageButton;