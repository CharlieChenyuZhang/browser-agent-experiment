import React from "react";
import "./App.css";
import logo from "./logo.svg";

function App() {
  const [formValues, setFormValues] = React.useState({
    resume: null,
    fullName: "",
    email: "",
    phone: "",
    currentLocation: "",
    currentCompany: "",
    linkedin: "",
    twitter: "",
    github: "",
    portfolio: "",
    otherWebsite: "",
    fourDayOfficeExpectation: "",
    workAuthUs: "",
    needsSponsorship: "",
    additionalInfo: "",
    gender: "",
    race: "",
    veteranStatus: "",
  });

  const [errors, setErrors] = React.useState({});
  const [submitted, setSubmitted] = React.useState(false);

  function updateField(fieldName, value) {
    setFormValues((prev) => ({ ...prev, [fieldName]: value }));
  }

  function validate(values) {
    const nextErrors = {};

    if (!values.fullName.trim()) nextErrors.fullName = "Full name is required.";
    if (!values.email.trim()) {
      nextErrors.email = "Email is required.";
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(values.email))
        nextErrors.email = "Enter a valid email.";
    }
    if (!values.phone.trim()) nextErrors.phone = "Phone is required.";
    if (!values.fourDayOfficeExpectation)
      nextErrors.fourDayOfficeExpectation = "Please select Yes or No.";
    if (!values.workAuthUs) nextErrors.workAuthUs = "Please select Yes or No.";
    if (!values.needsSponsorship)
      nextErrors.needsSponsorship = "Please select Yes or No.";

    return nextErrors;
  }

  function handleSubmit(event) {
    event.preventDefault();
    const foundErrors = validate(formValues);
    setErrors(foundErrors);
    if (Object.keys(foundErrors).length === 0) {
      setSubmitted(true);
    }
  }

  if (submitted) {
    return (
      <div className="app-container">
        <header className="header">
          <img src={logo} alt="Whoop logo" className="brand-logo" />
        </header>
        <main className="content">
          <h1>Congratulations</h1>
          <p>Your application has been submitted successfully.</p>
        </main>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="header">
        <img src={logo} alt="Whoop logo" className="brand-logo" />
        <div className="job-meta">
          <h1>
            Senior Machine Learning Engineer (Health) — TEST ENV (AI Agent
            Research)
          </h1>
          <div className="job-location">
            Boston, MA · Data Science & Research · On-site · TEST ENV (AI Agent
            Research)
          </div>
        </div>
      </header>

      <main className="content">
        <h2>Submit your application</h2>
        <form className="application-form" onSubmit={handleSubmit} noValidate>
          <fieldset className="section">
            <legend>Resume/CV (optional)</legend>
            <input
              type="file"
              accept=".pdf,.doc,.docx,.txt,.rtf"
              onChange={(e) =>
                updateField(
                  "resume",
                  e.target.files && e.target.files[0] ? e.target.files[0] : null
                )
              }
            />
            {/* Resume is optional; no error message */}
          </fieldset>

          <fieldset className="section">
            <legend>Basic Information</legend>
            <div className="grid two">
              <div className="field">
                <label htmlFor="fullName">Full name ✱</label>
                <input
                  id="fullName"
                  type="text"
                  value={formValues.fullName}
                  onChange={(e) => updateField("fullName", e.target.value)}
                />
                {errors.fullName && (
                  <div className="error">{errors.fullName}</div>
                )}
              </div>
              <div className="field">
                <label htmlFor="email">Email ✱</label>
                <input
                  id="email"
                  type="email"
                  value={formValues.email}
                  onChange={(e) => updateField("email", e.target.value)}
                />
                {errors.email && <div className="error">{errors.email}</div>}
              </div>
              <div className="field">
                <label htmlFor="phone">Phone ✱</label>
                <input
                  id="phone"
                  type="tel"
                  value={formValues.phone}
                  onChange={(e) => updateField("phone", e.target.value)}
                />
                {errors.phone && <div className="error">{errors.phone}</div>}
              </div>
              <div className="field">
                <label htmlFor="currentLocation">Current location</label>
                <input
                  id="currentLocation"
                  type="text"
                  value={formValues.currentLocation}
                  onChange={(e) =>
                    updateField("currentLocation", e.target.value)
                  }
                />
              </div>
              <div className="field">
                <label htmlFor="currentCompany">Current company</label>
                <input
                  id="currentCompany"
                  type="text"
                  value={formValues.currentCompany}
                  onChange={(e) =>
                    updateField("currentCompany", e.target.value)
                  }
                />
              </div>
            </div>
          </fieldset>

          <fieldset className="section">
            <legend>Links</legend>
            <div className="grid two">
              <div className="field">
                <label htmlFor="linkedin">LinkedIn URL</label>
                <input
                  id="linkedin"
                  type="url"
                  placeholder="https://www.linkedin.com/in/username"
                  value={formValues.linkedin}
                  onChange={(e) => updateField("linkedin", e.target.value)}
                />
              </div>
              <div className="field">
                <label htmlFor="twitter">Twitter URL</label>
                <input
                  id="twitter"
                  type="url"
                  placeholder="https://twitter.com/username"
                  value={formValues.twitter}
                  onChange={(e) => updateField("twitter", e.target.value)}
                />
              </div>
              <div className="field">
                <label htmlFor="github">GitHub URL</label>
                <input
                  id="github"
                  type="url"
                  placeholder="https://github.com/username"
                  value={formValues.github}
                  onChange={(e) => updateField("github", e.target.value)}
                />
              </div>
              <div className="field">
                <label htmlFor="portfolio">Portfolio URL</label>
                <input
                  id="portfolio"
                  type="url"
                  value={formValues.portfolio}
                  onChange={(e) => updateField("portfolio", e.target.value)}
                />
              </div>
              <div className="field">
                <label htmlFor="otherWebsite">Other website</label>
                <input
                  id="otherWebsite"
                  type="url"
                  value={formValues.otherWebsite}
                  onChange={(e) => updateField("otherWebsite", e.target.value)}
                />
              </div>
            </div>
          </fieldset>

          <fieldset className="section">
            <legend>4 Day In Office Expectation ✱</legend>
            <p className="hint">
              This is an on-site position, working out of our Boston, MA office
              a minimum of 4 days per week. Does this setup align to the working
              environment you are seeking in your next opportunity?
            </p>
            <div className="choices">
              <label>
                <input
                  type="radio"
                  name="fourDayOfficeExpectation"
                  value="Yes"
                  checked={formValues.fourDayOfficeExpectation === "Yes"}
                  onChange={(e) =>
                    updateField("fourDayOfficeExpectation", e.target.value)
                  }
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="fourDayOfficeExpectation"
                  value="No"
                  checked={formValues.fourDayOfficeExpectation === "No"}
                  onChange={(e) =>
                    updateField("fourDayOfficeExpectation", e.target.value)
                  }
                />
                No
              </label>
            </div>
            {errors.fourDayOfficeExpectation && (
              <div className="error">{errors.fourDayOfficeExpectation}</div>
            )}
          </fieldset>

          <fieldset className="section">
            <legend>Work Authorization ✱</legend>
            <div className="choices">
              <label>
                <input
                  type="radio"
                  name="workAuthUs"
                  value="Yes"
                  checked={formValues.workAuthUs === "Yes"}
                  onChange={(e) => updateField("workAuthUs", e.target.value)}
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="workAuthUs"
                  value="No"
                  checked={formValues.workAuthUs === "No"}
                  onChange={(e) => updateField("workAuthUs", e.target.value)}
                />
                No
              </label>
            </div>
            {errors.workAuthUs && (
              <div className="error">{errors.workAuthUs}</div>
            )}
          </fieldset>

          <fieldset className="section">
            <legend>Visa Sponsorship ✱</legend>
            <div className="choices">
              <label>
                <input
                  type="radio"
                  name="needsSponsorship"
                  value="Yes"
                  checked={formValues.needsSponsorship === "Yes"}
                  onChange={(e) =>
                    updateField("needsSponsorship", e.target.value)
                  }
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="needsSponsorship"
                  value="No"
                  checked={formValues.needsSponsorship === "No"}
                  onChange={(e) =>
                    updateField("needsSponsorship", e.target.value)
                  }
                />
                No
              </label>
            </div>
            {errors.needsSponsorship && (
              <div className="error">{errors.needsSponsorship}</div>
            )}
          </fieldset>

          <fieldset className="section">
            <legend>Additional information</legend>
            <textarea
              rows="5"
              placeholder="Add a cover letter or anything else you want to share."
              value={formValues.additionalInfo}
              onChange={(e) => updateField("additionalInfo", e.target.value)}
            />
          </fieldset>

          <fieldset className="section">
            <legend>
              U.S. Equal Employment Opportunity information (Voluntary)
            </legend>
            <p className="hint">
              Providing this information is optional. It will not be accessible
              or used in the hiring process.
            </p>
            <div className="grid three">
              <div className="field">
                <label htmlFor="gender">Gender</label>
                <select
                  id="gender"
                  value={formValues.gender}
                  onChange={(e) => updateField("gender", e.target.value)}
                >
                  <option value="">Select ...</option>
                  <option value="Female">Female</option>
                  <option value="Male">Male</option>
                  <option value="Non-binary">Non-binary</option>
                  <option value="Prefer not to say">Prefer not to say</option>
                </select>
              </div>
              <div className="field">
                <label htmlFor="race">Race</label>
                <select
                  id="race"
                  value={formValues.race}
                  onChange={(e) => updateField("race", e.target.value)}
                >
                  <option value="">Select ...</option>
                  <option value="American Indian or Alaska Native">
                    American Indian or Alaska Native
                  </option>
                  <option value="Asian">Asian</option>
                  <option value="Black or African American">
                    Black or African American
                  </option>
                  <option value="Hispanic or Latino">Hispanic or Latino</option>
                  <option value="Native Hawaiian or Other Pacific Islander">
                    Native Hawaiian or Other Pacific Islander
                  </option>
                  <option value="White">White</option>
                  <option value="Two or more races">Two or more races</option>
                  <option value="Prefer not to say">Prefer not to say</option>
                </select>
              </div>
              <div className="field">
                <label htmlFor="veteranStatus">Veteran status</label>
                <select
                  id="veteranStatus"
                  value={formValues.veteranStatus}
                  onChange={(e) => updateField("veteranStatus", e.target.value)}
                >
                  <option value="">Select ...</option>
                  <option value="I am not a protected veteran">
                    I am not a protected veteran
                  </option>
                  <option value="I identify as one or more of the classifications of a protected veteran">
                    I identify as a protected veteran
                  </option>
                  <option value="I don't wish to answer">
                    I don't wish to answer
                  </option>
                </select>
              </div>
            </div>
          </fieldset>

          <div className="actions">
            <button type="submit" className="primary">
              Submit application
            </button>
          </div>
        </form>
      </main>

      <footer className="footer">
        <span>Test environment for AI agent research</span>
      </footer>
    </div>
  );
}

export default App;
