class System:
    """Class that define a system to be analyzed. It can be linear or non-linear and continuous or discrete."""

    def __init__(
        self,
        is_linear: bool,
        is_continuous: bool,
        variables: list[float] = [],
        parameters: list[float] = [],
        equations: list[str] = [],
        initial_conditions: list[float] = [],
    ):
        self.is_linear = is_linear
        self.is_continuous = is_continuous
        self.variables = variables
        self.parameters = parameters
        self.equations = equations
        self.initial_conditions = initial_conditions

    def calculate_equilibrium_points(self):
        """Calculate the equilibrium points of the system."""
        # Placeholder for equilibrium point calculation logic
        print("Calculating equilibrium points...")
        # Implement actual calculation here
        equilibrium_points = [(0, 0)]  # Example placeholder
        return equilibrium_points

    def phase_diagram(self):
        """Generate the phase diagram of the system."""
        # Placeholder for phase diagram generation logic
        print("Generating phase diagram...")
        # Implement actual phase diagram generation here
        phase_diagram_data = {}  # Example placeholder
        return phase_diagram_data

    def simulate(self, time_span: tuple[float, float], time_steps: int):
        """Simulate the system over a given time span."""
        # Placeholder for simulation logic
        print(
            f"Simulating system from {time_span[0]} to {time_span[1]} with {time_steps} steps..."
        )
        # Implement actual simulation here
        simulation_results = []  # Example placeholder
        return simulation_results

    def __str__(self):
        return f"System(linear={self.is_linear}, continuous={self.is_continuous}, variables={self.variables}, parameters={self.parameters})"

    def __repr__(self):
        return self.__str__()

    def add_equation(self, equation: str):
        """Add an equation to the system."""
        self.equations.append(equation)

    def set_initial_conditions(self, initial_conditions: list[float]):
        """Set the initial conditions for the system."""
        self.initial_conditions = initial_conditions

    def get_equations(self):
        """Get the equations of the system."""
        return self.equations

    def get_initial_conditions(self):
        """Get the initial conditions of the system."""
        return self.initial_conditions

    def get_variables(self):
        """Get the variables of the system."""
        return self.variables

    def get_parameters(self):
        """Get the parameters of the system."""
        return self.parameters

    def is_nonlinear(self):
        """Check if the system is non-linear."""
        return not self.is_linear

    def is_discrete(self):
        """Check if the system is discrete."""
        return not self.is_continuous

    def summary(self):
        """Print a summary of the system."""
        print("System Summary:")
        print(f"  Linear: {self.is_linear}")
        print(f"  Continuous: {self.is_continuous}")
        print(f"  Variables: {self.variables}")
        print(f"  Parameters: {self.parameters}")
        print(f"  Equations: {self.equations}")
        print(f"  Initial Conditions: {self.initial_conditions}")
