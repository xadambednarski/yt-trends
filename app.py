import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("Sinus Function Plotter")

# Sidebar for parameters
st.sidebar.header("Adjust Sinusoidal Parameters")

# Inputs for amplitude, frequency, phase, and range
amplitude = st.sidebar.slider("Amplitude", 0.1, 5.0, 1.0)
frequency = st.sidebar.slider("Frequency", 0.1, 10.0, 1.0)
phase = st.sidebar.slider("Phase Shift", 0.0, 2 * np.pi, 0.0, step=0.1)
x_min = st.sidebar.number_input("X-axis Minimum", value=0.0)
x_max = st.sidebar.number_input("X-axis Maximum", value=10.0)

# Check for valid x-axis range
if x_min >= x_max:
    st.error("X-axis minimum must be less than X-axis maximum.")
else:
    # Generate x and y values
    x = np.linspace(x_min, x_max, 500)
    y = amplitude * np.sin(2 * np.pi * frequency * x + phase)

    # Plot the function
    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"{amplitude} * sin(2π * {frequency} * x + {phase:.2f})")
    ax.set_title("Sinus Function")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)
