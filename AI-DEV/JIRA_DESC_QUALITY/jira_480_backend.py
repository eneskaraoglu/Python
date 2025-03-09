from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
import io
from jira_457_metircs_for_backend import JiraAnalyzer  # Eski dosyadan sınıfı import ediyoruz

app = FastAPI()
analyzer = JiraAnalyzer()  # Sınıfı başlatıyoruz

class AnalyzeRequest(BaseModel):
    description: str

@app.post("/analyze-single/")
def analyze_single(request: AnalyzeRequest):
    """Tek bir kayıt için analiz yapar"""
    cleaned_text = analyzer.clean_description(request.description)
    features = analyzer.extract_features(cleaned_text)
    
    response = {
        "original_text": request.description,
        "cleaned_text": cleaned_text,
        "features": features.to_dict()  # DataFrame yerine JSON formatına dönüştürüyoruz
    }
    return response

@app.post("/analyze-batch/")
async def analyze_batch(file: UploadFile = File(...)):
    """Toplu CSV analizi yapar"""
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    if 'Description' not in df.columns:
        raise HTTPException(status_code=400, detail="CSV dosyasında 'Description' sütunu eksik!")

    df["cleaned_Description"] = df["Description"].apply(analyzer.clean_description)
    features_df = df["cleaned_Description"].apply(analyzer.extract_features)
    df = pd.concat([df, features_df], axis=1)

    output = io.StringIO()
    df.to_csv(output, index=False)
    return {"message": "Dosya başarıyla işlendi!", "data": output.getvalue()}
