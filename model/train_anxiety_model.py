import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle

# Load dataset
df = pd.read_csv("model/anxiety_dataset.csv")

# Features and target
X = df[['q1','q2','q3','q4','q5','q6','q7']]
y = df['class']

# Train-test split (80-20)  
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation Metrics
print("Model Evaluation Results")
print("-------------------------")

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Plot Confusion Matrix
plt.figure(figsize=(6,5))
sns.heatmap(cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=["Minimal", "Moderate", "Severe"],
            yticklabels=["Minimal", "Moderate", "Severe"])

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Confusion Matrix - Anxiety Model")
plt.tight_layout()
plt.show()

# Save model
pickle.dump(model, open("anxiety_model.pkl", "wb"))

print("\nModel saved successfully as anxiety_model.pkl")
