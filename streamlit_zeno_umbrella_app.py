import numpy as np
import streamlit as st


def simulate_level_one(dt, total_time, sigma_base, sigma_amp, sigma_freq, z_base, z_amp, z_freq):
    t = np.arange(0, total_time, dt)
    e = np.zeros_like(t)
    e[0] = 1.0
    sigma = sigma_base + sigma_amp * np.sin(sigma_freq * t)
    z = z_base - z_amp * np.sin(z_freq * t)
    z = np.clip(z, 0.0, 0.999)

    for i in range(1, len(t)):
        d_e = -((1 - z[i]) * sigma[i] * e[i - 1]) * dt
        e[i] = e[i - 1] + d_e

    return t, e, z, sigma


def simulate_level_two(dt, total_time, sigma_base, sigma_amp, sigma_freq, z_initial, control_gain, target_energy):
    t = np.arange(0, total_time, dt)
    e = np.zeros_like(t)
    e[0] = 1.0
    sigma = sigma_base + sigma_amp * np.sin(sigma_freq * t)
    z = np.zeros_like(t)
    z[0] = z_initial

    for i in range(1, len(t)):
        z[i] = np.clip(z[i - 1] + control_gain * (e[i - 1] - target_energy) * dt, 0.0, 0.999)
        d_e = -((1 - z[i]) * sigma[i] * e[i - 1]) * dt
        e[i] = e[i - 1] + d_e

    return t, e, z, sigma


def simulate_level_three(grid_size, steps, dt, z_value, diffusion):
    e = np.ones((grid_size, grid_size))
    sigma = 1.0 + 0.5 * np.random.rand(grid_size, grid_size)

    for _ in range(steps):
        if diffusion > 0:
            laplacian = (
                np.roll(e, 1, axis=0)
                + np.roll(e, -1, axis=0)
                + np.roll(e, 1, axis=1)
                + np.roll(e, -1, axis=1)
                - 4 * e
            )
            e = e + diffusion * laplacian * dt
        e = e - (1 - z_value) * sigma * e * dt

    return e, sigma


st.set_page_config(page_title="Zeno Umbrella Simulator", layout="wide")

st.title("Zeno Umbrella Simulation")
st.markdown(
    "Simulate a Zeno-style loss-suppression system across three levels: a control toy model, "
    "feedback enforcement, and a spatial field toy."
)

level = st.sidebar.selectbox("Simulation level", ["Level 1: Control toy", "Level 2: Feedback", "Level 3: Spatial field"])

st.sidebar.header("Global settings")
dt = st.sidebar.number_input("Time step (dt)", min_value=0.001, max_value=0.1, value=0.01, step=0.001, format="%.3f")

if level in {"Level 1: Control toy", "Level 2: Feedback"}:
    total_time = st.sidebar.number_input("Total time", min_value=1.0, max_value=200.0, value=50.0, step=1.0)
    sigma_base = st.sidebar.slider("Sigma base", 0.1, 5.0, 1.0, 0.1)
    sigma_amp = st.sidebar.slider("Sigma amplitude", 0.0, 2.0, 0.3, 0.05)
    sigma_freq = st.sidebar.slider("Sigma frequency", 0.0, 2.0, 0.4, 0.05)

    if level == "Level 1: Control toy":
        st.sidebar.header("Zeno constraint")
        z_base = st.sidebar.slider("Z base", 0.0, 0.999, 0.98, 0.001)
        z_amp = st.sidebar.slider("Z amplitude", 0.0, 0.5, 0.02, 0.01)
        z_freq = st.sidebar.slider("Z frequency", 0.0, 2.0, 0.1, 0.05)

        t, e, z, sigma = simulate_level_one(
            dt, total_time, sigma_base, sigma_amp, sigma_freq, z_base, z_amp, z_freq
        )

    else:
        st.sidebar.header("Zeno feedback")
        z_initial = st.sidebar.slider("Initial Z", 0.0, 0.999, 0.9, 0.01)
        control_gain = st.sidebar.slider("Control gain", 0.1, 10.0, 2.0, 0.1)
        target_energy = st.sidebar.slider("Target energy", 0.1, 2.0, 1.0, 0.05)

        t, e, z, sigma = simulate_level_two(
            dt, total_time, sigma_base, sigma_amp, sigma_freq, z_initial, control_gain, target_energy
        )

    st.line_chart(
        {
            "Energy": e,
            "Zeno Z": z,
            "Sigma": sigma,
        },
        height=350,
    )

else:
    st.sidebar.header("Spatial field settings")
    grid_size = st.sidebar.slider("Grid size", 10, 100, 50, 5)
    steps = st.sidebar.slider("Steps", 10, 2000, 500, 10)
    z_value = st.sidebar.slider("Z value", 0.0, 0.999, 0.98, 0.001)
    diffusion = st.sidebar.slider("Diffusion", 0.0, 1.0, 0.0, 0.01)

    e, sigma = simulate_level_three(grid_size, steps, dt, z_value, diffusion)

    col1, col2 = st.columns(2)

    with col1:
        st.image(e, caption="Energy field", clamp=True)

    with col2:
        st.image(sigma, caption="Sigma field", clamp=True)

st.markdown(
    """
    **Interpretation**
    - The Zeno term suppresses decay rather than eliminating loss.
    - Stronger Z or faster feedback keeps the energy closer to the target.
    - The spatial field highlights how loss varies across space.
    """
)
