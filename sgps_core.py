import numpy as np
from relativity_math import SpacetimeMetric
from neural_matrix import SGPSNeuralMatrix
from symplectic_integrator import SymplecticIntegrator

class SGPSMasterSolver:
    def __init__(self, initial_position, initial_momentum):
        self.position = np.array(initial_position, dtype=float)
        self.momentum = np.array(initial_momentum, dtype=float)
        
        # Instantiate architectural pipeline tracking properties
        self.proper_time = 0.0
        self.coordinate_time = 0.0
        self.hull_integrity = 100.0
        
        self.spacetime = SpacetimeMetric(None)
        self.integrator = SymplecticIntegrator(self.spacetime)
        self.forecaster = SGPSNeuralMatrix()
        self.history = []

    def flight_loop_step(self, dlambda):
        """Advances transport coordinates forward via canonical derivatives."""
        self.integrator.spacetime = self.spacetime
        
        dx_dl, dp_dl = self.integrator.calculate_geodesic_derivatives(self.position, self.momentum)
        
        # Update coordinates using explicit integration steps
        self.position += dx_dl * dlambda
        self.momentum += dp_dl * dlambda
        
        self.coordinate_time = self.position[0]
        self.proper_time += dlambda
        
        # Calculate instant physical coordinate speed metric
        speed_magnitude = np.sqrt(np.sum(dx_dl[1:]**2))
        self.history.append({"pos": np.copy(self.position), "speed": speed_magnitude})
        
        # Run forward predictive matrix logging rows
        state_features = np.zeros(10)
        state_features[:4] = self.position
        state_features[4:8] = self.momentum
        state_features[8] = speed_magnitude
        state_features[9] = self.hull_integrity
        self.forecaster.log_and_predict(state_features)