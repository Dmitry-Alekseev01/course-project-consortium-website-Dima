import React, { useState } from 'react';
import './SortButton.css'; // Подключаем стили

const SortButton = () => {
  const [isOpen, setIsOpen] = useState(false); // Состояние для управления видимостью меню

  const toggleDropdown = () => {
    setIsOpen(!isOpen); // Переключаем состояние
  };

  return (
    <div className="dropdown">
      <button className="dropbtn" onClick={toggleDropdown}>
        Отсортировать
      </button>
      {isOpen && (
        <div className="dropdown-content">
          {/* <a href="#">Recommended</a> */}
          <a href="#">В алфавитном порядке</a>
          <a href="#">В обратном алфавитном порядке</a>
          <a href="#">По дате (по возрастанию)</a>
          <a href="#">По дате (по убыванию)</a>
        </div>
      )}
    </div>
  );
};

export default SortButton;