import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Home from "../pages/Home/Home";
import Events from "../pages/Events/Events";
import EventDetails from "../pages/Events/EventDetail";
import News from "../pages/News/News";
import Publications from "../pages/Publications/Publications";
import NoPage from "../pages/NoPage/NoPage";
import Projects from "../pages/Projects/Projects";
import Organisations from "../pages/Organisations/Organisations";
import SearchResults from "../pages/SearchResult/SearchResult";
import NewsDetails from "../pages/News/NewsDetails";
import PublicationDetails from "../pages/Publications/PublicationDetails";
import ProjectDetails  from "../pages/Projects/ProjectDetails";

const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/events" element={<Events />} />
      <Route path="/events/:id" element={<EventDetails />} />
      <Route path="/organisations" element={<Organisations />} />
      <Route path="/news" element={<News />} />
      <Route path="/publications" element={<Publications />} />
      <Route path="/projects" element={<Projects />} />
      <Route path="/notFound" element={<NoPage />} />
      <Route path="/search" element={<SearchResults />} />
      <Route path="*" element={<Navigate to="/notFound" />} />
      <Route path="/news/:id" element={<NewsDetails />} />
      <Route path="/publications/:id" element={<PublicationDetails />} />
      <Route path="/projects/:id" element={<ProjectDetails />} />
    </Routes>
  );
};

export default AppRouter;