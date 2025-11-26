# Use of streamlit to create a web app for project management
import streamlit as st
from analyzer import StabilityAnalyzer
from system import System

if __name__ == "__main__":
    st.title("System Analysis App")

    # Define system properties
    is_linear = st.checkbox("Is the system linear?", value=True)
    is_continuous = st.checkbox("Is the system continuous?", value=True)

    # Input variables, parameters, equations, and initial conditions
    variables = st.text_input("Variables (comma-separated)", "x1,x2").split(",")
    parameters = list(
        map(float, st.text_input("Parameters (comma-separated)", "1.0,1.0").split(","))
    )
    equations = st.text_area(
        "Equations (one per line)", "dx1/dt = -p1*x1 + p2*x2\ndx2/dt = p1*x1 - p2*x2"
    ).split("\n")
    initial_conditions = list(
        map(
            float,
            st.text_input("Initial Conditions (comma-separated)", "1.0,0.0").split(","),
        )
    )

    # Create System instance
    system = System(
        is_linear=is_linear,
        is_continuous=is_continuous,
        variables=variables,
        parameters=parameters,
        equations=equations,
        initial_conditions=initial_conditions,
    )

    st.write("System created:", system)

    # Perform analyses
    if st.button("Calculate Equilibrium Points"):
        eq_points = system.calculate_equilibrium_points()
        st.write("Equilibrium Points:", eq_points)

    if st.button("Generate Phase Diagram"):
        phase_diag = system.phase_diagram()
        st.write("Phase Diagram Data:", phase_diag)

    if st.button("Simulate System"):
        time_span = (0.0, 10.0)
        time_steps = 100
        sim_results = system.simulate(time_span, time_steps)
        st.write("Simulation Results:", sim_results)

    if st.button("Analyze Stability"):
        analyzer = StabilityAnalyzer(system)
        stability_results = analyzer.analyze()
        st.write("Stability Analysis Results:", stability_results)
