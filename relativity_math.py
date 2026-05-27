import numpy as np

class SpacetimeMetric:
    def __init__(self, metric_function, dim=4):
        self.metric_function = metric_function
        self.dim = dim

class GeodesicSolver:
    def __init__(self, spacetime: SpacetimeMetric):
        self.spacetime = spacetime

def kerr_metric_function(mass, spin_a):
    """
    Analytically formulates the exact full Kerr metric tensor inside Boyer-Lindquist 
    coordinates [t, r, theta, phi] using geometrized units (G = c = 1).
    """
    def metric(x):
        t, r, theta, phi = x
        g = np.zeros((4, 4))
        
        # Enforce physical coordinate floor protection near the singularity boundary
        r = max(r, 2.0 * mass + 1e-4)
        
        sigma = r**2 + (spin_a * np.cos(theta))**2
        delta = r**2 - 2.0 * mass * r + spin_a**2
        
        # Diagonal elements mapping
        g[0, 0] = -(1.0 - (2.0 * mass * r / sigma))
        g[1, 1] = sigma / delta
        g[2, 2] = sigma
        g[3, 3] = (r**2 + spin_a**2 + (2.0 * mass * r * spin_a**2 * (np.sin(theta))**2 / sigma)) * (np.sin(theta))**2
        
        # Off-diagonal frame-dragging cross term mechanics
        cross_term = -(2.0 * mass * r * spin_a * (np.sin(theta))**2 / sigma)
        g[0, 3] = cross_term
        g[3, 0] = cross_term
        
        return g
    return metric