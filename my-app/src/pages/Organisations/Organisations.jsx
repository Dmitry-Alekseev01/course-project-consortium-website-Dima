import "./Organisations.css";
import React, {useContext, useEffect, useState } from "react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { Link } from "react-router-dom";
import { LanguageContext } from "../../components/LanguageContext/LanguageContext";



const Organisations = () => {
  const { language } = useContext(LanguageContext);
  const [organisations, setOrganisations] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/organisations`)
      .then(response => response.json())
      .then(data => setOrganisations(data))
      .catch(error => console.error('Error fetching organisations:', error));
  }, []);

  const getFileType = (fileName) => {
    const extension = fileName.split(".").pop().toLowerCase();
    if (["jpg", "jpeg", "png", "gif"].includes(extension)) {
      return "image";
    } 
  };


  const renderFile = (fileUrl) => {
    const fileType = getFileType(fileUrl);

    switch (fileType) {
      case "image":
        return <img src={fileUrl} alt="Материалы" style={{ maxWidth: "100%", height: "auto" }} />;
    }
  };
  

  return (
    <div className="aboutUs">
      <Navbar />
      <h1>{language === 'ru' ? 'Члены консорциума' : 'Consortium members'}</h1>
      <div className="team">
        {organisations.map((organisation) => (
          <div key={organisation.id} className="teamMember">
            <Link to={organisation.link}><img src={renderFile(`${process.env.REACT_APP_API_URL}${encodeURIComponent(organisation.image)}`)}/> {/* <img src={organisation.image}/>*/}</Link> 
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default Organisations;