import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sqlalchemy import create_engine, text
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

class SimpleSQLAssistant:
    def __init__(self):
        self.llm = None
        self.db_path = None
        self.engine = None
        
    def setup_llm(self, api_key):
        """Initialize the ChatGroq LLM"""
        try:
            self.llm = ChatGroq(
                api_key=api_key,
                model_name="llama-3.1-70b-versatile",
                temperature=0
            )
            return True
        except Exception as e:
            st.error(f"Error setting up LLM: {str(e)}")
            return False
    
    def connect_database(self, db_path):
        """Connect to SQLite database"""
        try:
            self.db_path = db_path
            self.engine = create_engine(f"sqlite:///{db_path}")
            return True
        except Exception as e:
            st.error(f"Error connecting to database: {str(e)}")
            return False
    
    def get_database_schema(self):
        """Get database schema information"""
        try:
            with self.engine.connect() as conn:
                # Get table names
                tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
                tables_result = conn.execute(text(tables_query))
                tables = [row[0] for row in tables_result]
                
                schema_info = ""
                for table in tables:
                    schema_info += f"\nTable: {table}\n"
                    
                    # Get column info
                    columns_query = f"PRAGMA table_info({table})"
                    columns_result = conn.execute(text(columns_query))
                    
                    for col in columns_result:
                        schema_info += f"  - {col[1]} ({col[2]})\n"
                
                return schema_info
        except Exception as e:
            return f"Error getting schema: {str(e)}"
    
    def natural_language_to_sql(self, question, schema_info):
        """Convert natural language question to SQL using LLM"""
        prompt_template = PromptTemplate(
            input_variables=["question", "schema"],
            template="""
You are a SQL expert. Based on the database schema below, write a SQL query to answer the user's question.

Database Schema:
{schema}

User Question: {question}

Important guidelines:
1. Only return the SQL query, nothing else
2. Use proper SQL syntax for SQLite
3. Make sure column names and table names match exactly with the schema
4. Use appropriate WHERE clauses, JOINs, and aggregations as needed
5. If the question asks for trends or time-based data, use appropriate date functions
6. For top/bottom queries, use LIMIT clause

SQL Query:
"""
        )
        
        try:
            prompt = prompt_template.format(question=question, schema=schema_info)
            response = self.llm.invoke(prompt)
            
            # Extract SQL query from response
            sql_query = response.content.strip()
            
            # Clean up the response (remove any extra formatting)
            sql_query = re.sub(r'^```sql\s*', '', sql_query, flags=re.IGNORECASE)
            sql_query = re.sub(r'\s*```$', '', sql_query)
            sql_query = sql_query.strip()
            
            return sql_query
        except Exception as e:
            return f"Error generating SQL: {str(e)}"
    
    def execute_sql_query(self, sql_query):
        """Execute SQL query and return results"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql_query))
                columns = result.keys()
                data = result.fetchall()
                
                if data:
                    df = pd.DataFrame(data, columns=columns)
                    return df, None
                else:
                    return None, "No data returned from query"
        except Exception as e:
            return None, f"Error executing query: {str(e)}"
    
    def process_question(self, question):
        """Process natural language question and return results"""
        if not self.llm or not self.engine:
            return None, None, "Assistant not properly initialized"
        
        # Get database schema
        schema_info = self.get_database_schema()
        
        # Convert question to SQL
        sql_query = self.natural_language_to_sql(question, schema_info)
        
        if sql_query.startswith("Error"):
            return None, sql_query, sql_query
        
        # Execute SQL query
        df, error = self.execute_sql_query(sql_query)
        
        if error:
            return None, sql_query, error
        
        return df, sql_query, None

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
            return None
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="SQL Assistant - Simple Version",
        page_icon="🗃️",
        layout="wide"
    )
    
    st.title("🗃️ SQL Assistant - AI-Powered Database Chat (Simple Version)")
    st.markdown("Chat with your database using natural language! Powered by LangChain and Groq.")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = SimpleSQLAssistant()
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
        
        # Database file selection
        st.subheader("Database Connection")
        
        # Check for available databases
        available_dbs = []
        for file in os.listdir("."):
            if file.endswith(".db"):
                available_dbs.append(file)
        
        if available_dbs:
            selected_db = st.selectbox("Choose database:", available_dbs)
        else:
            st.error("No .db files found in current directory")
            selected_db = None
        
        # Connect button
        if st.button("🔗 Connect to Database"):
            if not api_key:
                st.error("Please enter your Groq API key")
            elif not selected_db:
                st.error("Please select a database file")
            else:
                with st.spinner("Setting up AI assistant..."):
                    # Setup LLM
                    if st.session_state.assistant.setup_llm(api_key):
                        st.success("✅ LLM connected")
                        
                        # Connect to database
                        if st.session_state.assistant.connect_database(selected_db):
                            st.success("✅ Database connected")
                            st.session_state.db_connected = True
                        else:
                            st.error("❌ Failed to connect to database")
        
        # Database info
        if st.session_state.db_connected:
            st.subheader("📊 Database Info")
            if st.button("Show Schema"):
                schema = st.session_state.assistant.get_database_schema()
                st.code(schema, language="sql")
    
    # Main chat interface
    if st.session_state.db_connected:
        st.header("💬 Chat with your Database")
        
        # Chat input
        user_question = st.text_input(
            "Ask a question about your data:",
            placeholder="e.g., Show me all employees in the Engineering department"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_btn = st.button("🚀 Ask Question", type="primary")
        with col2:
            clear_btn = st.button("🗑️ Clear Chat")
        
        if clear_btn:
            st.session_state.chat_history = []
            st.rerun()
        
        if submit_btn and user_question:
            with st.spinner("🤖 AI is thinking..."):
                # Process the question
                df, sql_query, error = st.session_state.assistant.process_question(user_question)
                
                if error:
                    st.error(f"Error: {error}")
                else:
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": user_question,
                        "sql_query": sql_query,
                        "data": df
                    })
        
        # Display chat history
        if st.session_state.chat_history:
            st.header("📜 Chat History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {chat['question'][:50]}...", expanded=(i==0)):
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown(f"**Generated SQL:**")
                    st.code(chat['sql_query'], language="sql")
                    
                    if chat['data'] is not None and not chat['data'].empty:
                        st.markdown(f"**Results:**")
                        st.dataframe(chat['data'], use_container_width=True)
                        
                        # Visualization options
                        st.subheader("📊 Data Visualization")
                        
                        viz_col1, viz_col2 = st.columns(2)
                        
                        with viz_col1:
                            chart_type = st.selectbox(
                                "Choose visualization:",
                                ["auto", "bar", "line", "scatter", "pie", "histogram"],
                                key=f"chart_type_{i}"
                            )
                        
                        with viz_col2:
                            if st.button("📈 Generate Chart", key=f"viz_btn_{i}"):
                                fig = create_visualizations(chat['data'], chart_type)
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("Unable to create visualization for this data")
                    else:
                        st.info("No data returned from query")
        
        # Sample questions
        st.header("💡 Sample Questions")
        sample_questions = [
            "Show me all employees and their salaries",
            "What is the average salary by department?",
            "Which customer made the most orders?",
            "Show me the top 5 products by revenue",
            "How many employees are in each department?",
            "What are the monthly sales totals?"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(sample_questions):
            with cols[i % 2]:
                if st.button(f"📝 {question}", key=f"sample_{i}"):
                    st.session_state.sample_question = question
                    st.rerun()
        
        # Handle sample question selection
        if hasattr(st.session_state, 'sample_question'):
            user_question = st.session_state.sample_question
            del st.session_state.sample_question
            
            with st.spinner("🤖 AI is thinking..."):
                df, sql_query, error = st.session_state.assistant.process_question(user_question)
                
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.session_state.chat_history.append({
                        "question": user_question,
                        "sql_query": sql_query,
                        "data": df
                    })
            st.rerun()
    
    else:
        st.info("👆 Please configure your API key and connect to a database in the sidebar to start chatting!")
        
        # Show available databases
        st.subheader("🗃️ Available Databases")
        available_dbs = [f for f in os.listdir(".") if f.endswith(".db")]
        if available_dbs:
            for db in available_dbs:
                st.write(f"📄 {db}")
        else:
            st.write("No database files found. Make sure you have .db files in the current directory.")

if __name__ == "__main__":
    main()
