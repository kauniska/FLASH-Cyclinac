import numpy as np
import matplotlib.pyplot as plt

def beta(W):
    # for protons with M=938.3MeV
    gamma = (W+938.3)/938.3
    return np.sqrt(1 - 1/(gamma**2))
    
def calculate_cell_length(Beta_in, W_in, m, lambd, q, E0T, phi):  # Energies inputted in MeV
    i = 0
    Beta = 0
    Beta_av = Beta_in
    check = False
    while check == False:
        if i != 0:
            Beta_av = Beta
        l = m*Beta_av*lambd/2
        dW = q*E0T*l*np.cos(phi)/(1.602*10**(-13))  # into MeV
        W_av = W_in + dW/2
        Beta = beta(W_av)
        check = np.abs(Beta-Beta_av) < 10**(-6)
        i += 1
        
    W_out = W_in + dW
    Beta_out = beta(W_out)
    return l, Beta_out, W_out


cell_lengths = []
energies = []
betas = []

# Define initial parameters
m = 983.3  # MeV/c2
W = 70  # Injection at 70 MeV
Beta = beta(W)
print(W)

# Define accelerator properties
E0T = 5*10**6 # Accelerating gradient
#phi = -30/180 * np.pi
phi = 2*np.pi
lambd = 299792458/(3*10**9) # 3 GHz

# Calculate cell lenghts until target kinetic energy of 230 MeV is reached
while W < 230:
    betas.append(Beta)
    energies.append(W)
    l, Beta, W = calculate_cell_length(Beta, W, m, lambd, 1.602*10**(-19), E0T, phi)
    print(W)
    cell_lengths.append(l)
    
print("Total length of accelerator: ")
print(np.sum(cell_lengths))
plt.plot(betas, cell_lengths)
plt.show()