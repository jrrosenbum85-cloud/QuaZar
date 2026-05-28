import numpy as np

class NumpyRNNPredictor:
    def __init__(self, input_dim=10, hidden_dim=32):
        # Deterministically seed array parameters to avoid erratic logic behavior
        np.random.seed(42)
        self.W_xh = np.random.randn(hidden_dim, input_dim) * 0.01
        self.W_hh = np.random.randn(hidden_dim, hidden_dim) * 0.01
        self.b_h = np.zeros((hidden_dim, 1))
        self.h = np.zeros((hidden_dim, 1))

    def forward_step(self, x_input):
        """Executes forward matrix validation pass to forecast metric trends."""
        x = np.array(x_input).reshape(-1, 1)
        self.h = np.tanh(np.dot(self.W_xh, x) + np.dot(self.W_hh, self.h) + self.b_h)
        return self.h

class SGPSNeuralMatrix:
    def __init__(self, sequence_length=5):
        self.sequence_length = sequence_length
        self.model = NumpyRNNPredictor(input_dim=10, hidden_dim=32)
        self.history = []

    def log_and_predict(self, dynamic_state_vector):
        self.history.append(dynamic_state_vector)
        if len(self.history) > self.sequence_length:
            self.history.pop(0)
        return self.model.forward_step(dynamic_state_vector)

    def evaluate_and_reroute(self, prediction_tensor, ship_solver, ship_id, master_log_path):
        """Analyzes prediction tensor for spacetime anomalies and auto-reroutes."""
        # Simple heuristic: if the mean of the hidden state prediction drops below -0.2, assume danger
        anomaly_score = np.mean(prediction_tensor)
        
        if anomaly_score < -0.2: 
            # Danger detected! Reroute by applying an emergency thrust (outward radial & angular momentum)
            ship_solver.momentum[1] += 2500.0  
            ship_solver.momentum[3] += 1000.0
            
            log_msg = f"[AI-OVERRIDE] {ship_id} - Predicted anomalous spatial decay (Score: {anomaly_score:.3f}). Emergency reroute initiated to preserve asset.\n"
            
            with open(master_log_path, "a") as ml:
                ml.write(log_msg)
            print(f" -> {log_msg.strip()}")
            
            # Dampen the hidden state to avoid rerouting on every single micro-tick
            self.model.h *= 0.1
            return True
        return False