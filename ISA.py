import math

# ════════════════════════════════════════════════════════════════
# CONSTANTS — these never change anywhere in the atmosphere
# ════════════════════════════════════════════════════════════════
G = 9.80665      # gravity (m/s²)
R = 287.05       # gas constant for dry air (J/kg·K)

# Sea-level reference values (the "starting point" of the atmosphere)
T0 = 288.15      # temperature at sea level (K) = 15°C
P0 = 101325.0    # pressure at sea level (Pa) = 1 atm


# ════════════════════════════════════════════════════════════════
# LAYER TABLE — defines all 7 ISA layers
# Each row: (base_altitude_m, lapse_rate_K_per_m)
# ════════════════════════════════════════════════════════════════
# base_altitude → where this layer STARTS
# lapse_rate (L) → how fast temp changes with altitude in this layer
#   L < 0  → temp drops as you go up
#   L = 0  → temp stays constant (isothermal layer)
#   L > 0  → temp rises as you go up
LAYERS = [
    (0,      -0.0065),   # Troposphere       (0 – 11 km)
    (11000,   0.0),      # Tropopause        (11 – 20 km)
    (20000,   0.001),    # Stratosphere 1    (20 – 32 km)
    (32000,   0.0028),   # Stratosphere 2    (32 – 47 km)
    (47000,   0.0),      # Stratopause       (47 – 51 km)
    (51000,  -0.0028),   # Mesosphere 1      (51 – 71 km)
    (71000,  -0.002),    # Mesosphere 2      (71 – 86 km)
]
# top of the model
H_MAX = 86000   # max altitude (m) — model invalid above this


# ════════════════════════════════════════════════════════════════
# HELPER 1: find which layer an altitude belongs to
# ════════════════════════════════════════════════════════════════
def find_layer(altitude):
    # loop through layers and find the LAST one whose base is ≤ altitude
    # example: altitude=15000 → returns index 1 (Tropopause, base 11000)
    for i in range(len(LAYERS) - 1, -1, -1):  # iterate backwards
        if altitude >= LAYERS[i][0]:
            return i
    return 0   # fallback (sea level)
# i=6: 25000 >= 71000?  NO
# i=5: 25000 >= 51000?  NO
# i=4: 25000 >= 47000?  NO
# i=3: 25000 >= 32000?  NO
# i=2: 25000 >= 20000?  YES → return 2  ✅ CORRECT (stratosphere 1)

# ════════════════════════════════════════════════════════════════
# HELPER 2: compute T and P at the BASE of a given layer
# (we need this because each layer "starts" where the previous one ended)
# ════════════════════════════════════════════════════════════════
def base_conditions(layer_index):
    # start at sea level
    T = T0
    P = P0
    
    # walk UP through each layer below the target, stacking results
    for i in range(layer_index):
        h_base, L = LAYERS[i]              # current layer
        h_top, _ = LAYERS[i + 1]           # next layer's base = this layer's top
        dh = h_top - h_base                # thickness of this layer
        
        T_top = T + L * dh                 # temp at the TOP of this layer
        
        if L == 0:
            # isothermal layer → pressure drops EXPONENTIALLY
            P = P * math.exp(-G * dh / (R * T))
        else:
            # gradient layer → pressure follows POWER law
            P = P * (T_top / T) ** (-G / (R * L))
        
        T = T_top   # the top of this layer becomes the base of the next
    
    return T, P


# ════════════════════════════════════════════════════════════════
# MAIN FUNCTION: compute T, P, ρ at any altitude
def calculate_isa(altitude):
    # safety check
    if altitude < 0:
        raise ValueError("Altitude cannot be negative.")
    if altitude > H_MAX:
        raise ValueError(f"ISA model only valid up to {H_MAX/1000} km.")
    
    # step 1: figure out which layer we're in
    idx = find_layer(altitude)
    h_base, L = LAYERS[idx]
    
    # step 2: get T and P at the BASE of our layer
    T_base, P_base = base_conditions(idx)
    
    # step 3: how far ABOVE the base of this layer are we?
    dh = altitude - h_base
    
    # step 4: compute T at our altitude
    T = T_base + L * dh
    
    # step 5: compute P using the right formula for this layer
    if L == 0:
        # isothermal → exponential drop
        P = P_base * math.exp(-G * dh / (R * T))
    else:
        # gradient → power formula
        P = P_base * (T / T_base) ** (-G / (R * L))
    
    # step 6: density ALWAYS comes from ideal gas law (universal)
    rho = P / (R * T)
    
    return T, P, rho


# ════════════════════════════════════════════════════════════════
# USER INTERFACE (only runs when ISA.py is run directly)
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("  ISA CALCULATOR — up to 86 km")
    print("=" * 50)

    try:
        alt = float(input("Enter altitude in meters: "))
        T, P, rho = calculate_isa(alt)
        
        # convert to friendly units for display
        print(f"\nResults at {alt} m ({alt/1000:.1f} km):")
        print(f"  Temperature : {T:.2f} K  ({T - 273.15:.2f} °C)")
        print(f"  Pressure    : {P:.2f} Pa ({P/100:.2f} hPa)")
        print(f"  Density     : {rho:.6f} kg/m³")
        
        # pilot insight
        pct = (rho / 1.225) * 100
        print(f"\n[Density is {pct:.2f}% of sea level]")

    except ValueError as e:
        print(f"Error: {e}")