import React, { useState } from "react";
import axios from "axios";

const LoginForm = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const [user, setUser] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(
        "http://localhost:5000/api/login",
        formData,
        { withCredentials: true } // allows Flask session cookie
      );
      setUser(res.data.user);
      setMessage(res.data.message);
    } catch (err) {
      if (err.response) {
        setMessage(err.response.data.error);
      } else {
        setMessage("An error occurred. Please try again.");
      }
    }
  };

  const handleLogout = async () => {
    await axios.post("http://localhost:5000/api/logout", {}, { withCredentials: true });
    setUser(null);
    setMessage("Logged out successfully");
  };

  return (
    <div style={styles.container}>
      <h2>User Login</h2>
      {!user ? (
        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            style={styles.input}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            style={styles.input}
            required
          />
          <button type="submit" style={styles.button}>Login</button>
        </form>
      ) : (
        <div style={styles.loggedIn}>
          <p>Welcome, {user.first_name || user.username}!</p>
          <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
        </div>
      )}
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
};

const styles = {
  container: { maxWidth: 400, margin: "auto", padding: 20, textAlign: "center" },
  form: { display: "flex", flexDirection: "column", gap: "10px" },
  input: { padding: "10px", fontSize: "16px", borderRadius: "8px", border: "1px solid #ccc" },
  button: { padding: "10px", fontSize: "16px", borderRadius: "8px", backgroundColor: "#28a745", color: "#fff", border: "none", cursor: "pointer" },
  message: { marginTop: 10, color: "green" },
  logoutButton: { padding: "10px", backgroundColor: "#dc3545", color: "#fff", border: "none", borderRadius: "8px" },
  loggedIn: { display: "flex", flexDirection: "column", alignItems: "center", gap: "10px" },
};

export default LoginForm;