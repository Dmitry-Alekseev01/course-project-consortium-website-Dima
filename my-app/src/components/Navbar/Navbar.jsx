import React, { useState, useContext, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";
import LanguageButton from "../../components/ChangeLanguageButton/ChangeLanguageButton";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const Navbar = () => {
  const { language } = useContext(LanguageContext);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (isMenuOpen && 
          !e.target.closest('.mobile-menu') && 
          !e.target.closest('.burger-menu')) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isMenuOpen]);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeAll = () => {
    setIsMenuOpen(false);
    setIsSearchOpen(false);
  };

  const toggleSearch = () => {
    setIsSearchOpen(!isSearchOpen);
    setSearchResults(null);
    setSearchQuery("");
    setError(null);
  };

  const handleSearchChange = async (e) => {
    const value = e.target.value;
    setSearchQuery(value);

    if (value.length > 2) {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/search?q=${encodeURIComponent(value)}`
        );
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        const data = await response.json();
        setSearchResults(data);
        setError(null);
      } catch (err) {
        console.error("Search error:", err);
        setError(language === 'ru' ? 'Ошибка поиска' : 'Search error');
      }
    } else {
      setSearchResults(null);
    }
  };

  const handleSearchKeyPress = (e) => {
    if (e.key === 'Enter' && searchQuery.trim().length > 2) {
      navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
      closeAll();
    }
  };

  return (
    <>
      <div className={`search-bar ${isSearchOpen ? "active" : ""}`} 
           style={{ top: isSearchOpen ? "0" : "-100px" }}>
        <input
          type="text"
          placeholder={language === 'ru' ? 'Поиск...' : 'Search...'}
          value={searchQuery}
          onChange={handleSearchChange}
          onKeyDown={handleSearchKeyPress}
        />
        <button className="close-search" onClick={toggleSearch}>
          <img src="/cross.png" alt="Close" />
        </button>
      </div>
      
      {searchResults && (
        <div className="search-results">
          {Object.keys(searchResults).map((category) =>
            searchResults[category].length > 0 && (
              <div key={category}>
                <h4>{category.toUpperCase()}</h4>
                <ul>
                  {searchResults[category].map((item) => (
                    <li key={item.id}>
                      <Link to={item.link || "#"} onClick={closeAll}>
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

      <nav className="navbar">
        <div className="navbar-container">
          <button 
            className={`burger-menu ${isMenuOpen ? 'active' : ''}`} 
            onClick={toggleMenu}
            aria-label={language === 'ru' ? 'Меню' : 'Menu'}
          >
            <div className="burger-line"></div>
            <div className="burger-line"></div>
            <div className="burger-line"></div>
          </button>

          <Link to="/" className="navbar-logo" onClick={closeAll}>
            <img src="/hse_logo.png" alt="HSE Logo" />
          </Link>

          <ul className="nav-menu">
            <li className="nav-item">
              <Link to="/" className="nav-link">{language === 'ru' ? 'Главная' : 'Home'}</Link>
            </li>
            <li className="nav-item">
              <Link to="/organisations" className="nav-link">{language === 'ru' ? 'Организации' : 'Organisations'}</Link>
            </li>
            <li className="nav-item">
              <Link to="/publications" className="nav-link">{language === 'ru' ? 'Публикации' : 'Publications'}</Link>
            </li>
            <li className="nav-item">
              <Link to="/news" className="nav-link">{language === 'ru' ? 'Новости' : 'News'}</Link>
            </li>
            <li className="nav-item">
              <Link to="/projects" className="nav-link">{language === 'ru' ? 'Проекты' : 'Projects'}</Link>
            </li>
            <li className="nav-item">
              <Link to="/events" className="nav-link">{language === 'ru' ? 'События' : 'Events'}</Link>
            </li>
          </ul>

          <div className="search-icon" onClick={toggleSearch}>
            <img src="/loopa.png" alt="Search" />
          </div>
          
          <div className="language-button-container">
            <LanguageButton />
          </div>

          <div className={`mobile-menu ${isMenuOpen ? 'active' : ''}`}>
            <ul>
              <li className="nav-item">
                <Link to="/" className="nav-link" onClick={closeAll}>{language === 'ru' ? 'Главная' : 'Home'}</Link>
              </li>
              <li className="nav-item">
                <Link to="/organisations" className="nav-link" onClick={closeAll}>{language === 'ru' ? 'Организации' : 'Organisations'}</Link>
              </li>
              <li className="nav-item">
                <Link to="/publications" className="nav-link" onClick={closeAll}>{language === 'ru' ? 'Публикации' : 'Publications'}</Link>
              </li>
              <li className="nav-item">
                <Link to="/news" className="nav-link" onClick={closeAll}>{language === 'ru' ? 'Новости' : 'News'}</Link>
              </li>
              <li className="nav-item">
                <Link to="/projects" className="nav-link" onClick={closeAll}>{language === 'ru' ? 'Проекты' : 'Projects'}</Link>
              </li>
              <li className="nav-item">
                <Link to="/events" className="nav-link" onClick={closeAll}>{language === 'ru' ? 'События' : 'Events'}</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;