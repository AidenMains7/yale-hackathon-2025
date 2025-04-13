import pickle
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage

# Load measured data
with open('noisy_wigner_0.pickle', 'rb') as f:
    data = pickle.load(f)
    xvec, yvec, W_measured = data
  
# Load generated data
with open('quantum_state_0.pickle', 'rb') as f:
    generated = pickle.load(f)

# 1. Estimate background (offset)
def estimate_background_b(W):
    edges = np.concatenate([
        W[0].ravel(),
        W[1].ravel(),
        W[-1].ravel(),
        W[-2].ravel(),
        W[:, 0].ravel(),
        W[:, 1].ravel(),
        W[:, -1].ravel(),
        W[:, -2].ravel(),
    ])
    return np.median(edges)

b = estimate_background_b(W_measured)

# 2. Subtract offset
W_unbiased = W_measured - b

# 3. Normalize so that integral over phase space = 1
dx = xvec[1] - xvec[0]
dy = yvec[1] - yvec[0]
norm = np.sum(W_filtered) * dx * dy
W_normalized = W_filtered / norm

# 4. Apply Gaussian filter (denoise)
W_filtered = scipy.ndimage.gaussian_filter(W_unbiased, sigma=5)


# 5. Rescale to be in [-2/π, +2/π]
# This step is optional if your normalization is correct, but if needed:
desired_max = 2 / np.pi
W_rescaled = W_normalized * desired_max

rescaled = (xvec, yvec, W_rescaled)

# Plot original measured Wigner function
plt.figure(figsize=(6, 5))
plt.imshow(W_measured, extent=[xvec[0], xvec[-1], yvec[0], yvec[-1]],
           origin='lower', cmap='RdBu_r', aspect='auto')
plt.xlabel('x')
plt.ylabel('p')
plt.title('Original Wigner Function (Measured)')
plt.colorbar()
plt.show()

# Plot denoised and normalized Wigner function
abs_max = np.max(np.abs(W_rescaled))
plt.figure(figsize=(6, 5))
plt.imshow(W_rescaled.T, extent=[xvec[0], xvec[-1], yvec[0], yvec[-1]],
           origin='lower', cmap='RdBu_r', aspect='auto',
           vmin=-abs_max, vmax=abs_max)
plt.xlabel('x')
plt.ylabel('p')
plt.title('Denoised & Normalized Wigner Function')
plt.colorbar()
plt.show()




def reconstruct_rho(coh):

  if len(coh) != 3:
    w = dq.wigner(coh, xvec=np.linspace(0,4,20), yvec=np.linspace(-2,2,20))
  else: 
    w= tuple(arr[::50] for arr in coh)

  print(len(w[0]))
  n = 50
  N = 50                 # Hilbert space dim
  points_x, points_y = [],[]
  min_val = 1
  max_val = 200
  for i in range(n):
    random_int = random.randint(min_val, max_val)
    points_x.append(random_int)
    random_int = random.randint(min_val, max_val)
    points_y.append(random_int)


  P = dq.parity(N)
  w_klist, E_ks = [], []

  for a in range(len(w[0])):
    for b in range(len(w[1])):
      D_ak = dq.displace(N, complex(w[0][a],w[1][b]))
      D_T = D_ak.dag()
      W_a = w[2][a,b]
      E = 1/2*(dq.eye(N)+D_ak @ P @ D_T)
      w_k = 1/2*(1+np.pi*W_a/2)
      E_ks.append(E)
      w_klist.append(w_k)


  import cvxpy as cp


  # Problem dimensions

  K = len(E_ks)             # Number of measurement operators

  # Variables
  rho = cp.Variable((N, N), complex=True)

  # Constraints:
  constraints = [
      rho >> 0,             # Positive semidefinite
      cp.trace(rho) == 1,   # Trace normalization
  ]

  # Objective:
  residuals = [cp.real(cp.trace(E_ks[k] @ rho)) - w_klist[k] for k in range(K)]
  objective = cp.Minimize(cp.sum_squares(cp.hstack(residuals)))

  # Solve
  problem = cp.Problem(objective, constraints)
  problem.solve(solver=cp.SCS)  # Or try 'CVXOPT', 'MOSEK', etc.

  # Extract solution
  return rho.value




rho_tilde = reconstruct_rho(rescaled)
rho = reconstruct_rho(generated)

F = dq.fidelity(rho, rho_tilde)
print(F)
