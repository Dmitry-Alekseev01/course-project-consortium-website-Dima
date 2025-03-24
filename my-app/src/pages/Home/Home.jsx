import MapSection from "../../components/MapSection/MapSection";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import ContactForm from "../../components/ContactForm/ContactForm";
import Contacts from "../../components/Contacts/Contacts"
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";
import React, {useContext, useEffect, useState } from "react";

const Home = () => {
  const { language } = useContext(LanguageContext);

  return (
    <div>
      <Navbar />
      <div className="page"> 
      {/* <h1>Добро пожаловать на сайт</h1> */}
      <h1>{language === 'ru' ? 'Добро пожаловать на сайт' : 'Welcome to site'}</h1>
      </div>
      <MapSection/>
      <Contacts/>
      <ContactForm/>
      <Footer />
    </div>
  );
};

export default Home;