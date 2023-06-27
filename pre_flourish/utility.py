def bmi(child_weight_kg, child_height_cm):
    """Calculate BMI from weight in kg and height in cm."""
    return float(child_weight_kg) / (
            (float(child_height_cm) / 100.0) ** 2.0)
