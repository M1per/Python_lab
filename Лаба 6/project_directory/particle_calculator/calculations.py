# particle_calculator/calculations.py

def calculate_specific_charge(mass, charge):
    """Calculate specific charge."""
    return charge / mass

def calculate_compton_wavelength(mass):
    """Calculate Compton wavelength."""
    h = 6.62607015e-34  # Planck's constant in J*s
    c = 299792458       # Speed of light in m/s
    return h / (mass * c)