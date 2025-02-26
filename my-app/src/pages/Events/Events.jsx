import React, { useEffect, useState } from "react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { Link } from "react-router-dom";

const Events = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/events')
      .then(response => response.json())
      .then(data => setEvents(data))
      .catch(error => console.error('Error fetching events:', error));
  }, []);

  return (
    <div className="page">
      <Navbar />
      <h1>События</h1>
      <div className="projects-list">
        {events.map((event) => (
          <div key={event.id} className="project">
            <h2>{event.title}</h2>
            <p>{event.description}</p>
            {/* <p><strong>Дата:</strong> {event.date}</p>
            <p><strong>Время:</strong> {event.time}</p> */}
            <p><strong>Дата проведения:</strong> {event.publication_date}</p>
            <p><strong>Место:</strong> {event.location}</p>
            <Link to={`/events/${event.id}`} state={event} className="event-link">
              Подробнее
            </Link>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default Events;