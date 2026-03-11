# Fuzzy Logic Based Washing Machine Simulation

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# -----------------------------
# 1. Define Input Variables
# -----------------------------

# Dirt level of clothes (0 - 10)
dirt = ctrl.Antecedent(np.arange(0, 11, 1), 'dirt')

# Load size of washing machine (0 - 10)
load = ctrl.Antecedent(np.arange(0, 11, 1), 'load')

# -----------------------------
# 2. Define Output Variable
# -----------------------------

# Washing time (0 - 60 minutes)
time = ctrl.Consequent(np.arange(0, 61, 1), 'time')

# -----------------------------
# 3. Membership Functions
# -----------------------------

# Dirt level categories
dirt['low'] = fuzz.trimf(dirt.universe, [0, 0, 5])
dirt['medium'] = fuzz.trimf(dirt.universe, [0, 5, 10])
dirt['high'] = fuzz.trimf(dirt.universe, [5, 10, 10])

# Load size categories
load['low'] = fuzz.trimf(load.universe, [0, 0, 5])
load['medium'] = fuzz.trimf(load.universe, [0, 5, 10])
load['high'] = fuzz.trimf(load.universe, [5, 10, 10])

# Washing time categories
time['short'] = fuzz.trimf(time.universe, [0, 0, 20])
time['medium'] = fuzz.trimf(time.universe, [10, 30, 50])
time['long'] = fuzz.trimf(time.universe, [40, 60, 60])

# -----------------------------
# 4. Fuzzy Rules
# -----------------------------

rule1 = ctrl.Rule(dirt['low'] & load['low'], time['short'])
rule2 = ctrl.Rule(dirt['low'] & load['medium'], time['short'])
rule3 = ctrl.Rule(dirt['low'] & load['high'], time['medium'])

rule4 = ctrl.Rule(dirt['medium'] & load['low'], time['short'])
rule5 = ctrl.Rule(dirt['medium'] & load['medium'], time['medium'])
rule6 = ctrl.Rule(dirt['medium'] & load['high'], time['long'])

rule7 = ctrl.Rule(dirt['high'] & load['low'], time['medium'])
rule8 = ctrl.Rule(dirt['high'] & load['medium'], time['long'])
rule9 = ctrl.Rule(dirt['high'] & load['high'], time['long'])

# -----------------------------
# 5. Control System Creation
# -----------------------------

time_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3,
    rule4, rule5, rule6,
    rule7, rule8, rule9
])

timer = ctrl.ControlSystemSimulation(time_ctrl)

# -----------------------------
# 6. User Input
# -----------------------------

dirt_input = float(input("Enter Dirt Level (0 - 10): "))
load_input = float(input("Enter Load Size (0 - 10): "))

timer.input['dirt'] = dirt_input
timer.input['load'] = load_input

# -----------------------------
# 7. Compute Result
# -----------------------------

timer.compute()

# -----------------------------
# 8. Output Result
# -----------------------------

print("\n------ Washing Machine Result ------")
print("Dirt Level :", dirt_input)
print("Load Size  :", load_input)
print("Recommended Washing Time :", round(timer.output['time'],2), "minutes")

# -----------------------------
# 9. Show Membership Graph
# -----------------------------

dirt.view()
load.view()
time.view()