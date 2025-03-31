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
        <h2>{event[`title_${language}`] || event.title}</h2>
        <p>{event[`description_${language}`] || event.description}</p>
        <p><strong>{language === 'ru' ? 'Дата проведения: ' : 'Date of the event : '}</strong> 
          {new Date(event.publication_date).toLocaleDateString(language === 'ru' ? 'ru-RU' : 'en-US')}
        </p>
        <p><strong>{language === 'ru' ? 'Место: ' : 'Place of the event: '}</strong> {event.location}</p>
        <ContactForm />
      </div>
      <Footer />
    </section>
  );
};

export default EventDetails;