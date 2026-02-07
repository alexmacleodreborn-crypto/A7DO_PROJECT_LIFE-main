import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(page_title="Zeno Umbrella Simulator", layout="wide")

st.title("Zeno Umbrella Simulator")
st.markdown(
    """
This app runs three progressively richer simulations of a Zeno-style loss suppression system:
1) a control-system toy model, 2) feedback-enforced Zeno constraint, 3) a spatial field toy.
"""
)


def simulate_level1(dt, total_time, sigma_base, sigma_amp, sigma_freq, z_base, z_amp, z_freq):
    t = np.arange(0, total_time, dt)
    e = np.zeros_like(t)
    e[0] = 1.0
    sigma = sigma_base + sigma_amp * np.sin(sigma_freq * t)
    z = z_base - z_amp * np.sin(z_freq * t)
    z = np.clip(z, 0.0, 0.999)

    for i in range(1, len(t)):
        d_e = - (1 - z[i]) * sigma[i] * e[i - 1] * dt
        e[i] = e[i - 1] + d_e

    return t, e, sigma, z


def simulate_level2(dt, total_time, sigma_base, sigma_amp, sigma_freq, z_init, e_target, gain, z_min, z_max):
    t = np.arange(0, total_time, dt)
    e = np.zeros_like(t)
    e[0] = 1.0
    sigma = sigma_base + sigma_amp * np.sin(sigma_freq * t)
    z = np.zeros_like(t)
    z[0] = z_init

    for i in range(1, len(t)):
        z[i] = np.clip(z[i - 1] + gain * (e[i - 1] - e_target) * dt, z_min, z_max)
        d_e = - (1 - z[i]) * sigma[i] * e[i - 1] * dt
        e[i] = e[i - 1] + d_e

    return t, e, sigma, z


def simulate_level3(grid_size, steps, dt, z_value, sigma_min, sigma_max, diffusion, seed):
    rng = np.random.default_rng(seed)
    e = np.ones((grid_size, grid_size), dtype=float)
    sigma = rng.uniform(sigma_min, sigma_max, size=(grid_size, grid_size))

    for _ in range(steps):
        decay = (1 - z_value) * sigma * e
        e -= decay * dt
        if diffusion > 0:
            e = (
                e
                + diffusion
                * dt
                * (
                    np.roll(e, 1, axis=0)
                    + np.roll(e, -1, axis=0)
                    + np.roll(e, 1, axis=1)
                    + np.roll(e, -1, axis=1)
                    - 4 * e
                )
            )
        e = np.clip(e, 0.0, None)

    return e, sigma


with st.sidebar:
    st.header("Global Settings")
    dt = st.number_input("dt", min_value=0.001, max_value=0.1, value=0.01, step=0.001, format="%.3f")
    total_time = st.number_input("Total time", min_value=1.0, max_value=200.0, value=50.0, step=1.0)

    st.header("Loss (Σ) settings")
    sigma_base = st.slider("Σ base", 0.1, 5.0, 1.0, 0.1)
    sigma_amp = st.slider("Σ amplitude", 0.0, 2.0, 0.3, 0.05)
    sigma_freq = st.slider("Σ frequency", 0.0, 2.0, 0.4, 0.05)

    st.header("Z settings")
    z_base = st.slider("Z base", 0.0, 0.999, 0.98, 0.001)
    z_amp = st.slider("Z amplitude", 0.0, 0.2, 0.02, 0.01)
    z_freq = st.slider("Z frequency", 0.0, 1.0, 0.1, 0.05)

    st.header("Feedback settings (Level 2)")
    z_init = st.slider("Z initial", 0.0, 0.999, 0.9, 0.01)
    e_target = st.slider("Target energy", 0.1, 2.0, 1.0, 0.05)
    gain = st.slider("Feedback gain", 0.0, 10.0, 2.0, 0.1)
    z_min = st.slider("Z min", 0.0, 0.999, 0.0, 0.01)
    z_max = st.slider("Z max", 0.0, 0.999, 0.999, 0.001)

    st.header("Field settings (Level 3)")
    grid_size = st.slider("Grid size", 10, 100, 50, 5)
    steps = st.slider("Steps", 10, 2000, 500, 50)
    z_value = st.slider("Z (field)", 0.0, 0.999, 0.98, 0.001)
    sigma_min = st.slider("Σ min", 0.1, 5.0, 1.0, 0.1)
    sigma_max = st.slider("Σ max", 0.1, 5.0, 1.5, 0.1)
    diffusion = st.slider("Diffusion D", 0.0, 1.0, 0.0, 0.05)
    seed = st.number_input("Random seed", min_value=0, max_value=9999, value=7, step=1)


level1_tab, level2_tab, level3_tab = st.tabs(["Level 1: Control", "Level 2: Feedback", "Level 3: Field"])

with level1_tab:
    st.subheader("Level 1 — Control-System Toy Model")
    t, e, sigma, z = simulate_level1(dt, total_time, sigma_base, sigma_amp, sigma_freq, z_base, z_amp, z_freq)
    df = pd.DataFrame({"time": t, "energy": e, "sigma": sigma, "z": z})
    st.line_chart(df, x="time", y=["energy", "z"])
    st.caption("Energy stays stable as Z approaches 1 while Σ remains nonzero.")

with level2_tab:
    st.subheader("Level 2 — Feedback-Enforced Zeno Constraint")
    t, e, sigma, z = simulate_level2(
        dt, total_time, sigma_base, sigma_amp, sigma_freq, z_init, e_target, gain, z_min, z_max
    )
    df = pd.DataFrame({"time": t, "energy": e, "sigma": sigma, "z": z})
    st.line_chart(df, x="time", y=["energy", "z"])
    st.caption("Z adjusts based on energy drift to suppress decay.")

with level3_tab:
    st.subheader("Level 3 — Spatial Field Model")
    e_field, sigma_field = simulate_level3(grid_size, steps, dt, z_value, sigma_min, sigma_max, diffusion, seed)
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        im = ax.imshow(e_field, cmap="viridis")
        ax.set_title("Energy field")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        im = ax.imshow(sigma_field, cmap="magma")
        ax.set_title("Loss field (Σ)")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        st.pyplot(fig)
    st.caption("Energy remains distributed despite spatially varying loss.")

st.markdown(
    """
---
**Run locally:** `streamlit run streamlit_zeno_umbrella_app.py`
"""
)
