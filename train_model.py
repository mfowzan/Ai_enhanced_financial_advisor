import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_investment_model(user_data_file, model_output_path=r"C:\\Users\\user\Desktop\\fowzan\\Aiproject\\models\\investment_model.pkl"
):
    """Train a model to recommend investment portfolios based on user profiles."""
    if not os.path.exists(user_data_file):
        logging.error(f"Error: {user_data_file} not found!")
        return

    # Load user profiles
    try:
        data = pd.read_csv(user_data_file)
        logging.info(f"Loaded user profiles from {user_data_file}")
    except Exception as e:
        logging.error(f"Failed to load user profiles: {e}")
        return
    
    # Ensure all necessary columns are present
    required_columns = ["income", "expenses", "savings", "investment_amount", "risk_tolerance"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        return
    
    # Handle missing or invalid data
    if data.isnull().sum().any():
        logging.warning("Dataset contains missing values. Filling missing values with mean for numerical columns.")
        data.fillna(data.mean(), inplace=True)
    
    # Features and target variable
    X = data[["income", "expenses", "savings", "investment_amount"]]
    y = data["risk_tolerance"]
    
    # Convert target to numerical labels
    label_mapping = {"low": 0, "medium": 1, "high": 2}
    if not set(y).issubset(set(label_mapping.keys())):
        logging.error("Unexpected values found in the 'risk_tolerance' column.")
        return
    y = y.map(label_mapping)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest Classifier
    logging.info("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model performance
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model Accuracy: {accuracy:.2f}")
    logging.info("\nClassification Report:\n" + classification_report(y_test, y_pred, target_names=["low", "medium", "high"]))
    
    # Save model
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)  # Create directory if it doesn't exist
    try:
        joblib.dump(model, model_output_path)
        logging.info(f"Model trained and saved at {model_output_path}")
    except Exception as e:
        logging.error(f"Failed to save the model: {e}")

if __name__ == "__main__":
    # Ensure the 'models' directory exists
    if not os.path.exists("models"):
        os.makedirs("models")
        logging.info("Created 'models' directory.")

    # Train the model using the generated user profiles
    user_data_file = "C:\\Users\\user\\Desktop\\fowzan\\Aiproject\\data\\user_profiles.csv"  # Path to the user profiles file
    train_investment_model(user_data_file)
