import numpy as np
from relativity_math import SpacetimeMetric

class SymplecticIntegrator:
    def __init__(self, spacetime: SpacetimeMetric):
        """
        Calculates Hamiltonian equations of motion across highly curved manifolds,
        strictly preserving the structural invariant Action Balance curve bounds.
        """
        self.spacetime = spacetime

    def calculate_geodesic_derivatives(self, position, momentum):
        """
        Computes the canonical derivatives utilizing standard numerical differentiation
        across the metric tensor variations to update coordinate velocities.
        """
        g_mu_nu = self.spacetime.metric_function(position)
        g_inv = np.linalg.inv(g_mu_nu)
        
        # Calculate velocities: dx^mu/dlambda = g^mu_nu * p_nu
        dx_dlambda = g_inv @ momentum
        dp_dlambda = np.zeros(self.spacetime.dim)
        
        # 64-bit numerical differentiator checking metric variations: partial g / partial x^mu
        delta = 1e-5
        for mu in range(self.spacetime.dim):
            x_pos = np.copy(position)
            x_neg = np.copy(position)
            x_pos[mu] += delta
            x_neg[mu] -= delta
            
            g_pos = self.spacetime.metric_function(x_pos)
            g_neg = self.spacetime.metric_function(x_neg)
            dg_dx_mu = (g_pos - g_neg) / (2.0 * delta)
            
            # dp_mu/dlambda = 0.5 * (partial g_alpha_beta / partial x^mu) * u^alpha * u^beta
            dp_dlambda[mu] = 0.5 * np.sum(dg_dx_mu * np.outer(dx_dlambda, dx_dlambda))
            
        return dx_dlambda, dp_dlambda