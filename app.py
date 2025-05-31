import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sqlite3
import os
from dotenv import load_dotenv

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

class SQLAssistant:
    def __init__(self):
        self.db = None
        self.agent = None
        self.llm = None
        
    def setup_llm(self, api_key):
        """Initialize the ChatGroq LLM"""
        try:
            self.llm = ChatGroq(
                api_key=api_key,
                model_name="mixtral-8x7b-32768",
                temperature=0
            )
            return True
        except Exception as e:
            st.error(f"Error setting up LLM: {str(e)}")
            return False
    
    def connect_database(self, db_path=None, db_url=None):
        """Connect to database - SQLite by default or custom URL"""
        try:
            if db_url:
                self.db = SQLDatabase.from_uri(db_url)
            elif db_path:
                # For SQLite
                db_uri = f"sqlite:///{db_path}"
                self.db = SQLDatabase.from_uri(db_uri)
            else:
                # Create default sample database
                self.create_sample_database()
                db_uri = "sqlite:///sample_data.db"
                self.db = SQLDatabase.from_uri(db_uri)
            
            return True
        except Exception as e:
            st.error(f"Error connecting to database: {str(e)}")
            return False
    
    def create_sample_database(self):
        """Create a sample database with demo data"""
        conn = sqlite3.connect('sample_data.db')
        cursor = conn.cursor()
        
        # Create employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                hire_date DATE NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        
        # Create sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                employee_id INTEGER,
                product TEXT NOT NULL,
                amount REAL NOT NULL,
                sale_date DATE NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # Insert sample data
        employees_data = [
            (1, 'John Doe', 'Engineering', 75000, '2022-01-15', 28),
            (2, 'Jane Smith', 'Marketing', 65000, '2021-03-20', 32),
            (3, 'Bob Johnson', 'Sales', 55000, '2023-06-10', 25),
            (4, 'Alice Brown', 'Engineering', 80000, '2020-11-05', 35),
            (5, 'Charlie Wilson', 'HR', 60000, '2022-08-12', 29),
            (6, 'Diana Davis', 'Sales', 58000, '2023-02-28', 27),
            (7, 'Eva Martinez', 'Marketing', 67000, '2021-09-15', 31),
            (8, 'Frank Lee', 'Engineering', 72000, '2022-04-03', 26)
        ]
        
        sales_data = [
            (1, 1, 'Software License', 15000, '2024-01-15'),
            (2, 3, 'Consulting Service', 25000, '2024-01-20'),
            (3, 6, 'Hardware', 8000, '2024-02-10'),
            (4, 3, 'Training', 12000, '2024-02-15'),
            (5, 6, 'Software License', 18000, '2024-03-05'),
            (6, 1, 'Consulting Service', 30000, '2024-03-12'),
            (7, 3, 'Hardware', 9500, '2024-04-08'),
            (8, 6, 'Training', 14000, '2024-04-20')
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?, ?, ?)', employees_data)
        cursor.executemany('INSERT OR REPLACE INTO sales VALUES (?, ?, ?, ?, ?)', sales_data)
        
        conn.commit()
        conn.close()
    
    def setup_agent(self):
        """Create the SQL agent"""
        if not self.db or not self.llm:
            return False
        
        try:
            toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            
            self.agent = create_sql_agent(
                llm=self.llm,
                toolkit=toolkit,
                verbose=True,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True
            )
            return True
        except Exception as e:
            st.error(f"Error setting up agent: {str(e)}")
            return False
    
    def query_database(self, question, callback_handler=None):
        """Query the database using natural language"""
        if not self.agent:
            return "Agent not initialized. Please check your setup."
        
        try:
            if callback_handler:
                response = self.agent.run(question, callbacks=[callback_handler])
            else:
                response = self.agent.run(question)
            return response
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def get_query_result_as_dataframe(self, sql_query):
        """Execute SQL query and return as DataFrame for visualization"""
        try:
            engine = create_engine(self.db.engine.url)
            df = pd.read_sql_query(text(sql_query), engine)
            return df
        except Exception as e:
            st.error(f"Error executing SQL query: {str(e)}")
            return None

def create_visualizations(df, chart_type="auto"):
    """Create visualizations based on the DataFrame"""
    if df is None or df.empty:
        return None
    
    # Determine chart type automatically if not specified
    if chart_type == "auto":
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(numeric_cols) >= 2:
            chart_type = "scatter"
        elif len(numeric_cols) == 1 and len(categorical_cols) >= 1:
            chart_type = "bar"
        elif len(categorical_cols) >= 1:
            chart_type = "pie"
        else:
            chart_type = "table"
    
    try:
        if chart_type == "bar" and len(df.columns) >= 2:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                        title=f"Bar Chart: {df.columns[1]} by {df.columns[0]}")
        
        elif chart_type == "line" and len(df.columns) >= 2:
            fig = px.line(df, x=df.columns[0], y=df.columns[1], 
                         title=f"Line Chart: {df.columns[1]} over {df.columns[0]}")
        
        elif chart_type == "scatter" and len(df.columns) >= 2:
            fig = px.scatter(df, x=df.columns[0], y=df.columns[1], 
                           title=f"Scatter Plot: {df.columns[1]} vs {df.columns[0]}")
        
        elif chart_type == "pie" and len(df.columns) >= 2:
            fig = px.pie(df, names=df.columns[0], values=df.columns[1], 
                        title=f"Pie Chart: {df.columns[1]} by {df.columns[0]}")
        
        elif chart_type == "histogram" and len(df.columns) >= 1:
            numeric_col = df.select_dtypes(include=['number']).columns[0]
            fig = px.histogram(df, x=numeric_col, title=f"Histogram: {numeric_col}")
        
        else:
            # Default to table view
            return None
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="SQL Assistant - AI-Powered Database Chat",
        page_icon="🗃️",
        layout="wide"
    )
    
    st.title("🗃️ SQL Assistant - AI-Powered Database Chat")
    st.markdown("Chat with your database using natural language! Powered by LangChain and Groq.")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = SQLAssistant()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'db_connected' not in st.session_state:
        st.session_state.db_connected = False
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Groq API Key",
            value=os.getenv("GROQ_API_KEY", ""),
            type="password",
            help="Enter your Groq API key"
        )
        
        # Database connection options
        st.subheader("Database Connection")
        db_option = st.radio(
            "Choose database option:",
            ["Use Sample Database", "Upload SQLite File", "Custom Database URL"]
        )
        
        if db_option == "Upload SQLite File":
            uploaded_file = st.file_uploader("Choose SQLite file", type=['db', 'sqlite', 'sqlite3'])
            if uploaded_file:
                # Save uploaded file
                with open("uploaded_database.db", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                db_path = "uploaded_database.db"
            else:
                db_path = None
        elif db_option == "Custom Database URL":
            db_url = st.text_input(
                "Database URL",
                placeholder="sqlite:///path/to/db.db or postgresql://user:pass@host:port/db"
            )
        else:
            db_path = None
            db_url = None
        
        # Connect button
        if st.button("🔗 Connect to Database"):
            if not api_key:
                st.error("Please enter your Groq API key")
            else:
                with st.spinner("Setting up AI assistant..."):
                    # Setup LLM
                    if st.session_state.assistant.setup_llm(api_key):
                        st.success("✅ LLM connected")
                        
                        # Connect to database
                        if db_option == "Upload SQLite File" and db_path:
                            success = st.session_state.assistant.connect_database(db_path=db_path)
                        elif db_option == "Custom Database URL" and db_url:
                            success = st.session_state.assistant.connect_database(db_url=db_url)
                        else:
                            success = st.session_state.assistant.connect_database()
                        
                        if success:
                            st.success("✅ Database connected")
                            
                            # Setup agent
                            if st.session_state.assistant.setup_agent():
                                st.success("✅ SQL Agent ready")
                                st.session_state.db_connected = True
                            else:
                                st.error("❌ Failed to setup SQL agent")
                        else:
                            st.error("❌ Failed to connect to database")
        
        # Database info
        if st.session_state.db_connected and st.session_state.assistant.db:
            st.subheader("📊 Database Info")
            try:
                tables = st.session_state.assistant.db.get_usable_table_names()
                st.write(f"**Tables:** {', '.join(tables)}")
                
                # Show table schemas
                if st.checkbox("Show table schemas"):
                    for table in tables:
                        with st.expander(f"Table: {table}"):
                            table_info = st.session_state.assistant.db.get_table_info([table])
                            st.code(table_info, language="sql")
            except:
                st.write("Unable to fetch database info")
    
    # Main chat interface
    if st.session_state.db_connected:
        st.header("💬 Chat with your Database")
        
        # Chat input
        user_question = st.text_input(
            "Ask a question about your data:",
            placeholder="e.g., Show me all employees in the Engineering department"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit_btn = st.button("🚀 Ask Question", type="primary")
        with col2:
            clear_btn = st.button("🗑️ Clear Chat")
        
        if clear_btn:
            st.session_state.chat_history = []
            st.rerun()
        
        if submit_btn and user_question:
            with st.spinner("🤖 AI is thinking..."):
                # Create callback handler for streaming
                callback_handler = StreamlitCallbackHandler(st.container())
                
                # Get response
                response = st.session_state.assistant.query_database(
                    user_question, 
                    callback_handler
                )
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": user_question,
                    "response": response
                })
        
        # Display chat history
        if st.session_state.chat_history:
            st.header("📜 Chat History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {chat['question'][:50]}...", expanded=(i==0)):
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown(f"**Answer:** {chat['response']}")
                    
                    # Try to extract and visualize SQL results
                    if "SELECT" in chat['response'].upper():
                        st.subheader("📊 Data Visualization")
                        
                        # Extract SQL query from response (basic extraction)
                        import re
                        sql_match = re.search(r'```sql\n(.*?)\n```', chat['response'], re.DOTALL)
                        if not sql_match:
                            sql_match = re.search(r'SELECT.*?(?=\n\n|\Z)', chat['response'], re.DOTALL | re.IGNORECASE)
                        
                        if sql_match:
                            sql_query = sql_match.group(1) if sql_match.group(1) else sql_match.group(0)
                            sql_query = sql_query.strip()
                            
                            try:
                                df = st.session_state.assistant.get_query_result_as_dataframe(sql_query)
                                
                                if df is not None and not df.empty:
                                    # Show data table
                                    st.dataframe(df, use_container_width=True)
                                    
                                    # Visualization options
                                    viz_col1, viz_col2 = st.columns(2)
                                    
                                    with viz_col1:
                                        chart_type = st.selectbox(
                                            "Choose visualization:",
                                            ["auto", "bar", "line", "scatter", "pie", "histogram"],
                                            key=f"chart_type_{i}"
                                        )
                                    
                                    with viz_col2:
                                        if st.button("📈 Generate Chart", key=f"viz_btn_{i}"):
                                            fig = create_visualizations(df, chart_type)
                                            if fig:
                                                st.plotly_chart(fig, use_container_width=True)
                                            else:
                                                st.info("Unable to create visualization for this data")
                            except Exception as e:
                                st.error(f"Error processing SQL result: {str(e)}")
        
        # Sample questions
        st.header("💡 Sample Questions")
        sample_questions = [
            "Show me all employees and their salaries",
            "What is the average salary by department?",
            "Which employee made the highest sales?",
            "Show me sales data for the last 6 months",
            "How many employees are in each department?",
            "What are the top 3 products by sales amount?"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(sample_questions):
            with cols[i % 2]:
                if st.button(f"📝 {question}", key=f"sample_{i}"):
                    # Set the question in the input and trigger processing
                    st.session_state.sample_question = question
                    st.rerun()
        
        # Handle sample question selection
        if hasattr(st.session_state, 'sample_question'):
            user_question = st.session_state.sample_question
            del st.session_state.sample_question
            
            with st.spinner("🤖 AI is thinking..."):
                callback_handler = StreamlitCallbackHandler(st.container())
                response = st.session_state.assistant.query_database(user_question, callback_handler)
                
                st.session_state.chat_history.append({
                    "question": user_question,
                    "response": response
                })
            st.rerun()
    
    else:
        st.info("👆 Please configure your API key and connect to a database in the sidebar to start chatting!")
        
        # Show sample database info
        st.subheader("🗃️ Sample Database Preview")
        st.markdown("""
        The sample database includes:
        - **Employees table**: Employee information with departments, salaries, and hire dates
        - **Sales table**: Sales transactions linked to employees
        
        Perfect for testing queries like:
        - "Show me all employees in Engineering"
        - "What's the average salary by department?"
        - "Which salesperson had the highest sales?"
        """)

if __name__ == "__main__":
    main()
