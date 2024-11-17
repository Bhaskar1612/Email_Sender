import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'; // Import your CSS file

function Home() {
  return (
    <div>
      <header className="title">Email-Sender</header>
    <div className='home-cont'>
      <h1 className="home-title">Welcome to Email Sender</h1>
      <div className="role-links">
        <Link to="/signin" className="role-link">SignIn</Link>
        <Link to="/signup" className="role-link">SignUp</Link>
      </div>
    </div>
    </div>
  );
}

export default Home;
