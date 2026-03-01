import pandas as pd
import numpy as np
import os

np.random.seed(42)

os.makedirs("../dataset", exist_ok=True)

# ---------------------------
# Academic Performance Dataset
# ---------------------------

academic_data = []

for _ in range(1000):
    accuracy = np.random.randint(30, 100)
    attempts = np.random.randint(3, 20)
    avg_time = np.random.randint(15, 60)
    difficulty = np.random.randint(1, 4)
    repeated_errors = np.random.randint(0, 6)

    # Label logic
    if accuracy > 75 and repeated_errors < 2:
        label = 0  # Strong
    elif 50 <= accuracy <= 75:
        label = 1  # Moderate
    else:
        label = 2  # Weak

    academic_data.append([
        accuracy, attempts, avg_time,
        difficulty, repeated_errors, label
    ])

academic_df = pd.DataFrame(
    academic_data,
    columns=[
        "accuracy", "attempts", "avg_time",
        "difficulty", "repeated_errors", "label"
    ]
)

academic_df.to_csv("../dataset/academic_data.csv", index=False)


# ---------------------------
# Burnout Dataset
# ---------------------------

burnout_data = []

for _ in range(1000):
    accuracy_trend = np.random.uniform(-20, 10)   # drop or rise
    time_increase = np.random.uniform(0, 20)
    consistency = np.random.uniform(0, 1)
    study_hours = np.random.randint(1, 12)

    # Label logic
    if accuracy_trend < -10 and time_increase > 10:
        label = 2  # High Risk
    elif accuracy_trend < -5:
        label = 1  # Medium Risk
    else:
        label = 0  # Low Risk

    burnout_data.append([
        accuracy_trend, time_increase,
        consistency, study_hours, label
    ])

burnout_df = pd.DataFrame(
    burnout_data,
    columns=[
        "accuracy_trend", "time_increase",
        "consistency", "study_hours", "label"
    ]
)

burnout_df.to_csv("../dataset/burnout_data.csv", index=False)

print("Datasets Generated Successfully!")