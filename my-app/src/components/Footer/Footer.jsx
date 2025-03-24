import React from 'react';
import './Footer.css';
import { Link } from "react-router-dom";

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-section">
                    <h2>Кардиогенетика</h2>
                    <p>Ваш надежный источник информации о кардиогенетике. Мы здесь, чтобы помочь вам разобраться в сложных вопросах!</p>
                    <Link to="#" className="btn-primary">Узнать больше</Link>
                </div>
                <div className="footer-section">
                    <ul>
                        <li>Поддержка</li>
                        <li>О нас</li>
                        <li>Контакты</li>
                    </ul>
                </div>
            </div>
            <div className="footer-bottom">
                <p>© 2024 Кардиогенетика. Все права защищены.</p>
            </div>
        </footer>
    );
};

export default Footer;
