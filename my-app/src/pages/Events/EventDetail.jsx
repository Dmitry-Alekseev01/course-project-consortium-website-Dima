import React, { useContext, useEffect, useState } from "react";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";
import { useParams } from 'react-router-dom';
import ContactForm from '../../components/ContactForm/ContactForm';
import './EventDetail.css';
import '../../components/Footer/Footer.css'
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";

const EventDetails = () => {
  const { id } = useParams(); // Извлекаем id из URL
  const { language } = useContext(LanguageContext);
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Запрашиваем данные о событии с бэкенда по его ID
    // fetch(`http://127.0.0.1:5000/api/events/${id}`)
    fetch(`${process.env.REACT_APP_API_URL}/events/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Событие не найдено');
        }
        return response.json();
      })
      .then(data => {
        setEvent(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка при загрузке события:', error);
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

  if (!event) {
    return <div>Событие не найдено</div>;
  }

  return (
    <section className="event-detail">
      <Navbar />
      <div className="container">
        {/* <h2>{event.title}</h2>
        <p><strong>Дата проведения:</strong> {event.publication_date}</p>
        <p><strong>Место проведения:</strong> {event.location}</p>
        <p>{event.description}</p> */}
        {/* <h2>{event.title}</h2> */}
        <h2>{event[`title_${language}`] || event.title}</h2>
        {/* <p>{event.description}</p> */}
        <p>{event[`description_${language}`] || event.description}</p>
        {/* <p><strong>Дата:</strong> {event.date}</p>
        <p><strong>Время:</strong> {event.time}</p> */}
        {/* <p><strong>Дата проведения:</strong> {event.publication_date}</p> */}
        <p><strong>{language === 'ru' ? 'Дата проведения: ' : 'Date of the event : '}</strong> 
          {new Date(event.publication_date).toLocaleDateString(language === 'ru' ? 'ru-RU' : 'en-US')}
        </p>
        {/* <p><strong>Место:</strong> {event.location}</p> */}
        <p><strong>{language === 'ru' ? 'Место: ' : 'Place of the event: '}</strong> {event.location}</p>
        <ContactForm />
      </div>
      <Footer />
    </section>
  );
};

export default EventDetails;