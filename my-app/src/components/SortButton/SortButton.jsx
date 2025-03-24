import React, { useState } from 'react';
import './SortButton.css'; 
import { Link } from "react-router-dom";


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
          <Link to="#" onClick={() => handleSort('alphabetical')}>По алфавиту (А - Я)</Link>
          <Link to="#" onClick={() => handleSort('reverse_alphabetical')}>По алфавиту (Я - А)</Link>
          <Link to="#" onClick={() => handleSort('date_asc')}>По дате (стар - нов)</Link>
          <Link to="#" onClick={() => handleSort('date_desc')}>По дате (нов - стар)</Link>
        </div>
      )}
    </div>
  );
};

export default SortButton;
