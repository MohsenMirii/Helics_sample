# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 10:48:36 2025

@author: Mohsen
"""

import helics as h
import matplotlib.pyplot as plt
import pandas as pd


period=1.0
offset=1.0

# Create Federate Info
fedinfo = h.helicsCreateFederateInfo()
h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")
h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, 1.0)

h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_PERIOD, period)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_OFFSET, offset)


# Create federate_C Federate
controller = h.helicsCreateCombinationFederate("federate_C", fedinfo)

# Register Publications and Subscriptions
sub_temperature = h.helicsFederateRegisterSubscription(controller, "temperature", "")
sub_tzone = h.helicsFederateRegisterSubscription(controller, "tzone", "")
pub_action = h.helicsFederateRegisterGlobalTypePublication(controller, "action", "double", "")

# Enter Execution Mode
h.helicsFederateEnterExecutingMode(controller)

granted_time=0.00
action_value=0.00
requested_times = []  # To store requested times
granted_times = []  # To store granted times


Subscribed_temperatures = []
Subscribed_tzones = []
published_actions = []

# Simulation Loop
for t in range(0, 10):
    
    # Request time step
    requested_time = round(granted_time,2) + period
    granted_time = h.helicsFederateRequestTime(controller, requested_time)
    
    # Get temperature from federate A    
    temperature_value = 0.0
    if h.helicsInputIsUpdated(sub_temperature):  # Check if a new value is available
       temperature_value = h.helicsInputGetDouble(sub_temperature)
    else:
       temperature_value = 0.0  # Default to 0 if no update received       
       
    
    # Get tzone from federate B  
    tzone_value = 0.0
    if h.helicsInputIsUpdated(sub_tzone):  # Check if a new value is available
       tzone_value = h.helicsInputGetDouble(sub_tzone)
    else:
       tzone_value = 0.0  # Default to 0 if no update received       

   

    # publish action
    action_value = action_value + 1.0    
    h.helicsPublicationPublishDouble(pub_action, action_value)
    
    requested_times.append(requested_time)
    granted_times.append(granted_time)
    published_actions.append(action_value)
    Subscribed_temperatures.append(temperature_value)
    Subscribed_tzones.append(tzone_value)
    

# Cleanup
h.helicsFederateDestroy(controller)



data = {
    "request time (s)": requested_times,
    "grant time (s)": granted_times,
    "published actions": published_actions,
    "subscribed temperatures": Subscribed_temperatures,
    "subscribed tzones": Subscribed_tzones,

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
plt.title("Federate C")


# Show the plots
plt.tight_layout()
plt.show()