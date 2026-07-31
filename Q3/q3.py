import numpy as np


class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initializes the RNN with random weights and zero biases.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.W_xh = np.random.randn(hidden_size, input_size) * 0.01
        self.W_hh = np.random.randn(hidden_size, hidden_size) * 0.01
        self.W_hy = np.random.randn(output_size, hidden_size) * 0.01

        self.b_h = np.zeros((hidden_size, 1))
        self.b_y = np.zeros((output_size, 1))

    def forward(self, x):
        """
        Forward pass through the RNN for a given sequence of inputs.
        """
        num_row = x.shape[0]
        h_previus = np.zeros((self.hidden_size, 1))

        step_network_state = []
        outputs = []

        step_network_state.append(h_previus)

        for t in range(num_row):
            current_x = x[t].reshape(-1, 1)
            current_h = np.tanh(np.dot(self.W_xh, current_x) + np.dot(self.W_hh, h_previus) + self.b_h)
            current_y = np.dot(self.W_hy, current_h) + self.b_y

            step_network_state.append(current_h)
            outputs.append(current_y)

            h_previus = current_h

        self.hidden_states = step_network_state
        self.outputs = np.hstack(outputs).T

        return self.outputs

    def backward(self, x, y, learning_rate):
        """
        Backpropagation through time to adjust weights.
        """
        predicate_output = self.forward(x)

        dw_xh = np.zeros(self.W_xh.shape)
        dw_hh = np.zeros(self.W_hh.shape)
        dw_hy = np.zeros(self.W_hy.shape)
        db_h = np.zeros(self.b_h.shape)
        db_y = np.zeros(self.b_y.shape)

        num_row = x.shape[0]

        dh_next_step = np.zeros((self.hidden_size , 1))
        for t in range(num_row - 1 , -1 , -1):
            current_x = x[t].reshape(-1,1)
            correct_y = y[t].reshape(-1,1)

            predicted_y = predicate_output[t].reshape(-1,1)
            h_current = self.hidden_states[t + 1]
            h_prev_step = self.hidden_states[t]

            dy = (predicted_y - correct_y) / self.output_size
            dw_hy += np.dot(dy, h_current.T)
            db_y += dy

            dh_from_output = np.dot(self.W_hy.T, dy)
            dh = dh_from_output + dh_next_step

            dh_active_func = dh * (1 - h_current ** 2)
            dw_xh += np.dot(dh_active_func, current_x.T)
            db_h += dh_active_func
            dw_hh += np.dot(dh_active_func, h_prev_step.T)
            dh_next_step = np.dot(self.W_hh.T , dh_active_func)

        self.W_xh = self.W_xh - learning_rate * dw_xh
        self.W_hh = self.W_hh - learning_rate * dw_hh
        self.W_hy = self.W_hy - learning_rate * dw_hy

        self.b_h = self.b_h - learning_rate * db_h
        self.b_y = self.b_y - learning_rate * db_y
