import uproot
import matplotlib.pyplot as plt
import numpy as np
import math
import hist
import mplhep as hep
import os

# CHOOSE SIZE OF THE HOLE [radians]
index = 0.2
os.system(f'python analysis/histmakers/pt2_hadron_xsec.py --limitingTheta {index}')
f = uproot.open("/home/submit/marinamn/fccee/FCCAnalyzer/tmp/output_hadron_xsec.root")
def qq(key):
    qq = f[f"kkmc_ee_uu_ecm91p2/{key}"].to_hist()+ f[f"kkmc_ee_dd_ecm91p2/{key}"].to_hist()+f[f"kkmc_ee_cc_ecm91p2/{key}"].to_hist() +f[f"kkmc_ee_ss_ecm91p2/{key}"].to_hist() + f[f"kkmc_ee_bb_ecm91p2/{key}"].to_hist()
    return qq

sample_list = ["kkmc_ee_uu_ecm91p2_noBES_noISR","wz3p8_ee_uu_ecm91p2_noBES_noISR", "kkmc_ee_uu_ecm91p2", "wz3p8_ee_uu_ecm91p2", "wzp6_ee_uu_ecm91p2"]
label_list = [r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8, no BES/ISR/FSR", r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8, no BES/ISR/FSR", r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8", r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8", r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 6"]
color_list = ["red", "blue", "lightskyblue", "violet", "darkgreen"]

thetavis = []
thetanonvis = []
numbervis = []
numbernonvis = []
rpevis = []
rpenonvis = []
evis = []
enonvis = []

for i in range(0,5):
    thetavis.append(f[f"{sample_list[i]}/RP_theta_vis"].to_hist())
    thetanonvis.append(f[f"{sample_list[i]}/RP_theta_NonVisible"].to_hist())
    numbervis.append(f[f"{sample_list[i]}/RP_no_vis"].to_hist())
    numbernonvis.append(f[f"{sample_list[i]}/RP_no_NonVisible"].to_hist())
    rpevis.append(f[f"{sample_list[i]}/norm_RP_e_vis"].to_hist())
    rpenonvis.append(f[f"{sample_list[i]}/norm_RP_e_NonVisible"].to_hist())
    evis.append(f[f"{sample_list[i]}/norm_energy_vis"].to_hist())
    enonvis.append(f[f"{sample_list[i]}/norm_energy_NonVisible"].to_hist())

hep.histplot(thetavis, label = label_list , color = color_list)
plt.xlim(0,3.15)
plt.xlabel(r"$ \theta_{particle}$, Visible Particles")
plt.legend()
plt.ylabel("Particles")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/thetavis_{index}.png")
plt.close()

hep.histplot(thetanonvis, label = label_list , color = color_list)
plt.xlim(0,3.15)
plt.xlabel(r"$ \theta_{particle}$, Non Visible Particles")
plt.legend()
plt.ylabel("Particles")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/thetanonvis_{index}.png")
plt.close()

hep.histplot(numbervis, label = label_list , color = color_list)
plt.xlim(0,120)
plt.xlabel("Number of Visible Reconstructed Particles")
plt.legend()
plt.ylabel("Events")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/numbervis_{index}.png")
plt.close()

hep.histplot(numbernonvis, label = label_list , color = color_list)
plt.xlim(0,20)
plt.xlabel("Number of Non Visible Reconstructed Particles")
plt.legend()
plt.ylabel("Events")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/numbernonvis_{index}.png")
plt.close()

hep.histplot(rpevis,label = label_list , color = color_list)
plt.xlim(0,0.5)
plt.xlabel(r"$E_{particle}$ / $ \sqrt{s}$, Visible Particles")
plt.legend()
plt.ylabel("Particles")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/rpevis_{index}.png")
plt.close()

hep.histplot(rpenonvis,label = label_list , color = color_list)
plt.xlim(0,0.5)
plt.xlabel(r"$E_{particle}$ / $ \sqrt{s}$, Non Visible Particles")
plt.legend()
plt.ylabel("Particles")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/rpenonvis_{index}.png")
plt.close()

hep.histplot(evis,label = label_list , color = color_list)
plt.xlim(0.4,1.1)
plt.xlabel(r"$E_{vis}$ / $ \sqrt{s}$, Visible Particles")
plt.legend()
plt.ylabel("Events")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/evis_{index}.png")
plt.close()

hep.histplot(enonvis,label = label_list , color = color_list)
plt.xlim(0,0.55)
plt.xlabel(r"$E_{vis}$ / $ \sqrt{s}$, Non Visible Particles")
plt.legend()
plt.ylabel("Events")
plt.yscale("log")
plt.title(r"$\sqrt{s} = 91.2 GeV, 150 ab^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold", style = "italic")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/enonvis_{index}.png")
plt.close()
