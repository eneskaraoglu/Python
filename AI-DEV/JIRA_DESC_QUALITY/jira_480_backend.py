from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import io
from jira_457_metircs_for_backend import JiraAnalyzer  # Import the class from the existing file

app = FastAPI()
analyzer = JiraAnalyzer()  # Initialize the class

class AnalyzeRequest(BaseModel):
    description: str

@app.post("/analyze-single/")
def analyze_single(request: AnalyzeRequest):
    """Analyzes a single record"""
    cleaned_text = analyzer.clean_description(request.description)
    features = analyzer.extract_features(cleaned_text)
    
    response = {
        "original_text": request.description,
        "cleaned_text": cleaned_text,
        "features": features # Converting DataFrame to JSON format
    }
    return response

@app.post("/analyze-batch/")
async def analyze_batch(file: UploadFile = File(...)):
    """Analyzes a batch CSV file"""
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    if 'Description' not in df.columns:
        raise HTTPException(status_code=400, detail="CSV file is missing the 'Description' column!")

    df["cleaned_Description"] = df["Description"].apply(analyzer.clean_description)
    features_df = df["cleaned_Description"].apply(analyzer.extract_features)
    df = pd.concat([df, features_df], axis=1)

    output = io.StringIO()
    df.to_csv(output, index=False)
    return {"message": "File processed successfully!", "data": output.getvalue()}

# Frontend HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jira Description Analyzer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f7fa;
        }
        
        h1 {
            text-align: center;
            color: #0052CC;
            margin-bottom: 30px;
        }
        
        .container {
            display: flex;
            gap: 20px;
        }
        
        .input-section, .results-section {
            flex: 1;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        textarea {
            width: 100%;
            height: 200px;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            box-sizing: border-box;
        }
        
        button {
            background-color: #0052CC;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
            transition: background-color 0.2s;
        }
        
        button:hover {
            background-color: #003d99;
        }
        
        button:disabled {
            background-color: #97a0af;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin-top: 10px;
        }
        
        .loading-spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0052CC;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result-block {
            margin-bottom: 20px;
        }
        
        .result-title {
            font-weight: bold;
            margin-bottom: 5px;
            color: #0052CC;
        }
        
        .result-content {
            background-color: #f4f5f7;
            padding: 10px;
            border-radius: 4px;
            white-space: pre-wrap;
            word-break: break-word;
            font-size: 14px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 14px;
        }
        
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #f4f5f7;
            font-weight: 600;
        }
        
        .features-table {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .error-message {
            color: #de350b;
            background-color: #ffebe6;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            display: none;
        }
        
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <h1>Jira Description Analyzer</h1>
    
    <div class="container">
        <div class="input-section">
            <h2>Input</h2>
            <p>Enter a Jira description to analyze:</p>
            <textarea id="description" placeholder="Enter your Jira description here..."></textarea>
            <div class="error-message" id="errorMessage"></div>
            <button id="analyzeBtn">Analyze Description</button>
            <div class="loading" id="loading">
                <div class="loading-spinner"></div>
                <p>Analyzing...</p>
            </div>
        </div>
        
        <div class="results-section">
            <h2>Results</h2>
            <div id="resultsContainer">
                <p>Analysis results will appear here.</p>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const descriptionTextarea = document.getElementById('description');
            const analyzeBtn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const resultsContainer = document.getElementById('resultsContainer');
            const errorMessage = document.getElementById('errorMessage');
            
            // Example description for testing
            const exampleDescription = "As a user, I want to be able to reset my password so that I can regain access to my account if I forget my password. \\n\\nAcceptance Criteria:\\n1. User should be able to click on 'Forgot Password' link on the login page\\n2. System should send a password reset link to the user's registered email\\n3. Link should expire after 24 hours\\n4. User should be able to set a new password that meets security requirements";
            
            // Set example text for easy testing
            descriptionTextarea.placeholder = "Enter your Jira description here...\\n\\nExample:\\n" + exampleDescription;
            
            analyzeBtn.addEventListener('click', async function() {
                const description = descriptionTextarea.value.trim();
                
                if (!description) {
                    errorMessage.textContent = "Please enter a description to analyze.";
                    errorMessage.style.display = "block";
                    return;
                }
                
                errorMessage.style.display = "none";
                loading.style.display = "block";
                analyzeBtn.disabled = true;
                resultsContainer.innerHTML = '<p>Analyzing...</p>';
                
                try {
                    const response = await fetch('/analyze-single/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ description }),
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    displayResults(data);
                } catch (error) {
                    console.error('Error:', error);
                    errorMessage.textContent = `Error: ${error.message || 'Something went wrong. Please try again.'}`;
                    errorMessage.style.display = "block";
                    resultsContainer.innerHTML = '<p>Failed to analyze description. Please try again.</p>';
                } finally {
                    loading.style.display = "none";
                    analyzeBtn.disabled = false;
                }
            });
            
            function displayResults(data) {
                let html = '';
                
                // Original Text
                html += `
                <div class="result-block">
                    <div class="result-title">Original Text:</div>
                    <div class="result-content">${escapeHtml(data.original_text)}</div>
                </div>
                `;
                
                // Cleaned Text
                html += `
                <div class="result-block">
                    <div class="result-title">Cleaned Text:</div>
                    <div class="result-content">${escapeHtml(data.cleaned_text)}</div>
                </div>
                `;
                
                // Features
                html += `
                <div class="result-block">
                    <div class="result-title">Extracted Features:</div>
                    <div class="features-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Feature</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                // Add all features dynamically
                for (const [key, value] of Object.entries(data.features)) {
                    html += `
                        <tr>
                            <td>${escapeHtml(key)}</td>
                            <td>${typeof value === 'object' ? JSON.stringify(value) : escapeHtml(String(value))}</td>
                        </tr>
                    `;
                }
                
                html += `
                            </tbody>
                        </table>
                    </div>
                </div>
                `;
                
                resultsContainer.innerHTML = html;
            }
            
            // Helper function to escape HTML
            function escapeHtml(unsafe) {
                return unsafe
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;")
                    .replace(/"/g, "&quot;")
                    .replace(/'/g, "&#039;");
            }
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_analyzer_frontend():
    """Serves the frontend HTML interface"""
    return HTMLResponse(content=HTML_TEMPLATE)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)