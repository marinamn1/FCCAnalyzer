import uproot
import matplotlib.pyplot as plt
import numpy as np
import hist
from hist import Hist
import mplhep as hep
import math

f = uproot.open("/home/submit/marinamn/fccee/FCCAnalyzer/tmp/output_hadron_xsec.root")
g = uproot.open("/home/submit/marinamn/fccee/FCCAnalyzer/tmp/output_hadron_xsec_gen.root")

def qq(key):
    qq = f[f"kkmc_ee_uu_ecm91p2/{key}"].to_hist()+ f[f"kkmc_ee_dd_ecm91p2/{key}"].to_hist()+f[f"kkmc_ee_cc_ecm91p2/{key}"].to_hist() +f[f"kkmc_ee_ss_ecm91p2/{key}"].to_hist() + f[f"kkmc_ee_bb_ecm91p2/{key}"].to_hist()
    return qq

def plot(number,samples,key,name,xlabel_name,vline_x = 0,ylabel_name = "Events",legend_loc = "best",legend_size = "8",stack_yn = True,fill_yn = "fill", lim = None, yscale_yn = True, vline = False, vline_color = "blue", vline_style = "-", vline_label = "Cut", save = False):
    
    histograms = []
    labels = []
    colors = []
    
    sample_dict = {"wzp_qq": "wzp6_ee_qq_ecm91p2", "mu": "wzp6_ee_mumu_ecm91p2", "tau": "wzp6_ee_tautau_ecm91p2", "e": "p8_ee_Zee_ecm91", "gaga":"wzp6_gaga_qq_5_ecm91p2","p8_mu": "p8_ee_Zmumu_ecm91", "p8_tau": "p8_ee_Ztautau_ecm91", "uu": "kkmc_ee_uu_ecm91p2", "dd": "kkmc_ee_dd_ecm91p2", "cc": "kkmc_ee_cc_ecm91p2", "ss": "kkmc_ee_ss_ecm91p2", "bb": "kkmc_ee_bb_ecm91p2", "u_p8": "p8_ee_Zuu_ecm91p2_noBES_noISR", "u_kkmc_no": "kkmc_ee_uu_ecm91p2_noBES_noISR", "u_wz3p8_no":"wz3p8_ee_uu_ecm91p2_noBES_noISR", "u_kkmc": "kkmc_ee_uu_ecm91p2", "u_wz3p8": "wz3p8_ee_uu_ecm91p2", "u_wzp6": "wzp6_ee_uu_ecm91p2"}
    label_dict = {"qq": r"$e^{+} e^{-} \rightarrow q \bar{q}$, KKMC", "wzp_qq": r"$e^{+} e^{-} \rightarrow q \bar{q}$, Whizard", "mu": r"$e^{+} e^{-} \rightarrow \mu^{+} \mu^{-}$, Whizard", "tau": r"$e^{+} e^{-} \rightarrow \tau^{+} \tau^{-}$, Whizard", "e": r"$e^{+} e^{-} \rightarrow e^{+} e^{-}$, Pythia", "gaga":r"$e^{+} e^{-} \rightarrow e^{+} e^{-}$ hadrons, Whizard","p8_mu": r"$e^{+} e^{-} \rightarrow \mu^{+} \mu^{-}$, Pythia", "p8_tau": r"$e^{+} e^{-} \rightarrow \tau^{+} \tau^{-}$, Pythia", "uu": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC", "dd": r"$e^{+} e^{-} \rightarrow d \bar{d}$, KKMC", "cc": r"$e^{+} e^{-} \rightarrow c \bar{c}$, KKMC", "ss": r"$e^{+} e^{-} \rightarrow s \bar{s}$, KKMC", "bb": r"$e^{+} e^{-} \rightarrow b \bar{b}$, KKMC", "u_p8": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Pythia 8", "u_kkmc_no": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8, no BES/ISR/FSR", "u_wz3p8_no": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8, no BES/ISR/FSR", "u_kkmc": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8", "u_wz3p8": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8", "u_wzp6": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 6"}
    color_dict = {"qq": "paleturquoise", "wzp_qq": "darkviolet", "mu": "red", "tau": "limegreen", "e": "yellow", "gaga":"pink","p8_mu": "sandybrown", "p8_tau": "darkolivegreen", "uu": "moccasin", "dd": "chocolate", "cc": "magenta", "ss": "palegreen", "bb": "deepskyblue", "u_p8": "sandybrown", "u_kkmc_no": "red", "u_wz3p8_no": "blue", "u_kkmc" : "lightskyblue", "u_wz3p8": "violet", "u_wzp6": "darkgreen"}
                   
    for i in range (0,number):
        if samples[i] == "qq":
            histograms.append(qq(key))
        else:
            histograms.append(f[f"{sample_dict[samples[i]]}/{key}"].to_hist())
        labels.append(f"{label_dict[samples[i]]}")
        colors.append(f"{color_dict[samples[i]]}")
                   
    hep.histplot(histograms, label = labels, color = colors, stack = stack_yn, histtype = fill_yn)
                   
    if yscale_yn:
        plt.yscale("log")
    if lim != None:
        plt.xlim(lim[0],lim[1])
    if vline:
        plt.axvline(x = vline_x, color = vline_color, linestyle = vline_style, label = vline_label)
    plt.xlabel(xlabel_name)
    plt.ylabel(ylabel_name)
    plt.legend(loc = legend_loc, fontsize = legend_size)
    plt.title(r"$\sqrt{s} = 91.2 $ GeV, 75 ab$^{-1}$", loc = "right")
    plt.title("FCC-ee simulation", loc = "left", weight = "bold")
                   
    if save:
        plt.savefig(f"images/{name}.png")
        
def compare(number,tipo,samples,key,name,xlabel_name,ylabel_name = "Events",legend_loc = "best",legend_size = "8",stack_yn = True,fill_yn = "fill", lim = None, y_lim = None, ratio_lim = None, yscale_yn = True, save = False):
    
    histograms = []
    labels = []
    colors = []
    
    sample_dict = {"wzp_qq": "wzp6_ee_qq_ecm91p2", "mu": "wzp6_ee_mumu_ecm91p2", "tau": "wzp6_ee_tautau_ecm91p2", "e": "p8_ee_Zee_ecm91", "gaga":"wzp6_gaga_qq_5_ecm91p2","p8_mu": "p8_ee_Zmumu_ecm91", "p8_tau": "p8_ee_Ztautau_ecm91", "uu": "kkmc_ee_uu_ecm91p2", "dd": "kkmc_ee_dd_ecm91p2", "cc": "kkmc_ee_cc_ecm91p2", "ss": "kkmc_ee_ss_ecm91p2", "bb": "kkmc_ee_bb_ecm91p2", "u_p8": "p8_ee_Zuu_ecm91p2_noBES_noISR", "u_kkmc_no": "kkmc_ee_uu_ecm91p2_noBES_noISR", "u_wz3p8_no":"wz3p8_ee_uu_ecm91p2_noBES_noISR", "u_kkmc": "kkmc_ee_uu_ecm91p2", "u_wz3p8": "wz3p8_ee_uu_ecm91p2", "u_wzp6": "wzp6_ee_uu_ecm91p2"}
    label_dict = {"qq": r"$e^{+} e^{-} \rightarrow q \bar{q}$, KKMC", "wzp_qq": r"$e^{+} e^{-} \rightarrow q \bar{q}$, Whizard", "mu": r"$e^{+} e^{-} \rightarrow \mu^{+} \mu^{-}$, Whizard", "tau": r"$e^{+} e^{-} \rightarrow \tau^{+} \tau^{-}$, Whizard", "e": r"$e^{+} e^{-} \rightarrow e^{+} e^{-}$, Pythia", "gaga":r"$e^{+} e^{-} \rightarrow e^{+} e^{-}$ hadrons, Whizard","p8_mu": r"$e^{+} e^{-} \rightarrow \mu^{+} \mu^{-}$, Pythia", "p8_tau": r"$e^{+} e^{-} \rightarrow \tau^{+} \tau^{-}$, Pythia", "uu": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC", "dd": r"$e^{+} e^{-} \rightarrow d \bar{d}$, KKMC", "cc": r"$e^{+} e^{-} \rightarrow c \bar{c}$, KKMC", "ss": r"$e^{+} e^{-} \rightarrow s \bar{s}$, KKMC", "bb": r"$e^{+} e^{-} \rightarrow b \bar{b}$, KKMC", "u_p8": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Pythia 8", "u_kkmc_no": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8, no BES/ISR/FSR", "u_wz3p8_no": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8, no BES/ISR/FSR", "u_kkmc": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8", "u_wz3p8": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8", "u_wzp6": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 6"}
    color_dict = {"qq": "paleturquoise", "wzp_qq": "darkviolet", "mu": "red", "tau": "limegreen", "e": "yellow", "gaga":"pink","p8_mu": "sandybrown", "p8_tau": "darkolivegreen", "uu": "moccasin", "dd": "chocolate", "cc": "magenta", "ss": "palegreen", "bb": "deepskyblue", "u_p8": "sandybrown", "u_kkmc_no": "red", "u_wz3p8_no": "blue", "u_kkmc" : "lightskyblue", "u_wz3p8": "violet", "u_wzp6": "darkgreen"}
    sample_dict_g = {"u_kkmc": "kkmc_ee_uu_ecm91p2", "u_wz3p8": "wz3p8_ee_uu_ecm91p2", "u_wzp6": "wzp6_ee_uu_ecm91p2"}
    label_dict_g = {"u_kkmc": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8, Gen", "u_wz3p8": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8, Gen", "u_wzp6": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 6, Gen"}
    color_dict_g = {"u_kkmc" : "blue", "u_wz3p8": "red", "u_wzp6": "green"}
    
    y = [None]*number
    x = [None]*number
    
    fig = plt.figure()
    gs = fig.add_gridspec(2, hspace=0.1, height_ratios = (2,1))
    axs = gs.subplots(sharex=True)
    axs[0].set_title("FCC-ee simulation", loc= "left", weight = "bold")
    axs[0].set_title(r"$\sqrt{s} = 91.2 $ GeV, 75 ab$^{-1}$", loc = "right")
    
    for i in range (0,number):
        if tipo[i] == "reco":
            if samples[i] == "qq":
                histograms.append(qq(key))
            else:
                histograms.append(f[f"{sample_dict[samples[i]]}/{key}"].to_hist())
            labels.append(f"{label_dict[samples[i]]}")
            colors.append(f"{color_dict[samples[i]]}")
        else:
            histograms.append(g[f"{sample_dict_g[samples[i]]}/{key}"].to_hist())
            labels.append(f"{label_dict_g[samples[i]]}")
            colors.append(f"{color_dict_g[samples[i]]}")
        if y_lim != None:
            axs[0].set_ylim(y_lim)
    
        y[i],x[i] = histograms[i].to_numpy()
        axs[0].stairs(y[i],x[i], color = colors[i], label = labels[i])
        if i != 0:
            axs[1].stairs(y[i]/y[0], x[0], color = colors[i])

    
    axs[0].set_ylabel(ylabel_name)
    if yscale_yn:
        axs[0].set_yscale("log")
    axs[0].legend(loc = legend_loc, fontsize = legend_size)

    if ratio_lim == None:
        ymin = 0.5
        ymax = 1.5
    else:
        ymin = ratio_lim[0]
        ymax = ratio_lim[1]
    axs[1].set_ylim(ymin,ymax)
    axs[1].set_yticks(np.arange(ymin,ymax,0.25*(ymax-ymin)))
    axs[1].set_yticks(np.arange(ymin,ymax,0.05*(ymax-ymin)), minor = True)
    axs[1].set_ylabel("Ratio")
    axs[1].set_xlabel(xlabel_name)
    if lim != None:
        axs[1].set_xlim(lim[0],lim[1])
    axs[1].axhline(y = 1, color = 'gray', linestyle = 'solid', linewidth = "0.5")

    for ax in axs:
        ax.label_outer()
                   
    if save:
        plt.savefig(f"images/{name}.png")
        
def compare_prop(number,samples,key, key_name,name,xlabel_name,ylabel_name = "Events",legend_loc = "best",legend_size = "8",stack_yn = True,fill_yn = "fill", lim = None, ratio_lim = None, yscale_yn = True, save = False):
    
    histograms = []
    labels = []
    colors = []
    
    sample_dict = {"wzp_qq": "wzp6_ee_qq_ecm91p2", "mu": "wzp6_ee_mumu_ecm91p2", "tau": "wzp6_ee_tautau_ecm91p2", "e": "p8_ee_Zee_ecm91", "gaga":"wzp6_gaga_qq_5_ecm91p2","p8_mu": "p8_ee_Zmumu_ecm91", "p8_tau": "p8_ee_Ztautau_ecm91", "uu": "kkmc_ee_uu_ecm91p2", "dd": "kkmc_ee_dd_ecm91p2", "cc": "kkmc_ee_cc_ecm91p2", "ss": "kkmc_ee_ss_ecm91p2", "bb": "kkmc_ee_bb_ecm91p2", "u_p8": "p8_ee_Zuu_ecm91p2_noBES_noISR", "u_kkmc_no": "kkmc_ee_uu_ecm91p2_noBES_noISR", "u_wz3p8_no":"wz3p8_ee_uu_ecm91p2_noBES_noISR", "u_kkmc": "kkmc_ee_uu_ecm91p2", "u_wz3p8": "wz3p8_ee_uu_ecm91p2", "u_wzp6": "wzp6_ee_uu_ecm91p2"}
    label_dict = {"qq": r"$e^{+} e^{-} \rightarrow q \bar{q}$, KKMC", "wzp_qq": r"$e^{+} e^{-} \rightarrow q \bar{q}$, Whizard", "mu": r"$e^{+} e^{-} \rightarrow \mu^{+} \mu^{-}$, Whizard", "tau": r"$e^{+} e^{-} \rightarrow \tau^{+} \tau^{-}$, Whizard", "e": r"$e^{+} e^{-} \rightarrow e^{+} e^{-}$, Pythia", "gaga":r"$e^{+} e^{-} \rightarrow e^{+} e^{-}$ hadrons, Whizard","p8_mu": r"$e^{+} e^{-} \rightarrow \mu^{+} \mu^{-}$, Pythia", "p8_tau": r"$e^{+} e^{-} \rightarrow \tau^{+} \tau^{-}$, Pythia", "uu": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC", "dd": r"$e^{+} e^{-} \rightarrow d \bar{d}$, KKMC", "cc": r"$e^{+} e^{-} \rightarrow c \bar{c}$, KKMC", "ss": r"$e^{+} e^{-} \rightarrow s \bar{s}$, KKMC", "bb": r"$e^{+} e^{-} \rightarrow b \bar{b}$, KKMC", "u_p8": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Pythia 8", "u_kkmc_no": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8, no BES/ISR/FSR", "u_wz3p8_no": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8, no BES/ISR/FSR", "u_kkmc": r"$e^{+} e^{-} \rightarrow u \bar{u}$, KKMC Pythia 8", "u_wz3p8": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 8", "u_wzp6": r"$e^{+} e^{-} \rightarrow u \bar{u}$, Whizard Pythia 6"}
    color_dict = {"qq": "paleturquoise", "wzp_qq": "darkviolet", "mu": "red", "tau": "limegreen", "e": "yellow", "gaga":"pink","p8_mu": "sandybrown", "p8_tau": "darkolivegreen", "uu": "moccasin", "dd": "chocolate", "cc": "magenta", "ss": "palegreen", "bb": "deepskyblue", "u_p8": "sandybrown", "u_kkmc_no": "red", "u_wz3p8_no": "blue", "u_kkmc" : "lightskyblue", "u_wz3p8": "violet", "u_wzp6": "darkgreen"}
    color_list = ["paleturquoise", "darkviolet", "red", "limegreen", "yellow", "pink", "sandybrown", "darkolivegreen", "moccasin", "chocolate", "magenta", "palegreen", "deepskyblue", "sandybrown", "red", "blue", "lightskyblue", "violet", "darkgreen"]
    
    y = [None]*number
    x = [None]*number
    
    fig = plt.figure()
    gs = fig.add_gridspec(2, hspace=0.1, height_ratios = (2,1))
    axs = gs.subplots(sharex=True)
    axs[0].set_title("FCC-ee simulation", loc= "left", weight = "bold")
    axs[0].set_title(r"$\sqrt{s} = 91.2 $ GeV, 75 ab$^{-1}$", loc = "right")
    
    for i in range (0,number):
        if samples[i] == "qq":
            histograms.append(qq(key[i]))
        else:
            histograms.append(f[f"{sample_dict[samples[i]]}/{key[i]}"].to_hist())
        labels.append(f"{label_dict[samples[i]]}" + ", " + f"{key_name[i]}")
        if samples[i] == samples[i-1]:
            colors.append(f"{color_list[i]}")
        else:
            colors.append(f"{color_dict[samples[i]]}")
    
        y[i],x[i] = histograms[i].to_numpy()
        axs[0].stairs(y[i],x[i], color = colors[i], label = labels[i])
        if i != 0:
            axs[1].stairs(y[i]/y[0], x[0], color = colors[i])

    
    axs[0].set_ylabel(ylabel_name)
    if yscale_yn:
        axs[0].set_yscale("log")
    axs[0].legend(loc = legend_loc, fontsize = legend_size)

    if ratio_lim == None:
        ymin = 0.5
        ymax = 1.5
    else:
        ymin = ratio_lim[0]
        ymax = ratio_lim[1]
    axs[1].set_ylim(ymin,ymax)
    axs[1].set_yticks(np.arange(ymin,ymax,0.25*(ymax-ymin)))
    axs[1].set_yticks(np.arange(ymin,ymax,0.05*(ymax-ymin)), minor = True)
    axs[1].set_ylabel("Ratio")
    axs[1].set_xlabel(xlabel_name)
    if lim != None:
        axs[1].set_xlim(lim[0],lim[1])
    axs[1].axhline(y = 1, color = 'gray', linestyle = 'solid', linewidth = "0.5")

    for ax in axs:
        ax.label_outer()
                   
    if save:
        plt.savefig(f"images/{name}.png")