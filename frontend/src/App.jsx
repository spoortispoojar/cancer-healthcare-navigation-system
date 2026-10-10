import { useState } from "react";
import "./App.css";

function App() {
  const [showAssessment, setShowAssessment] = useState(false);
  const [formData, setFormData] = useState({
    cancerType: "",
    treatment: "",
    symptoms: [],
    severity: "",
    duration: "",
    city: "",
  });
  const [errors, setErrors] = useState({});

  const symptomOptions = [
    "Pain",
    "Vomiting",
    "Weakness",
    "Fever",
    "Breathlessness",
    "Cough",
    "Fatigue",
    "Other",
  ];

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setErrors((previous) => ({
      ...previous,
      [name]: "",
    }));
  }

  function handleSymptomChange(symptom) {
    setFormData((previous) => ({
      ...previous,
      symptoms: previous.symptoms.includes(symptom)
        ? previous.symptoms.filter((item) => item !== symptom)
        : [...previous.symptoms, symptom],
    }));

    setErrors((previous) => ({
      ...previous,
      symptoms: "",
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    const newErrors = {};

    if (!formData.cancerType) {
      newErrors.cancerType = "Please select a cancer type.";
    }

    if (!formData.treatment) {
      newErrors.treatment = "Please select your current treatment.";
    }

    if (formData.symptoms.length === 0) {
      newErrors.symptoms = "Please select at least one symptom.";
    }

    if (!formData.severity) {
      newErrors.severity = "Please select symptom severity.";
    }

    if (
      formData.duration === "" ||
      !Number.isInteger(Number(formData.duration)) ||
      Number(formData.duration) <= 0
    ) {
      newErrors.duration = "Enter a positive whole number of days.";
    }

    if (!formData.city.trim()) {
      newErrors.city = "Please enter your city.";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      // Temporary development output.
      // API integration will be added when the backend is ready.
      console.log("Patient assessment:", formData);
      alert("Form validated successfully! Check the browser console.");
    }
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div
          className="logo"
          onClick={() => setShowAssessment(false)}
          role="button"
          tabIndex={0}
        >
          CarePath
        </div>
        <span className="nav-label">Healthcare Support</span>
      </nav>

      {!showAssessment ? (
        <main className="hero">
          <div className="hero-content">
            <p className="eyebrow">PERSONALIZED HEALTHCARE SUPPORT</p>

            <h1>
              Find the healthcare support
              <br />
              that suits your needs.
            </h1>

            <p className="description">
              Share information about your current treatment and symptoms
              to receive a healthcare support assessment and find suitable
              healthcare facilities.
            </p>

            <button
              className="primary-button"
              onClick={() => setShowAssessment(true)}
            >
              Start Assessment →
            </button>

            <p className="note">
              This system supports healthcare navigation and does not
              provide a medical diagnosis.
            </p>
          </div>
        </main>
      ) : (
        <main className="assessment">
          <button
            type="button"
            className="back-button"
            onClick={() => setShowAssessment(false)}
          >
            ← Back to Home
          </button>

          <h1>Patient Assessment</h1>
          <p className="form-intro">
            Please provide the following information to help us understand
            your healthcare support needs.
          </p>

          <form onSubmit={handleSubmit} noValidate>
            <div className="form-group">
              <label htmlFor="cancerType">Cancer Type *</label>
              <select
                id="cancerType"
                name="cancerType"
                value={formData.cancerType}
                onChange={handleChange}
              >
                <option value="">Select cancer type</option>
                <option value="Breast">Breast Cancer</option>
                <option value="Lung">Lung Cancer</option>
              </select>
              {errors.cancerType && (
                <p className="error">{errors.cancerType}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="treatment">Current Treatment *</label>
              <select
                id="treatment"
                name="treatment"
                value={formData.treatment}
                onChange={handleChange}
              >
                <option value="">Select current treatment</option>
                <option value="Chemotherapy">Chemotherapy</option>
                <option value="Radiation Therapy">Radiation Therapy</option>
                <option value="Surgery">Surgery</option>
                <option value="Immunotherapy">Immunotherapy</option>
                <option value="Other">Other</option>
              </select>
              {errors.treatment && (
                <p className="error">{errors.treatment}</p>
              )}
            </div>

            <fieldset className="form-group symptoms-group">
              <legend>Current Symptoms *</legend>
              <p className="field-hint">Select all that apply.</p>

              <div className="symptom-grid">
                {symptomOptions.map((symptom) => (
                  <label className="symptom-option" key={symptom}>
                    <input
                      type="checkbox"
                      checked={formData.symptoms.includes(symptom)}
                      onChange={() => handleSymptomChange(symptom)}
                    />
                    {symptom}
                  </label>
                ))}
              </div>

              {errors.symptoms && (
                <p className="error">{errors.symptoms}</p>
              )}
            </fieldset>

            <div className="form-group">
              <label htmlFor="severity">Symptom Severity *</label>
              <select
                id="severity"
                name="severity"
                value={formData.severity}
                onChange={handleChange}
              >
                <option value="">Select severity</option>
                <option value="Mild">Mild</option>
                <option value="Moderate">Moderate</option>
                <option value="Severe">Severe</option>
              </select>
              {errors.severity && (
                <p className="error">{errors.severity}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="duration">Symptom Duration (days) *</label>
              <input
                id="duration"
                name="duration"
                type="number"
                min="1"
                step="1"
                value={formData.duration}
                onChange={handleChange}
                placeholder="e.g. 2"
              />
              {errors.duration && (
                <p className="error">{errors.duration}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="city">City *</label>
              <input
                id="city"
                name="city"
                type="text"
                value={formData.city}
                onChange={handleChange}
                placeholder="Enter your city"
              />
              {errors.city && <p className="error">{errors.city}</p>}
            </div>

            <button type="submit" className="primary-button submit-button">
              Submit Assessment →
            </button>

            <p className="form-disclaimer">
              This form is for healthcare support navigation, not diagnosis.
              If you experience severe or rapidly worsening symptoms,
              seek urgent medical care rather than waiting for this system.
            </p>
          </form>
        </main>
      )}

      <footer>
        <p>Healthcare navigation and support · Not a medical diagnosis</p>
      </footer>
    </div>
  );
}

export default App;