// // import React, { useState } from "react";
// import React, {useContext, useState } from "react";
// import { Link } from "react-router";
// import { useNavigate } from "react-router-dom";
// import "./Navbar.css";
// import LanguageButton from "../../components/ChangeLanguageButton/ChangeLanguageButton";
// import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

// const Navbar = () => {
//   const { language } = useContext(LanguageContext);
//   const [isSearchOpen, setIsSearchOpen] = useState(false);
//   const [searchQuery, setSearchQuery] = useState("");
//   const [searchResults, setSearchResults] = useState(null);
//   const [error, setError] = useState(null);
//   const navigate = useNavigate();

//   const toggleSearch = () => {
//     console.log("Тоггл поиска. Сейчас:", isSearchOpen);
//     setIsSearchOpen(!isSearchOpen);
//     setSearchResults(null);
//     setSearchQuery("");
//     setError(null);
//   };

//   const handleSearchChange = async (e) => {
//     const value = e.target.value;
//     setSearchQuery(value);
//     console.log("Изменение ввода, текущее значение:", value);

//     if (value.length > 2) {
//       await performSearch(value);
//     } else {
//       setSearchResults(null);
//     }
//   };

//   const handleSearchKeyPress = async (e) => {
//     if (e.key === "Enter" && searchQuery.trim().length > 2) {
//       console.log("Enter нажат. Перенаправление на страницу поиска...");
//       navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
//     }
//   };

//   const performSearch = async (query) => {
//     console.log(" Отправка запроса:", query);

//     try {
//       const response = await fetch(`${process.env.REACT_APP_API_URL}/search?q=${encodeURIComponent(query)}`);
//       console.log("Ответ от сервера (статус):", response.status);
//       if (!response.ok) {
//         throw new Error(`Ошибка сервера: ${response.status}`);
//       }

//       const data = await response.json();
//       console.log("Данные с сервера:", data);

//       setSearchResults(data);
//       setError(null);
//     } catch (err) {
//       console.error("Ошибка при поиске:", err);
//       setError("Ошибка загрузки результатов поиска");
//     }
//   };

//   return (
//     <>
//       <div className={`search-bar ${isSearchOpen ? "active" : ""}`} style={{ top: isSearchOpen ? "0" : "-100px" }}>
//         <input
//           type="text"
//           placeholder={language === 'ru' ? 'Поиск...' : 'Search...'}
//           value={searchQuery}
//           onChange={handleSearchChange}
//           onKeyDown={handleSearchKeyPress}
//         />
//         <button className="close-search" onClick={toggleSearch}>
//           <img src="/cross.png" alt="Закрыть" />
//         </button>
//       </div>

//       {error && <p className="error-message">{error}</p>}
//       {searchResults && (
//         <div className="search-results">
//           {Object.keys(searchResults).map((category) =>
//             searchResults[category].length > 0 ? (
//               <div key={category}>
//                 <h4>{category.toUpperCase()}</h4>
//                 <ul>
//                   {searchResults[category].map((item) => (
//                     <li key={item.id}>
//                       <Link to={item.link || "#"}>{item.title || item.name}</Link>
//                     </li>
//                   ))}
//                 </ul>
//               </div>
//             ) : null
//           )}
//         </div>
//       )}
//       <nav className="navbar">
//         <div className="navbar-container">
//           <Link to="/" className="navbar-logo">
//             <img src="/hse_logo.png" alt="HSE Logo" />
//           </Link>
//           <ul className="nav-menu">
//             <li className="nav-item"><Link to="/" className="nav-link">{language === 'ru' ? 'Главная' : 'Home'}</Link></li>
//             <li className="nav-item"><Link to="/organisations" className="nav-link">{language === 'ru' ? 'Организации' : 'Organisations'}</Link></li>
//             <li className="nav-item"><Link to="/publications" className="nav-link">{language === 'ru' ? 'Публикации' : 'Publications'}</Link></li>
//             <li className="nav-item"><Link to="/news" className="nav-link">{language === 'ru' ? 'Новости' : 'News'}</Link></li>
//             <li className="nav-item"><Link to="/projects" className="nav-link">{language === 'ru' ? 'Проекты' : 'Projects'}</Link></li>
//             <li className="nav-item"><Link to="/events" className="nav-link">{language === 'ru' ? 'События' : 'Events'}</Link></li>
//           </ul>
//           <div className="search-icon" onClick={toggleSearch}>
//             <img src="/loopa.png" alt="Поиск" />
//           </div>
//           <div> <LanguageButton/> </div>
//         </div>
//       </nav>
//     </>
//   );
// };

// export default Navbar;


import React, { useContext, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";
import LanguageButton from "../../components/ChangeLanguageButton/ChangeLanguageButton";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const Navbar = () => {
  const { language } = useContext(LanguageContext);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();

  // Закрытие меню при изменении размера экрана
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setIsMenuOpen(false);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const toggleSearch = () => {
    setIsSearchOpen(!isSearchOpen);
    setSearchResults(null);
    setSearchQuery("");
    setError(null);
    if (isMenuOpen) setIsMenuOpen(false);
  };

  const handleSearchChange = async (e) => {
    const value = e.target.value;
    setSearchQuery(value);

    if (value.length > 2) {
      await performSearch(value);
    } else {
      setSearchResults(null);
    }
  };

  const handleSearchKeyPress = async (e) => {
    if (e.key === "Enter" && searchQuery.trim().length > 2) {
      navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
      setIsSearchOpen(false);
    }
  };

  const performSearch = async (query) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/search?q=${encodeURIComponent(query)}`
      );
      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }
      const data = await response.json();
      setSearchResults(data);
      setError(null);
    } catch (err) {
      setError(language === 'ru' 
        ? "Ошибка загрузки результатов поиска" 
        : "Error loading search results");
    }
  };

  return (
    <>
      {/* Поисковая строка */}
      <div className={`search-bar ${isSearchOpen ? "active" : ""}`}>
        <input
          type="text"
          placeholder={language === 'ru' ? 'Поиск...' : 'Search...'}
          value={searchQuery}
          onChange={handleSearchChange}
          onKeyDown={handleSearchKeyPress}
        />
        <button className="close-search" onClick={toggleSearch}>
          <img src="/cross.png" alt={language === 'ru' ? 'Закрыть' : 'Close'} />
        </button>
      </div>

      {/* Результаты поиска */}
      {error && <p className="error-message">{error}</p>}
      {searchResults && (
        <div className="search-results">
          {Object.keys(searchResults).map((category) =>
            searchResults[category].length > 0 && (
              <div key={category}>
                <h4>{category.toUpperCase()}</h4>
                <ul>
                  {searchResults[category].map((item) => (
                    <li key={item.id}>
                      <Link 
                        to={item.link || "#"} 
                        onClick={() => {
                          setIsSearchOpen(false);
                          setIsMenuOpen(false);
                        }}
                      >
                        {item.title || item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            )
          )}
        </div>
      )}

      {/* Основная навигация */}
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-logo" onClick={() => setIsMenuOpen(false)}>
            <img src="/hse_logo.png" alt="HSE Logo" />
          </Link>

          {/* Бургер-меню для мобильных */}
          <div 
            className={`menu-toggle ${isMenuOpen ? 'active' : ''}`} 
            onClick={toggleMenu}
            aria-label={language === 'ru' ? 'Меню' : 'Menu'}
          >
            <span></span>
            <span></span>
            <span></span>
          </div>

          {/* Основное меню */}
          <ul className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
            <li className="nav-item">
              <Link 
                to="/" 
                className="nav-link"
                onClick={() => setIsMenuOpen(false)}
              >
                {language === 'ru' ? 'Главная' : 'Home'}
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/organisations" 
                className="nav-link"
                onClick={() => setIsMenuOpen(false)}
              >
                {language === 'ru' ? 'Организации' : 'Organisations'}
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/publications" 
                className="nav-link"
                onClick={() => setIsMenuOpen(false)}
              >
                {language === 'ru' ? 'Публикации' : 'Publications'}
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/news" 
                className="nav-link"
                onClick={() => setIsMenuOpen(false)}
              >
                {language === 'ru' ? 'Новости' : 'News'}
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/projects" 
                className="nav-link"
                onClick={() => setIsMenuOpen(false)}
              >
                {language === 'ru' ? 'Проекты' : 'Projects'}
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/events" 
                className="nav-link"
                onClick={() => setIsMenuOpen(false)}
              >
                {language === 'ru' ? 'События' : 'Events'}
              </Link>
            </li>
          </ul>

          {/* Иконки поиска и языка */}
          <div className="nav-icons">
            <div className="search-icon" onClick={toggleSearch}>
              <img src="/loopa.png" alt={language === 'ru' ? 'Поиск' : 'Search'} />
            </div>
            <LanguageButton />
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;