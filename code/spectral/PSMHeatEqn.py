# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:51:42 2015
PSM HEAT EQUATION
u_t=a*(u_xx+u_yy)
12.04.15 algus
@author: Mart
"""

import numpy as np
import scipy.io
import scipy.integrate

#siin paneme paika vajalikud parameetrid
punktide_arv=256
salv=.01    #kui tiheda sammuga salvestan
tf=0.1       #lppaeg
atol=1e-12
rtol=1e-10
nsteps=1e7
integrator='vode'

def psm_start(punktide_arv,salv,tf,atol,rtol):
	dx=(1*2*np.pi/punktide_arv)
	#sisuliselt omega, et tuletisi vtta
	abi=np.hstack((np.arange(punktide_arv/2),np.arange(-punktide_arv/2,0)))
	suurK=abi
	for i in range(punktide_arv-1):
		suurK=np.vstack((suurK,abi))

	#omega transponeeritud, et tuletisi vtta y’st
	suurL=suurK.swapaxes(0,1)

	#print ’max,min’,np.max(suurKP),np.min(suurKP)
	x=dx*np.arange(-punktide_arv/2,punktide_arv/2)
	y=x

	xx,yy=np.meshgrid(x,y)
	u0=np.exp(-(xx**2+yy**2)*25.0)

	print('integreerin ',integrator,"'ga", u0.shape)
	solver=scipy.integrate.ode(funktsioon).set_integrator(integrator,nsteps=nsteps,atol=atol, rtol=rtol)

	u0 = u0.flatten ()
	solver.set_initial_value(u0, 0).set_f_params(suurK,suurL)
	lahend=[u0.copy()]
	tv=[0,]
	counter=0
	while solver.t< tf:#solver.successful() and solver.t < tf:
		counter+=1
		solver.integrate(solver.t + salv)
		print(np.min(solver.y), np.max(solver.y))

		ucurrent=solver.y
		print(np.shape(ucurrent), np.max(np.abs(ucurrent-u0)))

		lahend.append(ucurrent)

		tv.append(solver.t)
		print('arvutan, aeg: ',solver.t,solver.successful())
		if counter-1>tf/float(salv):
			break
	scipy.io.savemat('heat_eq_test_12_04', {'u0':u0,'suurK':suurK,'lahend':lahend,'tv':tv,'x':x\
,'y':y,'punktide_arv':punktide_arv})

def funktsioon(t,xxyy,suurK,suurL):
	a=1
	xxyy = np.reshape( xxyy, (punktide_arv,)*2)
	#print ’SIIN!!!’
	#print ’================================================================’
	uxx=np.real(np.fft.ifft(-suurK**2*np.fft.fft(xxyy,axis=1),axis=1))
	uyy=np.real(np.fft.ifft(-suurL**2*np.fft.fft(xxyy,axis=0),axis=0))

	tul=a*(uxx+uyy)
	#print ’sain tulemuse:’, tul.shape
	#print max(tul),min(tul)
	return tul.flatten ()

psm_start(punktide_arv,salv,tf,atol,rtol)

