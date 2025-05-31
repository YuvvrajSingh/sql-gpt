# Configuration settings for SQL Assistant

# Default LLM settings
DEFAULT_MODEL = "mixtral-8x7b-32768"
DEFAULT_TEMPERATURE = 0
MAX_TOKENS = 4096

# Database settings
DEFAULT_DB_NAME = "sample_data.db"
SUPPORTED_DB_TYPES = [
    "sqlite",
    "postgresql", 
    "mysql",
    "mssql",
    "oracle"
]

# Visualization settings
DEFAULT_CHART_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
]

CHART_TYPES = {
    "bar": "Bar Chart",
    "line": "Line Chart", 
    "scatter": "Scatter Plot",
    "pie": "Pie Chart",
    "histogram": "Histogram",
    "box": "Box Plot",
    "heatmap": "Heatmap",
    "area": "Area Chart"
}

# Streamlit configuration
PAGE_CONFIG = {
    "page_title": "SQL Assistant - AI-Powered Database Chat",
    "page_icon": "🗃️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Sample queries for different database types
SAMPLE_QUERIES = {
    "basic": [
        "Show me all records from the employees table",
        "What is the total number of employees?",
        "List all unique departments",
        "Show me the highest paid employee"
    ],
    "analytics": [
        "What is the average salary by department?",
        "Show me sales trends over the last 6 months", 
        "Which products have the highest revenue?",
        "Calculate the total revenue for each region"
    ],
    "advanced": [
        "Find employees whose salary is above the department average",
        "Show me the top 5 customers by total order value",
        "Calculate the monthly growth rate in sales",
        "Identify seasonal patterns in our data"
    ]
}

# Error messages
ERROR_MESSAGES = {
    "no_api_key": "Please enter your Groq API key to continue",
    "db_connection_failed": "Failed to connect to database. Please check your connection settings.",
    "query_failed": "Query execution failed. Please check your question and try again.",
    "no_data": "No data found for your query",
    "visualization_error": "Unable to create visualization for this data"
}
