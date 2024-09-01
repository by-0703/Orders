import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Generate a sample dataset
np.random.seed(42)
n_samples = 1000

data = {
    'distance': np.random.uniform(50, 1000, n_samples),
    'weight': np.random.uniform(0.5, 10, n_samples),
    'priority': np.random.choice(['low', 'medium', 'high'], n_samples),
    'weather_condition': np.random.choice(['normal', 'rain', 'snow', 'extreme weather alert'], n_samples),
    'on_time': np.random.choice([0, 1], n_samples)
}

df = pd.DataFrame(data)

# Convert categorical variables to numeric
df['priority'] = pd.Categorical(df['priority']).codes
df['weather_condition'] = pd.Categorical(df['weather_condition']).codes

# Split features and target
X = df[['distance', 'weight', 'priority', 'weather_condition']]
y = df['on_time']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create and train the logistic regression model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_scaled)

# Print model evaluation metrics
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Print feature coefficients
feature_names = X.columns
coefficients = model.coef_[0]
for name, coef in zip(feature_names, coefficients):
    print(f"{name}: {coef}")

# Function to predict delivery status for a new package
def predict_delivery(distance, weight, priority, weather_condition):
    priority_map = {'low': 0, 'medium': 1, 'high': 2}
    weather_map = {'normal': 0, 'rain': 1, 'snow': 2, 'extreme weather alert': 3}
    
    features = np.array([[
        distance,
        weight,
        priority_map[priority],
        weather_map[weather_condition]
    ]])
    
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    probability = model.predict_proba(scaled_features)[0][1]
    
    return "On time" if prediction[0] == 1 else "Not on time", probability

# Example usage
result, prob = predict_delivery(500, 5, 'medium', 'rain')
print(f"\nPrediction for a new package: {result}")
print(f"Probability of being on time: {prob:.2f}")