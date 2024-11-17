// src/components/SignIn.js
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import "./SignIn.css"; // Import the CSS file

const SignIn = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Initialize navigate hook

  const handleSignIn = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/login", {
        email,
        password,
      });

      const token = response.data.access_token;
      const user = {
        username: response.data.username, // Assuming the backend returns username
        email: response.data.email,       // and email in the response
      };

      localStorage.setItem("token", token); // Store the token in local storage
      setMessage("Sign-in successful!");
      console.log(user);
      setTimeout(() => {
        navigate("/main-display", { state: { user } });
      }, 2000);
      // Navigate to MainDisplay and pass the user info as state
    } catch (error) {
      setMessage("Error signing in. Please check your credentials.");
    }
  };

  return (
    <div className="form-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSignIn}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="form-input"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="form-input"
        />
        <button type="submit" className="form-button">Sign In</button>
      </form>
      {message && <p className="form-message">{message}</p>}
    </div>
  );
};

export default SignIn;
