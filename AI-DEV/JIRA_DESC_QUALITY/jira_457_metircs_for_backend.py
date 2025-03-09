import pandas as pd
import re

class JiraAnalyzer:
    def __init__(self, df=None):
        self.df = df

    def clean_description(self, text):
        """Metni temizleyen fonksiyon"""
        if pd.isnull(text):
            return text
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,;:!?()[\]```\-*•]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_features(self, text):
        """Metinden özellik çıkaran fonksiyon (Kalite Skoru Dahil)"""
        if pd.isnull(text):
            return {
                'char_count': 0,
                'word_count': 0,
                'sentence_count': 0,
                'avg_word_length': 0,
                'has_screenshots': False,
                'url_count': False,
                'has_acceptance_criteria': False,
                'has_expected_result': False,
                'has_altsistem': False,
                'quality': 'Low',
                'score': 0
            }

        char_count = len(text)
        words = text.split()
        word_count = len(words)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip() != '']
        sentence_count = len(sentences)
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

        has_screenshots = bool(re.search(r'(\[image\]|\.png|\.jpg|\.jpeg|\.gif)', text.lower()))
        url_count = bool(re.search(r'(\d+\.|http|www)', text.lower()))
        has_acceptance_criteria = 'kabul kriterleri' in text.lower() or 'meli' in text.lower() or 'malı' in text.lower()
        has_expected_result = 'olmalı' in text.lower() or 'çözüm' in text.lower()
        has_altsistem = any(x in text.lower() for x in ['stok', 'kalite', 'finans', 'üretim', 'satış', 'satınalma'])

        # Tüm metrikleri içeren dict oluştur
        features = {
            'char_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': avg_word_length,
            'has_screenshots': has_screenshots,
            'url_count': url_count,
            'has_acceptance_criteria': has_acceptance_criteria,
            'has_expected_result': has_expected_result,
            'has_altsistem': has_altsistem
        }

        # **quality_score metodunu çağır ve kalite skorunu ekle**
        quality_result = self.quality_score(features)
        features.update(quality_result)  # Metriklere kalite skorunu da ekle

        return features

    def quality_score(self, features):
        """Kalite skorunu hesaplayan fonksiyon (text yerine features alır!)"""
        score = 0
        if features['word_count'] >= 30: score += 1
        if features['word_count'] >= 60: score += 1
        if features['sentence_count'] >= 3: score += 1
        if features['avg_word_length'] >= 4: score += 1
        if features['has_screenshots']: score += 1
        if features['has_acceptance_criteria']: score += 2
        if features['has_expected_result']: score += 3
        if features['has_altsistem']: score += 1
        if features['url_count']: score += 1

        if score >= 7:
            quality = 'High'
        elif score >= 4:
            quality = 'Medium'
        else:
            quality = 'Low'

        return {'quality': quality, 'score': score}

    def analyze(self):
        """Ana işleme fonksiyonu: Tüm metrikleri çıkarır ve kaliteyi değerlendirir."""
        if self.df is not None:
            self.df['clean_description'] = self.df['description'].apply(self.clean_description)
            feature_dicts = self.df['clean_description'].apply(self.extract_features)
            feature_df = pd.DataFrame(feature_dicts.tolist())  # Özellikleri DataFrame'e dönüştür
            self.df = pd.concat([self.df, feature_df], axis=1)

            return self.df
        else:
            print("Veri çerçevesi bulunamadı!")
