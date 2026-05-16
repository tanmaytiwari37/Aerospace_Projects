# 🌍 ISA Atmospheric Calculator

> A Python implementation of the **International Standard Atmosphere (ISA)** model — computes temperature, pressure, and density at any altitude from **0 to 86 km**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

---

## ✈️ About

The atmosphere isn't uniform — temperature, pressure, and density behave very differently as you climb through its layers. This project models the **vertical structure of Earth's atmosphere** using the official ISA equations adopted by ICAO and aerospace engineers worldwide.

Built as a 1st-year **Aerospace Engineering** project at **VIT Bhopal** to deepen my understanding of atmospheric physics — a foundation for flight performance, propulsion design, and re-entry trajectory analysis.

## 🎯 What It Does

Given an altitude (in meters), this calculator returns:

- 🌡️ **Temperature** (Kelvin & Celsius)
- 💨 **Pressure** (Pascals & hPa/mbar)
- ⚖️ **Density** (kg/m³)
- 📊 **Density ratio** (% of sea-level — useful for pilots)

It correctly handles **all 7 ISA layers**:

| Layer | Altitude (km) | Behavior |
|---|---|---|
| Troposphere | 0 – 11 | Temp drops linearly |
| Tropopause | 11 – 20 | Isothermal |
| Stratosphere 1 | 20 – 32 | Temp rises slowly |
| Stratosphere 2 | 32 – 47 | Temp rises faster |
| Stratopause | 47 – 51 | Isothermal |
| Mesosphere 1 | 51 – 71 | Temp drops |
| Mesosphere 2 | 71 – 86 | Temp drops slower |

## 🧠 The Physics

The ISA model treats the atmosphere as a layered fluid in **hydrostatic equilibrium** — the pressure at any altitude must support the weight of all the air above it. Three properties define the state of air at any altitude: **temperature (T)**, **pressure (P)**, and **density (ρ)**.

---

### 🌡️ 1. Temperature

Temperature changes **linearly** within each layer, governed by the layer's **lapse rate (L)**:

$$T = T_{base} + L \cdot \Delta h$$

Where:
- `T_base` = temperature at the base of the layer (K)
- `L` = lapse rate of the layer (K/m)
- `Δh` = altitude above the layer's base (m)

**Two cases:**
- `L ≠ 0` → **gradient layer** (temperature changes with altitude)
- `L = 0` → **isothermal layer** (temperature stays constant)

The sign of `L` matters:
- Negative `L` → temp drops with altitude (troposphere, mesosphere)
- Positive `L` → temp rises with altitude (stratosphere)

---

### 💨 2. Pressure

Pressure is derived from the **hydrostatic equation** combined with the **ideal gas law**. The resulting formula depends on whether the layer is gradient or isothermal — because the math diverges (you'd divide by zero in the gradient formula when L = 0).

**Gradient layers** (L ≠ 0) — *power-law decay*:

$$P = P_{base} \cdot \left(\frac{T}{T_{base}}\right)^{-G/(RL)}$$

**Isothermal layers** (L = 0) — *exponential decay*:

$$P = P_{base} \cdot e^{-G \cdot \Delta h / (RT)}$$

Where:
- `G` = standard gravity (9.80665 m/s²)
- `R` = specific gas constant for dry air (287.05 J/kg·K)
- `P_base` = pressure at the base of the layer (Pa)

**Why two formulas?** In gradient layers, temperature itself is a function of altitude, so the integration yields a power law. In isothermal layers, temperature is a constant — integration is simpler and gives a pure exponential.

---

### ⚖️ 3. Density

Density is **universal** — the same formula works in every layer because it comes directly from the **ideal gas law**:

$$\rho = \frac{P}{R \cdot T}$$

Once `T` and `P` are known at an altitude, density follows immediately. No layer-specific logic needed. ✅

---

### 📐 Constants Used

| Symbol | Value | Meaning |
|---|---|---|
| `G` | 9.80665 m/s² | Standard gravity |
| `R` | 287.05 J/(kg·K) | Specific gas constant for dry air |
| `T₀` | 288.15 K | Sea-level temperature (15°C) |
| `P₀` | 101325 Pa | Sea-level pressure (1 atm) |
| `ρ₀` | 1.225 kg/m³ | Sea-level density |
---

### 🔁 How They Connect

## 🛠️ Tech Stack

- **Python 3.10+** — core implementation
- **math** module — no external dependencies ✅

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.10
```

### Run
```bash
git clone https://github.com/tanmaytiwari37/Aerospace_Projects.git
cd Aerospace_Projects
python ISA.py
```

### Example Usage
==================================================
```
==================================================
  ISA CALCULATOR — up to 86 km
==================================================
Enter altitude in meters: 7000

Results at 7000.0 m (7.0 km):
  Temperature : 242.65 K  (-30.50 °C)
  Pressure    : 41061.23 Pa (410.61 hPa)
  Density     : 0.590015 kg/m³

[Density is 48.16% of sea level]
```

## 📁 Project Structure
```
Aerospace_Projects/
├── .gitignore
├──Graph.png            # Output in graph
├── ISA.py              # Main calculator
└── README.md
```

## 🧠 What I Learned

- **The ISA model** — how each atmospheric layer follows its own lapse rate
- **Translating physics into code** — converting textbook equations into clean Python
- **Data-driven design** — storing layer info in a table instead of hardcoded `if/elif` chains
- **Accumulator pattern** — "climbing" through layers to compute conditions at any altitude
- **Why models have limits** — ISA breaks down above 86 km because gases stop being uniformly mixed

## 🔭 Roadmap

- [ ] Plot full atmospheric profile (0–86 km) using `matplotlib`
- [ ] Add non-standard day calculations (hot day, cold day, tropical)
- [ ] Compute speed of sound and Mach number at altitude
- [ ] Extend with **NRLMSISE-00** model for altitudes above 86 km
- [ ] Wrap as a CLI tool with `argparse`

## ⚠️ Limitations

- Valid only from **0 to 86 km**. Above this, the ISA model breaks down because the atmosphere's composition changes with altitude (lighter gases like H and He separate out).
- Assumes a **standard atmosphere** — doesn't account for weather, latitude, or seasonal variation.

## 👨‍🚀 About Me

**Tanmay Tiwari** — 1st-year B.Tech Aerospace Engineering, VIT Bhopal

- 🌐 GitHub: [@tanmaytiwari37](https://github.com/tanmaytiwari37)
- 📧 itanmaytiwari37@gmail.com
- 🎯 Currently exploring: atmospheric modeling, computational fluid dynamics, and ML for aerospace systems

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and learn from it.

---
<sub>Built as part of independent study alongside coursework. Not affiliated with any commercial aviation or meteorological service.</sub>