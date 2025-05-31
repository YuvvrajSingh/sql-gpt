import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
import re
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sqlalchemy import create_engine, text, inspect
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

class EnhancedSQLAssistant:
    def __init__(self):
        self.llm = None
        self.db_path = None
        self.engine = None
        self.schema_info = None
        
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
        """Connect to SQLite database and extract schema"""
        try:
            self.db_path = db_path
            self.engine = create_engine(f"sqlite:///{db_path}")
            
            # Get schema information
            inspector = inspect(self.engine)
            self.schema_info = {}
            
            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                foreign_keys = inspector.get_foreign_keys(table_name)
                indexes = inspector.get_indexes(table_name)
                
                self.schema_info[table_name] = {
                    'columns': [(col['name'], str(col['type'])) for col in columns],
                    'foreign_keys': foreign_keys,
                    'indexes': indexes
                }
            
            return True
        except Exception as e:
            st.error(f"Error connecting to database: {str(e)}")
            return False
    
    def get_schema_description(self):
        """Generate a comprehensive schema description for the LLM"""
        if not self.schema_info:
            return "No schema information available."
        
        description = "Database Schema:\n\n"
        
        for table_name, info in self.schema_info.items():
            description += f"Table: {table_name}\n"
            description += "Columns:\n"
            for col_name, col_type in info['columns']:
                description += f"  - {col_name} ({col_type})\n"
            
            if info['foreign_keys']:
                description += "Foreign Keys:\n"
                for fk in info['foreign_keys']:
                    description += f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}\n"
            
            description += "\n"
        
        return description
    
    def get_sample_data(self, table_name, limit=3):
        """Get sample data from a table"""
        try:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            df = pd.read_sql_query(query, self.engine)
            return df.to_string(index=False)
        except Exception as e:
            return f"Error getting sample data: {str(e)}"
    
    def generate_sql_query(self, natural_language_query):
        """Generate SQL query from natural language using LLM"""
        if not self.llm or not self.schema_info:
            return None, "LLM or database not initialized"
        
        # Get schema description
        schema_desc = self.get_schema_description()
        
        # Get sample data for context
        sample_data = ""
        for table_name in list(self.schema_info.keys())[:3]:  # Only first 3 tables
            sample_data += f"\nSample data from {table_name}:\n"
            sample_data += self.get_sample_data(table_name, 2)
            sample_data += "\n"
        
        prompt_template = PromptTemplate(
            input_variables=["schema", "sample_data", "question"],
            template="""
You are an expert SQL query generator. Given the database schema and sample data below, generate a SQL query to answer the user's question.

{schema}

{sample_data}

User Question: {question}

Important Instructions:
1. Generate ONLY a valid SQL query, no explanations
2. Use proper SQLite syntax
3. Include appropriate JOINs when needed
4. Use aggregate functions when appropriate
5. Add LIMIT clauses for large result sets (default LIMIT 100)
6. Use proper column aliases for readability
7. Ensure the query is safe and doesn't modify data

SQL Query:
"""
        )
        
        try:
            prompt = prompt_template.format(
                schema=schema_desc,
                sample_data=sample_data,
                question=natural_language_query
            )
            
            response = self.llm.invoke(prompt)
            sql_query = response.content.strip()
            
            # Clean up the response - remove any markdown formatting
            sql_query = re.sub(r'```sql\n?', '', sql_query)
            sql_query = re.sub(r'```\n?', '', sql_query)
            sql_query = sql_query.strip()
            
            return sql_query, None
        except Exception as e:
            return None, f"Error generating query: {str(e)}"
    
    def execute_query(self, sql_query):
        """Execute SQL query and return results"""
        try:
            # Security check - only allow SELECT statements
            if not sql_query.strip().upper().startswith('SELECT'):
                return None, "Only SELECT queries are allowed for security reasons"
            
            df = pd.read_sql_query(sql_query, self.engine)
            return df, None
        except Exception as e:
            return None, f"Error executing query: {str(e)}"
    
    def suggest_visualizations(self, df, query):
        """Suggest appropriate visualizations based on data"""
        if df is None or df.empty:
            return []
        
        suggestions = []
        
        # Check for numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
            suggestions.append({
                'type': 'bar',
                'title': 'Bar Chart',
                'description': f'Show {numeric_cols[0]} by {categorical_cols[0]}'
            })
            
            if len(numeric_cols) >= 2:
                suggestions.append({
                    'type': 'scatter',
                    'title': 'Scatter Plot',
                    'description': f'Show relationship between {numeric_cols[0]} and {numeric_cols[1]}'
                })
        
        if len(numeric_cols) >= 1:
            suggestions.append({
                'type': 'histogram',
                'title': 'Histogram',
                'description': f'Distribution of {numeric_cols[0]}'
            })
        
        if len(categorical_cols) >= 1:
            suggestions.append({
                'type': 'pie',
                'title': 'Pie Chart',
                'description': f'Distribution of {categorical_cols[0]}'
            })
        
        return suggestions
    
    def create_visualization(self, df, viz_type, x_col=None, y_col=None):
        """Create visualization based on type and columns"""
        try:
            if viz_type == 'bar':
                fig = px.bar(df, x=x_col, y=y_col, title=f'{y_col} by {x_col}')
            elif viz_type == 'scatter':
                fig = px.scatter(df, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
            elif viz_type == 'histogram':
                fig = px.histogram(df, x=x_col, title=f'Distribution of {x_col}')
            elif viz_type == 'pie':
                # Group by the column and count
                pie_data = df[x_col].value_counts().reset_index()
                pie_data.columns = [x_col, 'count']
                fig = px.pie(pie_data, values='count', names=x_col, title=f'Distribution of {x_col}')
            elif viz_type == 'line':
                fig = px.line(df, x=x_col, y=y_col, title=f'{y_col} over {x_col}')
            else:
                return None
            
            return fig
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            return None
    
    def is_visualization_requested(self, query):
        """Check if the user is asking for a visualization"""
        viz_keywords = [
            'chart', 'graph', 'plot', 'visualize', 'visualization', 'show chart',
            'bar chart', 'pie chart', 'line chart', 'scatter plot', 'histogram',
            'draw', 'display chart', 'create chart', 'generate chart'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in viz_keywords)

def main():
    st.set_page_config(
        page_title="Enhanced SQL Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Enhanced SQL Assistant")
    st.markdown("Chat with your SQL database using natural language!")
      # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = EnhancedSQLAssistant()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    if 'show_visualization' not in st.session_state:
        st.session_state.show_visualization = False
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input("Groq API Key", type="password", 
                               value=os.getenv("GROQ_API_KEY", ""))
        
        if api_key and not st.session_state.assistant.llm:
            if st.session_state.assistant.setup_llm(api_key):
                st.success("✅ LLM connected!")
        
        # Database selection
        st.header("Database")
        
        # Check for sample database
        sample_db_path = "extended_sample_data.db"
        if os.path.exists(sample_db_path):
            if st.button("Use Sample Database"):
                if st.session_state.assistant.connect_database(sample_db_path):
                    st.success("✅ Connected to sample database!")
        
        # File upload for custom database
        uploaded_file = st.file_uploader("Upload SQLite Database", type=['db', 'sqlite', 'sqlite3'])
        if uploaded_file:
            # Save uploaded file
            with open("uploaded_database.db", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if st.session_state.assistant.connect_database("uploaded_database.db"):
                st.success("✅ Database uploaded and connected!")
        
        # Display schema information
        if st.session_state.assistant.schema_info:
            st.header("Database Schema")
            for table_name, info in st.session_state.assistant.schema_info.items():
                with st.expander(f"Table: {table_name}"):
                    st.write("**Columns:**")
                    for col_name, col_type in info['columns']:
                        st.write(f"• {col_name} ({col_type})")
      # Main chat interface
    if st.session_state.assistant.llm and st.session_state.assistant.schema_info:
        
        # Chat controls and example queries
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.header("💬 Chat with your Database")
        
        with col2:
            if st.button("🗑️ Clear Chat", help="Clear chat history"):
                st.session_state.chat_history = []
                st.session_state.current_data = None
                st.rerun()
        
        # Example queries section
        with st.expander("💡 Example Queries (click to use)"):
            example_queries = [
                "Show all tables in the database",
                "Count total records in each table", 
                "Show the first 10 records from any table",
                "Find records with null values",
                "Show table with the most records",
                "Display column names and types for all tables"
            ]
            
            cols = st.columns(2)
            for i, example in enumerate(example_queries):
                with cols[i % 2]:
                    if st.button(example, key=f"example_{i}"):
                        st.session_state.pending_query = example
          # Chat input
        user_query = st.chat_input("Ask me anything about your database...")
        
        # Handle example query clicks
        if 'pending_query' in st.session_state:
            user_query = st.session_state.pending_query
            del st.session_state.pending_query
        
        if user_query:
            # Check if visualization is requested
            visualization_requested = st.session_state.assistant.is_visualization_requested(user_query)
            
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            # Generate SQL query
            with st.spinner("Generating SQL query..."):
                sql_query, error = st.session_state.assistant.generate_sql_query(user_query)
            
            if error:
                st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {error}"})
            else:
                # Execute query
                with st.spinner("Executing query..."):
                    df, exec_error = st.session_state.assistant.execute_query(sql_query)
                  if exec_error:
                    st.session_state.chat_history.append({"role": "assistant", "content": f"SQL Error: {exec_error}"})
                else:
                    # Store current data for visualization
                    st.session_state.current_data = df
                    st.session_state.show_visualization = visualization_requested
                    
                    # Add results to chat history
                    result_message = f"**Generated SQL:**\n```sql\n{sql_query}\n```\n\n**Results:** {len(df)} rows returned"
                    if visualization_requested:
                        result_message += "\n\n*Visualization options will be shown below the results.*"
                    st.session_state.chat_history.append({"role": "assistant", "content": result_message})
                    if visualization_requested:
                        result_message += "\n\n*Visualization options will be shown below the results.*"
                    st.session_state.chat_history.append({"role": "assistant", "content": result_message})
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Display current results and visualization options
        if st.session_state.current_data is not None and not st.session_state.current_data.empty:
            st.header("Query Results")
            
            # Display data table
            st.dataframe(st.session_state.current_data, use_container_width=True)
              # Download button
            csv = st.session_state.current_data.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )
            
            # Visualization section - only show when requested
            if hasattr(st.session_state, 'show_visualization') and st.session_state.show_visualization:
                st.header("📈 Data Visualization")
                
                # Get visualization suggestions
                suggestions = st.session_state.assistant.suggest_visualizations(
                    st.session_state.current_data, 
                    st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""                )
                
                if suggestions:
                    # Create columns for visualization controls
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        viz_type = st.selectbox("Chart Type", 
                                              [s['type'] for s in suggestions],
                                              format_func=lambda x: next(s['title'] for s in suggestions if s['type'] == x))
                    
                    # Get column options
                    numeric_cols = st.session_state.current_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
                    categorical_cols = st.session_state.current_data.select_dtypes(include=['object']).columns.tolist()
                    all_cols = st.session_state.current_data.columns.tolist()
                    
                    with col2:
                        if viz_type in ['bar', 'scatter', 'line']:
                            x_col = st.selectbox("X-axis", all_cols)
                        elif viz_type in ['histogram', 'pie']:
                            x_col = st.selectbox("Column", all_cols)
                        else:
                            x_col = None
                    
                    with col3:
                        if viz_type in ['bar', 'scatter', 'line']:
                            y_col = st.selectbox("Y-axis", numeric_cols if numeric_cols else all_cols)
                        else:
                            y_col = None
                    
                    # Create and display visualization
                    if st.button("Create Visualization"):
                        fig = st.session_state.assistant.create_visualization(
                            st.session_state.current_data, viz_type, x_col, y_col
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No suitable visualizations available for this data.")
            else:
                st.info("💡 **Tip:** Ask for a chart or visualization in your query to see data visualization options!")
                st.markdown("**Example:** *'Show me a bar chart of sales by region'* or *'Create a pie chart of customer distribution'*")
    
    else:
        st.info("Please configure your API key and connect to a database to start chatting!")
        
        # Quick start section
        st.header("Quick Start")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **1. Get your Groq API Key**
            - Visit [console.groq.com](https://console.groq.com/)
            - Create an account and get your API key
            - Enter it in the sidebar
            """)
        
        with col2:
            st.markdown("""
            **2. Connect to Database**
            - Use the sample database (if available)
            - Or upload your own SQLite database
            - Schema will be displayed in sidebar
            """)
        
        st.markdown("""
        **3. Start Chatting**
        - Ask questions in natural language
        - "Show me all customers from New York"
        - "What are the top 5 selling products?"
        - "Calculate total revenue by month"
        """)

if __name__ == "__main__":
    main()
