# 🤖 Enhanced SQL Assistant

An intelligent SQL database chat interface powered by Groq AI models. Chat with your databases using natural language and get instant results with optional data visualizations.

![SQL Assistant Demo](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-FF6B35?style=for-the-badge&logoColor=white)

## ✨ Features

### 🤖 **Advanced AI Integration**
- **Multiple AI Models**: Choose from various Groq models with automatic fallback
- **Smart Model Selection**: Auto-detection finds the best working model
- **SQL Agent**: Intelligent query processing with LangChain SQL Agent
- **Streaming Responses**: Real-time AI responses for better user experience

### 💬 **Natural Language Querying**
- Ask questions in plain English
- Automatic SQL query generation
- Context-aware responses
- Example queries for quick start

### 📊 **Data Visualization**
- **Smart Visualization**: Only shows charts when explicitly requested
- **Multiple Chart Types**: Bar charts, pie charts, histograms, scatter plots, line charts
- **Interactive Plots**: Powered by Plotly for rich interactions
- **Auto-suggestions**: AI suggests the best visualization for your data

### 🎛️ **User-Friendly Interface**
- **Clean Chat Interface**: Intuitive conversation flow
- **Clear Chat**: Reset conversation history with one click
- **Database Schema Viewer**: Explore your database structure
- **Sample Database**: Included for immediate testing
- **CSV Export**: Download query results instantly

### 🔒 **Security & Reliability**
- **Read-only Operations**: Only SELECT queries allowed
- **Error Handling**: Robust error management and user feedback
- **Model Fallback**: Automatic switching if primary model fails
- **Safe SQL Generation**: Protected against SQL injection

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YuvvrajSingh/sql-gpt.git
cd sql-gpt
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
Create a `.env` file with your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from [Groq Console](https://console.groq.com/)

### 4. Run the Application
```bash
streamlit run app_enhanced_final.py
```

Or use the batch file on Windows:
```cmd
start.bat
```

## 📱 Available Applications

Choose from multiple app versions based on your needs:

| App | Description | Best For |
|-----|-------------|----------|
| `app_enhanced_final.py` | **🌟 Recommended** - Full-featured with SQL Agent | Production use |
| `app_robust.py` | Robust with model fallback | Reliability focused |
| `app_enhanced_fixed.py` | Enhanced features | Feature testing |
| `app_simple.py` | Basic functionality | Learning/Development |

## 💡 Example Queries

Try these example queries to get started:

### 📊 **Data Exploration**
- "Show all tables in the database"
- "Count total records in each table"
- "Show the first 10 records from any table"
- "Display column names and types for all tables"

### 📈 **Analytics Queries**
- "What are the top 5 customers by total order value?"
- "Show monthly sales trends for this year"
- "Which products have the highest profit margins?"
- "Find employees with salaries above average"

### 🎨 **Visualization Requests**
- "Create a bar chart of sales by region"
- "Show me a pie chart of product categories"
- "Visualize the distribution of employee salaries"
- "Plot the correlation between price and sales"

## 🗄️ Database Support

### **Built-in Sample Database**
- **Customers**: Company information and contacts
- **Products**: Product catalog with pricing
- **Orders**: Sales transactions and shipping
- **Employees**: Staff information and hierarchy
- **Order Details**: Line items and pricing

### **Custom Databases**
- **SQLite**: Upload your own `.db` files
- **MySQL**: Connect to remote MySQL databases (coming soon)
- **PostgreSQL**: Support planned for future releases

## 🛠️ Technical Architecture

### **AI Models (Groq)**
- **Primary**: Llama 3.1 70B Versatile (best for complex queries)
- **Fallback**: Llama 3.1 8B Instant (faster responses)
- **Alternative**: Gemma 2 9B IT (backup option)

### **Core Technologies**
- **Frontend**: Streamlit (Python web framework)
- **AI/ML**: LangChain + Groq API
- **Database**: SQLAlchemy (universal database toolkit)
- **Visualization**: Plotly (interactive charts)
- **Data Processing**: Pandas (data manipulation)

### **Key Components**
- **SQL Agent**: LangChain agent with SQL toolkit for intelligent query processing
- **Model Manager**: Automatic model selection and fallback handling
- **Query Processor**: Natural language to SQL conversion
- **Visualization Engine**: Smart chart generation based on data types
- **Security Layer**: SQL injection protection and query validation

## 📋 Requirements

### **System Requirements**
- Python 3.8 or higher
- 4GB+ RAM recommended
- Internet connection for AI model access

### **Python Dependencies**
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
python-dotenv>=1.0.0
langchain>=0.1.0
langchain-groq>=0.1.0
sqlalchemy>=2.0.0
```

## 🚀 Deployment Options

### **Streamlit Cloud** (Recommended)
1. Push code to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Add secrets for `GROQ_API_KEY`
4. Deploy with one click

### **Local Development**
```bash
streamlit run app_enhanced_final.py --server.port 8501
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Groq** for providing fast AI inference
- **LangChain** for the SQL agent framework
- **Streamlit** for the web framework
- **Plotly** for interactive visualizations

---

⭐ **Star this repository if you find it helpful!**

Made with ❤️ by [Yuvraj Singh](https://github.com/YuvvrajSingh)
| `app_simple.py` | Basic functionality | Learning/Development |
- **Data Processing**: Pandas

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd SQLGPT
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your API keys:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🎯 Getting Started

### Option 1: Use Sample Database

1. Enter your Groq API key in the sidebar
2. Select "Use Sample Database"
3. Click "Connect to Database"
4. Start asking questions!

### Option 2: Upload SQLite File

1. Enter your Groq API key
2. Select "Upload SQLite File"
3. Upload your `.db` file
4. Connect and start querying

### Option 3: Custom Database

1. Enter your Groq API key
2. Select "Custom Database URL"
3. Enter your database connection string
4. Connect and explore your data

## 💡 Sample Questions

Try these example queries with the sample database:

- "Show me all employees and their salaries"
- "What is the average salary by department?"
- "Which employee made the highest sales?"
- "Show me sales data for the last 6 months"
- "How many employees are in each department?"
- "What are the top 3 products by sales amount?"

## 🗄️ Sample Database Schema

The built-in sample database includes:

### Employees Table

- `id`: Primary key
- `name`: Employee name
- `department`: Department (Engineering, Marketing, Sales, HR)
- `salary`: Annual salary
- `hire_date`: Date of hiring
- `age`: Employee age

### Sales Table

- `id`: Primary key
- `employee_id`: Foreign key to employees
- `product`: Product/service sold
- `amount`: Sale amount
- `sale_date`: Date of sale

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)
- `DATABASE_URL`: Optional default database URL

### Supported Database URLs

- SQLite: `sqlite:///path/to/database.db`
- PostgreSQL: `postgresql://username:password@localhost:5432/dbname`
- MySQL: `mysql://username:password@localhost:3306/dbname`

## 📊 Visualization Features

The application automatically generates visualizations based on query results:

- **Bar Charts**: For categorical data with numeric values
- **Line Charts**: For time series data
- **Scatter Plots**: For correlation analysis
- **Pie Charts**: For distribution analysis
- **Histograms**: For frequency distributions
- **Data Tables**: Always available as fallback

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Dark/Light Mode**: Streamlit's built-in theme support
- **Real-time Feedback**: Streaming responses and progress indicators
- **Interactive Charts**: Zoom, pan, and explore visualizations
- **Copy/Export**: Easy data export capabilities

## 🔒 Security Considerations

- API keys are handled securely through environment variables
- Database connections use SQLAlchemy's secure connection methods
- No SQL injection vulnerabilities due to LangChain's parameterized queries
- Local file handling for uploaded databases

## 🚨 Troubleshooting

### Common Issues

1. **"Agent not initialized" error**:

   - Ensure your Groq API key is correct
   - Check database connection status

2. **Database connection fails**:

   - Verify database URL format
   - Check database accessibility
   - Ensure database drivers are installed

3. **Visualization not showing**:
   - Check if query returns data
   - Try different chart types
   - Ensure numeric columns exist for charts

## 🔮 Future Enhancements

- [ ] Support for more LLM providers (OpenAI, Anthropic, etc.)
- [ ] Advanced visualization options
- [ ] Query optimization suggestions
- [ ] Database performance monitoring
- [ ] Export functionality for reports
- [ ] Multi-database querying
- [ ] Custom chart templates
- [ ] Query history and favorites

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support and questions, please open an issue in the repository.

---

Built with ❤️ using LangChain, Streamlit, and Groq
