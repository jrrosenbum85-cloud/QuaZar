import numpy as np
import requests
import uuid
import hashlib
import time

class SpaceEnvironmentGenerator:
    def __init__(self):
        self.nasa_url = (
            "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
            "query=select+top+5+pl_name,st_mass,st_teff+from+ps+"
            "where+st_mass+is+not+null+order+by+random()&format=json"
        )
        self.solar_fallbacks = [
            {"pl_name": "Alpha Centauri Core Node", "st_mass": 1.10, "st_teff": 5790.0},
            {"pl_name": "Sirius Gravitational Node", "st_mass": 2.06, "st_teff": 9940.0}
        ]

    def _generate_sha256_entropy_array(self):
        token = uuid.uuid4().hex
        digest = hashlib.sha256((token + str(time.time_ns())).encode('utf-8')).hexdigest()
        return [int(digest[i:i+8], 16) / 4294967295.0 for i in range(0, 64, 8)]

    def formulate_environment_packet(self):
        """Sources real planetary coordinates and layers cryptographic micro-modulations."""
        try:
            res = requests.get(self.nasa_url, timeout=3)
            macro_data = np.random.choice(res.json()) if res.status_code == 200 else np.random.choice(self.solar_fallbacks)
        except Exception:
            macro_data = np.random.choice(self.solar_fallbacks)
            
        entropy = self._generate_sha256_entropy_array()
        
        raw_name = macro_data.get("pl_name", "Procedural Zone")
        base_mass = float(macro_data.get("st_mass", 1.0))
        base_temp = float(macro_data.get("st_teff", 5778.0))
        
        # Dynamically scale systems up to black-hole classification tiers using entropy offsets
        mass = base_mass * (15.0 + (entropy[0] * 120.0)) if entropy[1] > 0.82 else base_mass * np.random.uniform(0.6, 4.0)
        spin_a = mass * entropy[2] * 0.98
        rs = 2.0 * mass
        r0 = rs * (8.0 + (entropy[3] * 140.0))
        
        return {
            "sector_id": f"SYS-EXO-{hashlib.md5(str(entropy).encode()).hexdigest()[:6].upper()}",
            "catalog_anchor": raw_name,
            "base_baryonic_mass_M": mass,
            "kerr_spin_parameter_a": spin_a,
            "horizon_rs": rs,
            "orbit_insertion_radius_r0": r0,
            # Quantum/Exotic Weather parameters mapping across integration layers
            "dark_matter_halo_density": entropy[4] * 2.5e-21,
            "antimatter_density_m3": entropy[5] * 4.8e4,
            "solar_wind_velocity_flux_ev": base_temp * (0.5 + entropy[6] * 3.5),
            "gravitational_wave_noise_hz": entropy[7] * 2.8e-4
        }