# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 10:48:15 2025

@author: Mohsen
"""

import helics as h
import matplotlib.pyplot as plt
import pandas as pd

period=1.0
offset=0.0


# Create Federate Info
fedinfo = h.helicsCreateFederateInfo()
h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")


h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_PERIOD, period)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_OFFSET, offset)

# Create federate_A Federate
battery = h.helicsCreateCombinationFederate("federate_A", fedinfo)

# Register Publications
pub_temperature = h.helicsFederateRegisterGlobalTypePublication(battery, "temperature", "double", "")

# Enter Execution Mode
h.helicsFederateEnterExecutingMode(battery)

# Data collection for plotting
requested_times = []  # To store requested times
granted_times = []  # To store granted times
temperature_value=0.0
temperature_values =[]
granted_time=0.00

# Simulation Loop
for t in range(0, 10):
    
    # Request time step    
    requested_time = round(granted_time,2) + period
    granted_time = h.helicsFederateRequestTime(battery, requested_time)
    
    
    
    temperature_value = temperature_value + 1.0
    
    # publish temperatore
    h.helicsPublicationPublishDouble(pub_temperature, temperature_value)
    
    
    granted_times.append(granted_time)    
    requested_times.append(requested_time)    
    temperature_values.append(temperature_value)

# Cleanup
h.helicsFederateDestroy(battery)


#Table

data = {
    "request time (s)": requested_times,
    "grant time (s)": granted_times,
    "published temperatures": temperature_values,
}
df = pd.DataFrame(data)

# Plot the table using matplotlib
fig, ax = plt.subplots(figsize=(8, 4))  # Create a figure and axis
ax.axis('tight')  # Disable axis
ax.axis('off')  # Hide axes
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')  # Create the table

# Adjust table style
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Scale the table

# Show the table
plt.title("Federate A")


# Show the plots
plt.tight_layout()
plt.show()