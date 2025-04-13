import cvxpy as cp
import numpy as np

def get_rho(w):
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

  K = len(E_ks)             # Number of measurement operators

  rho = cp.Variable((N, N), complex=True)

  constraints = [
      rho >> 0,             # Positive semidefinite
      cp.trace(rho) == 1,   # Trace normalization
  ]

  residuals = [cp.real(cp.trace(E_ks[k] @ rho)) - w_klist[k] for k in range(K)]
  objective = cp.Minimize(cp.sum_squares(cp.hstack(residuals)))


def add_noise(w, sigma):
  gaussian_noise = np.random.normal(0, sigma**2, size=w[2].shape)
  return (w[0], w[1], w[2] + gaussian_noise)


def FidelityVsSigma(w):
  F = []
  for s in sigma:
    noisy_wigner = add_noise(w, s)
    rho = dq.coherent_dm(N, 2)
    rho_est = get_rho(noisy_wigner)
    F.append(dq.fidelity(rho, rho_est))  
  return F

coh = dq.coherent(N, 2)
w = dq.wigner(coh, xvec=np.linspace(0,4,20), yvec=np.linspace(-2,2,20))
sigma = np.linspace(0.01,1,10)

plt.plot(sigma, FidelityVsSigma(w))
plt.xlabel('Sigma (Noise)')
plt.ylabel('Fidelity')
plt.show()
