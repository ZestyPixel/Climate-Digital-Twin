import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load historical data
df = pd.read_csv("data/rainfall_temp.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df = df.rename(columns={"YEAR": "Year", "TEMPERATURE": "Temperature_C", "RAINFALL": "Rainfall_mm"})

# Drop rows with missing values
df = df.dropna()

# Independent variable (year) needs to be reshaped
X = df[["Year"]]

# === Train Rainfall Model ===
y_rain = df["Rainfall_mm"]
rain_model = LinearRegression()
rain_model.fit(X, y_rain)

# === Train Temperature Model ===
y_temp = df["Temperature_C"]
temp_model = LinearRegression()
temp_model.fit(X, y_temp)

# === Predict for 2016–2050 ===
future_years = np.arange(2016, 2101).reshape(-1, 1)

rain_preds = rain_model.predict(future_years)
temp_preds = temp_model.predict(future_years)

# === Create future dataframe ===
future_df = pd.DataFrame({
    "Year": future_years.flatten(),
    "Rainfall_mm": rain_preds,
    "Temperature_C": temp_preds,
    "Source": "Predicted"
})

# Label historical data
df["Source"] = "Historical"

# Combine
combined = pd.concat([df, future_df], ignore_index=True)

# Save
combined.to_csv("data/predicted_rainfall_temp.csv", index=False)
print("✅ Saved predictions to 'data/predicted_rainfall_temp.csv'")
