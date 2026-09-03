import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_PATH = os.path.join(ROOT_DIR, "data", "crop_recommendation.csv")
DEFAULT_OUTPUT_DIR = os.path.join(ROOT_DIR, "models")

def train_pipeline(data_path=DEFAULT_DATA_PATH, output_dir=DEFAULT_OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[*] Loading dataset from {data_path}...")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
        
    df = pd.read_csv(data_path)
    print(f"[+] Loaded {len(df)} samples across {df['label'].nunique()} crop classes.")
    
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_cols]
    y = df['label']
    
    # Calculate crop benchmarks (mean, min, max) for nutrient gap advisory
    print("[*] Computing agronomic benchmarks per crop...")
    benchmarks = {}
    for crop in df['label'].unique():
        crop_df = df[df['label'] == crop]
        benchmarks[crop] = {
            col: {
                "mean": round(float(crop_df[col].mean()), 2),
                "min": round(float(crop_df[col].min()), 2),
                "max": round(float(crop_df[col].max()), 2)
            }
            for col in feature_cols
        }
        
    benchmark_path = os.path.join(output_dir, "crop_benchmarks.json")
    with open(benchmark_path, "w") as f:
        json.dump(benchmarks, f, indent=2)
    print(f"[+] Saved crop benchmarks to {benchmark_path}")
    
    # Label Encoding
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Train-test split (80/20 stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model 1: Random Forest
    print("[*] Training Random Forest Classifier (n_estimators=100)...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_scaled, y_train)
    rf_preds = rf_model.predict(X_test_scaled)
    rf_acc = accuracy_score(y_test, rf_preds)
    print(f"[+] Random Forest Accuracy: {rf_acc * 100:.2f}%")
    
    # Model 2: XGBoost Classifier
    print("[*] Training XGBoost Classifier (n_estimators=100)...")
    xgb_model = XGBClassifier(
        n_estimators=100, 
        random_state=42, 
        eval_metric='mlogloss',
        learning_rate=0.1,
        n_jobs=-1
    )
    xgb_model.fit(X_train_scaled, y_train)
    xgb_preds = xgb_model.predict(X_test_scaled)
    xgb_acc = accuracy_score(y_test, xgb_preds)
    print(f"[+] XGBoost Accuracy: {xgb_acc * 100:.2f}%")
    
    # Select Best Model
    if rf_acc >= xgb_acc:
        best_model = rf_model
        best_name = "RandomForestClassifier"
        best_preds = rf_preds
        best_acc = rf_acc
        feature_importances = rf_model.feature_importances_
    else:
        best_model = xgb_model
        best_name = "XGBClassifier"
        best_preds = xgb_preds
        best_acc = xgb_acc
        feature_importances = xgb_model.feature_importances_
        
    print(f"\n[*] Selected Best Model: {best_name} with Accuracy: {best_acc * 100:.2f}%\n")
    
    # Metrics & Evaluation
    report = classification_report(
        y_test, 
        best_preds, 
        target_names=label_encoder.classes_, 
        output_dict=True
    )
    cm = confusion_matrix(y_test, best_preds).tolist()
    
    feat_imp_dict = {
        col: round(float(imp), 4) 
        for col, imp in zip(feature_cols, feature_importances)
    }
    
    metrics_data = {
        "best_model": best_name,
        "best_accuracy": round(float(best_acc), 4),
        "random_forest_accuracy": round(float(rf_acc), 4),
        "xgboost_accuracy": round(float(xgb_acc), 4),
        "feature_importances": feat_imp_dict,
        "classes": list(label_encoder.classes_),
        "confusion_matrix": cm,
        "macro_avg_f1": round(float(report['macro avg']['f1-score']), 4),
        "weighted_avg_f1": round(float(report['weighted avg']['f1-score']), 4)
    }
    
    # Save artifacts
    model_path = os.path.join(output_dir, "crop_model.pkl")
    scaler_path = os.path.join(output_dir, "scaler.pkl")
    le_path = os.path.join(output_dir, "label_encoder.pkl")
    metrics_path = os.path.join(output_dir, "metrics.json")
    
    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(label_encoder, le_path)
    
    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f, indent=2)
        
    print(f"[+] Successfully saved model to {model_path}")
    print(f"[+] Successfully saved scaler to {scaler_path}")
    print(f"[+] Successfully saved label encoder to {le_path}")
    print(f"[+] Successfully saved metrics to {metrics_path}")
    print("\n[+] Training and evaluation complete!")

if __name__ == "__main__":
    train_pipeline()
