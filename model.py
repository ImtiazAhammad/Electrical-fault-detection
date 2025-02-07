from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd

# --------------------------
# AHU Model Training
# --------------------------
ahu_df = pd.read_csv('ahu_data.csv')
ahu_features = [
    'supply_air_temp', 'return_air_temp', 'fan_speed', 
    'cooling_state', 'filter_dp', 'cool_water_valve'
]
ahu_X = ahu_df[ahu_features]
ahu_y = ahu_df['fault_type']

ahu_X_train, ahu_X_test, ahu_y_train, ahu_y_test = train_test_split(
    ahu_X, ahu_y, test_size=0.2, random_state=42
)

ahu_model = RandomForestClassifier(n_estimators=100)
ahu_model.fit(ahu_X_train, ahu_y_train)
joblib.dump(ahu_model, 'ahu_fault_model.pkl')

# --------------------------
# Chiller Model Training
# --------------------------
chiller_df = pd.read_csv('chiller_data.csv')
chiller_features = [
    'chill_water_outlet_temp', 'chill_water_inlet_temp',
    'condenser_pressure', 'differential_pressure'
]
chiller_X = chiller_df[chiller_features]
chiller_y = chiller_df['fault_type']

chiller_X_train, chiller_X_test, chiller_y_train, chiller_y_test = train_test_split(
    chiller_X, chiller_y, test_size=0.2, random_state=42
)

chiller_model = RandomForestClassifier(n_estimators=100)
chiller_model.fit(chiller_X_train, chiller_y_train)
joblib.dump(chiller_model, 'chiller_fault_model.pkl')

# --------------------------
# Generator Model Training
# --------------------------
generator_df = pd.read_csv('generator_data.csv')
generator_features = [
    'oil_pressure', 'coolant_temp', 'phase1_voltage', 'frequency'
]
generator_X = generator_df[generator_features]
generator_y = generator_df['fault_type']

generator_X_train, generator_X_test, generator_y_train, generator_y_test = train_test_split(
    generator_X, generator_y, test_size=0.2, random_state=42
)

generator_model = RandomForestClassifier(n_estimators=100)
generator_model.fit(generator_X_train, generator_y_train)
joblib.dump(generator_model, 'generator_fault_model.pkl')