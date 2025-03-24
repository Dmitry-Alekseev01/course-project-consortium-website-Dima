import "./Organisations.css";
import React, { useEffect, useState } from "react";
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import { Link } from "react-router-dom";


const Organisations = () => {
  const [organisations, setOrganisations] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/organisations`)
      .then(response => response.json())
      .then(data => setOrganisations(data))
      .catch(error => console.error('Error fetching organisations:', error));
  }, []);

  return (
    <div className="aboutUs">
      <Navbar />
      <h1>Члены консорциума</h1>
      <div className="team">
        {organisations.map((organisation) => (
          <div key={organisation.id} className="teamMember">
            <Link to={organisation.link} ><img src={organisation.image}/></Link>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default Organisations;