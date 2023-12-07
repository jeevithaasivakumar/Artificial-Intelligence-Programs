class CertaintyFactor:
    def __init__(self, belief, disbelief, uncertainty):
        self.belief = belief
        self.disbelief = disbelief
        self.uncertainty = uncertainty

    def calculate_cf(self):
        if self.uncertainty == 0:
            return self.belief - self.disbelief
        else:
            return (self.belief - self.disbelief) * (1 - abs(self.uncertainty))

# Input from the user
temperature = float(input("Enter the temperature (in degrees Fahrenheit): "))
humidity = float(input("Enter the humidity (normalized between 0 and 1): "))
belief = float(input("Enter the degree of belief (0 to 1): "))
disbelief = float(input("Enter the degree of disbelief (0 to 1): "))
uncertainty = float(input("Enter the degree of uncertainty (0 to 1): "))

# Check if the input values are within the valid range
if 0 <= temperature <= 100 and 0 <= humidity <= 1 and 0 <= belief <= 1 and 0 <= disbelief <= 1 and 0 <= uncertainty <= 1:
    cf = CertaintyFactor(belief, disbelief, uncertainty)
    certainty_factor = cf.calculate_cf()

    # Define the fuzzy_membership function
    def fuzzy_membership(value, low, high):
        if value <= low:
            return 0.0
        elif value >= high:
            return 1.0
        else:
            return (value - low) / (high - low)

    # Define additional fuzzy linguistic variables and rules
    # Example: Comfort level
    very_uncomfortable = min(fuzzy_membership(temperature, 80, 100), fuzzy_membership(humidity, 0.7, 1))
    uncomfortable = min(fuzzy_membership(temperature, 70, 80), fuzzy_membership(humidity, 0.6, 0.7))
    comfortable = min(fuzzy_membership(temperature, 60, 70), fuzzy_membership(humidity, 0.4, 0.6))
    very_comfortable = min(fuzzy_membership(temperature, 50, 60), fuzzy_membership(humidity, 0, 0.4))

    # Aggregation of fuzzy rules (e.g., using "max" operator)
    aggregated_comfort = max(very_uncomfortable, uncomfortable, comfortable, very_comfortable)

    # Defuzzification using the certainty factor
    defuzzified_comfort = certainty_factor * aggregated_comfort

    print("Certainty Factor:", certainty_factor)
    print("Fuzzy Output (Comfort Level - Before Defuzzification):", defuzzified_comfort)
else:
    print("Invalid input values. Please enter values within the valid range.")
