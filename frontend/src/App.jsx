
import { useState } from 'react'
import './App.css'

const steps = [
  'Patient Information',
  'Cancer Information',
  'Treatment Information',
  'Symptom Details',
  'Symptoms Checklist',
  'Support Requirements',
  'Review & Submit',
]

const treatments = [
  'Chemoradiation',
  'Chemotherapy',
  'Chemotherapy + Immunotherapy',
  'Chemotherapy + Radiation therapy',
  'Chemotherapy + Targeted therapy',
  'Follow-up only (treatment completed)',
  'Hormone therapy',
  'Immunotherapy',
  'Not started yet (newly diagnosed)',
  'Palliative / supportive care',
  'Radiation therapy',
  'Surgery (lobectomy or segmentectomy)',
  'Surgery (lumpectomy)',
  'Surgery (mastectomy)',
  'Targeted therapy (EGFR/ALK)',
  'Targeted therapy (HER2)',
]

const symptoms = [
  'Fatigue',
  'Shortness of breath',
  'Nausea',
  'Bone pain',
  'Weight loss',
  'Anxiety or low mood',
  'Loss of appetite',
  'Persistent cough',
  'Sleep difficulty',
  'Breast lump',
  'Breast pain',
  'Chest pain',
  'Tingling or numbness in hands/feet',
  'Shoulder stiffness',
  'Arm swelling (lymphedema)',
  'Skin changes or redness',
  'Hair loss',
  'Coughing up blood',
  'Wheezing',
  'Recurrent chest infections',
  'Hot flashes',
  'Hoarseness',
  'Difficulty swallowing',
  'Skin rash',
  'Nipple discharge',
  'Joint or muscle pain',
]

const initialForm = {
  age_years: '',
  city: '',
  cancer_type: '',
  cancer_stage: '',
  current_treatment: '',
  symptom_severity: '',
  symptom_duration: '',
  symptom_frequency: '',
  needs_caregiver_support: '',
  has_transport_to_hospital: '',
  ...Object.fromEntries(symptoms.map((symptom) => [symptom, 0])),
}

function App() {
  const [page, setPage] = useState('home')
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [submitted, setSubmitted] = useState(false)

  const updateField = (name, value) => {
    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))

    setErrors((previous) => ({
      ...previous,
      [name]: '',
    }))
  }

  const startAssessment = () => {
    setPage('assessment')
    setStep(1)
    setSubmitted(false)
  }

  const goHome = () => {
    setPage('home')
  }

  const validateStep = () => {
    const newErrors = {}

    if (step === 1) {
      const age = Number(formData.age_years)

      if (
        !formData.age_years ||
        !Number.isInteger(age) ||
        age < 1 ||
        age > 120
      ) {
        newErrors.age_years = 'Please enter a valid age between 1 and 120.'
      }

      if (formData.city.trim().length < 2) {
        newErrors.city = 'Please enter a valid city name.'
      }
    }

    if (step === 2) {
      if (!formData.cancer_type) {
        newErrors.cancer_type = 'Please select the cancer type.'
      }

      if (!formData.cancer_stage) {
        newErrors.cancer_stage = 'Please select the cancer stage.'
      }
    }

    if (step === 3 && !formData.current_treatment) {
      newErrors.current_treatment = 'Please select the current treatment.'
    }

    if (step === 4) {
      if (!formData.symptom_severity) {
        newErrors.symptom_severity = 'Please select symptom severity.'
      }

      if (!formData.symptom_duration) {
        newErrors.symptom_duration = 'Please select symptom duration.'
      }

      if (!formData.symptom_frequency) {
        newErrors.symptom_frequency = 'Please select symptom frequency.'
      }
    }

    if (step === 6) {
      if (!formData.needs_caregiver_support) {
        newErrors.needs_caregiver_support = 'Please select an option.'
      }

      if (!formData.has_transport_to_hospital) {
        newErrors.has_transport_to_hospital = 'Please select an option.'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const nextStep = () => {
    if (!validateStep()) return

    setStep((previous) => Math.min(previous + 1, 7))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const previousStep = () => {
    setErrors({})
    setStep((previous) => Math.max(previous - 1, 1))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    if (!validateStep()) return

    setSubmitted(true)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const selectedSymptoms = symptoms.filter(
    (symptom) => formData[symptom] === 1
  )

  const restartAssessment = () => {
    setFormData(initialForm)
    setErrors({})
    setStep(1)
    setSubmitted(false)
    setPage('assessment')
  }

  const renderSelect = (name, label, options, placeholder) => (
    <div className="form-group">
      <label htmlFor={name}>{label} *</label>

      <select
        id={name}
        value={formData[name]}
        onChange={(event) => updateField(name, event.target.value)}
        className={errors[name] ? 'input-error' : ''}
      >
        <option value="">{placeholder}</option>

        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>

      {errors[name] && (
        <span className="error-message">{errors[name]}</span>
      )}
    </div>
  )

  const renderRadioCards = (name, label, options) => (
    <div className="form-group">
      <label>{label} *</label>

      <div className="radio-grid">
        {options.map((option) => (
          <label
            key={option}
            className={`radio-card ${
              formData[name] === option ? 'selected' : ''
            }`}
          >
            <input
              type="radio"
              name={name}
              value={option}
              checked={formData[name] === option}
              onChange={(event) => updateField(name, event.target.value)}
            />

            <span>{option}</span>
          </label>
        ))}
      </div>

      {errors[name] && (
        <span className="error-message">{errors[name]}</span>
      )}
    </div>
  )

  const renderHome = () => (
    <>
      <section className="hero-section">
        <div className="hero-content">
          <span className="eyebrow">YOUR HEALTHCARE SUPPORT PARTNER</span>

          <h1>
            Find the healthcare support
            <span> that suits your needs.</span>
          </h1>

          <p>
            Navigate your cancer healthcare journey with personalized
            support and suitable healthcare facility recommendations.
          </p>

          <button className="primary-button" onClick={startAssessment}>
            Start Assessment <span>→</span>
          </button>

          <p className="disclaimer">
            This system supports healthcare navigation and does not
            provide a medical diagnosis.
          </p>
        </div>

        <div className="hero-visual">
          <div className="medical-circle">
            <div className="medical-icon">✚</div>
            <span className="circle-text">CarePath</span>
            <span className="circle-subtext">Healthcare Navigation</span>
          </div>
        </div>
      </section>

      <section className="features-section" id="about">
        <div className="section-heading">
          <span>HOW CAREPATH HELPS</span>
          <h2>Healthcare support, made simpler.</h2>
          <p>Guidance to help you navigate your healthcare needs.</p>
        </div>

        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">♡</div>
            <h3>Guided Assessment</h3>
            <p>Share your healthcare information through a simple assessment.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⌕</div>
            <h3>Personalized Support</h3>
            <p>Organize your healthcare support requirements.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">✚</div>
            <h3>Facility Recommendations</h3>
            <p>Find facilities based on your treatment and location needs.</p>
          </div>
        </div>
      </section>
    </>
  )

  const renderReview = () => (
    <div className="review-list">
      <div className="review-section">
        <div className="review-heading">
          <h3>Patient Information</h3>
          <button type="button" onClick={() => setStep(1)}>Edit</button>
        </div>
        <p><strong>Age:</strong> {formData.age_years} years</p>
        <p><strong>City:</strong> {formData.city}</p>
      </div>

      <div className="review-section">
        <div className="review-heading">
          <h3>Cancer Information</h3>
          <button type="button" onClick={() => setStep(2)}>Edit</button>
        </div>
        <p><strong>Cancer Type:</strong> {formData.cancer_type}</p>
        <p><strong>Cancer Stage:</strong> {formData.cancer_stage}</p>
      </div>

      <div className="review-section">
        <div className="review-heading">
          <h3>Treatment Information</h3>
          <button type="button" onClick={() => setStep(3)}>Edit</button>
        </div>
        <p><strong>Current Treatment:</strong> {formData.current_treatment}</p>
      </div>

      <div className="review-section">
        <div className="review-heading">
          <h3>Symptom Details</h3>
          <button type="button" onClick={() => setStep(4)}>Edit</button>
        </div>
        <p><strong>Severity:</strong> {formData.symptom_severity}</p>
        <p><strong>Duration:</strong> {formData.symptom_duration}</p>
        <p><strong>Frequency:</strong> {formData.symptom_frequency}</p>
      </div>

      <div className="review-section">
        <div className="review-heading">
          <h3>Symptoms Checklist</h3>
          <button type="button" onClick={() => setStep(5)}>Edit</button>
        </div>
        <p>
          {selectedSymptoms.length > 0
            ? selectedSymptoms.join(', ')
            : 'No symptoms selected.'}
        </p>
      </div>

      <div className="review-section">
        <div className="review-heading">
          <h3>Support Requirements</h3>
          <button type="button" onClick={() => setStep(6)}>Edit</button>
        </div>
        <p>
          <strong>Caregiver Support:</strong>{' '}
          {formData.needs_caregiver_support}
        </p>
        <p>
          <strong>Hospital Transport:</strong>{' '}
          {formData.has_transport_to_hospital}
        </p>
      </div>

      <p className="review-note">
        Please check your information before completing the assessment.
      </p>
    </div>
  )

  const renderAssessmentStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="assessment-form">
            <h2>Patient Information</h2>
            <p className="form-description">
              Let's start with some basic information.
            </p>

            <div className="form-group">
              <label htmlFor="age_years">Age (in years) *</label>
              <input
                id="age_years"
                type="number"
                min="1"
                max="120"
                placeholder="Enter your age"
                value={formData.age_years}
                onChange={(event) =>
                  updateField('age_years', event.target.value)
                }
                className={errors.age_years ? 'input-error' : ''}
              />
              {errors.age_years && (
                <span className="error-message">{errors.age_years}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="city">City *</label>
              <input
                id="city"
                type="text"
                minLength="2"
                maxLength="100"
                placeholder="Enter your city"
                value={formData.city}
                onChange={(event) => updateField('city', event.target.value)}
                className={errors.city ? 'input-error' : ''}
              />
              {errors.city && (
                <span className="error-message">{errors.city}</span>
              )}
            </div>
          </div>
        )

      case 2:
        return (
          <div className="assessment-form">
            <h2>Cancer Information</h2>
            <p className="form-description">
              Please provide the cancer-related information.
            </p>

            {renderSelect(
              'cancer_type',
              'Cancer Type',
              ['Breast Cancer', 'Lung Cancer'],
              'Select cancer type'
            )}

            {renderSelect(
              'cancer_stage',
              'Cancer Stage',
              ['Not sure', 'Stage I', 'Stage II', 'Stage III', 'Stage IV'],
              'Select cancer stage'
            )}
          </div>
        )

      case 3:
        return (
          <div className="assessment-form">
            <h2>Treatment Information</h2>
            <p className="form-description">
              Select the treatment that applies to you.
            </p>

            {renderSelect(
              'current_treatment',
              'Current Treatment',
              treatments,
              'Select current treatment'
            )}
          </div>
        )

      case 4:
        return (
          <div className="assessment-form">
            <h2>Symptom Details</h2>
            <p className="form-description">
              Tell us about the severity, duration and frequency of symptoms.
            </p>

            {renderSelect(
              'symptom_severity',
              'Symptom Severity',
              ['Mild', 'Moderate', 'Severe'],
              'Select severity'
            )}

            {renderSelect(
              'symptom_duration',
              'Symptom Duration',
              [
                '1-3 months',
                '1-4 weeks',
                '3-6 months',
                'Less than 1 week',
                'More than 6 months',
                'Not applicable',
              ],
              'Select duration'
            )}

            {renderSelect(
              'symptom_frequency',
              'Symptom Frequency',
              [
                'Constant',
                'Daily',
                'Not applicable',
                'Occasionally',
                'Several times a week',
              ],
              'Select frequency'
            )}
          </div>
        )

      case 5:
        return (
          <div className="assessment-form">
            <h2>Symptoms Checklist</h2>
            <p className="form-description">
              Select all symptoms that are currently present. You can leave
              all options unselected if none apply.
            </p>

            <div className="symptom-grid">
              {symptoms.map((symptom) => (
                <label
                  key={symptom}
                  className={`symptom-option ${
                    formData[symptom] === 1 ? 'selected' : ''
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={formData[symptom] === 1}
                    onChange={(event) =>
                      updateField(symptom, event.target.checked ? 1 : 0)
                    }
                  />
                  <span>{symptom}</span>
                </label>
              ))}
            </div>

            <p className="selection-count">
              {selectedSymptoms.length} of 26 symptoms selected
            </p>
          </div>
        )

      case 6:
        return (
          <div className="assessment-form">
            <h2>Support Requirements</h2>
            <p className="form-description">
              Tell us about the additional support you may need.
            </p>

            {renderRadioCards(
              'needs_caregiver_support',
              'Do you need caregiver support?',
              ['No', 'Sometimes', 'Yes']
            )}

            {renderRadioCards(
              'has_transport_to_hospital',
              'Do you have transport to the hospital?',
              ['No', 'Sometimes', 'Yes']
            )}
          </div>
        )

      case 7:
        return (
          <div className="assessment-form">
            <h2>Review Your Information</h2>
            <p className="form-description">
              Please review all the information before submitting.
            </p>
            {renderReview()}
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo" onClick={goHome}>
          <span className="logo-icon">✚</span>
          <span>CarePath</span>
        </div>

        <nav>
          <button className="nav-link" onClick={goHome}>Home</button>
          <button className="nav-link" onClick={goHome}>About</button>
          <button className="nav-button" onClick={startAssessment}>
            Get Started
          </button>
        </nav>
      </header>

      {page === 'home' && renderHome()}

      {page === 'assessment' && (
        <main className="assessment-page">
          <div className="assessment-container">
            {submitted ? (
              <div className="assessment-form success-panel">
                <div className="success-icon">✓</div>
                <h2>Assessment Completed!</h2>
                <p>
                  Your assessment information has been collected successfully.
                </p>
                <p className="review-note">
                  This is a frontend demonstration. Your information has not
                  yet been sent to the backend or ML model.
                </p>
                <button className="primary-button" onClick={restartAssessment}>
                  Start Again
                </button>
                <button className="back-button" onClick={goHome}>
                  Back to Home
                </button>
              </div>
            ) : (
              <>
                <span className="eyebrow">CAREPATH ASSESSMENT</span>
                <h1>Patient Assessment</h1>
                <p className="assessment-description">
                  Please provide your information to help us understand your
                  healthcare support requirements.
                </p>

                <div className="progress-info">
                  <span>Step {step} of 7</span>
                  <span>{steps[step - 1]}</span>
                </div>

                <div
                  className="progress-bar"
                  role="progressbar"
                  aria-valuenow={step}
                  aria-valuemin="1"
                  aria-valuemax="7"
                >
                  <div
                    className="progress-fill"
                    style={{ width: `${(step / 7) * 100}%` }}
                  />
                </div>

                <form
                  onSubmit={
                    step === 7
                      ? handleSubmit
                      : (event) => {
                          event.preventDefault()
                          nextStep()
                        }
                  }
                >
                  {renderAssessmentStep()}

                  <div className="form-buttons">
                    {step > 1 ? (
                      <button
                        type="button"
                        className="back-button"
                        onClick={previousStep}
                      >
                        ← Previous
                      </button>
                    ) : (
                      <button
                        type="button"
                        className="back-button"
                        onClick={goHome}
                      >
                        ← Back to Home
                      </button>
                    )}

                    {step < 7 ? (
                      <button type="submit" className="primary-button">
                        Next →
                      </button>
                    ) : (
                      <button type="submit" className="primary-button">
                        Complete Assessment ✓
                      </button>
                    )}
                  </div>
                </form>
              </>
            )}
          </div>
        </main>
      )}

      <footer className="footer">
        <p>© 2026 CarePath | Healthcare Navigation System</p>
        <p>Supporting your healthcare journey.</p>
      </footer>
    </div>
  )
}

export default App
