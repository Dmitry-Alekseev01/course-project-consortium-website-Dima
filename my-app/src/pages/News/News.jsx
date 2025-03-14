import React, { useContext, useEffect, useState } from "react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";
import { Link } from "react-router-dom";


const News = () => {
  const { language } = useContext(LanguageContext);
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/news')
      .then((response) => response.json())
      .then((data) => setNews(data))
      .catch((error) => console.error('Ошибка при загрузке новостей:', error));
  }, []);

  const formatAuthors = (authors) => {
    return authors.map(author => {
      const firstName = author[`first_name_${language}`] || author.first_name;
      const lastName = author[`last_name_${language}`] || author.last_name;
      return `${firstName} ${lastName}`;
    }).join(', ');
  };

  const getFileType = (fileName) => {
    const extension = fileName.split(".").pop().toLowerCase();
    if (["jpg", "jpeg", "png", "gif"].includes(extension)) {
      return "image";
    } else if (["mp3", "wav"].includes(extension)) {
      return "audio";
    } else if (extension === "pdf") {
      return "pdf";
    } else {
      return "unknown";
    }
  };

  const renderFile = (fileUrl) => {
    const fileType = getFileType(fileUrl);

    switch (fileType) {
      case "image":
        return <img src={fileUrl} alt="Материалы" style={{ maxWidth: "100%", height: "auto" }} />;
      case "audio":
        return (
          <audio controls>
            <source src={fileUrl} type={`audio/${fileUrl.split(".").pop()}`} />
            Ваш браузер не поддерживает аудио.
          </audio>
        );
      case "pdf":
        return (
          <a href={fileUrl} download>
            Скачать PDF
          </a>
        );
      default:
        return (
          <a href={fileUrl} download>
            Скачать файл
          </a>
        );
    }
  };

  return (
    <div className="page">
      <Navbar />
      <h1>{language === 'ru' ? 'Новости' : 'News'}</h1>
      <div className="projects-list">
        {news.map((news) => (
          <div key={news.id} className="project">
            {/* <h2>{news.title}</h2> */}
            <h2>{news[`title_${language}`] || news.title}</h2>
            {/* <p><strong>Авторы:</strong> {news.authors.join(', ')}</p>
            <p><strong>Дата публикации:</strong> {news.publication_date}</p> */}
            <p><strong>{language === 'ru' ? 'Авторы: ' : 'Authors: '}</strong> {formatAuthors(news.authors)}</p>
            <p><strong>{language === 'ru' ? 'Дата публикации: ' : 'Publication Date: '}</strong> 
              {new Date(news.publication_date).toLocaleDateString(language === 'ru' ? 'ru-RU' : 'en-US')}
            </p>
            {/* <p><strong>Описание:</strong> {news.description}</p> */}
            <p><strong>{language === 'ru' ? 'Описание: ' : 'Abstract: '}</strong> 
              {news[`description_${language}`] || news.description}
            </p>
            <p>
            {news.magazine && (
              <p><strong>{language === 'ru' ? 'Журнал: ' : 'Journal: '}</strong> 
                {news.magazine[`name_${language}`] || news.magazine.name}
              </p>
            )}
            </p>
            {/* <p><strong>Журнал:</strong> {news.magazine.name || "Не издавалась"}</p> */}
            <p><strong>Текст:</strong> {news.content}</p>
            <p>
              <strong>Материалы:</strong>{" "}
              {news.materials ? renderFile(`http://127.0.0.1:5000${news.materials}`) : "Файл отсутствует"}
            </p>
            <Link to={`/news/${news.id}`} state={news} className="news-link">
              Подробнее
            </Link>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default News;