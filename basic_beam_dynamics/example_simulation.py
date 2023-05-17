import numpy as np
import matplotlib.pyplot as plt

import xobjects as xo
import xtrack as xt
import xpart as xp

from linac import Linac

# Define the elements of the accelerator
elements = [
    xt.Drift(length=1.),
    xt.Cavity(voltage=100, frequency=10*3, lag=0),
    xt.Drift(length=2.),
    xt.Multipole(order=2, knl=[0, 1.], ksl=[0,0]),
    xt.Drift(length=1.),
    xt.Multipole(order=2, knl=[0, -1.], ksl=[0,0])
    ]

element_names=['drift_0', 'cavity_0', 'drift_1', 'quad_0', 'drift_2', 'quad_1']

# Create a set of particles
n_part = 200
ref_E = 150 # Reference energy in MeV
particles = xp.Particles(p0c=ref_E*10**6,
            q0=1, mass0=xp.PROTON_MASS_EV,
            x=np.random.uniform(-1e-3, 1e-3, n_part),
            px=np.random.uniform(-1e-5, 1e-5, n_part),
            y=np.random.uniform(-2e-3, 2e-3, n_part),
            py=np.random.uniform(-3e-5, 3e-5, n_part),
            zeta=np.random.uniform(-1e-2, 1e-2, n_part),
            delta=np.random.uniform(-1e-4, 1e-4, n_part))
        
# Create linac and simulate
l = Linac(elements=elements, element_names=element_names, ref_particle_type='p', ref_energy=ref_E)
tw = l.twiss()
x,px = l.simulate(particles=particles, context='CPU', turns=1)

# Plot twiss parameters
fig1 = plt.figure(1, figsize=(6.4, 4.8*1.5))
spbet = plt.subplot(3,1,1)
spco = plt.subplot(3,1,2, sharex=spbet)
spdisp = plt.subplot(3,1,3, sharex=spbet)

spbet.plot(tw['s'], tw['betx'])
spbet.plot(tw['s'], tw['bety'])

spco.plot(tw['s'], tw['x'])
spco.plot(tw['s'], tw['y'])

spdisp.plot(tw['s'], tw['dx'])
spdisp.plot(tw['s'], tw['dy'])

spbet.set_ylabel(r'$\beta_{x,y}$ [m]')
spco.set_ylabel(r'(Closed orbit)$_{x,y}$ [m]')
spdisp.set_ylabel(r'$D_{x,y}$ [m]')
spdisp.set_xlabel('s [m]')

fig1.suptitle(
    r'$q_x$ = ' f'{tw["qx"]:.5f}' r' $q_y$ = ' f'{tw["qy"]:.5f}' '\n'
    r"$Q'_x$ = " f'{tw["dqx"]:.2f}' r" $Q'_y$ = " f'{tw["dqy"]:.2f}'
    r' $\gamma_{tr}$ = '  f'{1/np.sqrt(tw["momentum_compaction_factor"]):.2f}'
)

fig1.subplots_adjust(left=.15, right=.92, hspace=.27)
plt.show()
