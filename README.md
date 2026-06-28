# ModaMind 🧠👗

### Multi-Agent Fashion Brand Intelligence Platform

Built for the **Google × Kaggle Agentic AI Capstone Competition**.

---

## Overview

ModaMind is a multi-agent AI platform that helps fashion brands make smarter business decisions by generating a comprehensive brand intelligence report. It combines trend forecasting, brand analysis, ethics verification, consumer psychology, influencer discovery, and content generation into a single collaborative AI workflow.

---

## Features

* 📈 Trend forecasting and market intelligence
* 🏷️ Brand positioning and competitor analysis
* 🌱 Sustainability and ethics auditing
* 🧠 Consumer psychology insights
* 🤝 Influencer recommendation engine
* ✍️ AI-generated marketing content
* 📄 Automated brand intelligence reports
* 🤖 Multi-agent orchestration with specialized AI agents

---

## Agent Architecture

1. Trend Scout Agent
2. Brand Analyst Agent
3. Ethics Auditor Agent
4. Consumer Psychology Agent
5. Influencer Matcher Agent
6. Synthesis Agent
7. Critic Agent
8. Content Agent
9. Report Agent
10. Orchestrator Agent (`main.py`)

---

## Tech Stack

* Python 3.11
* Google Gemini API (`google-genai` SDK)
* Gradio
* Requests
* Python Dotenv
* FPDF2

---

## Project Structure

```text
ModaMind/
├── agents/
├── utils/
├── app.py
├── main.py
├── test_api.py
├── README.md
└── .gitignore
```

---

## Installation

Install the required dependencies:

```bash
pip install google-genai gradio requests python-dotenv fpdf2
```

Create a `.env` file in the project root and add your Gemini API key:

```env
API_KEY_for_ModaMind=your_key_here
```

Run the application:

```bash
python app.py
```

---

## Future Roadmap

* Multi-agent collaboration using A2A
* MCP tool integration
* Real-time fashion trend analysis
* Professional PDF report generation
* Interactive analytics dashboard

---

## Author

**Janhavi Chauhan**

Computer Engineering Student
PVG's College of Engineering & Technology and Management, Pune

---

## License

This project was developed for educational purposes as part of the Google × Kaggle Agentic AI Capstone Competition.
