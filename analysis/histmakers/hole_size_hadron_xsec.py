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

# VISIBLE PARTICLES

# KKMC

numbervis = qq("RP_no_vis")
hep.histplot(numbervis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,120)
plt.xlabel(r"Number of Reconstructed Particles")
plt.legend(loc = "lower center")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/numbervis_{index}.png")
plt.close()

evis = qq("RP_e_vis")
hep.histplot(evis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,100)
plt.xlabel(r"Energy per Particle[GeV]")
plt.legend(loc = "lower center")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/e_particle_vis_{index}.png")
plt.close()

# evis = qq("sum_energy_vis")
# hep.histplot(evis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
# plt.xlim(0,100)
# plt.xlabel(r"Scalar Energy[GeV]")
# plt.legend(loc = "lower center")
# plt.ylabel("Events")
# plt.title(f"Visible Particles, hole of {index} radians")
# plt.savefig(f"/my_codes/pt2_hadrons_xsec/hole_size/sum_energy_vis_{index}.png")
# plt.close()

# WHIZARD

numbervis = f['wzp6_ee_qq_ecm91p2/RP_no_vis'].to_hist()
hep.histplot(numbervis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,120)
plt.xlabel(r"Number of Reconstructed Particles")
plt.legend(loc = "lower center")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/wzp_numbervis_{index}.png")
plt.close()

evis = f['wzp6_ee_qq_ecm91p2/RP_e_vis'].to_hist()
hep.histplot(evis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,100)
plt.xlabel(r"Energy per Particle[GeV]")
plt.legend(loc = "lower center")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/wzp_e_particle_vis_{index}.png")
plt.close()

# evis = f['wzp6_ee_qq_ecm91p2/sum_energy_vis'].to_hist()
# hep.histplot(evis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
# plt.xlim(0,100)
# plt.xlabel(r"Scalar Energy[GeV]")
# plt.legend(loc = "lower center")
# plt.ylabel("Events")
# plt.title(f"Visible Particles, hole of {index} radians")
# plt.savefig(f"/my_codes/pt2_hadrons_xsec/hole_size/wzp_sum_energy_vis_{index}.png")
# plt.close()

# NON VISIBLE PARTICLES

# KKMC

numbernonvis = qq("RP_no_NonVisible")
hep.histplot(numbernonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,30)
plt.xlabel("Number of Reconstructed Particles")
plt.legend(loc = "upper right")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Non Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/numbernonvis_{index}.png")
plt.close()

enonvis = qq("RP_e_NonVisible")
hep.histplot(enonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,100)
plt.xlabel(r"Energy per Particle [GeV]")
plt.legend(loc = "lower center")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Non Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/e_particle_nonvis_{index}.png")
plt.close()

# enonvis = qq("sum_energy_NonVisible")
# hep.histplot(enonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
# plt.xlim(0,100)
# plt.xlabel(r"Scalar Energy [GeV]")
# plt.legend(loc = "lower center")
# plt.ylabel("Events")
# plt.title(f"Non Visible Particles, hole of {index} radians")
# plt.savefig(f"/my_codes/pt2_hadrons_xsec/hole_size/sum_energy_nonvis_{index}.png")
# plt.close()

# WHIZARD

numbernonvis = f['wzp6_ee_qq_ecm91p2/RP_no_NonVisible'].to_hist()
hep.histplot(numbernonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,30)
plt.xlabel("Number of Reconstructed Particles")
plt.legend(loc = "upper right")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Non Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/wzp_numbernonvis_{index}.png")
plt.close()

enonvis = f['wzp6_ee_qq_ecm91p2/RP_e_NonVisible'].to_hist()
hep.histplot(enonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
plt.xlim(0,100)
plt.xlabel(r"Energy per Particle [GeV]")
plt.legend(loc = "lower center")
plt.ylabel("Events")
plt.yscale("log")
plt.title(f"Non Visible Particles, hole of {index} radians")
plt.savefig(f"my_codes/pt2_hadrons_xsec/hole_size/wzp_e_particle_nonvis_{index}.png")
plt.close()

# enonvis = f['wzp6_ee_qq_ecm91p2/sum_energy_NonVisible'].to_hist()
# hep.histplot(enonvis, label = r"$e^{+} e^{-} \rightarrow q \bar{q}$", color = "paleturquoise", histtype = "fill")
# plt.xlim(0,100)
# plt.xlabel(r"Scalar Energy [GeV]")
# plt.legend(loc = "lower center")
# plt.ylabel("Events")
# plt.title(f"Non Visible Particles, hole of {index} radians")
# plt.savefig(f"/my_codes/pt2_hadrons_xsec/hole_size/wzp_sum_energy_nonvis_{index}.png")
# plt.close()