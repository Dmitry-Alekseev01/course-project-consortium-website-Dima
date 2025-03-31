import React, {useContext} from 'react';
import './Contacts.css';
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const Contacts = () => {
  const { language } = useContext(LanguageContext);

  const address = encodeURIComponent("Покровский бульвар, 11С10");
  const mapUrl = `https://www.google.com/maps/search/?api=1&query=${address}`;
  
  return (
    <div className="contact-field" id="contacts">
      <h2>{language === 'ru' ? "Контакты" : "Contacts"}</h2>
      <div className="contact-info">
        <div className="contact-item">
          <img src="/telephone.png" alt='telephone'/>
          <a href="tel:+7 (916) 216-79-87" className="contact-link">+7 (916) 216-79-87</a>
        </div>
        <div className="contact-item">
          <img src="/mail_icon.png" alt='mail icon'/>
          <a href="mailto:frtg1123456@gmail.com" className="contact-link">frtg1123456@gmail.com</a>
        </div>
        <div className="contact-item">
          <img src="/geo_pos.png" alt='geo_pos'/>
          <a 
            href={mapUrl} 
            className="contact-link"
            target="_blank" 
            rel="noopener noreferrer">
            Покровский бульвар, 11С10          
          </a>
        </div>
      </div>
    </div>
  );
};

export default Contacts;