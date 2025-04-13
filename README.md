# Reconstructing Quantum States Using the Wigner Function
Group Members: Nikolas Cruz, Daniel Huffman, Aiden Mains, Saimonth Muñoz, Kate Saltovets 

Team Name: Cappuccino Assassino
## [Alice and Bob Challenge](https://github.com/schlegeldavid/yq25_alice-bob_challenge/tree/main)
We use Dynamiqs to simulate various quantum states and their Wigner functions. We reconstruct quantum states from noise-polluted data using the density matrix ρ that we get from Wigner function.

The Wigner function is a probability distribution in the complex plane. However, unlike a classical probability distribution, the Wigner function may take negative values, which is a sign of purely quantum interference.

Next, we measure accuracy by computing the fidelity of the observed data and the numerically computed fit.

Finally, we analyze the accuracy of this fitting method by adding gaussian noise (with zero mean) to a Wigner function computed from a known quantum state by varying the standard deviation $\sigma$, which is equivalent to the magnitude of noise.

# Results

## Part A

We obtained Wigner function for the following states: 

Fock state $\ket{n=3}$

![download (1)](https://github.com/user-attachments/assets/7bfccff6-fa46-44e1-83ac-4ff5fcd6ceb8)

Coherent state $\alpha = 2$

![download (2)](https://github.com/user-attachments/assets/ac8a0fca-e8ab-4363-a217-af17ba8bdef8)

2-cat state and 3-cat state:

![download (3)](https://github.com/user-attachments/assets/a62ff175-3652-457a-b193-bd9ff61a2ea4)

![3](https://github.com/user-attachments/assets/d6225083-20ba-4144-b4c8-e3a063fc759e)

## Part B: Estimating density matrix

We obtained a great result for the coherent state with $\alpha = 2$

![image (2)](https://github.com/user-attachments/assets/508eaf44-1781-4fc7-b404-e1a441f933e3)

With a Fidelity = 1.0001802. We also reconstructed the Wigner function for the estimated state:

![download (1) (1)](https://github.com/user-attachments/assets/a2c3c842-37f2-4e24-bff0-bd3f650f3827)

Fidelity of the 2-cat state with $\alpha = 2$, on the other hand, had the worst performance, improving up to 1.5 as we zoom in closer into the function while we're probing the points. 


