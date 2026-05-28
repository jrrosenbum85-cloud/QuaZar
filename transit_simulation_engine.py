import numpy as np
import os
import time
import uuid
from rando_truz_spaze import SpaceEnvironmentGenerator
from sgps_core import SGPSMasterSolver
from relativity_math import kerr_metric_function

def calculate_kerr_circular_momentum(M, a, r):
    omega = 1.0 / (r**(1.5) + a * np.sqrt(M))
    g_tt = -(1.0 - (2.0 * M / r))
    g_tphi = -(2.0 * M * a / r)
    g_phiphi = (r**2 + a**2 + (2.0 * M * a**2 / r))
    
    denom = g_tt + 2.0 * g_tphi * omega + g_phiphi * (omega**2)
    if denom >= 0: raise ValueError("Unstable coordinate zone.")
        
    u_t = np.sqrt(-1.0 / denom)
    u_phi = omega * u_t
    return [g_tt * u_t + g_tphi * u_phi, 0.0, 0.0, g_tphi * u_t + g_phiphi * u_phi]

def run_fleet_simulation():
    print("======================================================================")
    print("SGPS PHASE 4: PROJECT QUAZAR LONG-TERM FLEET DEPLOYMENT ENGINE")
    print("======================================================================")
    
    log_dir = "phase4_fleet_logs"
    if not os.path.exists(log_dir): os.makedirs(log_dir)
    
    env_engine = SpaceEnvironmentGenerator()
    master_log_path = os.path.join(log_dir, "master_fleet_history.log")
    
    if not os.path.exists(master_log_path):
        with open(master_log_path, "w") as ml:
            ml.write("=== SGPS MASTER FLIGHT REGISTRY: VEHICLE ENDURANCES AND METRICS ===\n")
            ml.write("-"*120 + "\n")
            ml.write(f"{'SHIP ID':<14} | {'SECTORS':<7} | {'TOP SPEED (c)':<13} | {'DISTANCE TRAVELED':<17} | {'PROPER TIME':<11} | {'DESTRUCTION CAUSE':<25}\n")
            ml.write("-"*120 + "\n")

    try:
        while True:
            ship_id = f"HULL-{uuid.uuid4().hex[:8].upper()}"
            ship_solver = SGPSMasterSolver([0.0, 100.0, np.pi/2, 0.0], [-1.0, 0.0, 0.0, 0.5])
            ship_solver.hull_integrity = 100.0
            
            sectors_cleared, max_speed, total_distance, total_proper_time = 0, 0.0, 0.0, 0.0
            final_fate = "Structural Fatigue Breakdown"
            
            ship_log_path = os.path.join(log_dir, f"ship_{ship_id}.log")
            with open(ship_log_path, "w") as sf:
                sf.write(f"=== FLIGHT CHRONICLE FOR INDIVIDUAL ASSET: {ship_id} ===\n")
                
                while ship_solver.hull_integrity > 0:
                    env = env_engine.formulate_environment_packet()
                    base_M = env["base_baryonic_mass_M"]
                    spin_a = env["kerr_spin_parameter_a"]
                    r0 = env["orbit_insertion_radius_r0"]
                    rs = env["horizon_rs"]
                    rho_dm = env["dark_matter_halo_density"]
                    
                    ship_solver.position = [ship_solver.position[0], r0, np.pi/2, 0.0]
                    try:
                        ship_solver.momentum = calculate_kerr_circular_momentum(base_M, spin_a, r0)
                    except ValueError:
                        continue
                    
                    steps = int(np.random.uniform(2500, 5000))
                    dlambda = max(1.0, float(10**(int(np.log10(base_M)) - 3)))
                    
                    for step in range(steps):
                        current_r = ship_solver.position[1]
                        if current_r <= rs + 1e-2:
                            final_fate = f"Horizon Singularity @ {env['catalog_anchor']}"
                            ship_solver.hull_integrity = 0.0
                            break
                        
                        # --- PHYSICAL EXOTIC MATTERS ALLOCATION MATRIX ---
                        # Dynamic Dark Matter profile density halo volumetric expansion tracking
                        # Includes a log-buffer for smoothing density spikes (Mass Parameter Smoothing)
                        dm_density_buffered = rho_dm * (1.0 + np.tanh(rho_dm / 1e-9))
                        enclosed_dm_mass = 4.0 * np.pi * (current_r ** 3) * dm_density_buffered * 1.5e5
                        dynamic_mass_parameter = base_M + enclosed_dm_mass
                        ship_solver.spacetime.metric_function = kerr_metric_function(mass=dynamic_mass_parameter, spin_a=spin_a)
                        
                        r_prev = current_r
                        ship_solver.flight_loop_step(dlambda=dlambda)
                        
                        # AI Rerouting check based on predictive matrix
                        if hasattr(ship_solver, 'last_prediction'):
                            ship_solver.forecaster.evaluate_and_reroute(
                                ship_solver.last_prediction,
                                ship_solver,
                                ship_id,
                                master_log_path
                            )
                        
                        # Accumulate structural tracks
                        current_speed = ship_solver.history[-1]['speed']
                        if current_speed > max_speed: max_speed = current_speed
                            
                        g_rr = (current_r**2) / (current_r**2 - 2.0*dynamic_mass_parameter*current_r + spin_a**2)
                        total_distance += np.sqrt(max(0.0, g_rr * ((ship_solver.position[1] - r_prev)**2)))
                        total_proper_time += dlambda
                        
                        # All unassigned weather parameters explicitly mapped into material destruction profile
                        # Coefficients recalibrated for extended endurance in high-entropy sectors
                        antimatter_wear = env["antimatter_density_m3"] * 1.2e-9
                        solar_wind_wear = env["solar_wind_velocity_flux_ev"] * 1.5e-11
                        grav_wave_strains = env["gravitational_wave_noise_hz"] * 1.2
                        tidal_tearing = (base_M * 2e-4) / (current_r ** 2)
                        
                        ship_solver.hull_integrity -= (antimatter_wear + solar_wind_wear + grav_wave_strains + tidal_tearing) * dlambda
                        
                        if ship_solver.hull_integrity <= 0:
                            final_fate = f"Environmental Fatigue @ {env['catalog_anchor']}"
                            break
                            
                    if ship_solver.hull_integrity <= 0:
                        break
                    sectors_cleared += 1
                    
            with open(master_log_path, "a") as ml:
                ml.write(f"{ship_id:<14} | {sectors_cleared:<7} | {max_speed:<13.5f} | {total_distance:<17.2f} | {total_proper_time:<11.1f} | {final_fate:<25}\n")
            print(f" -> Telemetry logged for {ship_id}. Sectors cleared: {sectors_cleared}.")
            time.sleep(0.4)
            
    except KeyboardInterrupt:
        print("\n[INFO] Run complete.")

if __name__ == "__main__":
    run_fleet_simulation()