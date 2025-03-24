import React, { useState } from "react";
import { Link } from "react-router";
import { useNavigate } from "react-router-dom";
import "./Navbar.css";
import LanguageButton from "../../components/ChangeLanguageButton/ChangeLanguageButton";

const Navbar = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const toggleSearch = () => {
    console.log("Тоггл поиска. Сейчас:", isSearchOpen);
    setIsSearchOpen(!isSearchOpen);
    setSearchResults(null);
    setSearchQuery("");
    setError(null);
  };

  const handleSearchChange = async (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    console.log("Изменение ввода, текущее значение:", value);

    if (value.length > 2) {
      await performSearch(value);
    } else {
      setSearchResults(null);
    }
  };

  const handleSearchKeyPress = async (e) => {
    if (e.key === "Enter" && searchQuery.trim().length > 2) {
      console.log("Enter нажат. Перенаправление на страницу поиска...");
      navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
    }
  };

  const performSearch = async (query) => {
    console.log(" Отправка запроса:", query);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/search?q=${encodeURIComponent(query)}`);
      console.log("Ответ от сервера (статус):", response.status);
      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }

      const data = await response.json();
      console.log("Данные с сервера:", data);

      setSearchResults(data);
      setError(null);
    } catch (err) {
      console.error("Ошибка при поиске:", err);
      setError("Ошибка загрузки результатов поиска");
    }
  };

  return (
    <>
      <div className={`search-bar ${isSearchOpen ? "active" : ""}`} style={{ top: isSearchOpen ? "0" : "-100px" }}>
        <input
          type="text"
          placeholder="Поиск..."
          value={searchQuery}
          onChange={handleSearchChange}
          onKeyDown={handleSearchKeyPress}
        />
        <button className="close-search" onClick={toggleSearch}>
          <img src="/cross.png" alt="Закрыть" />
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}
      {searchResults && (
        <div className="search-results">
          {Object.keys(searchResults).map((category) =>
            searchResults[category].length > 0 ? (
              <div key={category}>
                <h4>{category.toUpperCase()}</h4>
                <ul>
                  {searchResults[category].map((item) => (
                    <li key={item.id}>
                      <Link to={item.link || "#"}>{item.title || item.name}</Link>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null
          )}
        </div>
      )}
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-logo">
            <img src="/hse_logo.png" alt="HSE Logo" />
          </Link>
          <ul className="nav-menu">
            <li className="nav-item"><Link to="/" className="nav-link">Главная</Link></li>
            <li className="nav-item"><Link to="/organisations" className="nav-link">Организации</Link></li>
            <li className="nav-item"><Link to="/publications" className="nav-link">Публикации</Link></li>
            <li className="nav-item"><Link to="/news" className="nav-link">Новости</Link></li>
            <li className="nav-item"><Link to="/projects" className="nav-link">Проекты</Link></li>
            <li className="nav-item"><Link to="/events" className="nav-link">События</Link></li>
          </ul>
          <div className="search-icon" onClick={toggleSearch}>
            <img src="/loopa.png" alt="Поиск" />
          </div>
          <div> <LanguageButton/> </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
