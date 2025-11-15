# dec_exp01_pendulum_v_rock.py
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Helper functions
# -------------------------
def tanh(x): 
    return np.tanh(x)

def generate_challenge(T, dt, low_freq=0.01, high_freq=0.5, amp_low=0.6, amp_high=0.4, noise_level=0.05, spike_prob=0.002, spike_amp=1.0):
    t = np.arange(0, T*dt, dt)
    low = amp_low * np.sin(2*np.pi*low_freq*t)
    high = amp_high * np.sin(2*np.pi*high_freq*t)
    noise = noise_level * np.random.randn(len(t))
    spikes = np.zeros_like(t)
    # rare spikes
    spike_inds = np.random.rand(len(t)) < spike_prob
    spikes[spike_inds] = spike_amp * (2*np.random.randint(0,2,size=spike_inds.sum()) - 1)
    c = (low + high + noise + spikes)
    # clip to [-1,1]
    c = np.clip(c, -1.0, 1.0)
    return t, c

def desired_response(c):
    # simple desired = sign (with 0 mapped to 0)
    d = np.sign(c)
    return d

# -------------------------
# Agent dynamics
# -------------------------
def simulate_rock(c, alpha_rock=1.0, bias=0.0, alpha_c=1.0):
    # rock decision per time step; static bias
    a = tanh(alpha_rock * bias + alpha_c * c)
    return a

def simulate_pendulum(c, dt=0.1, gamma=0.5, omega0=1.0, k_drive=1.0, alpha_theta=1.0, alpha_c=0.2):
    N = len(c)
    theta = np.zeros(N)
    v = np.zeros(N)
    a = np.zeros(N)
    # initial conditions
    theta[0] = 0.0
    v[0] = 0.0
    for i in range(1, N):
        # discrete time integration (Euler)
        v[i] = v[i-1] + dt * (-gamma * v[i-1] - (omega0**2) * theta[i-1] + k_drive * c[i-1])
        theta[i] = theta[i-1] + dt * v[i]
        a[i] = tanh(alpha_theta * theta[i] + alpha_c * c[i])
    return a, theta, v

# -------------------------
# Utility and failure metrics
# -------------------------
def compute_utility(a, c):
    d = desired_response(c)
    u = 1.0 - np.abs(a - d)  # higher is better (<=1)
    return u

# -------------------------
# Single-run demo and plotting
# -------------------------
def run_demo():
    # Simulation settings
    T = 2000      # number of steps
    dt = 0.02
    t, c = generate_challenge(T, dt, low_freq=0.02, high_freq=1.2, amp_low=0.6, amp_high=0.4, noise_level=0.05, spike_prob=0.003, spike_amp=1.0)

    # Rock params (rigid)
    alpha_rock = 2.0
    bias = 0.0
    alpha_c = 1.0
    a_rock = simulate_rock(c, alpha_rock=alpha_rock, bias=bias, alpha_c=alpha_c)
    u_rock = compute_utility(a_rock, c)
    U_rock = np.cumsum(u_rock)

    # Pendulum params (adaptive)
    gamma = 0.9
    omega0 = 2.0
    k_drive = 1.8
    alpha_theta = 0.9
    alpha_c = 0.2
    a_pend, theta, v = simulate_pendulum(c, dt=dt, gamma=gamma, omega0=omega0, k_drive=k_drive, alpha_theta=alpha_theta, alpha_c=alpha_c)
    u_pend = compute_utility(a_pend, c)
    U_pend = np.cumsum(u_pend)

    # Plot
    fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    axs[0].plot(t, c, label='Challenge c_t', color='black')
    axs[0].set_ylabel('c_t')
    axs[0].legend(loc='upper right')

    axs[1].plot(t, a_rock, label='Rock decision', color='tab:orange', alpha=0.9)
    axs[1].plot(t, a_pend, label='Pendulum decision', color='tab:blue', alpha=0.9)
    axs[1].plot(t, desired_response(c), '--', label='Desired (sign)', color='gray', alpha=0.6)
    axs[1].set_ylabel('decisions a_t')
    axs[1].legend(loc='upper right')

    axs[2].plot(t, u_rock, label='Rock instant utility', color='tab:orange', alpha=0.6)
    axs[2].plot(t, u_pend, label='Pendulum instant utility', color='tab:blue', alpha=0.6)
    axs[2].set_ylabel('u_t')
    axs[2].legend(loc='upper right')

    axs[3].plot(t, U_rock, label='Rock cumsum utility', color='tab:orange')
    axs[3].plot(t, U_pend, label='Pendulum cumsum utility', color='tab:blue')
    axs[3].set_ylabel('Cumulative U')
    axs[3].set_xlabel('time')
    axs[3].legend(loc='upper right')

    plt.tight_layout()
    plt.show()

    # Print final summary
    print("Final cumulative utility: Rock = {:.1f}, Pendulum = {:.1f}".format(U_rock[-1], U_pend[-1]))
    print("Mean instant utility: Rock = {:.3f}, Pendulum = {:.3f}".format(np.mean(u_rock), np.mean(u_pend)))

if __name__ == "__main__":
    run_demo()
