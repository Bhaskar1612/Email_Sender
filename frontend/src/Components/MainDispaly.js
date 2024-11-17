// src/components/MainDisplay.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import './MainDisplay.css';

const MainDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [emails, setEmails] = useState([]);
  const [emailStats, setEmailStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const user = location.state?.user || {}; // Retrieve user info from state


  useEffect(() => {
    const fetchEmails = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/emails", {
          params: { email: user.email },
        });
        setEmails(response.data);
      } catch (error) {
        console.error("Error fetching emails", error);
      }
    };

    const fetchEmailStats = async (email) => {
      try {
        setLoading(true);
        console.log(email)
        const response = await axios.get(
        `http://localhost:8000/email_stats/`,
        {
          params: { email },
        }
        );

      setEmailStats(response.data);
      } catch (err) {
      console.error("Failed to fetch email stats. Please try again.");
      } finally {
      setLoading(false);
      }
    };

    if (user.email) {
      fetchEmails();
      fetchEmailStats(user.email);
    }
  }, [user.email]);

  

  const handleSendViaGmail = async () => {
  try {
    // Step 1: Check if Gmail permissions are already granted
    const checkResponse = await axios.get("http://127.0.0.1:8000/check_gmail", {
      params: { email: user.email }, // Pass the user's email as a query parameter
    });

    if (checkResponse.data === true) {
      // Navigate to Gmail page if permission is already granted
      navigate("/gmail", { state: { user } });
    } else {
      // Direct the user to the authorization URL
      window.open(`http://localhost:8000/start-auth?email=${user.email}`, "_blank");

      // Step 3: Show an alert once the user completes authorization
      alert("Email verified. Click 'Send via Gmail' again to access Gmail page.");
    }
  } catch (error) {
    console.error("Error in Gmail permission flow:", error);
    alert("An error occurred. Please try again.");
  }
  };

    const handleSendViaSendGrid = async () => {
  try {
    // Step 1: Check if Gmail permissions are already granted
    const checkResponse = await axios.get("http://127.0.0.1:8000/check_sendgrid", {
      params: { email: user.email }, // Pass the user's email as a query parameter
    });

    if (checkResponse.data === true) {
      navigate("/sendgrid", { state: { user } });
    } else {
      navigate("/sendgrid-api", { state: { user } });
    }
  } catch (error) {
    console.error("Error in Gmail permission flow:", error);
    alert("An error occurred. Please try again.");
  }
  };

 

  return (
    <div className="main-display">
      <h2>Welcome, {user.username}!</h2>
      <p><strong>Email: {user.email}</strong></p>

      {loading && <p>Loading email statistics...</p>}

      {emailStats && (
        <div> 
          <p><strong>Total Emails:</strong> - {emailStats.total_count},<strong>Pending Emails:</strong> - {emailStats.pending_count}, <strong>Failed Emails:</strong> - {emailStats.failed_count}, <strong>Sent Emails:</strong> - {emailStats.sent_count}</p>
        </div>
      )}
      <p> . </p>

      <h3>Your Sent Emails</h3>
      <table>
        <thead>
          <tr>
            <th>Index</th>
            <th>Recipient</th>
            <th>Content</th>
            <th>Send Time</th>
            <th>Send Status</th>
            <th>Delivery Status</th>
            <th>ESP</th>
          </tr>
        </thead>
        <tbody>
          {emails.map((email,index) => (
            <tr key={email.id}>
              <td>{index+1}</td>
              <td>{email.recipient_email}</td>
              <td>{email.body}</td>
              <td>{new Date(email.send_time).toLocaleString()}</td>
              <td>{email.send_status}</td>
              <td>{email.delivery_status}</td>
              <td>{email.esp}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="send-options">
        <button onClick={handleSendViaGmail}>Send via Gmail</button>
        <button onClick={handleSendViaSendGrid}>Send by SendGrid</button>
      </div>
    </div>
  );
};

export default MainDisplay;
