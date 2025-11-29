import "../styles/AuthForm.css";
import { useState } from "react";
import { z } from "zod";
import { register } from "../services/authService";
import { useNavigate } from "react-router-dom";

// Zod schema – full, strong password
const registerSchema = z.object({
  name: z.string().min(3, "Name must be at least 3 characters"),
  email: z.string().email("Invalid email"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must include at least one uppercase letter")
    .regex(/[a-z]/, "Must include at least one lowercase letter")
    .regex(/[0-9]/, "Must include at least one number")
    .regex(/[^A-Za-z0-9]/, "Must include at least one special character"),
});

type FieldErrors = {
  name?: string;
  email?: string;
  password?: string;
};

export default function RegisterForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    // validate entire form with zod
    const result = registerSchema.safeParse({ name, email, password });

    if (!result.success) {
      const flat = result.error.flatten().fieldErrors;
      setFieldErrors({
        name: flat.name?.[0],
        email: flat.email?.[0],
        password: flat.password?.[0],
      });
      return;
    }

    // clear errors if all good
    setFieldErrors({});

    try {
      const res = await register(name, email, password);

      if (res.message) {
        setMessage("✅ " + res.message);
        navigate("/login");
      } else {
        setMessage("❌ " + (res.error || "Unknown error"));
      }
    } catch (err) {
      console.error(err);
      setMessage("❌ Error connecting to server");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2 className="auth-title">Create account</h2>
        <p className="auth-subtitle">
          Use a strong password to keep your account safe
        </p>

        <form onSubmit={handleSubmit} className="auth-form">
          {/* Name */}
          <div className="auth-field">
            <label className="auth-label" htmlFor="reg-name">
              Name
            </label>
            <input
              id="reg-name"
              className={`auth-input ${
                fieldErrors.name ? "auth-input--error" : ""
              }`}
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="John Doe"
            />
            {fieldErrors.name && (
              <div className="field-error">
                <span className="field-error-icon">⚠️</span>
                <span>{fieldErrors.name}</span>
              </div>
            )}
          </div>

          {/* Email */}
          <div className="auth-field">
            <label className="auth-label" htmlFor="reg-email">
              Email
            </label>
            <input
              id="reg-email"
              className={`auth-input ${
                fieldErrors.email ? "auth-input--error" : ""
              }`}
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
            {fieldErrors.email && (
              <div className="field-error">
                <span className="field-error-icon">⚠️</span>
                <span>{fieldErrors.email}</span>
              </div>
            )}
          </div>

          {/* Password */}
          <div className="auth-field">
            <label className="auth-label" htmlFor="reg-password">
              Password
            </label>
            <input
              id="reg-password"
              type="password"
              className={`auth-input ${
                fieldErrors.password ? "auth-input--error" : ""
              }`}
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
            />
            {fieldErrors.password && (
              <div className="field-error">
                <span className="field-error-icon">⚠️</span>
                <span>{fieldErrors.password}</span>
              </div>
            )}
          </div>

          <button className="auth-button" type="submit">
            Register
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}