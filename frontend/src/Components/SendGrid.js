import React, { useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import "./SendGrid.css"; // Import the CSS file

const SendGrid = () => {
  const location = useLocation();
  const user = location.state?.user || {}; // Retrieve user info from state
  const [singleEmail, setSingleEmail] = useState({
    recipient: "",
    subject: "",
    send_time: "",
    name:"",
    company_name:"",
    template:""
  });
  const [csvFile, setCsvFile] = useState(null);
  const [spreadsheetDetails, setSpreadsheetDetails] = useState({
    spreadsheet_id: "",
    range_name: "",
  });
  const [message, setMessage] = useState("");

  // Handle Add Email
  const handleAddEmail = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/add_email", {
        sender: user.email,
        esp: "sendgrid",
        ...singleEmail,
      });
      setMessage("Email added successfully!");
    } catch (error) {
      setMessage("Error adding email. Please try again.");
    }
  };

  // Handle Upload CSV
  const handleUploadCSV = async (e) => {
    e.preventDefault();
    if (!csvFile) {
      setMessage("Please select a CSV file to upload.");
      return;
    }
    console.log(user);
    const formData = new FormData();
    formData.append("file", csvFile); // Add the file
    formData.append("sender", user.email); // Add the sender
    formData.append("esp", "sendgrid"); 

    try {
      await axios.post("http://127.0.0.1:8000/upload_csv", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("CSV uploaded successfully!");
    } catch (error) {
      setMessage("Error uploading CSV. Please try again.");
    }
};

  // Handle Import Google Sheet
  const handleImportGoogleSheet = async (e) => {
   e.preventDefault();
  
   // Validate input fields
   if (!spreadsheetDetails.spreadsheet_id || !spreadsheetDetails.range_name) {
    setMessage("Please fill in all fields.");
    return;
   }


    const formData = new FormData();
    formData.append("sender", user.email); // Add sender
    formData.append("esp", "sendgrid"); // Add ESP
    formData.append("spreadsheet_id", spreadsheetDetails.spreadsheet_id); // Spreadsheet ID
    formData.append("range_name", spreadsheetDetails.range_name);

   try {
    const response = await axios.post("http://127.0.0.1:8000/import_google_sheet", formData);
    setMessage("Google Sheet imported successfully!");
   } catch (error) {
    console.error("Error importing Google Sheet:", error);
    setMessage("Error importing Google Sheet. Please try again.");
   }
};

  return (
    <div className="reply-to-page">
      <h2>SendGrid Emails</h2>
      <p>
        Send emails using a SendGrid esp tool. While also getting constant status of the email.
      </p>

      {message && <p className="message">{message}</p>}

      <div className="section">
        <h3>Add a Single Email</h3>
        <form onSubmit={handleAddEmail}>
          <input
            type="text"
            placeholder="Recipient"
            value={singleEmail.recipient}
            onChange={(e) => setSingleEmail({ ...singleEmail, recipient: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Subject"
            value={singleEmail.subject}
            onChange={(e) => setSingleEmail({ ...singleEmail, subject: e.target.value })}
            required
          />
          <textarea
            placeholder="Name"
            value={singleEmail.name}
            onChange={(e) => setSingleEmail({ ...singleEmail, name: e.target.value })}
            required
          />
          <textarea
            placeholder="Company_Name"
            value={singleEmail.company_name}
            onChange={(e) => setSingleEmail({ ...singleEmail, company_name: e.target.value })}
            required
          />
          <textarea
            placeholder="Template"
            value={singleEmail.template}
            onChange={(e) => setSingleEmail({ ...singleEmail, template: e.target.value })}
            required
          />
          <input
            type="datetime-local"
            value={singleEmail.send_time}
            onChange={(e) => setSingleEmail({ ...singleEmail, send_time: e.target.value })}
            required
          />
          <button type="submit">Add Email</button>
        </form>
      </div>

      <div className="section">
        <h3>Upload a CSV File</h3>
        <form onSubmit={handleUploadCSV}>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setCsvFile(e.target.files[0])}
            required
          />
          <button type="submit">Upload CSV</button>
        </form>
      </div>

      <div className="section">
        <h3>Connect Google Spreadsheet</h3>
        <form onSubmit={handleImportGoogleSheet}>
          <input
            type="text"
            placeholder="Spreadsheet ID"
            value={spreadsheetDetails.spreadsheet_id}
            onChange={(e) =>
              setSpreadsheetDetails({ ...spreadsheetDetails, spreadsheet_id: e.target.value })
            }
            required
          />
          <input
            type="text"
            placeholder="Range Name (e.g., Sheet1!A1:E)"
            value={spreadsheetDetails.range_name}
            onChange={(e) =>
              setSpreadsheetDetails({ ...spreadsheetDetails, range_name: e.target.value })
            }
            required
          />
          <button type="submit">Import Google Sheet</button>
        </form>
        <p className="info">
          Ensure the Google Sheet is shared with the service account email provided in your
          application settings.
        </p>
      </div>
    </div>
  );
};

export default SendGrid;
