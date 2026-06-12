# 🤖 Multi-Agent AI Research System

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)
![AI Agents](https://img.shields.io/badge/AI-Multi--Agent_System-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

A powerful, fully autonomous Multi-Agent Artificial Intelligence system that takes any research topic and automatically searches the web, reads the top resources, writes a comprehensive report, and has a critic agent review and refine it.

## ✨ Features

Our architecture involves multiple specialized AI agents working together sequentially:
- 🔍 **Search Agent:** Autonomously searches the web for the most reliable and recent sources based on the user's topic.
- 📖 **Reader Agent:** Scrapes the selected top sources, cleans the content, and extracts key insights and raw notes.
- ✍️ **Writer Agent:** Compiles the scraped content and insights into a beautifully formatted, comprehensive research report.
- 🧐 **Critic Agent:** Reviews the generated report for tone, accuracy, and completeness, providing actionable feedback.
- 💻 **Streamlit UI:** A clean, modern web interface to easily interact with the agents and view the research pipeline step-by-step.

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/krishcode11/Multi-Agent-Ai-Research-System.git
cd Multi-Agent-Ai-Research-System
```

### 2. Set up Virtual Environment (Recommended)
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_search_api_key_here
# (Add any other keys your tools.py requires)
```

### 5. Run the Application
```bash
streamlit run app.py
```
*The app will automatically launch in your browser at `http://localhost:8501`.*

---

## 📂 Project Structure

```text
├── agents.py           # Contains the definitions for the Search, Reader, Writer, and Critic agents
├── tools.py            # Custom tools used by the agents (e.g., web scraping, search API wrappers)
├── pipeline.py         # The core logic linking the agents together sequentially
├── app.py              # The Streamlit web interface 
├── requirements.txt    # Project dependencies
└── README.md           # You are here!
```

---

## 🌐 Deploying to Streamlit Community Cloud

1. Create a [Streamlit Community Cloud](https://share.streamlit.io/) account.
2. Click **New app**.
3. Select this repository and the `app.py` file.
4. Go to **Advanced settings** > **Secrets** and paste your API keys from your `.env` file.
5. Click **Deploy!**

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/krishcode11/Multi-Agent-Ai-Research-System/issues).

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
