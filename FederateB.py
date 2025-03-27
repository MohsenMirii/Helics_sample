import helics as h
import random
import matplotlib.pyplot as plt
import pandas as pd


period=1.0
offset=0.0

# Create Federate Info
fedinfo = h.helicsCreateFederateInfo()
h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_PERIOD, period)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_OFFSET, offset)

# Create federate_B Federate
charger = h.helicsCreateCombinationFederate("federate_B", fedinfo)

# Register Publications and Subscriptions
pub_tzone = h.helicsFederateRegisterGlobalTypePublication(charger, "tzone", "double", "")
sub_action = h.helicsFederateRegisterSubscription(charger, "action", "")

# Enter Execution Mode
h.helicsFederateEnterExecutingMode(charger)

# Data collection for plotting
requested_times = []  # To store requested times
granted_times = []  # To store granted times
published_values = []
subscribed_values = []
granted_time=0.00
tzone_value=0.00
# Simulation Loop
for t in range(0, 10):
    
    # Request time step
    requested_time = round(granted_time,2) + period
    granted_time = h.helicsFederateRequestTime(charger, requested_time)
    
    # Get action signal from federate C    
    action_signal = 1.0
    if h.helicsInputIsValid(sub_action):  # Check if a new value is available
       action_signal = h.helicsInputGetDouble(sub_action)
    else:
       action_signal = 1.0  # Default to 0 if no update received       
    
    
    
    # publish tzone
    tzone_value = tzone_value + 1.0    
    h.helicsPublicationPublishDouble(pub_tzone, tzone_value)
    
    
    requested_times.append(requested_time)
    granted_times.append(granted_time)
    published_values.append(tzone_value)
    subscribed_values.append(action_signal)
    


# Cleanup
h.helicsFederateDestroy(charger)

data = {
    "request time (s)": requested_times,
    "grant time (s)": granted_times,
    "published tzones": published_values,
    "subscribed actions": subscribed_values,

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
plt.title("Federate B")


# Show the plots
plt.tight_layout()
plt.show()