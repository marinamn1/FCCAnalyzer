import uproot
import matplotlib.pyplot as plt
import numpy as np
import math
import hist
import mplhep as hep
import os

acceptances = [[],[]]
angles = [[],[]]
errors = [[],[]]
ratios = []
sig = []
#final_events = []
#initial_events = []

sample_list = ["kkmc_ee_uu_ecm91p2", "wz3p8_ee_uu_ecm91p2"]
label_list = [r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8", r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8"]
color_list = ["lightskyblue", "violet"]

for i in range(0,26,5):
    
    # Run the analysis with an specific hole size
    
    index = i/100
    print(f"Looking at limiting angle {index} radians")
    os.system(f'python /home/submit/marinamn/fccee/FCCAnalyzer/analysis/histmakers/pt2_hadron_xsec.py --limitingTheta {index}')
    f = uproot.open("/home/submit/marinamn/fccee/FCCAnalyzer/tmp/output_hadron_xsec.root")
    
    for j in range(0,2):
    
        # Calculate the Acepptance of the analysis with specific hole size
    
        cutsy,cutsx = f[f"{sample_list[j]}/cutFlow"].to_numpy()
        A = cutsy[2]/cutsy[0]
        acceptances[j].append(A)
        # final_events.append(cutsy[2])
        # initial_events.append(cutsy[0])
        angles[j].append(index)
        errors[j].append(np.sqrt(cutsy[2]*(1-A))/cutsy[0])
    ratio = 10000*(acceptances[1][-1]-acceptances[0][-1])/acceptances[1][-1]
    sig.append((acceptances[1][-1]-acceptances[0][-1])/np.sqrt(errors[0][-1]**2+errors[1][-1]**2))
    ratios.append(ratio)

np.savez("analysis/histmakers/new_result_acceptances", acceptances = acceptances, errors = errors, angles = angles[0], ratios = ratios, sig = sig)

for i in range(0, len(angles[0])):
    print(f"At hole size {angles[0][i]} radians")
    print(f"KKMC Acceptance = {100*acceptances[0][i]} % +- {errors[0][i]}")
    print(f"Whizard Acceptance = {100*acceptances[1][i]} % +- {errors[1][i]}")
    print(f"Significance = {sig[i]}")