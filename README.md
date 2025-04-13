# Reconstructing Quantum States
Group Members: Nikolas Cruz, Daniel Huffman, Aiden Mains, Saimonth Muñoz, Kate Saltovets
## [Alice and Bob Challenge](https://github.com/schlegeldavid/yq25_alice-bob_challenge/tree/main)
We use dynamiqs to simulate cat states and their Wigner functions. We reconstruct quantum states from noise-polluted data using the density matrix $\rho$. 

The Wigner function is a probability distribution in the complex plane. However, unlike a classical probability distribution, the Wigner function may take negative values, which is a sign of purely quantum interference.

We analyze experimental Wigner function data and use the observation values to fit a density matrix $\tilde{\rho}$. By computing the fidelty between the observed data and the numerically computed fit, we have a measurement of accuracy.

We analyze the accuracy of this fitting method by adding gaussian noise (with zero mean) to a Wigner function computed from a known quantum state by varying the standard deviation $\sigma$, which is equivalent to the magnitude of noise.
