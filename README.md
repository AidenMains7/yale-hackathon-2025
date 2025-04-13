# Reconstructing Quantum States from the Wigner function
Group Members: Nikolas Cruz, Daniel Huffman, Aiden Mains, Saimonth Muñoz, Kate Saltovets 

Team Name: Cappuccino Assassino
## [Alice and Bob Challenge](https://github.com/schlegeldavid/yq25_alice-bob_challenge/tree/main)
We use Dynamiqs to simulate various quantum states and their Wigner functions. We reconstruct quantum states from noise-polluted data using the density matrix ρ that we get from Wigner function.

The Wigner function is a probability distribution in the complex plane. However, unlike a classical probability distribution, the Wigner function may take negative values, which is a sign of purely quantum interference.

Next, we measure accuracy by computing the fidelity of the observed data and the numerically computed fit.

Finally, we analyze the accuracy of this fitting method by adding gaussian noise (with zero mean) to a Wigner function computed from a known quantum state by varying the standard deviation $\sigma$, which is equivalent to the magnitude of noise.
