import uproot
import matplotlib.pyplot as plt
import numpy as np
import math
import hist
import mplhep as hep
import os

kkmc_acceptances = []
wzp_acceptances = []
angles = []
#final_events = []
#initial_events = []

for i in range(0,46,5):
    
    # Run the analysis with an specific hole size
    
    index = i/100
    print(f"Looking at limiting angle {index} radians")
    os.system(f'python analysis/histmakers/pt2_hadron_xsec.py --limitingTheta {index}')
    f = uproot.open("/home/submit/marinamn/fccee/FCCAnalyzer/tmp/output_hadron_xsec.root")
    
    # Function to combine jet flavours to a single sample
    
    def qq(key):
        qq = f[f"kkmc_ee_uu_ecm91p2/{key}"].to_hist()+ f[f"kkmc_ee_dd_ecm91p2/{key}"].to_hist()+f[f"kkmc_ee_cc_ecm91p2/{key}"].to_hist() +f[f"kkmc_ee_ss_ecm91p2/{key}"].to_hist() + f[f"kkmc_ee_bb_ecm91p2/{key}"].to_hist()
        return qq
    
    # Calculate the Acepptance of the analysis with specific hole size
    
    kkmc_cutsy,kkmc_cutsx = qq("cutFlow").to_numpy()
    wzp_cutsy, wzp_cutsx = f['wzp6_ee_qq_ecm91p2/cutFlow'].to_numpy()
    kkmc_A = kkmc_cutsy[2]/kkmc_cutsy[0]
    kkmc_acceptances.append(kkmc_A)
    wzp_A = wzp_cutsy[2]/wzp_cutsy[0]
    wzp_acceptances.append(wzp_A)
    # final_events.append(cutsy[2])
    # initial_events.append(cutsy[0])
    angles.append(index)
    
#     # Plot information about Visible Particles
    
#     thetavis = qq("RP_theta")
#     hep.histplot(thetavis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
#     plt.xlim(0,3.15)
#     plt.xlabel(r"$\theta$ [radians] per particle")
#     plt.legend(loc = "lower center")
#     plt.ylabel("Events")
#     plt.title(f"Visible Particles, hole of {index} radians")
#     plt.savefig(f"thetavis_{index}.png")
#     plt.close()
    
#     numbervis = qq("RP_no")
#     hep.histplot(numbervis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
#     plt.xlim(0,80)
#     plt.xlabel(r"Number of Reconstructed Particles")
#     plt.legend(loc = "lower center")
#     plt.ylabel("Events")
#     plt.title(f"Visible Particles, hole of {index} radians")
#     plt.savefig(f"numbervis_{index}.png")
#     plt.close()
    
#     # Plot information about Non Visible Particles
    
#     thetanonvis = qq("RP_theta_NonVisible")
#     hep.histplot(thetanonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
#     plt.xlim(0,3.15)
#     plt.xlabel(r"$\theta$ [radians] per particle")
#     plt.legend(loc = "lower center")
#     plt.ylabel("Events")
#     plt.title(f"Non Visible Particles, hole of {index} radians")
#     plt.savefig(f"thetanonvis_{index}.png")
#     plt.close()
    
#     numbernonvis = qq("RP_no_NonVisible")
#     hep.histplot(numbernonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
#     plt.xlim(0,30)
#     plt.xlabel("Number of Reconstructed Particles")
#     plt.legend(loc = "upper right")
#     plt.ylabel("Events")
#     plt.title(f"Non Visible Particles, hole of {index} radians")
#     plt.savefig(f"numbernonvis_{index}.png")
#     plt.close()
    
    
plt.scatter(angles,kkmc_acceptances)
plt.title(r"$\sqrt{s} = 91.2 $ GeV, 75 ab$^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold")
plt.xlabel("Radius of the hole [radians], KKMC")
plt.ylabel("Acceptance")
plt.ylim(0.85,1)
plt.grid(visible=True)
plt.savefig("a_vs_theta_plot.png")
plt.close()

plt.scatter(angles,wzp_acceptances)
plt.title(r"$\sqrt{s} = 91.2 $ GeV, 75 ab$^{-1}$", loc = "right")
plt.title("FCC-ee simulation", loc = "left", weight = "bold")
plt.xlabel("Radius of the hole [radians], Whizard")
plt.ylabel("Acceptance")
plt.ylim(0.85,1)
plt.grid(visible=True)
plt.savefig("wzp_a_vs_theta_plot.png")
plt.close()
    
    
# plt.scatter(angles,final_events)
# plt.xlabel("Radius of the hole [radians]")
# plt.ylabel("Events after cuts")
# plt.grid(visible=True)
# plt.savefig("finalEvents_vs_theta_plot.png")
# plt.close()

# plt.scatter(angles,initial_events)
# plt.xlabel("Radius of the hole [radians]")
# plt.ylabel("Events before cuts")
# plt.grid(visible=True)
# plt.savefig("initialEvents_vs_theta_plot.png")
# plt.close()