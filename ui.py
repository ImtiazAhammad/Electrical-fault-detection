import customtkinter as ctk
import joblib
import pandas as pd

class FaultPredictionApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Equipment Fault Predictor")
        self.window.geometry("600x500")
        
        # Load trained models
        self.ahu_model = joblib.load('ahu_fault_model.pkl')
        self.chiller_model = joblib.load('chiller_fault_model.pkl')
        self.generator_model = joblib.load('generator_fault_model.pkl')
        
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        # Device Selection
        ctk.CTkLabel(self.window, text="Select Device:").pack(pady=10)
        self.device_var = ctk.StringVar(value="AHU")
        device_options = ["AHU", "Chiller", "Generator"]
        self.device_menu = ctk.CTkComboBox(self.window, values=device_options, 
                                         variable=self.device_var,
                                         command=self.update_input_fields)
        self.device_menu.pack(pady=10)
        
        # Input Fields Frame
        self.input_frame = ctk.CTkFrame(self.window)
        self.input_frame.pack(pady=20, fill='both', expand=True)
        
        # Result Display
        self.result_label = ctk.CTkLabel(self.window, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        # Initial fields
        self.update_input_fields()

    def update_input_fields(self, choice=None):
        # Clear previous inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        device = self.device_var.get()
        
        if device == "AHU":
            self.create_ahu_fields()
        elif device == "Chiller":
            self.create_chiller_fields()
        elif device == "Generator":
            self.create_generator_fields()
            
        # Add Predict Button
        ctk.CTkButton(self.input_frame, text="Predict Fault", 
                     command=self.predict_fault).pack(pady=20)

    def create_ahu_fields(self):
        # AHU-specific parameters from client's point list
        params = [
            ("Supply Air Temp (°C)", "18.0"),
            ("Return Air Temp (°C)", "23.0"),
            ("Fan Speed (%)", "50"),
            ("Filter DP (Pa)", "150"),
            ("Cooling State", ["OFF", "ON"]),
            ("Cool Water Valve (%)", "0")
        ]
        
        self.inputs = {}
        for label, default in params:
            frame = ctk.CTkFrame(self.input_frame)
            frame.pack(fill='x', padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=label).pack(side='left', padx=5)
            
            if isinstance(default, list):  # Dropdown for cooling state
                entry = ctk.CTkComboBox(frame, values=default)
                entry.set(default[0])
            else:
                entry = ctk.CTkEntry(frame)
                entry.insert(0, default)
            
            entry.pack(side='right', padx=5)
            self.inputs[label] = entry

    def create_chiller_fields(self):
        # Chiller parameters
        params = [
            ("Chill Water Outlet Temp (°C)", "6.0"),
            ("Condenser Pressure (bar)", "4.5"),
            ("Differential Pressure (kPa)", "15.0"),
            ("Cooling Tower Fan Status", ["OFF", "ON"])
        ]
        
        self.inputs = {}
        for label, default in params:
            frame = ctk.CTkFrame(self.input_frame)
            frame.pack(fill='x', padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=label).pack(side='left', padx=5)
            
            if isinstance(default, list):  # Dropdown for status
                entry = ctk.CTkComboBox(frame, values=default)
                entry.set(default[0])
            else:
                entry = ctk.CTkEntry(frame)
                entry.insert(0, default)
            
            entry.pack(side='right', padx=5)
            self.inputs[label] = entry

    def create_generator_fields(self):
        # Generator parameters
        params = [
            ("Oil Pressure (bar)", "2.0"),
            ("Coolant Temp (°C)", "85.0"),
            ("Battery Voltage (V)", "24.0"),
            ("Phase 1 Voltage (V)", "230.0")
        ]
        
        self.inputs = {}
        for label, default in params:
            frame = ctk.CTkFrame(self.input_frame)
            frame.pack(fill='x', padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=label).pack(side='left', padx=5)
            
            entry = ctk.CTkEntry(frame)
            entry.insert(0, default)
            
            entry.pack(side='right', padx=5)
            self.inputs[label] = entry

    def predict_fault(self):
        device = self.device_var.get()
        input_data = []
        
        try:
            if device == "AHU":
                # Map inputs to model features
                features = [
                    float(self.inputs["Supply Air Temp (°C)"].get()),
                    float(self.inputs["Return Air Temp (°C)"].get()),
                    float(self.inputs["Fan Speed (%)"].get()),
                    1 if self.inputs["Cooling State"].get() == "ON" else 0,
                    float(self.inputs["Filter DP (Pa)"].get()),
                    float(self.inputs["Cool Water Valve (%)"].get())
                ]
                prediction = self.ahu_model.predict([features])[0]
                faults = ["Normal", "Fan Fault", "Filter Dirty", "Coil Fault"]
            
            elif device == "Chiller":
                features = [
                    float(self.inputs["Chill Water Outlet Temp (°C)"].get()),
                    float(self.inputs["Condenser Pressure (bar)"].get()),
                    float(self.inputs["Differential Pressure (kPa)"].get()),
                    1 if self.inputs["Cooling Tower Fan Status"].get() == "ON" else 0
                ]
                prediction = self.chiller_model.predict([features])[0]
                faults = ["Normal", "Compressor Fault", "Condenser Fault", "Flow Fault"]
            
            elif device == "Generator":
                features = [
                    float(self.inputs["Oil Pressure (bar)"].get()),
                    float(self.inputs["Coolant Temp (°C)"].get()),
                    float(self.inputs["Battery Voltage (V)"].get()),
                    float(self.inputs["Phase 1 Voltage (V)"].get())
                ]
                prediction = self.generator_model.predict([features])[0]
                faults = ["Normal", "Oil System Fault", "Cooling System Fault", "Electrical Fault"]
            
            self.result_label.configure(text=f"Predicted Status: {faults[prediction]}", 
                                      text_color="green")
            
        except ValueError:
            self.result_label.configure(text="Invalid input values!", text_color="red")

if __name__ == "__main__":
    app = FaultPredictionApp()