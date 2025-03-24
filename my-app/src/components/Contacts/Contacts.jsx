import React, {useContext} from 'react';
import './Contacts.css';
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const Contacts = () => {
  const { language } = useContext(LanguageContext);
  
  return (
    <div className="contact-field" id="contacts">
      <h2>{language === 'ru' ? "Контакты" : "Contacts"}</h2>
      <div className="contact-info">
        <div className="contact-item">
          <i className="icon-phone"></i>
          {/* <i src="/telephone.jpg"/> */}
          <p>+7 123 456 7890</p>
        </div>
        <div className="contact-item">
          <i className="icon-email"></i>
          {/* <i src="/mail_icon.png"/> */}
          <p>info@cardiogenetics.ru</p>
        </div>
        <div className="contact-item">
          <i className="icon-location"></i>
          {/* <i src="/geo_pos.jpg"/> */}
          <p>Russian Federation</p>
        </div>
      </div>
    </div>
  );
};

export default Contacts;
