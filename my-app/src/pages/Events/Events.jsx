import React, {useContext, useEffect, useState } from "react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { Link } from "react-router-dom";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const Events = () => {
  const { language } = useContext(LanguageContext);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // fetch('http://127.0.0.1:5000/api/events')
    fetch(`${process.env.REACT_APP_API_URL}/events`)
      .then(response => response.json())
      .then(data => setEvents(data))
      .catch(error => console.error('Error fetching events:', error));
  }, []);

  return (
    <div className="page">
      <Navbar />
      <h1>{language === 'ru' ? 'События' : 'Events'}</h1>
      <div className="projects-list">
        {events.map((event) => (
          <div key={event.id} className="project">
            <h2>{event[`title_${language}`] || event.title}</h2>
            <p>{event[`description_${language}`] || event.description}</p>
            <p><strong>{language === 'ru' ? 'Дата проведения: ' : 'Date of the event : '}</strong> 
              {new Date(event.publication_date).toLocaleDateString(language === 'ru' ? 'ru-RU' : 'en-US')}
            </p>
            <p><strong>{language === 'ru' ? 'Место: ' : 'Place of the event: '}</strong> {event.location}</p>
            <Link to={`/events/${event.id}`} state={event} className="event-link">
                {language === 'ru' ? 'Подробнее' : 'Read more'}
            </Link>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default Events;