Wallet Trust Scoring System - README
An end-to-end data pipeline that analyzes blockchain wallet behavior and assigns a Human Trust Score to detect bot-like activity.
Overview
This project builds a full analytics system that transforms raw blockchain transaction data into an interpretable trust score. It identifies human vs bot-like wallets, detects suspicious behavior, and provides a scalable scoring framework with API access.
Pipeline
Raw Transactions → Data Ingestion → Feature Engineering → Trust Scoring → Evaluation → API
Key Features
- Longevity: Wallet age - Activity: Transaction frequency - Temporal Patterns: Burst behavior - Network Behavior: Counterparty diversity - Economic Activity: Transaction value
Trust Score
TrustScore = 0.25*Age + 0.20*Activity + 0.20*Temporal + 0.20*Network + 0.15*Economic Range: 0–100
Trust Tiers
80–100: Gold 60–79: Silver 0–59: Bronze
API Usage
Run: pip install -r requirements.txt uvicorn api.app:app --reload  Open: http://127.0.0.1:8000/docs
Evaluation
Evaluation includes score distribution, feature relationships, and simulated wallet testing.
Limitations
No labeled dataset, heuristic scoring, potential bot mimicry.
Future Work
Machine learning models, graph analysis, real-time scoring, dashboard visualization.
Summary
Full pipeline from raw data to trust scoring with API deployment.
