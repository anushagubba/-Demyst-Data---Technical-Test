import React from 'react'
import { Link } from "react-router-dom";

import './App.css';

function App() {
  return (
    <div className="home-container">
      <h1 id="pageHeader" className="home-text">
        Simple Business Loan Application System
      </h1>
      <section className="App">
    </section>
    <div className="home-apply">
      <Link
        to="/LoanApplication"
        id="applicationButton"
        className="home-navlink button"
      >
        Apply for Loan
      </Link>
      </div>
    </div>
  )
}

export default App;
