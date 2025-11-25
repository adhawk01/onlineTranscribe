import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("Loading...");
  const apiUrl = process.env.REACT_APP_API_URL;
  console.log("API URL:", apiUrl);

  useEffect(() => {
    fetch(`${apiUrl}/hello`)
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => setMessage("❌ Error connecting to Flask"));
  }, []);

  return (
    <div style={{
      fontFamily: "Arial, sans-serif",
      textAlign: "center",
      marginTop: "100px"
    }}>
      <h1 style={{ color: "#0078ff" }}>🚀 Flask + React Connected!</h1>
      <p style={{ fontSize: "20px", color: "#333" }}>
        Flask says: <strong>{message}</strong>
      </p>
      <p style={{ marginTop: "40px", color: "#666" }}>
        If you see this page and the message above, your integration works! 🎉
      </p>
    </div>
  );
}

export default App;