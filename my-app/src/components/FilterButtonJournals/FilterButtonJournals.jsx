import React, {useContext, useState, useEffect } from 'react';
import '../../components/FilterButtonAuthors/FilterButtonAuthors.css';
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const JournalFilter = ({ onApply }) => {
  const { language } = useContext(LanguageContext);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedAuthors, setSelectedMagazines] = useState([]);
  const [magazines, setMagazines] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/magazines`)
      .then(res => res.json())
      .then(data => setMagazines(data))
      .catch(console.error);
  }, []);

  const toggleDropdown = () => setIsOpen(!isOpen);

  const handleCheckboxChange = (magazineId) => {
    setSelectedMagazines(prev => prev.includes(magazineId) ? prev.filter(id => id !== magazineId) : [...prev, magazineId]
    );
  };

  return (
    <div className="author-filter">
      <button className="filter-button" onClick={toggleDropdown}> {language === 'ru' ? 'Журналы' : 'Journals'}</button>
      
      {isOpen && (
        <div className="dropdown-content">
          {magazines.map(magazine => (
            <label 
              key={magazine.id} 
              className="filter-item">
              <input
                type="checkbox"
                checked={selectedAuthors.includes(magazine.id)}
                onChange={() => handleCheckboxChange(magazine.id)}/>
              <span className="author-name">
                {magazine.name} {magazine.news} {magazine.publications}
              </span>
            </label>
          ))}
          
          <button 
            className="apply-button"
            onClick={() => {
              onApply(selectedAuthors);
              setIsOpen(false);
            }}>
            {language === 'ru' ? 'Применить' : 'Apply'}
            </button>
        </div>
      )}
    </div>
  );
};

export default JournalFilter;