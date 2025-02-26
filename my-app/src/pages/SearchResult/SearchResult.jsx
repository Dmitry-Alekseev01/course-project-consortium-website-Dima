// import React, { useEffect, useState } from "react";
// import "./SearchResult.css";
// import Navbar from "../../components/Navbar/Navbar";
// import Footer from "../../components/Footer/Footer";
// import SortButton from "../../components/SortButton/SortButton";
// import { useLocation, useHistory } from "react-router-dom";
// import AuthorFilter from "../../components/FilterButtonAuthors/FilterButtonAuthors";
// import MagazineFilter from "../../components/FilterButtonJournals/FilterButtonJournals";
// // import DateFilter from "../../components/FilterButtonDate/FilterButtonDate";

// const SearchResults = () => {
//   const location = useLocation();
//   const history = useHistory();
//   const queryParams = new URLSearchParams(location.search);
//   const query = queryParams.get("query");
//   const sortType = queryParams.get("sort");
//   const authors = queryParams.getAll("authors[]");
//   const magazines = queryParams.getAll("magazines[]");
//   const dateFrom = queryParams.get("dateFrom");
//   const dateTo = queryParams.get("dateTo");

//   const [searchResults, setSearchResults] = useState(null);
//   const [error, setError] = useState(null);
//   const [filters, setFilters] = useState({
//     authors: authors,
//     magazines: magazines,
//     dateFrom: dateFrom || '',
//     dateTo: dateTo || ''
//   });

//   const performSearch = async (query, sortType = null, filters = {}) => {
//     try {
//       const params = new URLSearchParams({
//         q: query,
//         ...(sortType && { sort: sortType }),
//         ...(filters.authors && { 'authors[]': filters.authors }),
//         ...(filters.magazines && { 'magazines[]': filters.magazines }),
//         ...(filters.dateFrom && { dateFrom: filters.dateFrom }),
//         ...(filters.dateTo && { dateTo: filters.dateTo })
//       });

//       const url = `http://127.0.0.1:5000/api/search?${params.toString()}`;
//       const response = await fetch(url);
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

//   useEffect(() => {
//     if (query) {
//       performSearch(query, sortType, filters);
//     }
//   }, [query, sortType, filters]);

//   const handleSort = (sortType) => {
//     const params = new URLSearchParams(location.search);
//     params.set("sort", sortType);
//     history.push({ search: params.toString() });
//   };

//   const handleAuthorFilter = (authors) => {
//     const params = new URLSearchParams(location.search);
//     params.delete("authors[]");
//     authors.forEach(author => params.append("authors[]", author));
//     history.push({ search: params.toString() });
//     setFilters(prev => ({ ...prev, authors }));
//   };

//   const handleMagazineFilter = (magazines) => {
//     const params = new URLSearchParams(location.search);
//     params.delete("magazines[]");
//     magazines.forEach(magazine => params.append("magazines[]", magazine));
//     history.push({ search: params.toString() });
//     setFilters(prev => ({ ...prev, magazines }));
//   };

//   const handleDateFilter = ({ dateFrom, dateTo }) => {
//     const params = new URLSearchParams(location.search);
//     params.set("dateFrom", dateFrom);
//     params.set("dateTo", dateTo);
//     history.push({ search: params.toString() });
//     setFilters(prev => ({ ...prev, dateFrom, dateTo }));
//   };


  

//   return (
//     <div>
//       <Navbar />
//       <div className="news-header">
//         <h2>Результаты поиска по запросу: "{query}"</h2>
//         <SortButton onSort={handleSort} />
//         <AuthorFilter onApply={handleAuthorFilter} />
//         <MagazineFilter onApply={handleMagazineFilter} />
//         {/* <DateFilter onApply={handleDateFilter} /> */}
//       </div>
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
//       <Footer />
//     </div>
//   );
// };

// export default SearchResults;





import React, { useEffect, useState } from "react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import SortButton from "../../components/SortButton/SortButton";
import { useLocation, useNavigate } from "react-router-dom";
import AuthorFilter from "../../components/FilterButtonAuthors/FilterButtonAuthors";
import MagazineFilter from "../../components/FilterButtonJournals/FilterButtonJournals";
// import DateFilter from "../../components/FilterButtonDate/FilterButtonDate";

const SearchResults = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const query = queryParams.get("query");
  const sortType = queryParams.get("sort");
  const authors = queryParams.getAll("authors[]");
  const magazines = queryParams.getAll("magazines[]");
  const dateFrom = queryParams.get("dateFrom");
  const dateTo = queryParams.get("dateTo");

  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    authors: authors,
    magazines: magazines,
    dateFrom: dateFrom || '',
    dateTo: dateTo || ''
  });

  const performSearch = async (query, sortType = null, filters = {}) => {
    try {
      const params = new URLSearchParams({
        q: query,
        ...(sortType && { sort: sortType }),
        ...(filters.authors && { 'authors[]': filters.authors }),
        ...(filters.magazines && { 'magazines[]': filters.magazines }),
        ...(filters.dateFrom && { dateFrom: filters.dateFrom }),
        ...(filters.dateTo && { dateTo: filters.dateTo })
      });

      const url = `http://127.0.0.1:5000/api/search?${params.toString()}`;
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
      performSearch(query, sortType, filters);
    }
  }, [query, sortType, filters]);

  const handleSort = (sortType) => {
    const params = new URLSearchParams(location.search);
    params.set("sort", sortType);
    navigate(`${location.pathname}?${params.toString()}`, { replace: true });
  };

  const handleAuthorFilter = (authors) => {
    const params = new URLSearchParams(location.search);
    params.delete("authors[]");
    authors.forEach(author => params.append("authors[]", author));
    navigate(`${location.pathname}?${params.toString()}`, { replace: true });
    setFilters(prev => ({ ...prev, authors }));
  };

  const handleMagazineFilter = (magazines) => {
    const params = new URLSearchParams(location.search);
    params.delete("magazines[]");
    magazines.forEach(magazine => params.append("magazines[]", magazine));
    navigate(`${location.pathname}?${params.toString()}`, { replace: true });
    setFilters(prev => ({ ...prev, magazines }));
  };

  const handleDateFilter = ({ dateFrom, dateTo }) => {
    const params = new URLSearchParams(location.search);
    params.set("dateFrom", dateFrom);
    params.set("dateTo", dateTo);
    navigate(`${location.pathname}?${params.toString()}`, { replace: true });
    setFilters(prev => ({ ...prev, dateFrom, dateTo }));
  };

  

  return (
    <div>
      <Navbar />
      <div className="news-header">
        <h2>Результаты поиска по запросу: "{query}"</h2>
        <SortButton onSort={handleSort} />
        <AuthorFilter onApply={handleAuthorFilter} />
        <MagazineFilter onApply={handleMagazineFilter} />
        {/* <DateFilter onApply={handleDateFilter} /> */}
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
      <Footer />
    </div>
  );
};

export default SearchResults;
