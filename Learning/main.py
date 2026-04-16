from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import joblib

inputs_df  = pd.read_csv("inputs.csv").dropna()
outputs_df = pd.read_csv("outputs.csv").dropna()

assert len(inputs_df) == len(outputs_df), "CSVs must have the same number of rows"

ohe_string = OneHotEncoder(sparse_output=False)
ohe_finger = OneHotEncoder(sparse_output=False)

string_encoded = ohe_string.fit_transform(inputs_df[["string"]])
finger_encoded = ohe_finger.fit_transform(inputs_df[["finger"]])
fret = inputs_df[["fret"]].values

X = np.hstack([string_encoded, fret, finger_encoded])

output_cols = [
    "tip1_x", "tip1_y", "tip1_z",
    "tip2_x", "tip2_y", "tip2_z",
    "tip3_x", "tip3_y", "tip3_z",
    "tip4_x", "tip4_y", "tip4_z",
    "tip5_x", "tip5_y", "tip5_z",
    "wrist_x", "wrist_y", "wrist_z"
]
y = outputs_df[output_cols].values  # shape: (n_samples, 18)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = MLPRegressor(hidden_layer_sizes=(128, 64), max_iter=500)
model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print(f"R² score: {score:.4f}")

def predict_landmarks(string, fret, finger):
    string_enc = ohe_string.transform([[string]])
    finger_enc = ohe_finger.transform([[finger]])
    fret_arr   = np.array([[fret]])
    X_input    = np.hstack([string_enc, fret_arr, finger_enc])

    predicted = model.predict(X_input).reshape(6, 3)

    labels = ["tip1", "tip2", "tip3", "tip4", "tip5", "wrist"]
    for label, (x, y, z) in zip(labels, predicted):
        print(f"{label}: x={x:.4f}, y={y:.4f}, z={z:.4f}")

    return predicted

predict_landmarks(string=3, fret=5, finger=2)

joblib.dump(model, "guitar_model.pkl")
joblib.dump(ohe_string, "ohe_string.pkl")
joblib.dump(ohe_finger, "ohe_finger.pkl")

model      = joblib.load("guitar_model.pkl")
ohe_string = joblib.load("ohe_string.pkl")
ohe_finger = joblib.load("ohe_finger.pkl")