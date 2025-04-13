import dynamiqs as dq
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np
import cvxpy as cp
import os


def run_quantum_tomography(
    N=50,
    n = 3,
    alpha0=2.0,
    state = "coherent",
    output_dir="outputs",
    x_range=(0, 4),
    y_range=(-2, 2),
    grid_points=20,
    solver="SCS",
    show_plots=True,
    save_outputs=True,
    return_problem=False,
):
    """
    Perform quantum state tomography on a coherent state using Dynamiqs.

    Parameters:
    - N: Hilbert space dimension
    - alpha0: Amplitude of the coherent state
    - output_dir: Directory to save plots and fidelity info
    - x_range, y_range: Tuple ranges for Wigner sampling
    - grid_points: Number of samples in x and y
    - solver: CVXPY solver (e.g., 'SCS', 'CVXOPT', 'MOSEK')
    - show_plots: If True, display plots inline
    - save_outputs: If True, save plots and fidelity.txt
    - return_problem: If True, also return CVXPY problem for inspection

    Returns:
    - rho_estimated: Estimated density matrix
    - fidelity: Reconstructed vs. true state fidelity
    - (optional) problem: The CVXPY optimization problem
    """
    if save_outputs and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # --- Generate state and Wigner function ---
    if state == "coherent":
        state = dq.coherent(N, alpha0)
        rho_true = dq.coherent_dm(N, alpha0)
    if state == "cat": #only 2-cat right now
        state = dq.coherent(N, alpha0)+dq.coherent(N, -alpha0)
        rho_true = dq.todm(state)
    if state == "fock":
        state = dq.fock(N,n)
        rho_true = dq.fock_dm(N, n)
    
    w = dq.wigner(
        state,
        xvec=np.linspace(*x_range, grid_points),
        yvec=np.linspace(*y_range, grid_points),
    )
    P = dq.parity(N)
    w_klist, E_ks = [], []

    # --- Construct measurement operators ---
    for a in range(len(w[0])):
        for b in range(len(w[1])):
            D_ak = dq.displace(N, complex(w[0][a], w[1][b]))
            D_T = D_ak.dag()
            W_a = w[2][a, b]
            E = 0.5 * (dq.eye(N) + D_ak @ P @ D_T)
            w_k = 0.5 * (1 + np.pi * W_a / 2)
            E_ks.append(E)
            w_klist.append(w_k)

    # --- Tomographic Reconstruction ---
    K = len(E_ks)
    rho_var = cp.Variable((N, N), complex=True)

    constraints = [rho_var >> 0, cp.trace(rho_var) == 1]
    residuals = [cp.real(cp.trace(E_ks[k] @ rho_var)) - w_klist[k] for k in range(K)]
    objective = cp.Minimize(cp.sum_squares(cp.hstack(residuals)))

    problem = cp.Problem(objective, constraints)
    problem.solve(solver=solver)

    rho_estimated = dq.asqarray(rho_var.value)

    # --- Fidelity Check ---
    fidelity = dq.fidelity(rho_true, rho_estimated)

    if save_outputs:
        with open(os.path.join(output_dir, "fidelity.txt"), "w") as f:
            f.write(f"Fidelity: {fidelity:.6f}\n")

    # --- Plot density matrices ---
    rho_est_np = np.abs(np.array(rho_estimated))
    rho_true_np = np.abs(np.array(rho_true))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    im1 = ax1.imshow(rho_true_np, cmap='viridis', origin='lower')
    ax1.set_title('Original Density Matrix |ρ|')
    fig.colorbar(im1, ax=ax1)

    im2 = ax2.imshow(rho_est_np, cmap='viridis', origin='lower')
    ax2.set_title('Estimated Density Matrix |ρ_estimated|')
    fig.colorbar(im2, ax=ax2)

    plt.tight_layout()
    if save_outputs:
        plt.savefig(os.path.join(output_dir, "density_matrix_comparison.png"))
    if show_plots:
        plt.show()
    else:
        plt.close()

    # --- Plot Wigner functions ---
    dq.plot.wigner(rho_true)
    plt.title("Wigner of Original Coherent State")
    if save_outputs:
        plt.savefig(os.path.join(output_dir, "wigner_true.png"))
    if show_plots:
        plt.show()
    else:
        plt.close()

    dq.plot.wigner(rho_estimated)
    plt.title("Wigner of Estimated Density Matrix")
    if save_outputs:
        plt.savefig(os.path.join(output_dir, "wigner_estimated.png"))
    if show_plots:
        plt.show()
    else:
        plt.close()

    if return_problem:
        return rho_estimated, fidelity, problem
    return rho_estimated, fidelity

