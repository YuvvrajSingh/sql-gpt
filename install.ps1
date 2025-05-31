# SQL Assistant Installation Script for Windows PowerShell
# Run this script in PowerShell as Administrator for best results

Write-Host "🚀 SQL Assistant Setup for Windows" -ForegroundColor Green
Write-Host "=" * 50

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -ge 3 -and $minor -ge 8) {
            Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
        } else {
            Write-Host "❌ Python 3.8 or higher is required. Found: $pythonVersion" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Check if pip is available
try {
    pip --version | Out-Null
    Write-Host "✅ pip is available" -ForegroundColor Green
} catch {
    Write-Host "❌ pip is not available" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "📦 Installing required packages..." -ForegroundColor Blue
try {
    pip install -r requirements.txt
    Write-Host "✅ Successfully installed all packages!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error installing packages" -ForegroundColor Red
    exit 1
}

# Setup environment file
if (-not (Test-Path ".env")) {
    Write-Host "🔧 Setting up environment file..." -ForegroundColor Blue
    
    $groqKey = Read-Host "Enter your Groq API key (or press Enter to skip)"
    
    $envContent = @"
# GROQ API Configuration
GROQ_API_KEY=$groqKey

# Database Configuration (Optional - for custom databases)
# DATABASE_URL=sqlite:///your_database.db
# or for other databases:
# DATABASE_URL=postgresql://username:password@localhost:5432/dbname
# DATABASE_URL=mysql://username:password@localhost:3306/dbname
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Environment file created!" -ForegroundColor Green
    
    if (-not $groqKey) {
        Write-Host "⚠️  Don't forget to add your Groq API key to the .env file!" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Environment file already exists!" -ForegroundColor Green
}

# Create sample database
Write-Host "🗃️ Creating sample database..." -ForegroundColor Blue
try {
    python create_sample_db.py
    Write-Host "✅ Sample database created successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error creating sample database" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Add your Groq API key to the .env file if you haven't already"
Write-Host "2. Run the application: streamlit run app.py"
Write-Host "3. Open your browser and start chatting with your database!"

# Ask if user wants to run the app
$runNow = Read-Host "`nWould you like to run the application now? (y/n)"
if ($runNow -match "^[Yy]") {
    Write-Host "🚀 Starting SQL Assistant..." -ForegroundColor Green
    streamlit run app.py
}
