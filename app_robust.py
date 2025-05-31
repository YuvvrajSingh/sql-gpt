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
from models_config import AVAILABLE_MODELS, DEFAULT_MODEL, FALLBACK_MODELS

# Load environment variables
load_dotenv()

class RobustSQLAssistant:
    def __init__(self):
        self.llm = None
        self.db_path = None
        self.engine = None
        self.current_model = None
        
    def setup_llm(self, api_key, preferred_model=None):
        """Initialize the ChatGroq LLM with automatic fallback"""
        models_to_try = [preferred_model] if preferred_model else [DEFAULT_MODEL] + FALLBACK_MODELS
        
        for model_name in models_to_try:
            if model_name is None:
                continue
                
            try:
                self.llm = ChatGroq(
                    api_key=api_key,
                    model_name=model_name,
                    temperature=0
                )
                # Test the model with a simple query
                test_response = self.llm.invoke("Hello")
                self.current_model = model_name
                return True, f"Successfully connected using {AVAILABLE_MODELS.get(model_name, {}).get('name', model_name)}"
            except Exception as e:
                error_msg = str(e)
                if "decommissioned" in error_msg.lower() or "not supported" in error_msg.lower():
                    continue  # Try next model
                else:
                    return False, f"Error with {model_name}: {error_msg}"
        
        return False, "All available models failed. Please check your API key and try again."
    
    def connect_database(self, db_path):
        """Connect to SQLite database"""
        try:
            self.db_path = db_path
            self.engine = create_engine(f"sqlite:///{db_path}")
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            return True, "Database connected successfully"
        except Exception as e:
            return False, f"Error connecting to database: {str(e)}"
    
    def get_database_schema(self):
        """Get database schema information"""
        try:
            query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
            tables = pd.read_sql_query(query, self.engine)
            
            schema_info = {}
            for table in tables['name']:
                # Get column information
                columns_query = f"PRAGMA table_info({table})"
                columns = pd.read_sql_query(columns_query, self.engine)
                schema_info[table] = columns.to_dict('records')
            
            return schema_info
        except Exception as e:
            st.error(f"Error getting schema: {str(e)}")
            return {}
    
    def get_sample_data(self, table_name, limit=3):
        """Get sample data from a table"""
        try:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            df = pd.read_sql_query(query, self.engine)
            return df
        except Exception as e:
            st.error(f"Error getting sample data: {str(e)}")
            return pd.DataFrame()
    
    def generate_sql_query(self, natural_language_query):
        """Generate SQL query from natural language using LLM"""
        if not self.llm:
            return None, "LLM not initialized"
        
        # Get schema information
        schema_info = self.get_database_schema()
        if not schema_info:
            return None, "Could not retrieve database schema"
        
        # Build schema description
        schema_desc = "Database Schema:\n"
        for table_name, columns in schema_info.items():
            schema_desc += f"\nTable: {table_name}\n"
            for col in columns:
                schema_desc += f"  - {col['name']} ({col['type']})\n"
        
        # Get sample data
        sample_data = "\nSample Data:\n"
        for table_name in list(schema_info.keys())[:3]:  # First 3 tables
            sample_df = self.get_sample_data(table_name, 2)
            if not sample_df.empty:
                sample_data += f"\n{table_name}:\n{sample_df.to_string(index=False)}\n"
        
        prompt_template = PromptTemplate(
            input_variables=["schema", "sample_data", "question"],
            template="""You are an expert SQL query generator. Generate a SQL query for the given question using the database schema below.

{schema}

{sample_data}

User Question: {question}

Instructions:
1. Generate ONLY a valid SQL query, no explanations
2. Use proper SQLite syntax
3. Include JOINs when needed
4. Add LIMIT 100 for large result sets
5. Use proper aliases for readability
6. Only SELECT queries are allowed

SQL Query:"""
        )
        
        try:
            prompt = prompt_template.format(
                schema=schema_desc,
                sample_data=sample_data,
                question=natural_language_query
            )
            
            response = self.llm.invoke(prompt)
            sql_query = response.content.strip()
            
            # Clean up response
            sql_query = re.sub(r'```sql\n?', '', sql_query)
            sql_query = re.sub(r'```\n?', '', sql_query)
            sql_query = sql_query.strip()
            
            return sql_query, None
        except Exception as e:
            return None, f"Error generating query: {str(e)}"
    
    def execute_query(self, sql_query):
        """Execute SQL query and return results"""
        try:
            # Security check
            if not sql_query.strip().upper().startswith('SELECT'):
                return None, "Only SELECT queries are allowed"
            
            df = pd.read_sql_query(sql_query, self.engine)
            return df, None
        except Exception as e:
            return None, f"Error executing query: {str(e)}"
    
    def create_visualization(self, df, viz_type="auto"):
        """Create appropriate visualization for the data"""
        if df.empty:
            return None
        
        try:
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if viz_type == "auto":
                if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
                    # Bar chart
                    fig = px.bar(df.head(20), x=categorical_cols[0], y=numeric_cols[0])
                elif len(numeric_cols) >= 2:
                    # Scatter plot
                    fig = px.scatter(df.head(100), x=numeric_cols[0], y=numeric_cols[1])
                elif len(numeric_cols) >= 1:
                    # Histogram
                    fig = px.histogram(df, x=numeric_cols[0])
                elif len(categorical_cols) >= 1:
                    # Count plot
                    value_counts = df[categorical_cols[0]].value_counts().head(10)
                    fig = px.bar(x=value_counts.index, y=value_counts.values)
                else:
                    return None
                    
                fig.update_layout(title="Data Visualization")
                return fig
            
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            return None

def main():
    st.set_page_config(
        page_title="Robust SQL Assistant", 
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Robust SQL Assistant")
    st.markdown("Chat with your SQL database using natural language - Now with automatic model fallback!")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = RobustSQLAssistant()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key
        api_key = st.text_input("Groq API Key", type="password", 
                               value=os.getenv("GROQ_API_KEY", ""))
        
        # Model selection
        st.subheader("Model Selection")
        model_options = ["Auto (Recommended)"] + list(AVAILABLE_MODELS.keys())
        selected_model = st.selectbox("Choose Model", model_options)
        
        if selected_model == "Auto (Recommended)":
            preferred_model = None
        else:
            preferred_model = selected_model
            st.info(f"**{AVAILABLE_MODELS[selected_model]['name']}**\n\n{AVAILABLE_MODELS[selected_model]['description']}")
        
        # Setup LLM
        if api_key and st.button("Connect to AI"):
            with st.spinner("Connecting to AI model..."):
                success, message = st.session_state.assistant.setup_llm(api_key, preferred_model)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
        
        # Database section
        st.header("🗄️ Database")
        
        # Sample database
        sample_db_path = "extended_sample_data.db"
        if os.path.exists(sample_db_path):
            if st.button("Use Sample Database"):
                success, message = st.session_state.assistant.connect_database(sample_db_path)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
        
        # Upload database
        uploaded_file = st.file_uploader("Upload SQLite Database", type=['db', 'sqlite', 'sqlite3'])
        if uploaded_file:
            with open("uploaded_database.db", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            success, message = st.session_state.assistant.connect_database("uploaded_database.db")
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
        
        # Show current status
        st.header("📊 Status")
        if st.session_state.assistant.current_model:
            st.success(f"🤖 Model: {st.session_state.assistant.current_model}")
        else:
            st.warning("🤖 No AI model connected")
            
        if st.session_state.assistant.db_path:
            st.success(f"🗄️ Database: Connected")
        else:
            st.warning("🗄️ No database connected")
    
    # Main interface
    if st.session_state.assistant.llm and st.session_state.assistant.engine:
        
        # Chat interface
        st.header("💬 Chat with your Database")
        
        # Display schema info
        with st.expander("📋 Database Schema"):
            schema_info = st.session_state.assistant.get_database_schema()
            for table_name, columns in schema_info.items():
                st.subheader(f"Table: {table_name}")
                col_df = pd.DataFrame(columns)
                st.dataframe(col_df[['name', 'type']], use_container_width=True)
        
        # Example queries
        with st.expander("💡 Example Queries"):
            examples = [
                "Show me all customers",
                "What are the top 5 selling products?",
                "Calculate total revenue by month",
                "Show customer orders with product details",
                "Find customers who haven't placed any orders"
            ]
            for example in examples:
                if st.button(example, key=f"example_{example}"):
                    st.session_state.current_query = example
        
        # Chat input
        user_query = st.chat_input("Ask me anything about your database...")
        
        # Handle example query button clicks
        if 'current_query' in st.session_state:
            user_query = st.session_state.current_query
            del st.session_state.current_query
        
        if user_query:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            # Generate and execute query
            with st.spinner("🤔 Generating SQL query..."):
                sql_query, error = st.session_state.assistant.generate_sql_query(user_query)
            
            if error:
                st.session_state.chat_history.append({"role": "assistant", "content": f"❌ Error: {error}"})
            else:
                with st.spinner("⚡ Executing query..."):
                    df, exec_error = st.session_state.assistant.execute_query(sql_query)
                
                if exec_error:
                    st.session_state.chat_history.append({"role": "assistant", "content": f"❌ SQL Error: {exec_error}"})
                else:
                    # Success - show results
                    result_msg = f"""✅ **Generated SQL:**
```sql
{sql_query}
```

📊 **Results:** {len(df)} rows returned"""
                    st.session_state.chat_history.append({"role": "assistant", "content": result_msg})
                    
                    # Store results for display
                    st.session_state.current_results = df
                    st.session_state.current_sql = sql_query
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Display current results
        if 'current_results' in st.session_state and not st.session_state.current_results.empty:
            st.header("📈 Query Results")
            
            # Results table
            st.dataframe(st.session_state.current_results, use_container_width=True)
            
            # Download button
            csv = st.session_state.current_results.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )
            
            # Auto visualization
            fig = st.session_state.assistant.create_visualization(st.session_state.current_results)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Setup instructions
        st.info("👋 Welcome! Please configure your API key and connect to a database to get started.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🔑 Step 1: Get API Key
            1. Visit [console.groq.com](https://console.groq.com/)
            2. Create account & get API key
            3. Enter it in the sidebar
            """)
        
        with col2:
            st.markdown("""
            ### 🗄️ Step 2: Connect Database  
            1. Use sample database, or
            2. Upload your SQLite file
            3. Start asking questions!
            """)

if __name__ == "__main__":
    main()
