import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../Events/EventDetail.css';
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { Link } from "react-router-dom";

const NewsDetails = () => {
  const { id } = useParams();
  const [news, setNews] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // fetch(`http://127.0.0.1:5000/api/news/${id}`)
    fetch(`${process.env.REACT_APP_API_URL}/news/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Новость не найдена');
        }
        return response.json();
      })
      .then(data => {
        setNews(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка при загрузке новости:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>Ошибка: {error}</div>;
  }

  if (!news) {
    return <div>Новость не найдена</div>;
  }

  return (
    <section className="event-detail">
      <Navbar />
      <div className="container">
        <h2>{news.title}</h2>
        <p><strong>Авторы:</strong> {news.authors.join(', ')}</p>
        <p><strong>Дата публикации:</strong> {news.publication_date}</p>
        <p><strong>Описание:</strong> {news.description}</p>
        <p><strong>Журнал:</strong> {news.magazine.name || "Не указан"}</p>
        <p><strong>Текст:</strong> {news.content}</p>
        {news.materials && (
          <p>
            <strong>Материалы:</strong>{" "}
            <Link to={`/uploads/${news.materials}`} download>
              Скачать
            </Link>
          </p>
        )}
      </div>
      <Footer />
    </section>
  );
};

export default NewsDetails;