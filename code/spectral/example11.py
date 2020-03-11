import numpy as np
import scipy
import matplotlib.pyplot as plt

from scipy.fftpack import *
from scipy.fftpack import diff
from scipy.integrate import ode

def cosh(x): # hyperbolic cosine
	sisene = np.exp(x)/2+1/(2*np.exp(x))
	return sisene

def InitialCondition(Ao,Bo,x,loik,c): # Sech**2 initial condition
	xx = x-loik*np.pi #profile shift
	u0 = Ao/(cosh(Bo*xx))**2 #initial pulse
	u0x = diff(u0,period=2*np.pi*loik); #speed -c*u0x
	yx[:n] = u0 # space
	yx[n:] = -c*u0x; # speed
	return yx.real

def EQ(t,yx): # equation to be solved
	nn = len(yx)/2
	ru = yx[:nn] # space displacement
	v = yx[nn:] # speed, or dr/dt, y[n] to y[2n-1]
	x_xx = diff(ru,2,period=2*np.pi*loik)  # second spatial derivative
	ytx[:nn] = v #du/dt=v
	ytx[nn:] = x_xx # wave equation utt = c* uxx, c=1 in normalized equation
	return ytx

n = 2**12   # number of grid-points
loik = 64   # number 2 pi sections in space
dt = 1      # time step
narv = 6001 # number of time-steps
x = np.arange(n,dtype=np.float64)*loik*2*np.pi/n        # coordinate x
yx = np.arange(n*2,dtype=np.float64)
ytx = np.arange(n*2,dtype=np.float64)
c = 1       # speed squared of wave equation
Bo = 1/8; Ao = 1; # initial pulse param
yx = InitialCondition(Ao,Bo,x,loik,c);
t0 = 0.0; t_end = narv*dt # final time to integrate to

tvektorx = []; tulemusx = []; # arrays for results
runnerx = ode(EQ)         # using ode from scipy
runnerx.set_integrator('vode',nsteps=1e7,rtol=1e-5,atol=1e-5);
runnerx.set_initial_value(yx,t0);

while runnerx.successful() and runnerx.t < t_end: # integration
	tvektorx.append(runnerx.t);
	tulemusx.append(runnerx.y);
	print('z ',runnerx.t);
	runnerx.integrate(runnerx.t+dt);

f = plt.figure()
for i in range(len(tulemusx)):
 plt.plot(tulemusx[i])

plt.show()
plt.close('all')
