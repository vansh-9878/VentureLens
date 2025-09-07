# 🚀 VentureLens : A clear lens into Feasibility and Market reality

An AI-powered Startup Feasibility Checker service that evaluates startup ideas using a **multi-agent architecture**. The system works like a "virtual team": a **Planner agent** breaks down the analysis, and multiple specialized agents (Market Analyst, Competitor Scout, SWOT Analyst, and Financial Modeler) run in parallel to produce structured results. A **Synthesizer agent** then merges everything into a concise feasibility report with a GO / CONDITIONAL / NO-GO verdict.

---

## ✨ Features
- **Multi-agent architecture** built with LangGraph  
- **Parallel execution** of market, competitor, SWOT, and finance agents  
- **Structured JSON outputs** with Pydantic validation  
- **Up-to-date data fetching** via tools (web search, finance APIs, trends)  
- **Transparent results** – citations for market and competitor data  
- **Feasibility scoring** with weighted criteria (market, finance, competition, risks)  

---

## 🏗️ Architecture Overview

### Multi-Agent Workflow

1. **Planner Agent**: Receives startup idea and creates structured analysis plan
2. **Parallel Execution**: Four specialized agents run concurrently:
   - **Market Analyst**: TAM, growth, trends analysis
   - **Competitor Scout**: Direct/indirect competitor research  
   - **SWOT Analyst**: Strengths, weaknesses, opportunities, threats
   - **Financial Modeler**: Budget, runway, revenue projections
3. **Synthesizer Agent**: Combines outputs into final feasibility verdict

---

## 🛠️ Tech Stack
- **Python 3.12**  
- **LangGraph** for agent orchestration  
- **Pydantic** for schema enforcement  
- **APIs**: SerpAPI

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11 or higher
- Gemini API key (for LLM agents)
- SerpAPI key for web search

### Installation Steps

```bash
# Clone repository
git clone https://github.com/vansh-9878/VentureLens.git
cd VentureLens

# Install dependencies
pip install -r requirements.txt

```

## ▶️ Running the Backend

### Command Line Usage

Run the orchestrator with:

```bash
python main.py
```

### API Usage 

```bash
# Start FastAPI server
python backend.py

# Test endpoint
curl -X POST "http://localhost:8000/api/getResults" \
  -H "Content-Type: application/json" \
  -d '{"title":"MindCares","description" : "A chatbot that takes care of your mental health, knows everythin about you and becomes you best friends"}'
```

---

## 🤝 Contributing

I welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Add tests**: Ensure new code has test coverage
4. **Commit changes**: `git commit -m "Add amazing feature"`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Open Pull Request**

### Development Guidelines

- Use type hints throughout
- Add docstrings for all public methods
- Keep agent responsibilities focused and single-purpose
- Test both successful and error scenarios


---


**⭐ If this project helps validate your startup ideas, please star the repository!**
