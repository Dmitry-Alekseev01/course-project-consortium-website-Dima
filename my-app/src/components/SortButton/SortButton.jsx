import React, { useState } from 'react';
import './SortButton.css'; // Подключаем стили

const SortButton = ({ onSort }) => {
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
        Отсортировать
      </button>
      {isOpen && (
        <div className="dropdown-content">
          <a href="#" onClick={() => handleSort('alphabetical')}>По алфавиту (А - Я)</a>
          <a href="#" onClick={() => handleSort('reverse_alphabetical')}>По алфавиту (Я - А)</a>
          <a href="#" onClick={() => handleSort('date_asc')}>По дате (стар - нов)</a>
          <a href="#" onClick={() => handleSort('date_desc')}>По дате (нов - стар)</a>
        </div>
      )}
    </div>
  );
};

export default SortButton;
