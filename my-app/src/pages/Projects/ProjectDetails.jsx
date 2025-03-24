import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../Events/EventDetail.css';
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { Link } from "react-router-dom";

const ProjectDetails = () => {
  const { id } = useParams(); // Извлекаем id из URL
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Запрашиваем данные о проекте с бэкенда по его ID
    fetch(`${process.env.REACT_APP_API_URL}/projects/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Проект не найден');
        }
        return response.json();
      })
      .then(data => {
        setProject(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка при загрузке проекта:', error);
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

  if (!project) {
    return <div>Проект не найден</div>;
  }

  return (
    <section className="event-detail">
      <Navbar />
      <div className="container">
        <h2>{project.title}</h2>
        <p><strong>Дата публикации:</strong> {project.publication_date}</p>
        <p><strong>Описание:</strong> {project.description}</p>
        <p><strong>Содержание:</strong> {project.content}</p>
        {project.materials && (
          <p>
            <strong>Материалы:</strong>{" "}
            <Link to={`/uploads/${project.materials}`} download>
              Скачать
            </Link>
          </p>
        )}
      </div>
      <Footer />
    </section>
  );
};

export default ProjectDetails;