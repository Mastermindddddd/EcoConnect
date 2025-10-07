import React, { useState } from "react";
import axios from "axios";

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone: "",
    address: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/api/register", formData);
      setMessage(res.data.message);
      setFormData({
        username: "",
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        phone: "",
        address: "",
      });
    } catch (err) {
      if (err.response) {
        setMessage(err.response.data.error);
      } else {
        setMessage("An error occurred. Please try again.");
      }
    }
  };

  return (
    <div style={styles.container}>
      <h2>User Registration</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        {Object.keys(formData).map((key) => (
          <input
            key={key}
            type={key === "password" ? "password" : "text"}
            name={key}
            value={formData[key]}
            onChange={handleChange}
            placeholder={key.replace("_", " ").toUpperCase()}
            style={styles.input}
            required={["username", "email", "password"].includes(key)}
          />
        ))}
        <button type="submit" style={styles.button}>Register</button>
      </form>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
};

const styles = {
  container: { maxWidth: 400, margin: "auto", padding: 20, textAlign: "center" },
  form: { display: "flex", flexDirection: "column", gap: "10px" },
  input: { padding: "10px", fontSize: "16px", borderRadius: "8px", border: "1px solid #ccc" },
  button: { padding: "10px", fontSize: "16px", borderRadius: "8px", backgroundColor: "#007bff", color: "#fff", border: "none", cursor: "pointer" },
  message: { marginTop: 10, color: "green" },
};

export default RegistrationForm;
