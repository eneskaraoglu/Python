import pandas as pd
import re

df = pd.read_csv(r'C:\ANALIZ_DATA\ERP_WORKLOG_90.csv', delimiter=";", encoding="utf-8")
print(df.head())

#"project";"issuestatus";"JKEY";"WORKLOG_SAHIBI";"worklogbody";"STARTDATE";"CREATED";"ESTIMATE_HR";"T_WORKLOG_HR";"WORKLOG_KISI";"WORKLOG_HR";"SUMMARY";"DESCRIPTION";"JIRA_CREATED";"JIRA_UPDATED";"JIRA_DUEDATE";"JIRA_RESOLUTIONDATE";"JIRA_TIMEORIGINALESTIMATE";"JIRA_TIMEESTIMATE";"JIRA_TIMESPENT";"JIRA_CREATOR";"SORUMLU_GELISTIRICI"

def clean_description(text):
    if pd.isnull(text):
        return text
    # HTML tag'lerini temizle
    text = re.sub(r'<.*?>', '', text)
    # Türkçe karakterler dahil olmak üzere, sadece belirlenen karakterleri koru
    text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,;:!?()-]', '', text)
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()
    # Metni küçük harfe çevir
    text = text.lower()
    return text

df['cleaned_worklogbody'] = df['worklogbody'].apply(clean_description)

print(df[['worklogbody', 'cleaned_worklogbody']].head())
