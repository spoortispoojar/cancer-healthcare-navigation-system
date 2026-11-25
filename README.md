# AI-Based Personalized Cancer Healthcare & Facility Recommendation System



## 1. Project Overview



This project aims to develop an AI-based healthcare navigation and facility recommendation system for breast and lung cancer patients.



The system collects structured patient information, maps healthcare requirements based on the patient's stated treatment, and identifies suitable healthcare facilities based on service availability and matching criteria.



The purpose is to help patients navigate healthcare services and identify potentially suitable facilities.



**Important:** This system is not intended to diagnose cancer, predict cancer occurrence, estimate survival, predict hospitalization, or establish that a patient is experiencing a medical emergency. It does not replace professional medical advice.



## 2. Approved Project Workflow



Patient → Patient Interface → Guided Assessment → Patient Information → Information Processing → Structured Patient Profile → ML Assessment → Healthcare Support/Urgency Level → Requirement Mapping → Required Healthcare Services → Recommendation Engine → Suitable Facilities → Explanation → Final Results.



## 3. Patient Input Parameters



The system considers the following patient information:



\- Cancer Type: Breast / Lung

\- Current Treatment: Chemotherapy / Radiation Therapy / Surgery / Immunotherapy / Other

\- Symptoms

\- Symptom Severity: Mild / Moderate / Severe

\- Symptom Duration

\- Location / City



## 4. Proposed ML Output



The proposed ML component aims to provide a healthcare support/urgency category:



\- Low

\- Moderate

\- High



**Data feasibility requirement:** Suitable labeled data must be identified and evaluated before developing the classification model. Labels will not be fabricated. If available datasets cannot scientifically support this task, the limitation will be documented and alternative approaches will be discussed with the project team.



## 5. Implemented Components



The current implementation includes:



\- PostgreSQL database integration using SQLAlchemy.

\- Healthcare facility and healthcare service data models.

\- Facility-service mapping.

\- Facility research and verification workflow.

\- Separation of research records from approved production data.

\- Healthcare requirement mapping based on stated treatment.

\- Facility recommendation based on required service matching.

\- Service-match percentage calculation.

\- Facility ranking based on service coverage.

\- Optional distance calculation using the Haversine formula.

\- Automated tests for distance calculation, recommendation, and requirement mapping.



Facility recommendations are based on service availability and matching criteria. They do not represent clinical quality, treatment effectiveness, or guaranteed suitability.



## 6. Technology Stack



\- Python

\- PostgreSQL

\- SQLAlchemy

\- Pandas

\- NumPy

\- Scikit-learn

\- Matplotlib

\- Seaborn

\- Joblib

\- Psycopg

\- Pytest

\- Python-dotenv



FastAPI is planned for later application integration.



## 7. Project Structure



```text

cancer-healthcare-navigation-system/

│

├── data/

│   └── processed/

│

├── src/

│   ├── database.py

│   ├── models.py

│   ├── research\_models.py

│   ├── requirement\_mapping.py

│   ├── recommendation.py

│   ├── distance.py

│   ├── main.py

│   └── tests/

│       ├── test\_distance.py

│       ├── test\_recommendation.py

│       └── test\_workflow.py

│

├── .env

├── .gitignore

├── requirements.txt

└── README.md

```



The `.env` file contains local database configuration and must not be committed to Git.



## 8. Installation



Clone the repository:



```bash

git clone https://github.com/spoortispoojar/cancer-healthcare-navigation-system.git

cd cancer-healthcare-navigation-system

```



Install the dependencies:



```bash

pip install -r requirements.txt

```



Configure the PostgreSQL database connection in a local `.env` file.



## 9. Running the Project



Run the main workflow demonstration:



```bash

python -m src.main

```



Run the automated tests:



```bash

python -m pytest -v

```



## 10. Current Development Status



The current development includes database setup, facility and service management, facility research and verification, healthcare requirement mapping, facility recommendation, distance calculation, and automated testing.



Further development will focus on validating facility information, completing the ML feasibility assessment, and integrating the patient interface and remaining application components.



## 11. Ethical and Safety Considerations



\- Patient information is used for healthcare navigation support.

\- The system does not provide cancer diagnosis or medical treatment decisions.

\- Facility data must be verified before being treated as approved production information.

\- Unverified research data must remain separate from approved facility records.

\- Recommendation results indicate service matching, not clinical superiority or guaranteed treatment outcomes.
