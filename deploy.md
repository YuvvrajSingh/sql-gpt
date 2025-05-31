# 🚀 Deployment Guide

## Quick Deploy to Streamlit Cloud

### 1. **Streamlit Cloud (Recommended)**

1. **Visit Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io/)

2. **Connect GitHub**: Sign in with your GitHub account

3. **Deploy the App**:
   - Click "New app"
   - Repository: `YuvvrajSingh/sql-gpt`
   - Branch: `master`
   - Main file path: `streamlit_app.py`
   - App URL: Choose your custom URL (e.g., `sql-assistant`)

4. **Set Environment Variables**:
   - In the Streamlit Cloud dashboard, go to "Secrets"
   - Add your secrets in TOML format:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```

5. **Deploy**: Click "Deploy!" and wait for the app to build

### 2. **Local Development**

```bash
# Clone the repository
git clone https://github.com/YuvvrajSingh/sql-gpt.git
cd sql-gpt

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Edit .env file and add your GROQ_API_KEY

# Run the app
streamlit run streamlit_app.py
```

### 3. **Other Deployment Options**

#### **Heroku**
1. Create a `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-sql-assistant
   heroku config:set GROQ_API_KEY=your_key_here
   git push heroku master
   ```

#### **Docker**
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
   ```

2. Build and run:
   ```bash
   docker build -t sql-assistant .
   docker run -p 8501:8501 -e GROQ_API_KEY=your_key sql-assistant
   ```

#### **Railway**
1. Connect your GitHub repository
2. Set environment variable: `GROQ_API_KEY`
3. Deploy automatically

#### **Render**
1. Connect your GitHub repository
2. Build command: `pip install -r requirements.txt`
3. Start command: `streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT`
4. Set environment variable: `GROQ_API_KEY`

### 4. **Environment Variables Required**

- `GROQ_API_KEY`: Your Groq API key from [console.groq.com](https://console.groq.com/)

### 5. **Features Available After Deployment**

✅ **AI Model Selection with Auto-Fallback**
✅ **Natural Language to SQL Translation**
✅ **Interactive Data Visualization**
✅ **Multiple Database Support**
✅ **Real-time Chat Interface**
✅ **CSV Export Functionality**
✅ **Sample Database Included**

### 6. **Troubleshooting**

**Common Issues:**
- **Module not found**: Make sure all dependencies are in `requirements.txt`
- **API Key errors**: Verify your GROQ_API_KEY is set correctly
- **Database connection**: Ensure your database file is accessible
- **Port issues**: Use the provided port from the hosting platform

**Performance Tips:**
- Use the "Auto (Recommended)" model selection for best results
- Clear chat history periodically for better performance
- Upload smaller database files for faster processing

### 7. **Post-Deployment Checklist**

- [ ] App loads without errors
- [ ] API key is configured in secrets/environment variables
- [ ] Sample database connection works
- [ ] Chat functionality responds correctly
- [ ] Visualizations display properly
- [ ] File upload works for custom databases
- [ ] Clear chat button functions
- [ ] CSV download works

### 8. **Demo & Testing**

After deployment, test these features:
1. Connect to AI with your API key
2. Use the sample database
3. Try example queries
4. Request a visualization
5. Upload a custom database
6. Clear chat history

---

**🎉 Your SQL Assistant is now live and ready to help users chat with their databases!**
