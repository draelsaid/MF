#coding=iso-8859-15
#/usr/bin/env python

import numpy as np
import scipy
import matplotlib.pyplot as plt
import time

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

def oomega(n): # omega calculation (n - gridpoints, loik = number of 2pi sections in space)
	qq = 0.0
	kk = 0
	while kk<(n/2):
		omega[kk] = qq/loik
		omega[n/2+kk] = (-(n/2)+qq)/loik
		qq+=1.0
		kk+=1
	return omega

def ibioD(tulemusx,tvektorx,n): # inverse tranresetsfrom of results with H2 uttxx dimensionless EQ
	i = 0 ; um_t_reaalne = [] ; aprox_kiirus = []
	temp2 = [] ; ru = [] ; fft_r = [] # siirde jaoks
	temp3 = [] ; rut = [] ; fft_rt = [] # kiiruse jaoks
	omega = oomega(n)

	while i<len(tvektorx): # transfrom into real space
		temp2 = tulemusx[i][:n] # first part (space)
		temp3 = tulemusx[i][n:] # speed
		fft_r = fft(temp2,n,-1) # r forward
		fft_rt = fft(temp3,n,-1)
		r_ajutine = np.arange(n,dtype=np.complex128)
		rt_ajutine = np.arange(n,dtype=np.complex128)
		k = 0

		while k < n: # index 0 kuni n-1. calculation to inverse transform
			r_ajutine[k] = fft_r[k]/(1+HH2*omega[k]**2)
			rt_ajutine[k] = fft_rt[k]/(1+HH2*omega[k]**2)
			k = k+1
		ru = ifft(r_ajutine).real # end of inverse transform
		rut = ifft(rt_ajutine).real
		um_t_reaalne.append(ru) # space [row = coordinate, column = time]
		aprox_kiirus.append(rut)
		i=i+1
	return um_t_reaalne,aprox_kiirus

def Biosech2D(Ao,Bo,x,loik,c,HH2): # Sech**2 initial condition
	xx = x-loik*np.pi #profile shift
	u0 = Ao/(np.cosh(Bo*xx))**2
	u0x = diff(u0,period=2*np.pi*loik); #speed -c*u0x
	u0xx = diff(u0x,period=2*np.pi*loik);# second space derivative
	yx[:n] = u0-HH2*u0xx # space transformed
	yx[n:] = -c*u0x; #speed;
	return yx.real

def Bio2D(t,yx): #Improved HJ equation, dimensionless form
	nn = len(yx)/2

	omega = oomega(nn)
	temp2 = [] ; ru = [] ; fft_r = []
	temp2 = yx[:nn] #first part
	fft_r = fft(temp2,nn,-1) #r forward transform
	r_ajutine = np.arange(nn,dtype=np.complex128) # complex array ’D’
	kkk = 0
	while kkk < nn: #index 0 to n-1.
		r_ajutine[kkk] = fft_r[kkk]/(1+HH2*omega[kkk]**2)
		kkk = kkk+1
	ru = ifft(r_ajutine).real #inverse transform end
	rr = ru*ru  #nonlinear
	v = yx[nn:] #speed or dr/dt, y[n] to y[2n-1]
	x_x = diff(ru,1,period=2*np.pi*loik)   # first derivative
	x2 = x_x*x_x                              # square of first derivative
	x_xx = diff(ru,2,period=2*np.pi*loik)  # second derivative
	x_xxxx = diff(ru,4,period=2*np.pi*loik)# fourth derivative
	ytx[:nn] = v #du/dt=v
	ytx[nn:] = x_xx + PP * ru * x_xx + QQ * rr * x_xx + PP * x2 + 2 * QQ * ru * x2 - HH * x_xxxx
	return ytx

# Previous program paramters
n = 2**12   #number of grid-points
loik = 64   # number 2 pi sections in space
dt = 0.1    # time step
narv = 6001 # number of time-steps
x = np.arange(n,dtype=np.float64)*loik*2*np.pi/n #coordinate x
yx = np.arange(n*2,dtype=np.float64)
ytx = np.arange(n*2,dtype=np.float64)
c = 1             # speed squared of wave equation
Bo = 1/8; Ao = 1; # initial pulse param

# example set of normalized parameters
co = 1; co2 = co * co; rho0 = 1; l = 1; # geometric / material param
c = 1 + 0.1; gamma2 = (c*c)/co2
p = 0.05; q = 0.075; # nonlinear param
h2 = 0.05; h1 = gamma2*h2; # dispersion param
Bo = 1/8; Ao = 1; # initial pulse param

# dimensionless P = p * roo_0 / co2; Q = q * roo_0**2 / co2; H = h / (co2 * l)
PP = p * rho0 / co2; QQ = q * rho0**2 / co2; HH = h1 /(co2 * l**2); HH2 = h2 /(l**2);

yx = Biosech2D(Ao,Bo,x,loik,c,HH2); tyyp='sech2';
# ---------- integration of EQ -------------------------------------
t0 = 0.0; aeg_alg = time.clock() #initial time, floating point number
t_end = narv*dt #end time
tvektor1 = []; tvektor2 = [] ; tvektor3 = [] ; tulemus1 = []; tulemus2 = [];  tulemus3 = [];
tvektor4 = [] ; tulemus4 = []; tvektor5 = [] ; tulemus5 = []; tvektorx = []; tulemusx = [];
runnerx = ode(Bio2D) #for dimensionless form!
runnerx.set_integrator('vode',nsteps=1e7,rtol=1e-10,atol=1e-12);
runnerx.set_initial_value(yx,t0);

while runnerx.successful() and runnerx.t < t_end: #-h uxxxx - H2 uxxtt
	tvektorx.append(runnerx.t);
	tulemusx.append(runnerx.y);
	print('z ',runnerx.t);
	runnerx.integrate(runnerx.t+dt);

(um_t_reaalne,aproxkiirus) = ibioD(tulemusx,tvektorx,n) # inverse transform, dimensionless form
umx = transpose(um_t_reaalne); #umtx = transpose(aproxkiirus) H2 member
# and here you can save the results into Matlab

