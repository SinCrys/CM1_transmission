#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
import numpy as np
from xraydb import mu_elam, mu_chantler

# What bugs me:
# the angle a is constant and is not passed
# to the functions f_l and f_i as the unit
# transform for the secondary x-axis does
# not allow the passing of arguments. To
# circumvent only lambda and partials would
# work but are just as problematic as
# defining it constant. Just good enough
# for this script!

# CM1 thickness [µm] reference
# points to mark in the plot
p = [90,
     100,
     110,
    ]
# X-ray beam energy in ev
e = 15000
# Bragg angle (a) in degrees
#  a = 7.52 @ 23 keV
#  a = 8.53 @ 20 keV
a = 7.52
# mu, linear absorption coefficient
# float. 'elam' or 'chantler'
# https://11bm.xray.aps.anl.gov/absorb/absorb.php
#  -> µ = 1.85 cm-1
mu = 'chantler'
# 'elam' and 'chantler' give the 
# X-ray mass attenuation coefficient 
# mu/rho in units of cm^2/g
# -> * rho [g/cm^3] = mu
rho = 3.52
# Thickness range in µm
t_min = 85
t_max = 115

def f_m(mu, t):
    # Calculate transmission in %
    # mu: linear absorption coefficient [cm-1]
    # t : thickness [µm]
    return (np.exp(-(mu/1e-2)*(t/1e6)))*100

def f_l(t):
    # Effective path length
    # through CM1 at given
    # Bragg angle (a) in degrees
    #  a = 7.52 @ 23 keV
    #  a = 8.53 @ 20 keV
    # t: the thickness or diameter
    # a: cannot be passed to the function
    # as we use the function to transform
    # the units for the secondary x-axis
    return t/np.cos(np.deg2rad(90-a))

def f_i(l):
    # inverse of f_l
    return l * np.cos(np.deg2rad(90-a))

if mu == 'chantler':
    mu_rho = mu_chantler('C', e)
    mu = mu_rho * rho
elif mu == 'elam':
    mu_rho = mu_elam('C', e)
    mu = mu_rho * rho

t = np.arange(t_min, t_max, 1)
s = ['dashed', 'dashdot', 'dotted']
plt.title(f'CM1 thickness vs transmission for DanMAX @{e/1000} keV')
for i,p in enumerate(p):
    plt.axhline(f_m(mu, f_l(p)), ls=s[i%len(s)], c='red', lw=0.5, label=f'{f_m(mu, f_l(p)):.2f}% @ {p} µm ({f_l(p):.0f} µm)')
    plt.axvline(f_l(p), ls=s[i%len(s)], c='red', lw=0.5)
plt.plot(f_l(t), f_m(mu,f_l(t)), ls='-', label=f'CM1, $\\alpha$={a:.2f}˚, $µ$={mu:.2f} cm$^{{-1}}$', lw=2, c='black')
secax = plt.gca().secondary_xaxis('top', functions=(f_i, f_l))
secax.set_xlabel('CM1 thickness [µm]')
plt.xlabel(r'Effective thickness @ $\alpha$ [µm]')
plt.ylabel('Transmission [%]')
plt.legend(title=f'HPF(600 µm): {f_m(mu, 600):.2f}%')
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__),'CM1_transmission.png'), dpi=300)
plt.show()