import React from "react";
import './styles/Loader.css';   

export default function Loader() {
  return (
    <div className="loader-container">
      <div className="loader"></div>
      <p className="loader-text">Crunching your numbers...</p>
    </div>
  );
}
