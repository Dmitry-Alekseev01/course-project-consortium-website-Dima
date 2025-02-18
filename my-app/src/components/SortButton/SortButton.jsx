import React, { useState } from 'react';
import './SortButton.css'; // Подключаем стили

// const SortButton = () => {
//   const [isOpen, setIsOpen] = useState(false); // Состояние для управления видимостью меню

//   const toggleDropdown = () => {
//     setIsOpen(!isOpen); // Переключаем состояние
//   };

//   return (
//     <div className="dropdown">
//       <button className="dropbtn" onClick={toggleDropdown}>
//         Отсортировать
//       </button>
//       {isOpen && (
//         <div className="dropdown-content">
//           {/* <a href="#">Recommended</a> */}
//           <a href="#">В алфавитном порядке</a>
//           <a href="#">В обратном алфавитном порядке</a>
//           <a href="#">По дате (по возрастанию)</a>
//           <a href="#">По дате (по убыванию)</a>
//         </div>
//       )}
//     </div>
//   );
// };



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
          <a href="#" onClick={() => handleSort('date_asc')}>По дате (нов - стар)</a>
          <a href="#" onClick={() => handleSort('date_desc')}>По дате (стар - нов)</a>
        </div>
      )}
    </div>
  );
};

export default SortButton;
