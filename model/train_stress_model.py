import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle

# Load data
df = pd.read_csv("model/stress_data.csv")

# Features and target
X = df[["session_duration", "typing_delay", "click_rate", "checkin_score"]]
y = df["stress_label"]

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize model
model = DecisionTreeClassifier(random_state=42)

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# ----------------------------
# Evaluation Metrics
# ----------------------------

print("MODEL EVALUATION RESULTS")
print("------------------------")

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# ----------------------------
# Visualize Confusion Matrix
# ----------------------------

plt.figure(figsize=(6, 5))
sns.heatmap(cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=sorted(y.unique()),
            yticklabels=sorted(y.unique()))

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Confusion Matrix - Stress Model")
plt.tight_layout()
plt.show()

# ----------------------------
# Save Model
# ----------------------------

with open("stress_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nMODEL TRAINED AND SAVED SUCCESSFULLY!")