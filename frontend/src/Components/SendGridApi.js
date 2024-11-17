import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import axios from "axios";
import "./SendGridApi.css";

const SendGridApi = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [apiKey, setApiKey] = useState("");
  const [message, setMessage] = useState("");
  const user = location.state?.user || {}; // Retrieve user info from state

  const handleApiKeySubmit = async (e) => {
    e.preventDefault();
    console.log(user);
    try {
    const response = await axios.post("http://127.0.0.1:8000/add_sendgrid", null, {
    params: {
        email: user.email,
        sendgrid_api_key: apiKey,
    },
    });

      if (response.status === 200) {
        setMessage("API Key added successfully!");
        setTimeout(() => {
          navigate("/sendgrid", { state: { user } });
        }, 2000); // Navigate after showing the success message
      }
    } catch (error) {
      setMessage("Error adding API Key. Please try again.");
    }
  };

  return (
    <div className="sendgrid-api-container">
      <h1>Connect Your SendGrid Account</h1>
      <p>Please provide your SendGrid API Key to integrate with the application.</p>
      <form onSubmit={handleApiKeySubmit}>
        <label htmlFor="apiKey">SendGrid API Key:</label>
        <input
          type="text"
          id="apiKey"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          required
        />
        <button type="submit">Submit</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default SendGridApi;
