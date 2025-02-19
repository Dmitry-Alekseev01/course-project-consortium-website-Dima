import React, { useState, useEffect } from 'react';
import '../../components/FilterButtonAuthors/FilterButtonAuthors.css';

const JournalFilter = ({ onApply }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedAuthors, setSelectedMagazines] = useState([]);
  const [magazines, setMagazines] = useState([]);

  // Загрузка авторов с бэкенда
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/magazines')
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
      <button className="filter-button" onClick={toggleDropdown}>Журналы</button>
      
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
              {/* <span className="count">{magazine.news_count}</span> */}
            </label>
          ))}
          
          <button 
            className="apply-button"
            onClick={() => {
              onApply(selectedAuthors);
              setIsOpen(false);
            }}>
            Применить
          </button>
        </div>
      )}
    </div>
  );
};

export default JournalFilter;