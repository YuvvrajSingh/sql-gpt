# 🤖 Enhanced SQL Assistant

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-FF6B35?style=for-the-badge&logoColor=white)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Transform your database queries with AI-powered natural language processing**

An intelligent SQL database chat interface that allows you to interact with your databases using plain English. Powered by Groq's lightning-fast AI models and LangChain's SQL agent framework, this tool makes database querying accessible to everyone.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage](#-usage)
- [🛠️ Installation](#️-installation)
- [🗄️ Database Support](#️-database-support)
- [🎨 Visualization](#-visualization)
- [⚙️ Configuration](#️-configuration)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [🆘 Support](#-support)

---

## ✨ Features

### 🧠 **AI-Powered Intelligence**
- **Multiple AI Models**: Choose from Groq's fastest models with automatic fallback
- **Smart SQL Generation**: Converts natural language to optimized SQL queries
- **Context Awareness**: Understands your database schema for better results
- **Intelligent Agent**: Uses LangChain SQL Agent for complex query processing

### 💬 **Natural Language Interface**
- **Plain English Queries**: Ask questions like "Show me top customers by sales"
- **Example Templates**: Pre-built queries to get you started quickly
- **Chat History**: Maintains conversation context for follow-up questions
- **Real-time Responses**: Streaming AI responses for immediate feedback

### 📊 **Smart Visualizations**
- **On-Demand Charts**: Request visualizations with phrases like "show me a chart"
- **Multiple Chart Types**: Bar, pie, line, scatter plots, and histograms
- **Auto-Suggestions**: AI recommends the best visualization for your data
- **Interactive Plots**: Powered by Plotly for rich, interactive experiences

### 🔒 **Security & Reliability**
- **Read-Only Operations**: Only SELECT queries are allowed for safety
- **SQL Injection Protection**: Built-in security measures
- **Error Handling**: Graceful error management with helpful feedback
- **Model Fallback**: Automatic switching if primary AI model fails

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Groq API key ([Get yours free here](https://console.groq.com/))

### 1️⃣ Clone & Setup
```bash
# Clone the repository
git clone https://github.com/YuvvrajSingh/sql-gpt.git
cd sql-gpt

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure API Key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3️⃣ Launch the App
```bash
streamlit run streamlit_app.py
```

🎉 **That's it!** Your SQL Assistant is now running at `http://localhost:8501`

---

## 📖 Usage

### Getting Started
1. **Connect to AI**: Enter your Groq API key in the sidebar
2. **Choose a Database**: Use the sample database or upload your own SQLite file
3. **Start Chatting**: Ask questions in natural language

### Example Conversations

#### 📊 Data Exploration
```
You: "What tables are in this database?"
Assistant: Shows all available tables with descriptions

You: "Show me the first 5 customers"
Assistant: Returns customer data in a neat table format
```

#### 📈 Analytics & Insights
```
You: "Which products sell the most?"
Assistant: Analyzes sales data and shows top products

You: "Create a bar chart of sales by region"
Assistant: Generates an interactive bar chart visualization
```

#### 🔍 Complex Queries
```
You: "Find customers who haven't ordered in the last 6 months"
Assistant: Writes and executes complex SQL with date calculations
```

---

## 🛠️ Installation

### Option 1: Standard Installation
```bash
# Clone repository
git clone https://github.com/YuvvrajSingh/sql-gpt.git
cd sql-gpt

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Development Setup
```bash
# Clone with development dependencies
git clone https://github.com/YuvvrajSingh/sql-gpt.git
cd sql-gpt

# Install in development mode
pip install -e .
pip install -r requirements.txt
```

### Dependencies Overview
| Package | Purpose | Version |
|---------|---------|---------|
| `streamlit` | Web interface framework | >=1.28.0 |
| `langchain` | AI agent framework | >=0.1.0 |
| `langchain-groq` | Groq AI integration | >=0.1.0 |
| `pandas` | Data manipulation | >=2.0.0 |
| `plotly` | Interactive visualizations | >=5.15.0 |
| `sqlalchemy` | Database toolkit | >=2.0.0 |

---

## 🗄️ Database Support

### Built-in Sample Database
The app includes a comprehensive sample database with:
- **Customers**: Company information and contacts (50+ records)
- **Products**: Product catalog with pricing (100+ items)
- **Orders**: Sales transactions (1000+ orders)
- **Employees**: Staff information and hierarchy
- **Order Details**: Detailed line items and metrics

### Supported Database Types
| Database | Status | File Extensions |
|----------|---------|----------------|
| SQLite | ✅ Full Support | `.db`, `.sqlite`, `.sqlite3` |
| MySQL | 🔄 Coming Soon | - |
| PostgreSQL | 🔄 Planned | - |
| SQL Server | 🔄 Planned | - |

### Upload Your Own Database
1. Click **"Upload SQLite Database"** in the sidebar
2. Select your `.db` file (max 200MB)
3. The app automatically reads the schema
4. Start querying immediately!

---

## 🎨 Visualization

### Chart Types Available
- **Bar Charts**: Perfect for categorical comparisons
- **Pie Charts**: Great for showing proportions
- **Line Charts**: Ideal for trends over time
- **Scatter Plots**: Explore correlations between variables
- **Histograms**: Visualize data distributions

### How to Request Charts
Simply mention visualization keywords in your queries:
```
"Show me a bar chart of sales by category"
"Create a pie chart of customer distribution"
"Plot the trend of orders over time"
"Visualize the correlation between price and quantity"
```

### Interactive Features
- **Zoom & Pan**: Explore data in detail
- **Hover Tooltips**: See exact values
- **Download**: Save charts as PNG images
- **Responsive**: Works on all screen sizes

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with these settings:
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
LOG_LEVEL=INFO
```

### AI Model Configuration
The app uses intelligent model selection:

1. **Primary**: Llama 3.1 70B Versatile (best accuracy)
2. **Fallback**: Llama 3.1 8B Instant (faster responses)
3. **Backup**: Gemma 2 9B IT (alternative option)

### Streamlit Configuration
Customize the app behavior in `.streamlit/config.toml`:
```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)
[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub account
4. Deploy from `streamlit_app.py`
5. Add your `GROQ_API_KEY` in secrets
6. Click "Deploy"!

### Local Development
```bash
# Standard run
streamlit run streamlit_app.py

# Custom port
streamlit run streamlit_app.py --server.port 8502

# Development mode with auto-reload
streamlit run streamlit_app.py --server.runOnSave true
```

### Docker Deployment
```bash
# Build image
docker build -t sql-assistant .

# Run container
docker run -p 8501:8501 -e GROQ_API_KEY=your_key sql-assistant
```

### Other Platforms
- **Heroku**: Use the included `Procfile`
- **Railway**: Connect GitHub repo directly
- **Render**: Deploy with auto-detect settings

---

## 🤝 Contributing

We love contributions! Here's how you can help:

### 🐛 Report Bugs
- Use the [issue tracker](https://github.com/YuvvrajSingh/sql-gpt/issues)
- Include steps to reproduce
- Add screenshots if helpful

### 💡 Suggest Features
- Open a [feature request](https://github.com/YuvvrajSingh/sql-gpt/issues/new)
- Describe your use case
- Explain why it would be valuable

### 🔧 Submit Code
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### 📝 Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to new functions
- Test your changes thoroughly
- Update documentation as needed

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability accepted

---

## 🆘 Support

### 📚 Documentation
- **Deployment Guide**: See [deploy.md](deploy.md)
- **API Reference**: Check the code documentation
- **Examples**: Browse the example queries in the app

### 💬 Get Help
- **GitHub Issues**: [Report bugs or ask questions](https://github.com/YuvvrajSingh/sql-gpt/issues)
- **Email**: Contact the maintainer directly
- **Discussions**: Join the community discussions

### 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not working | Verify key at [console.groq.com](https://console.groq.com/) |
| App won't start | Check Python version (3.8+ required) |
| Database upload fails | Ensure file is valid SQLite (.db) |
| Charts not showing | Try clearing browser cache |

### 🏷️ Version Information
- **Current Version**: 2.0.0
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12
- **OS Support**: Windows, macOS, Linux

---

## 🌟 Acknowledgments

Special thanks to:
- **[Groq](https://groq.com/)** for lightning-fast AI inference
- **[LangChain](https://langchain.com/)** for the powerful agent framework
- **[Streamlit](https://streamlit.io/)** for the amazing web framework
- **[Plotly](https://plotly.com/)** for interactive visualizations
- **Open Source Community** for inspiration and feedback

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/YuvvrajSingh/sql-gpt?style=social)
![GitHub forks](https://img.shields.io/github/forks/YuvvrajSingh/sql-gpt?style=social)
![GitHub issues](https://img.shields.io/github/issues/YuvvrajSingh/sql-gpt)
![GitHub last commit](https://img.shields.io/github/last-commit/YuvvrajSingh/sql-gpt)

---

<div align="center">

### 🚀 **Ready to revolutionize how you interact with databases?**

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

**[⭐ Star this repo](https://github.com/YuvvrajSingh/sql-gpt)** • **[🍴 Fork it](https://github.com/YuvvrajSingh/sql-gpt/fork)** • **[📝 Report issues](https://github.com/YuvvrajSingh/sql-gpt/issues)**

Made with ❤️ by [Yuvraj Singh](https://github.com/YuvvrajSingh)

</div>

