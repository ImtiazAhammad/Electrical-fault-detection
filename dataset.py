import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# --------------------------
# AHU Data Generator
# --------------------------
def generate_ahu_data(num_samples=5000):
    np.random.seed(42)
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(num_samples)]
    
    data = {
        # From Client's AHU Point List
        'supply_air_temp': np.random.normal(18, 1.5, num_samples),  # Setpoint 18±2°C
        'return_air_temp': np.random.normal(23, 1.5, num_samples),  # Setpoint 23±2°C
        'room_air_temp': np.random.normal(23, 2, num_samples),
        'return_air_humidity': np.random.uniform(40, 60, num_samples),
        'fan_speed': np.random.randint(30, 100, num_samples),
        'cooling_state': np.random.choice([0, 1], num_samples, p=[0.6, 0.4]),
        'electric_reheat_state': np.random.choice([0, 1], num_samples, p=[0.8, 0.2]),
        'filter_dp': np.random.uniform(50, 200, num_samples),  # Pa (Filter Dirty >300Pa)
        'cool_water_valve': np.random.uniform(0, 100, num_samples),  # %
        
        # Faults (0=Normal, 1=Fan Fault, 2=Filter Dirty, 3=Coil Fault)
        'fault_type': np.random.choice([0,1,2,3], num_samples, p=[0.85,0.05,0.05,0.05])
    }
    
    # Inject Faults Based on Client's Thresholds
    for i in range(num_samples):
        if data['fault_type'][i] == 1:  # Fan Fault
            data['fan_speed'][i] = 0
            data['supply_air_temp'][i] += 5
        elif data['fault_type'][i] == 2:  # Filter Dirty
            data['filter_dp'][i] = np.random.uniform(350, 500)
        elif data['fault_type'][i] == 3:  # Coil Fault
            data['cool_water_valve'][i] = 0 if data['cooling_state'][i] == 1 else 100
            
    df = pd.DataFrame(data)
    df['timestamp'] = timestamps
    return df

# --------------------------
# Chiller Data Generator
# --------------------------
def generate_chiller_data(num_samples=5000):
    np.random.seed(42)
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(num_samples)]
    
    data = {
        # From Client's Chiller Point List
        'chill_water_outlet_temp': np.random.normal(6, 1, num_samples),  # Setpoint 6°C
        'chill_water_inlet_temp': np.random.normal(10, 1.5, num_samples),
        'condenser_pressure': np.random.normal(4.5, 0.5, num_samples),  # Bar
        'differential_pressure': np.random.normal(15, 3, num_samples),  # kPa
        'supply_water_temp': np.random.normal(45, 2, num_samples),  # Heating mode
        'cooling_tower_fan_status': np.random.choice([0, 1], num_samples, p=[0.3, 0.7]),
        
        # Faults (0=Normal, 1=Low Refrigerant, 2=Condenser Fault, 3=Flow Failure)
        'fault_type': np.random.choice([0,1,2,3], num_samples, p=[0.85,0.05,0.05,0.05])
    }
    
    # Inject Faults
    for i in range(num_samples):
        if data['fault_type'][i] == 1:  # Low Refrigerant
            data['condenser_pressure'][i] -= 2.5
        elif data['fault_type'][i] == 2:  # Condenser Fault
            data['differential_pressure'][i] += 20
        elif data['fault_type'][i] == 3:  # Flow Failure
            data['chill_water_outlet_temp'][i] += 8
            
    df = pd.DataFrame(data)
    df['timestamp'] = timestamps
    return df

# --------------------------
# Generator Data Generator 
# --------------------------
def generate_generator_data(num_samples=5000):
    np.random.seed(42)
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(num_samples)]
    
    data = {
        # From Client's Generator Point List
        'oil_pressure': np.random.normal(2.0, 0.3, num_samples),  # Bar (Shutdown <1.03bar)
        'coolant_temp': np.random.normal(85, 5, num_samples),     # Shutdown >120°C
        'battery_voltage': np.random.normal(24, 0.5, num_samples),
        'phase1_voltage': np.random.normal(230, 5, num_samples),
        'phase2_voltage': np.random.normal(230, 5, num_samples),
        'frequency': np.random.normal(50, 0.2, num_samples),      # Hz
        'load_percent': np.random.uniform(30, 90, num_samples),
        
        # Faults (0=Normal, 1=Low Oil, 2=Overheat, 3=Voltage Fault)
        'fault_type': np.random.choice([0,1,2,3], num_samples, p=[0.85,0.05,0.05,0.05])
    }
    
    # Inject Faults
    for i in range(num_samples):
        if data['fault_type'][i] == 1:  # Low Oil Pressure
            data['oil_pressure'][i] = np.random.uniform(0.8, 1.0)
        elif data['fault_type'][i] == 2:  # Overheat
            data['coolant_temp'][i] = np.random.uniform(125, 135)
        elif data['fault_type'][i] == 3:  # Voltage Fault
            data['phase1_voltage'][i] = np.random.uniform(180, 200)
            
    df = pd.DataFrame(data)
    df['timestamp'] = timestamps
    return df

# Generate all datasets
ahu_df = generate_ahu_data()
chiller_df = generate_chiller_data()
generator_df = generate_generator_data()

ahu_df.to_csv('ahu_data.csv', index=False)
chiller_df.to_csv('chiller_data.csv', index=False)
generator_df.to_csv('generator_data.csv', index=False)