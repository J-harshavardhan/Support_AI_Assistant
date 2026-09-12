🤖 SupportAI — Grounded Helpdesk Assistant

<p align="center">

AI-Powered Customer Support with Hybrid Retrieval, Confidence Scoring & Human Escalation

A grounded customer-support assistant that retrieves answers from a controlled FAQ knowledge base, evaluates confidence, uses an LLM only for grounded response generation, and escalates uncertain requests to human support.

<br>

<a href="https://harsha-support-ai-assistant.streamlit.app/">
  🚀 <strong>Live Demo</strong>
</a>
&nbsp;&nbsp;•&nbsp;&nbsp;
<a href="https://github.com/J-harshavardhan/Support_AI_Assistant">
  💻 <strong>GitHub Repository</strong>
</a>

</p>

📸 Application Preview

Screenshots: Create a screenshots/ folder in your repository and add the four project screenshots using these exact names:
home.png, query.png, answer.png, escalation.png.

<p align="center">
  <img src="screenshots/home.png" width="95%" alt="SupportAI Helpdesk Home Interface">
</p>

<p align="center">
  <em>SupportAI Helpdesk — a clean interface for grounded customer support.</em>
</p>

🌟 Overview

SupportAI is an AI-powered customer-support assistant built using Python, Streamlit, TF-IDF, hybrid retrieval, and the OpenRouter LLM API.

Instead of sending every customer question directly to an LLM, SupportAI first searches a controlled FAQ knowledge base and calculates a retrieval confidence score.

When a relevant FAQ is identified with sufficient confidence, the system uses the LLM to generate a natural conversational response based only on the retrieved FAQ content.

When the system cannot confidently identify an appropriate FAQ, it avoids guessing and provides a safe fallback with an option to escalate the request to human support.

🎯 Core Principle

Retrieve trusted information → evaluate confidence → generate a grounded answer → escalate when uncertain.

🚀 Live Demo

🌐 Try SupportAI

Live Application:
https://harsha-support-ai-assistant.streamlit.app/

Source Code:
https://github.com/J-harshavardhan/Support_AI_Assistant

The application is deployed using Streamlit Community Cloud.

Note: The Streamlit deployment URL may change if the application name or deployment configuration is updated.

✨ Key Features

Feature

Description

📚 Grounded FAQ Answers

Answers are based on a controlled FAQ knowledge base

🔎 Keyword Search

Finds FAQs using keyword-based matching

📊 TF-IDF Retrieval

Uses TF-IDF and cosine similarity for textual matching

🔀 Hybrid Search

Combines keyword and TF-IDF retrieval

🎯 Confidence Scoring

Measures the strength of the FAQ match

🤖 Grounded LLM

Generates conversational answers from retrieved FAQ content

💬 Conversation History

Maintains user and assistant conversation turns

🛟 Human Escalation

Provides a fallback path for uncertain requests

🎫 Mock Tickets

Generates support ticket IDs for escalated requests

🧯 API Fallback

Uses the official FAQ answer when the LLM API fails

🎈 Streamlit UI

Interactive web-based helpdesk interface

☁️ Cloud Deployment

Deployable through Streamlit Community Cloud

🧠 How SupportAI Works

flowchart TD

    User["👤 User Question"]
    UI["🖥️ Streamlit UI"]
    Agent["🤖 SupportAgent"]

    Hybrid["🔎 Hybrid Search"]

    Keyword["🔤 Keyword Search"]
    TFIDF["📊 TF-IDF + Cosine Similarity"]

    Rank["🏆 Result Ranking"]
    Confidence["🎯 Confidence Score"]

    Decision{"Confidence ≥ Threshold?"}

    LLM["🧠 Grounded LLM"]
    OpenRouter["🌐 OpenRouter API"]

    Fallback["🛟 Safe FAQ Fallback"]
    Escalation["👨‍💼 Human Escalation"]

    History["💬 Conversation History"]

    User --> UI
    UI --> Agent

    Agent --> Hybrid

    Hybrid --> Keyword
    Hybrid --> TFIDF

    Keyword --> Rank
    TFIDF --> Rank

    Rank --> Confidence
    Confidence --> Decision

    Decision -->|Yes| LLM
    LLM --> OpenRouter
    OpenRouter --> LLM
    LLM --> History

    Decision -->|No| Fallback
    Fallback --> Escalation
    Fallback --> History

    History --> UI

🔄 Request Lifecycle

sequenceDiagram

    participant U as 👤 User
    participant A as 🤖 SupportAgent
    participant H as 🔎 Hybrid Search
    participant F as 📚 FAQ Knowledge Base
    participant L as 🧠 Grounded LLM
    participant E as 👨‍💼 Human Support

    U->>A: Submit question
    A->>H: Search query
    H->>F: Keyword + TF-IDF lookup
    F-->>H: FAQ candidates
    H-->>A: Best FAQ + confidence

    alt Confidence meets threshold
        A->>L: User question + FAQ content
        L-->>A: Grounded conversational answer
        A-->>U: Answer + FAQ ID + confidence
    else Low confidence
        A-->>U: Safe fallback response
        A->>E: Offer human escalation
    end

🔎 Hybrid Retrieval

SupportAI combines two retrieval techniques.

1. 🔤 Keyword Search

Task 1 performs keyword-based matching against the FAQ knowledge base.

A keyword match receives a base score of:

0.50

This provides strong support for direct keyword matches.

2. 📊 TF-IDF Similarity

Task 3 converts FAQ questions and the user's query into TF-IDF vectors.

Cosine similarity is then used to measure textual similarity between the query and FAQ candidates.

Conceptually:

User Question
      │
      ▼
TF-IDF Vector
      │
      ▼
Cosine Similarity
      │
      ▼
FAQ Similarity Score

TF-IDF provides lexical/vector-space similarity, allowing differently worded questions to match related FAQ content.

3. 🔀 Hybrid Ranking

The hybrid search system:

Performs keyword matching.

Calculates TF-IDF cosine similarity.

Combines candidate results.

Removes duplicate FAQ IDs.

Retains the highest score for each FAQ.

Sorts candidates by score.

Selects the strongest FAQ match.

Applies the confidence threshold.

The default agent confidence threshold is:

0.15

🔍 Search Pipeline

                         USER QUESTION
                              │
                              ▼
                    ┌──────────────────┐
                    │ Query Processing │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
      🔤 Keyword Search              📊 TF-IDF Search
              │                             │
              │ Base score                  │ Cosine
              │ 0.50                        │ similarity
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Merge by FAQ ID │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Rank Candidates │
                    └────────┬────────┘
                             ▼
                    🎯 Confidence Score
                             │
                 ┌───────────┴───────────┐
                 │                       │
              HIGH                     LOW
                 │                       │
                 ▼                       ▼
          🧠 Grounded LLM          🛟 Safe Fallback
                 │                       │
                 ▼                       ▼
             AI Answer             👨‍💼 Escalation

📸 Natural-Language Query

<p align="center">
  <img src="screenshots/query.png" width="95%" alt="SupportAI Natural Language Query">
</p>

<p align="center">
  <em>A customer can ask a natural-language question instead of using the exact wording of an FAQ.</em>
</p>

Example:

How do I update my email address?

The system searches the FAQ knowledge base and identifies the most relevant FAQ.

🤖 Grounded AI Response

<p align="center">
  <img src="screenshots/answer.png" width="95%" alt="SupportAI Grounded AI Response">
</p>

<p align="center">
  <em>SupportAI returns a grounded conversational answer together with the matched FAQ ID and confidence score.</em>
</p>

Example:

User:
How do I update my email address?

SupportAI:

To update your email address, simply head over to your
account settings, find the personal information section,
and make the necessary change there.

FAQ: faq-007
Confidence: 0.83

The FAQ ID and confidence score provide visibility into the retrieval result.

📚 Grounded FAQ Answers

The LLM receives:

The user's question

The selected FAQ question

The official FAQ answer

The system prompt instructs the model to:

Use only the supplied FAQ content.

Keep the response professional and concise.

Avoid inventing policies.

Avoid inventing prices.

Avoid inventing dates.

Avoid inventing unsupported procedures.

Explain when the FAQ does not cover a requested detail.

This creates a separation between:

RETRIEVAL
    ↓
VERIFIED FAQ
    ↓
LLM GENERATION

The LLM's role is primarily to communicate retrieved information naturally rather than independently deciding what the support policy should be.

🎯 Confidence-Based Routing

Each retrieval attempt can produce a confidence score.

Example:

FAQ: faq-007
Confidence: 0.83

The confidence score determines the next step.

                  Confidence
                       │
              ┌────────┴────────┐
              │                 │
             HIGH              LOW
              │                 │
              ▼                 ▼
       Grounded LLM       Safe Fallback
              │                 │
              ▼                 ▼
           Answer           Escalation

Important: The confidence value is a retrieval score, not a calibrated probability.

🛟 Human Escalation

When SupportAI cannot confidently identify an appropriate FAQ, it can provide a human-support escalation path.

<p align="center">
  <img src="screenshots/escalation.png" width="95%" alt="SupportAI Human Escalation">
</p>

<p align="center">
  <em>Low-confidence requests can be escalated through a mock support-ticket workflow.</em>
</p>

Example:

Your request has been escalated to our support team.

Ticket ID:
TICKET-13438

Estimated response time:
within 4 business hours.

Confidence: 0.00

The ticket-generation functionality is currently a mock support workflow for demonstration purposes.

💬 Conversation State

SupportAgent maintains conversation history using the ConversationTurn dataclass.

Each assistant response can contain:

FAQ ID
Confidence Score
Response Content

The agent also tracks repeated low-confidence requests and can create a mock support ticket such as:

TICKET-48291

🧯 API Failure Resilience

SupportAI is designed to degrade gracefully when the LLM API is unavailable.

Possible failure conditions include:

Missing API key

Invalid API key

Authorization errors

Payment/credit errors

API connectivity problems

OpenRouter service failures

The fallback flow is:

OpenRouter Failure
       │
       ▼
Log Technical Error
       │
       ▼
Preserve FAQ Match
       │
       ▼
Display Official FAQ Answer

This allows a verified FAQ answer to remain available even when the LLM layer cannot generate a response.

📌 Supported Helpdesk Topics

SupportAI currently demonstrates FAQ handling for:

🔐 Password Reset
👤 Account Access
📦 Order Tracking
🚚 Shipping & Delivery
💰 Refunds
💳 Billing
📧 Email Address Updates
🔄 Subscription Cancellation
☎️ Customer Support

The FAQ knowledge base can be extended with additional categories and questions.

🏗️ Project Structure

Support_AI_Assistant/
│
├── 📄 app.py
│   └── Streamlit web application
│
├── 📄 task1.py
│   └── FAQ data + keyword search
│
├── 📄 task2.py
│   └── OpenRouter client + grounded prompts
│
├── 📄 task3.py
│   └── TF-IDF + cosine similarity + hybrid search
│
├── 📄 task4.py
│   └── SupportAgent + history + fallback + escalation
│
├── 📄 requirements.txt
│   └── Python dependencies
│
├── 🔐 .env
│   └── Local API configuration
│
├── 📁 screenshots/
│   ├── home.png
│   ├── query.png
│   ├── answer.png
│   └── escalation.png
│
└── 📄 README.md
    └── Project documentation

🧩 Component Responsibilities

File

Responsibility

task1.py

FAQ data, keyword search, ID lookup, category lookup

task2.py

OpenRouter configuration, API client, error handling, grounded prompts

task3.py

TF-IDF matching, cosine similarity, confidence thresholds, hybrid search

task4.py

Conversational agent, history, fallback handling, escalation

app.py

Streamlit web interface

requirements.txt

Python dependencies

.env

Local API key configuration

🛠️ Technology Stack

Technology

Purpose

🐍 Python

Core application logic

🎈 Streamlit

Interactive web interface

📊 Scikit-learn

TF-IDF and cosine similarity

🌐 OpenRouter

LLM API access

🔗 Requests

HTTP/API communication

🔐 Python Dotenv

Local environment configuration

🧠 LLM

Grounded conversational response generation

🧮 Dataclasses

Conversation state representation

💻 Example Conversation

┌──────────────────────────────────────────────┐
│ 👤 USER                                      │
├──────────────────────────────────────────────┤
│ I forgot my login credentials                │
└──────────────────────────────────────────────┘

                       │
                       ▼

┌──────────────────────────────────────────────┐
│ 🔎 HYBRID RETRIEVAL                          │
├──────────────────────────────────────────────┤
│ Best FAQ: faq-001                            │
│ Confidence: 0.50                             │
└──────────────────────────────────────────────┘

                       │
                       ▼

┌──────────────────────────────────────────────┐
│ 🤖 SUPPORTAI                                 │
├──────────────────────────────────────────────┤
│ Click "Forgot Password" on the login page.  │
│ Enter your registered email address and      │
│ check your inbox for the reset link.         │
│                                              │
│ FAQ: faq-001                                 │
│ Confidence: 0.50                            │
└──────────────────────────────────────────────┘

⚙️ Local Setup

1. Clone the Repository

git clone https://github.com/J-harshavardhan/Support_AI_Assistant.git

cd Support_AI_Assistant

2. Create a Virtual Environment

Windows Command Prompt

python -m venv .venv
.venv\Scripts\activate

PowerShell

python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Install Dependencies

python -m pip install -r requirements.txt

🔐 API Configuration

Create a local .env file in the project root:

OPENROUTER_API_KEY=your_new_openrouter_key

Never commit .env to Git.

⚠️ Security

Never expose API credentials in:

GitHub commits

Source code

README files

Screenshots

Terminal output

Screen recordings

Public documentation

If an API key is accidentally exposed:

1. Revoke the exposed key
2. Generate a new key
3. Update the local .env
4. Update Streamlit Secrets
5. Check Git history if necessary

▶️ Run the Web Application

streamlit run app.py

The application normally becomes available at:

http://localhost:8501

If port 8501 is already occupied:

streamlit run app.py --server.port 8502

🧪 Run Individual Tasks

Task 1 — FAQ & Keyword Search

python task1.py

Demonstrates:

FAQ data

Keyword matching

FAQ ID lookup

Category lookup

Task 2 — OpenRouter LLM

python task2.py

Demonstrates:

API configuration

OpenRouter communication

Grounded prompting

Error handling

Task 3 — Retrieval Comparison

python task3.py

Demonstrates:

Keyword Search
      ↓
TF-IDF Search
      ↓
Hybrid Search
      ↓
Confidence Ranking

Task 4 — CLI Support Agent

python task4.py

Demonstrates:

Conversational support

Retrieval

LLM orchestration

Conversation history

Fallback handling

Human escalation

☁️ Streamlit Community Cloud Deployment

SupportAI can be deployed using Streamlit Community Cloud.

Deployment Flow

GitHub Repository
       │
       ▼
Streamlit Community Cloud
       │
       ▼
Select Repository
       │
       ▼
Select main Branch
       │
       ▼
Set app.py
       │
       ▼
Configure Secrets
       │
       ▼
Deploy
       │
       ▼
🌐 Live SupportAI Application

Deployment Steps

Open Streamlit Community Cloud.

Sign in with GitHub.

Select the repository:

J-harshavardhan/Support_AI_Assistant

Select branch:

main

Set the application entry point:

app.py

Open Advanced settings.

Add the OpenRouter API key under Secrets.

Use TOML format:

OPENROUTER_API_KEY = "your_new_openrouter_key"

Save the configuration.

Deploy or reboot the application.

🔧 Configuration Behavior

SupportAI supports two configuration environments.

Local Development

.env
 │
 ▼
Python Dotenv
 │
 ▼
OPENROUTER_API_KEY

Streamlit Cloud

Streamlit Secrets
       │
       ▼
OPENROUTER_API_KEY

This keeps API credentials outside the application source code.

🖥️ Web Application Controls

The Streamlit application provides:

💬 New Conversation

Clears the current conversation state and starts a new support session.

🛟 Escalate to Human Support

Creates a mock support ticket for requests that require human assistance.

💡 Suggested Questions

Provides example questions for quickly testing the application.

🔎 FAQ Index

Allows users to search the FAQ knowledge base by topic or keyword.

💬 Chat Input

Users can enter natural-language questions and submit them through the chat interface.

🧪 Validation & Testing

The project has been validated across multiple layers.

Validation Area

Status

Python compilation

✅

Task 1 keyword search

✅

TF-IDF matching

✅

Hybrid search

✅

Confidence scoring

✅

Mocked LLM orchestration

✅

Missing API-key fallback

✅

OpenRouter error handling

✅

Streamlit startup

✅

Human escalation workflow

✅

🛡️ Safety & Grounding Strategy

SupportAI intentionally separates:

RETRIEVAL
    ↓
CONFIDENCE
    ↓
GENERATION

rather than allowing the LLM to independently determine the answer.

High-Confidence Request

User Question
      ↓
FAQ Match
      ↓
Confidence Check
      ↓
Grounded LLM
      ↓
Answer

Low-Confidence Request

User Question
      ↓
Weak / Unknown Match
      ↓
Confidence Check
      ↓
Safe Fallback
      ↓
Human Escalation

This architecture is designed to reduce the risk of unsupported customer-service responses.

⚠️ Limitations

SupportAI is intentionally built around a controlled FAQ knowledge base.

Current limitations include:

The FAQ knowledge base is relatively small.

Retrieval quality depends on the available FAQ corpus.

TF-IDF provides lexical/vector-space similarity rather than embedding-based semantic retrieval.

Confidence scores are retrieval scores and should not be interpreted as calibrated probabilities.

Human escalation currently uses a mock ticket workflow.

Conversation state is application-session based.

LLM availability depends on the configured OpenRouter model and account.

The project is intended for educational and demonstration purposes rather than production customer support.

🔮 Future Improvements

🔎 Retrieval

Embedding-based semantic retrieval

Vector database integration

Hybrid BM25 + embedding retrieval

Cross-encoder reranking

Query normalization

Multilingual retrieval

FAQ relevance evaluation

🧠 AI

Intent classification

Structured LLM responses

Hallucination detection

Grounding verification

Confidence calibration

Conversation-aware retrieval

Multi-turn intent tracking

👨‍💼 Support Operations

Real ticket-management integration

Ticket priority prediction

Agent dashboard

Support analytics

Conversation sentiment analysis

Customer history integration

SLA monitoring

☁️ Production Engineering

Authentication

Database-backed conversation history

API rate limiting

Automated CI/CD

Unit and integration test suite

Monitoring and observability

Structured application logging

Production deployment infrastructure

📈 Potential Production Architecture

                         ┌───────────────────┐
                         │       USER        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Web / Mobile    │
                         │      Client       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   API Gateway     │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │  Support Agent    │
                         └─────────┬─────────┘
                                   │
                       ┌───────────┴───────────┐
                       ▼                       ▼
                ┌─────────────┐         ┌─────────────┐
                │   Retriever │         │ Conversation│
                │             │         │   Memory    │
                └──────┬──────┘         └─────────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Keyword Search      Vector Search
             │                   │
             └─────────┬─────────┘
                       ▼
                    Reranker
                       │
                       ▼
                  Confidence
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Grounded LLM          Escalation
             │                   │
             ▼                   ▼
         Response          Human Agent

🎓 Learning Outcomes

This project demonstrates practical experience with:

Machine Learning

TF-IDF vectorization

Cosine similarity

Information retrieval

Similarity scoring

Ranking systems

Generative AI

LLM API integration

Grounded prompting

Retrieval-Augmented-style architecture

Controlled generation

LLM failure handling

Software Engineering

Modular Python architecture

Dataclasses

Error handling

Environment configuration

CLI applications

Web application development

Deployment

GitHub

Streamlit Community Cloud

Environment secrets

Application configuration

🧠 What Makes SupportAI Different?

SupportAI is not designed as a simple:

User → LLM → Answer

Instead, it follows:

User
 │
 ▼
FAQ Retrieval
 │
 ▼
Confidence Evaluation
 │
 ├─────────────────┐
 │                 │
 ▼                 ▼
Confident        Uncertain
 │                 │
 ▼                 ▼
Grounded LLM    Safe Fallback
 │                 │
 ▼                 ▼
Answer        Human Support

The goal is to make customer support more controlled, transparent, and reliable.

📌 Example Use Cases

SupportAI can be adapted for organizations that maintain structured support documentation.

Potential use cases include:

🛒 E-commerce customer support

💳 Billing support

📦 Order and delivery support

🔐 Account support

📧 Customer account management

🔄 Subscription support

🏢 Internal employee helpdesks

🎓 Educational institution support

💻 SaaS product support

📊 System Summary

Capability

SupportAI

FAQ Knowledge Base

✅

Keyword Retrieval

✅

TF-IDF Retrieval

✅

Cosine Similarity

✅

Hybrid Retrieval

✅

Confidence Scoring

✅

Grounded LLM Responses

✅

Conversation History

✅

API Error Handling

✅

FAQ Fallback

✅

Human Escalation

✅

Mock Ticket Generation

✅

Streamlit Interface

✅

Cloud Deployment

✅

🔐 Security Checklist

Before pushing the project to GitHub:

☑ .env is included in .gitignore
☑ API keys are not hardcoded
☑ API keys are not present in README
☑ API keys are not visible in screenshots
☑ API keys are not printed in logs
☑ .venv is ignored
☑ Python cache files are ignored

Recommended .gitignore:

# Environment
.env
.env.*

# Virtual environment
.venv/
venv/

# Python
__pycache__/
*.py[cod]
*.pyo

# IDE
.vscode/
.idea/

# Streamlit
.streamlit/secrets.toml

# OS
.DS_Store
Thumbs.db

🚀 Quick Start

For users who simply want to run SupportAI:

git clone https://github.com/J-harshavardhan/Support_AI_Assistant.git

cd Support_AI_Assistant

python -m venv .venv

Windows

.venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt

Configure the API key:

OPENROUTER_API_KEY=your_new_openrouter_key

Run the application:

streamlit run app.py

📚 Project Philosophy

The main idea behind SupportAI is:

Don't let the language model decide what is true. First retrieve trusted information, evaluate whether the match is reliable, and then use the model to communicate that information naturally.

The architecture combines:

       Information Retrieval
                +
        Machine Learning
                +
        Large Language Models
                +
       Confidence Routing
                +
        Human Escalation

📄 License

This project was created for educational and assessment purposes.

👨‍💻 Author

J. Harshavardhan

AI & ML Student

Project

🤖 SupportAI — Grounded Helpdesk Assistant

<a href="https://github.com/J-harshavardhan/Support_AI_Assistant">
  💻 View Source Code
</a>

  •  

<a href="https://harsha-support-ai-assistant.streamlit.app/">
  🚀 Try Live Demo
</a>

<p align="center">

🤖 SupportAI

<strong>Grounded answers. Confidence-aware retrieval. Safe escalation.</strong>

<br><br>

Built with 🐍 Python • 🎈 Streamlit • 📊 Scikit-learn • 🌐 OpenRouter

</p>
