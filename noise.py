import dynamiqs as dq
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np


def add_gaussian_noise(wigner, sigma:float):
  return wigner + np.random.normal(0, sigma**2, size=wigner.shape)

def plot_fock_noise_comparison(sigma):
  fock = dq.fock(8, 3)
  x, y, z = dq.wigner(fock)
  noisy_wigner = add_gaussian_noise(z, np.sqrt(0.125))
  
  fig, axs = plt.subplots(1, 2)
  im0 = axs[0].imshow(z, cmap="RdBu")
  im1 = axs[1].imshow(noisy_wigner, cmap="RdBu")
  axs[0].set_title("Original Wigner Function")
  axs[1].set_title(r"Noisy Wigner Function: $\sigma^2$="+str(sigma) )
  
  for ax in axs.flatten():
    for spine in ax.spines.values():
      spine.set_edgecolor("black")
      spine.set_linewidth(1)
    ax.tick_params(axis="both", color="black", labelcolor="black",bottom=False,top=False,left=False,right=False,
                   labelbottom=False,labelleft=False)
  plt.tight_layout()
  plt.colorbar(im1, ax=axs, orientation="horizontal")
  fig.subplots_adjust(bottom=0.2)
  plt.show()

if __name__ == "__main__":
  plot_fock_noise_comparison()
