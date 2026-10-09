# AI-Based Personalized Cancer Healthcare & Facility Recommendation System

## Project Overview

This project aims to develop a healthcare navigation and facility recommendation system for breast and lung cancer patients. It collects structured patient information and aims to support personalized healthcare-service mapping and facility recommendations.

The system is not intended to diagnose cancer, predict cancer occurrence, estimate survival, predict hospitalization, or establish that a patient is experiencing a medical emergency.

## Proposed Workflow

Patient Interface → Guided Assessment → Structured Patient Profile → ML-Based Healthcare Support/Urgency Assessment → Healthcare Requirement Mapping → Facility Recommendation → Explanation → Final Results.

## Patient Inputs

* Cancer type
* Current treatment
* Symptoms
* Symptom severity
* Symptom duration
* City

## Proposed ML Output

Healthcare support/urgency category: Low, Moderate, or High.

**Important:** The availability of suitable labeled data for these three categories must be established before model development. These labels will not be fabricated. If available datasets cannot support the intended classification task, the project will document that limitation and evaluate scientifically defensible alternatives with the project team.

## Technology Stack

* Python
* Pandas and NumPy
* scikit-learn
* Matplotlib and Seaborn
* Joblib
* FastAPI for later integration

## Current Stage

Repository setup, dataset research, and feasibility assessment.
