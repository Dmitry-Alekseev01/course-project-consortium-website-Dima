import React, {useContext } from 'react';
import './Footer.css';
import { Link } from "react-router-dom";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const Footer = () => {
    const { language } = useContext(LanguageContext);
    

    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-section">
                    <h2>{language === 'ru' ? 'Кардиогенетика' : 'Cardiogenetics'}</h2>
                    {/* <p>Ваш надежный источник информации о кардиогенетике. Мы здесь, чтобы помочь вам разобраться в сложных вопросах!</p> */}
                    <p>{language === 'ru' ? 'Ваш надежный источник информации о кардиогенетике. Мы здесь, чтобы помочь вам разобраться в сложных вопросах!' : 'Your reliable source of information about cardiogenetics. We are here to help you figure out difficult issues!'}</p>
                    <Link to="#" className="btn-primary">{language === 'ru' ? 'Узнать больше' : 'Read more'}</Link>
                </div>
                <div className="footer-section">
                    <ul>
                        <li>{language === 'ru' ? 'Поддержка' : 'Support'}</li>
                        <li>{language === 'ru' ? 'О нас' : 'About us'}</li>
                        <li>{language === 'ru' ? 'Контакты' : 'Contacts'}</li>
                    </ul>
                </div>
            </div>
            <div className="footer-bottom">
                {/* <p>© 2024 Кардиогенетика. Все права защищены.</p> */}
                <p>{language === 'ru' ? '© 2024 Кардиогенетика. Все права защищены.' : '© 2024 Cardiogenetics. All rights reserved.'}</p>
            </div>
        </footer>
    );
};

export default Footer;
