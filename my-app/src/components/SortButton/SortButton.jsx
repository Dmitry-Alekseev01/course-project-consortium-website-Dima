import React, {useContext, useState } from "react";
import './SortButton.css'; 
import { Link } from "react-router-dom";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";


const SortButton = ({ onSort }) => {
  const { language } = useContext(LanguageContext);
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleSort = (sortType) => {
    onSort(sortType);
    setIsOpen(false);
  };

  return (
    <div className="dropdown">
      <button className="dropbtn" onClick={toggleDropdown}>
        {language === 'ru' ? 'Отсортировать' : 'Sort'}
      </button>
      {isOpen && (
        <div className="dropdown-content">
          <Link to="#" onClick={() => handleSort('alphabetical')}>{language === 'ru' ? 'По алфавиту (А - Я)' : 'Alphabetical (A - Z)'}</Link>
          <Link to="#" onClick={() => handleSort('reverse_alphabetical')}>{language === 'ru' ? 'По алфавиту (Я - А)' : 'Alphabetical (Z - A)'}</Link>
          <Link to="#" onClick={() => handleSort('date_asc')}>{language === 'ru' ? 'По дате (стар - нов)' : 'Date (old - new)'}</Link>
          <Link to="#" onClick={() => handleSort('date_desc')}>{language === 'ru' ? 'По дате (нов - стар)' : 'Date (new - old)'}</Link>
        </div>
      )}
    </div>
  );
};

export default SortButton;
