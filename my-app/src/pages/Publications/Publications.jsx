import React, { useContext, useEffect, useState } from "react";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { Link } from "react-router-dom";

const Publications = () => {
  const { language } = useContext(LanguageContext);
  const [publications, setPublications] = useState([]);

  useEffect(() => {
    const fetchPublications = async () => {
      try {
        const response = await fetch ("http://94.158.219.154:5000/api/publications")//await fetch('http://127.0.0.1:5000/api/publications');
        const data = await response.json();
        setPublications(data);
      } catch (error) {
        console.error('Error fetching publications:', error);
      }
    };
    fetchPublications();
  }, []);

  const formatAuthors = (authors) => {
    return authors.map(author => {
      const firstName = author[`first_name_${language}`] || author.first_name;
      const lastName = author[`last_name_${language}`] || author.last_name;
      return `${firstName} ${lastName}`;
    }).join(', ');
  };

  return (
    <div className="page">
      <Navbar />
      <h1>{language === 'ru' ? 'Публикации' : 'Publications'}</h1>
      <div className="projects-list">
        {publications.map((publication) => (
          <div key={publication.id} className="project">
            <h2>{publication[`title_${language}`] || publication.title}</h2>
            <p><strong>{language === 'ru' ? 'Авторы: ' : 'Authors: '}</strong> {formatAuthors(publication.authors)}</p>
            <p><strong>{language === 'ru' ? 'Дата публикации: ' : 'Publication Date: '}</strong> 
              {new Date(publication.publication_date).toLocaleDateString(language === 'ru' ? 'ru-RU' : 'en-US')}
            </p>
            {publication.magazine && (
              <p><strong>{language === 'ru' ? 'Журнал: ' : 'Journal: '}</strong> 
                {publication.magazine[`name_${language}`] || publication.magazine.name}
              </p>
            )}
            <p><strong>{language === 'ru' ? 'Описание: ' : 'Abstract: '}</strong> 
              {publication[`annotation_${language}`] || publication.annotation}
            </p>
            <Link 
              to={`/publications/${publication.id}`} 
              state={publication} 
              className="publication-link"
            >
              {language === 'ru' ? 'Подробнее' : 'Read more'}
            </Link>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default Publications;