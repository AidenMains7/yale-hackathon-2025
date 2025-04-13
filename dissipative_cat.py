import dynamiqs as dq
import jax.numpy as jnp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle
from PIL import Image
from scipy import ndimage
import numpy as np
import cvxpy as cp

def plot_fock_state(state_number:int, n_dimensions:int=100) -> None:
  if n_dimensions <= state_number:
    print("The number of dimensions must be greater than the state number")
  fock = dq.fock(n_dimensions, state_number)
  fock_plot = dq.plot.wigner(fock)

def plot_cat_state(alpha:complex, n_dim=25) -> None:
  coh = dq.coherent(n_dim, alpha) + dq.coherent(n_dim, -alpha)
  wig_plot = dq.plot.wigner(coh)

def dissipative_cat(g2=1.0, epsilon_b=-4.0, kappa_b = 10.0, ndim_a = 25, ndim_b = 5):
  
  # Coupled annihilation operators of modes A and B
  a, b = dq.destroy(ndim_a, ndim_b)
  a_dag = a.dag()
  b_dag = b.dag()

  # Hamiltonian
  H = g2 * a_dag @ a_dag @ b + g2 * a @ a @ b_dag + epsilon_b * b + epsilon_b * b_dag
  
  t_grid = jnp.linspace(0., 4., 50)
  
  # Vacuum state
  psi0 = dq.tensor(dq.basis(ndim_a, 0), dq.basis(ndim_b, 0))
  
  jump_op = [jnp.sqrt(kappa_b) * b]
  
  result = dq.mesolve(H, jump_op, psi0, t_grid)
  return result
  
def plot_dissipative_gif(result_data_from_mesolve):
  return dq.plot.wigner_gif(result.states.ptrace(0), fps=25, clear=True)

def plot_expectation_value_of_modes(result_data_from_mesolve):
  n_a = a.dag() @ a  # Number opereator for mode 'a'
  n_a_vals = dq.expect(n_a, result_data_from_mesolve.states)
  n_a_vals = n_a_vals/n_a_vals.max()
  
  n_b = b.dag() @ b  # Number operator for mode 'b'
  n_b_vals = dq.expect(n_b, result_data_from_mesolve.states)
  n_b_vals = n_b_vals/n_b_vals.max()
  
  # Plot the expectation value of the photon number in mode 'a'
  fig, axs = plt.subplots(2, 1, figsize=(8, 4), sharex=True)
  axs[0].plot(t_grid, jnp.real(n_a_vals), label='real')
  axs[1].plot(t_grid, jnp.real(n_b_vals))
  for ax in axs.flatten():
    ax.grid()
  axs[0].set_ylabel("⟨a†a⟩")
  axs[1].set_ylabel("⟨b†b⟩")
  axs[1].set_xlabel("Time")
  fig.suptitle(r"Expectation value of modes $a$ and $b$")
  plt.tight_layout()
  plt.show()

if __name__ == "__main__":
  plot_fock_state(0)

  plot_cat_state(2.5 + 0.0j)

  result = dissipative_cat_state()
  plot_dissipative_gif(result)
  plot_expectation_value_of_modes(result)
  
