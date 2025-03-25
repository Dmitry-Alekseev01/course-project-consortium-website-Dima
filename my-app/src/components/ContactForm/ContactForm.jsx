// import React, {useContext, useState } from 'react';
// import './ContactForm.css'
// import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

// const ContactForm = () => {
//   const [formData, setFormData] = useState({
//     name: '',
//     email: '',
//     phone: '',
//     company: '',
//     message: '',
//   });

//   const { language } = useContext(LanguageContext);
//   const [status, setStatus] = useState(null);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setFormData({ ...formData, [name]: value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setStatus('sending');

//     try {
//       // fetch(`${process.env.REACT_APP_API_URL}/news`)
//       const response = await fetch(`${process.env.REACT_APP_API_URL}/contact`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(formData),
//       });

//       if (response.ok) {
//         setStatus('success');
//         setFormData({ name: '', email: '', phone: '', company: '', message: '' });
//       } else {
//         setStatus('error');
//       }
//     } catch (error) {
//       setStatus('error');
//     }
//   };

//   return (
//     <section className="contact-form-section">
//       <div className="container">
//         <div className="row">
//           <div className="col-lg-6 form-wrapper">
//             {/* <h2>Свяжитесь с нами</h2> */}
//             <h2>{language === 'ru' ? 'Свяжитесь с нами' : 'Connect to us'}</h2>
//             {/* <p>Мы всегда рады вашим вопросам и предложениям. Напишите нам, и мы ответим в кратчайшие сроки!</p> */}
//             <p>{language === 'ru' ? 'Мы всегда рады вашим вопросам и предложениям. Напишите нам, и мы ответим в кратчайшие сроки!' : 'We always welcome your questions and suggestions. Write to us and we will respond as soon as possible!'}</p>
//             <form onSubmit={handleSubmit} className="contact-form">
//               <input
//                 type="text"
//                 name="name"
//                 placeholder={language === 'ru' ? "Имя" : "Name"}
//                 value={formData.name}
//                 onChange={handleChange}
//                 required
//               />
//               <input
//                 type="email"
//                 name="email"
//                 placeholder="Email"
//                 value={formData.email}
//                 onChange={handleChange}
//                 required
//               />
//               <input
//                 type="text"
//                 name="phone"
//                 placeholder={language === 'ru' ? "Телефон" : "Telephone"}
//                 value={formData.phone}
//                 onChange={handleChange}
//                 required
//               />
//               <input
//                 type="text"
//                 name="company"
//                 placeholder={language === 'ru' ? "Компания" : "Company"}
//                 value={formData.company}
//                 onChange={handleChange}
//               />
//               <textarea
//                 name="message"
//                 placeholder={language === 'ru' ? "Сообщение" : "Message"}
//                 value={formData.message}
//                 onChange={handleChange}
//                 required
//               ></textarea>
//               <button type="submit" className="btn-submit">{language === 'ru' ? "Отправить" : "Send"}</button>
//             </form>
//             {status === 'success' && <p className="success">{language === 'ru' ? "Сообщение отправлено!" : "Message is sent!"}</p>}
//             {status === 'error' && <p className="error">{language === 'ru' ? "Ошибка при отправке. Попробуйте позже." : "Sending error. Retry later."}</p>}
//           </div>
//           <div className="col-lg-6">
//             <h3>{language === 'ru' ? "Наш адрес" : "Our address"}</h3>
//             <p>Russian Federation</p>
//             <p>info@cardiogenetics.ru</p>
//             <p>+7 123 456 7890</p>
//           </div>
//         </div>
//       </div>
//     </section>
//   );
// };

// export default ContactForm;


import React, { useContext, useState, useRef } from 'react';
import ReCAPTCHA from 'react-google-recaptcha';
import './ContactForm.css';
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";

const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    message: '',
  });

  const { language } = useContext(LanguageContext);
  const [status, setStatus] = useState(null);
  const [captchaVerified, setCaptchaVerified] = useState(false);
  const captchaRef = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCaptchaChange = (token) => {
    setCaptchaVerified(!!token);
    if (status === 'captcha_error') setStatus(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!captchaVerified) {
      setStatus('captcha_error');
      return;
    }

    setStatus('sending');
    
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          captcha: captchaRef.current.getValue()
        }),
      });

      if (response.ok) {
        setStatus('success');
        setFormData({ 
          name: '', 
          email: '', 
          phone: '', 
          company: '', 
          message: '' 
        });
        captchaRef.current.reset();
        setCaptchaVerified(false);
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('error');
    }
  };

  return (
    <section className="contact-form-section">
      <div className="container">
        <div className="row">
          <div className="col-lg-6 form-wrapper">
            <h2>{language === 'ru' ? 'Свяжитесь с нами' : 'Contact Us'}</h2>
            <p>{language === 'ru' 
              ? 'Мы всегда рады вашим вопросам и предложениям. Напишите нам, и мы ответим в кратчайшие сроки!' 
              : 'We always welcome your questions and suggestions. Write to us and we will respond as soon as possible!'}
            </p>
            
            <form onSubmit={handleSubmit} className="contact-form">
              <input
                type="text"
                name="name"
                placeholder={language === 'ru' ? "Имя" : "Name"}
                value={formData.name}
                onChange={handleChange}
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <input
                type="tel"
                name="phone"
                placeholder={language === 'ru' ? "Телефон" : "Phone"}
                value={formData.phone}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="company"
                placeholder={language === 'ru' ? "Компания" : "Company"}
                value={formData.company}
                onChange={handleChange}
              />
              <textarea
                name="message"
                placeholder={language === 'ru' ? "Сообщение" : "Message"}
                value={formData.message}
                onChange={handleChange}
                required
              ></textarea>

              <ReCAPTCHA
                ref={captchaRef}
                sitekey="6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" // Тестовый ключ
                onChange={handleCaptchaChange}
                hl={language}
                className="g-recaptcha"
              />

              {status === 'captcha_error' && (
                <p className="error-message">
                  {language === 'ru' 
                    ? "Пожалуйста, подтвердите, что вы не робот" 
                    : "Please verify that you're not a robot"}
                </p>
              )}

              <button 
                type="submit" 
                className="btn-submit"
                disabled={status === 'sending'}
              >
                {status === 'sending' 
                  ? (language === 'ru' ? "Отправка..." : "Sending...") 
                  : (language === 'ru' ? "Отправить" : "Send")}
              </button>

              {status === 'success' && (
                <p className="success-message">
                  {language === 'ru' 
                    ? "Сообщение успешно отправлено!" 
                    : "Message sent successfully!"}
                </p>
              )}

              {status === 'error' && (
                <p className="error-message">
                  {language === 'ru' 
                    ? "Ошибка при отправке. Пожалуйста, попробуйте позже." 
                    : "Sending error. Please try again later."}
                </p>
              )}
            </form>
          </div>

          <div className="col-lg-6">
            <h3>{language === 'ru' ? "Наши контакты" : "Our Contacts"}</h3>
            <p>Russian Federation</p>
            <p>info@example.com</p>
            <p>+7 123 456 7890</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactForm;