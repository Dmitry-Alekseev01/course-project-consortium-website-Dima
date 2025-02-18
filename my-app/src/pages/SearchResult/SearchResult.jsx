import React, { useEffect, useState } from "react";
import "./SearchResult.css"
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import SortButton from "../../components/SortButton/SortButton";
import { useLocation } from "react-router-dom";

// const SearchResults = () => {
//   const location = useLocation();
//   const query = new URLSearchParams(location.search).get("query");
//   const [searchResults, setSearchResults] = useState(null);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     if (query) {
//       performSearch(query);
//     }
//   }, [query]);

//   const performSearch = async (query) => {
//     try {
//       const response = await fetch(`http://127.0.0.1:5000/api/search?q=${encodeURIComponent(query)}`);
//       if (!response.ok) {
//         throw new Error(`Ошибка сервера: ${response.status}`);
//       }
//       const data = await response.json();
//       setSearchResults(data);
//       setError(null);
//     } catch (err) {
//       console.error("Ошибка при поиске:", err);
//       setError("Ошибка загрузки результатов поиска");
//     }
//   };

//   return (
//     <div>
//       <Navbar/>
//       <h2>Результаты поиска по запросу: "{query}"</h2>
//       {error && <p className="error-message">{error}</p>}
//       {searchResults ? (
//         Object.keys(searchResults).map((category) =>
//           searchResults[category].length > 0 ? (
//             <div key={category}>
//               <h4>{category.toUpperCase()}</h4>
//               <ul>
//                 {searchResults[category].map((item) => (
//                   <li key={item.id}>
//                     <a href={item.link || "#"}>{item.title}</a>
//                   </li>
//                 ))}
//               </ul>
//             </div>
//           ) : null
//         )
//       ) : (
//         <p>Загрузка...</p>
//       )}
//       <SortButton/>
//       <Footer/>
//     </div>
//   );
// };

// export default SearchResults;


const SearchResults = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("query");
  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);

  const performSearch = async (query, sortType = null) => {
    try {
      const url = `http://127.0.0.1:5000/api/search?q=${encodeURIComponent(query)}${sortType ? `&sort=${sortType}` : ''}`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }
      const data = await response.json();
      setSearchResults(data);
      setError(null);
    } catch (err) {
      console.error("Ошибка при поиске:", err);
      setError("Ошибка загрузки результатов поиска");
    }
  };

  useEffect(() => {
    if (query) {
      performSearch(query);
    }
  }, [query]);

  const handleSort = (sortType) => {
    performSearch(query, sortType);
  };

  return (
    <div>
      <Navbar/>
      <div className="news-header">
      <h2>Результаты поиска по запросу: "{query}"</h2>
        <SortButton onSort={handleSort} />
      </div>
      {error && <p className="error-message">{error}</p>}
      {searchResults ? (
        Object.keys(searchResults).map((category) =>
          searchResults[category].length > 0 ? (
            <div key={category}>
              <h4>{category.toUpperCase()}</h4>
              <ul>
                {searchResults[category].map((item) => (
                  <li key={item.id}>
                    <a href={item.link || "#"}>{item.title}</a>
                  </li>
                ))}
              </ul>
            </div>
          ) : null
        )
      ) : (
        <p>Загрузка...</p>
      )}
      <Footer/>
    </div>
  );
};

export default SearchResults;