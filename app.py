import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from ISA import calculate_isa, H_MAX

# ════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ISA Calculator",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 ISA Atmospheric Calculator")
st.markdown("### Compute Temperature, Pressure, and Density at any altitude (0 – 86 km)")
st.markdown("---")


# ════════════════════════════════════════════════════════════════
# USER INPUT
# ════════════════════════════════════════════════════════════════
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 Enter Altitude")
    altitude = st.number_input(
        "Altitude (meters):",
        min_value=0.0,
        max_value=float(H_MAX),
        value=7000.0,
        step=500.0,
        help="Range: 0 to 86,000 meters"
    )
    
    # ── Compute values at the user's altitude ─────────────
    T, P, rho = calculate_isa(altitude)
    
    st.markdown("### 📊 Results")
    
    # Display 3 metrics
    st.metric("🌡️ Temperature", f"{T:.2f} K", f"{T - 273.15:.2f} °C")
    st.metric("💨 Pressure", f"{P:.2f} Pa", f"{P/100:.2f} hPa")
    st.metric("⚖️ Density", f"{rho:.6f} kg/m³", f"{(rho/1.225)*100:.2f}% of sea level")


# ════════════════════════════════════════════════════════════════
# GENERATE FULL PROFILE FROM 0 TO 86 KM
# ════════════════════════════════════════════════════════════════
with col2:
    st.subheader("📈 Atmospheric Profile (0 – 86 km)")
    
    #️⃣ Create 500 evenly-spaced altitudes from 0 to H_MAX
    altitudes = np.linspace(0, H_MAX, 500)
    
    #️⃣ Compute T, P, ρ at each altitude
    temps = []
    pressures = []
    densities = []
    
    for h in altitudes:
        t, p, r = calculate_isa(h)
        temps.append(t)
        pressures.append(p)
        densities.append(r)
    
    #️⃣ Convert altitudes to km for plotting (cleaner axis)
    alt_km = altitudes / 1000
    
    # ── Create 3 subplots ─────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    
    # Plot 1: Temperature
    axes[0].plot(temps, alt_km, color='tomato', linewidth=2)
    axes[0].axhline(y=altitude/1000, color='black', linestyle='--', alpha=0.5)
    axes[0].set_xlabel("Temperature (K)")
    axes[0].set_ylabel("Altitude (km)")
    axes[0].set_title("🌡️ Temperature vs Altitude")
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Pressure (log scale because it drops 6 orders of magnitude)
    axes[1].plot(pressures, alt_km, color='steelblue', linewidth=2)
    axes[1].axhline(y=altitude/1000, color='black', linestyle='--', alpha=0.5)
    axes[1].set_xlabel("Pressure (Pa)")
    axes[1].set_xscale('log')  # log scale = better visualization
    axes[1].set_ylabel("Altitude (km)")
    axes[1].set_title("💨 Pressure vs Altitude")
    axes[1].grid(True, alpha=0.3, which='both')
    
    # Plot 3: Density (also log scale)
    axes[2].plot(densities, alt_km, color='seagreen', linewidth=2)
    axes[2].axhline(y=altitude/1000, color='black', linestyle='--', alpha=0.5)
    axes[2].set_xlabel("Density (kg/m³)")
    axes[2].set_xscale('log')
    axes[2].set_ylabel("Altitude (km)")
    axes[2].set_title("⚖️ Density vs Altitude")
    axes[2].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    st.pyplot(fig)


# ════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════
st.markdown("---")
st.caption(
    "Based on the International Standard Atmosphere (ISA) model. "
    "Dashed line on plots indicates your selected altitude. "
    "Pressure and density use log scale because they span several orders of magnitude."
)