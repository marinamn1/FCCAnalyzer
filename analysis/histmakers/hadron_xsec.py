
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=200)
parser.add_argument("--flavor", type=str, choices=["ee", "mumu", "qq"], help="Flavor (ee, mumu, qq)", default="qq")
parser.add_argument("--jetAlgo", type=str, choices=["kt", "valencia", "genkt"], default="kt", help="Jet clustering algorithm")
args = parser.parse_args()

functions.set_threads(args)

# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (20000, 0, 300) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins

bins_theta = (600, -1.5, 1.5)
bins_phi = (500, -5, 5)
bins_cut = (6,0,6)

bins_count = (120, 0, 120)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_et = (100,0,1)
bins_evis = (220, 0, 2.2)

bins_resolution = (10000, 0.95, 1.05)


jet_energy = (500, 0, 100) # 100 MeV bins
dijet_m = (2000, 0, 200) # 100 MeV bins
visMass = (2000, 0, 200) # 100 MeV bins
missEnergy  = (2000, 0, 200) # 100 MeV bins

dijet_m_final = (500, 50, 100) # 100 MeV bins
    
def build_graph_qq(df, dataset):

    print("build graph", dataset.name)
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Lepton0", "Electron#0.index")
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    
    
    df = df.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
    df = df.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
    df = df.Define("RP_pz", "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
    df = df.Define("RP_e",  "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df = df.Define("RP_m",  "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
    df = df.Define("RP_q",  "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
    df = df.Define("RP_no", "FCCAnalyses::ReconstructedParticle::get_n(ReconstructedParticles)")
    df = df.Define("visibleMass", "FCCAnalyses::visibleMass(ReconstructedParticles)") # scalar
    df = df.Define("missingEnergy_vec", "FCCAnalyses::missingEnergy(91.1, ReconstructedParticles)") # returns a vector
    df = df.Define("missingEnergy", "FCCAnalyses::ReconstructedParticle::get_e(missingEnergy_vec)")
    df = df.Define("sum_energy", "FCCAnalyses::sum_energy(RP_e)")
    df = df.Define("norm_energy", "FCCAnalyses::norm_energy(RP_e)")
    #df = df.Define("et", "FCCAnalyses::et(ReconstructedParticles)")
    #df = df.Define("ep", "FCCAnalyses::ep(ReconstructedParticles)")
    df = df.Define("energy_imbalance", "FCCAnalyses::energy_imbalance(ReconstructedParticles)")
    df = df.Define("energy_imbalance_tot", "energy_imbalance[0]")
    df = df.Define("energy_imbalance_trans", "energy_imbalance[1]/energy_imbalance[0]")
    df = df.Define("energy_imbalance_long", "energy_imbalance[2]/energy_imbalance[0]")
    df = df.Define("thrust_function", "FCCAnalyses::cos_thetat(ReconstructedParticles)")
    df = df.Define("thrust", "thrust_function[0]")
    df = df.Define("cos_thetat", "abs(thrust_function[3])")
    results.append(df.Histo1D(("cos_thetat", "", *bins_theta), "cos_thetat"))
    results.append(df.Histo1D(("thrust", "", *bins_theta), "thrust"))
    
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
    
    
    
    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    if args.jetAlgo == "kt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets)")
    elif args.jetAlgo == "valencia":
        df = df.Define("clustered_jets", "JetClustering::clustering_valencia(0.5, 1, 2, 0, 0, 1., 1.)(pseudo_jets)")
    elif args.jetAlgo == "genkt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
          


    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")
    df = df.Define("sum_e", "FCCAnalyses::sum_e(jets_e)")
    df = df.Define("mass_inv", "FCCAnalyses::mass_inv(jets)")
    df = df.Define("e1_e2", "FCCAnalyses::e1_e2(jets)")
    df = df.Define("e_ratio", "e1_e2[0]")
    df = df.Define("e1", "e1_e2[1]")
    df = df.Define("e2", "e1_e2[2]")
    df = df.Define("cos_thetajet", "FCCAnalyses::cos_thetajet(jets)")
    df = df.Define("cos_theta1", "cos_thetajet[0]")
    df = df.Define("cos_theta2", "cos_thetajet[1]")
    results.append(df.Histo1D(("e_ratio", "", *jet_energy), "e1_e2"))
    results.append(df.Histo1D(("e1", "", *jet_energy), "e1"))
    results.append(df.Histo1D(("e2", "", *jet_energy), "e2"))
    results.append(df.Histo1D(("cos_theta1", "", *bins_theta), "cos_theta1"))
    results.append(df.Histo1D(("cos_theta2", "", *bins_theta), "cos_theta2"))
    
        
    df = df.Define("njets", "jets_e.size()")
    results.append(df.Histo1D(("njets", "", *bins_count), "njets"))
        
    # reconstruct resonance (jets are pT ordered)
    df = df.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df = df.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df = df.Define("dijet", "jet1+jet2")
    df = df.Define("dijet_m", "dijet.M()")

    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    df = df.Define("cut1", "1")
    df = df.Define("cut2", "2")
    #df = df.Define("cut3", "3")
    #df = df.Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut0"))
   

    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    #df = df.Filter("njets >= 2")
    df = df.Filter("RP_no >= 10")
    results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut1"))
    df = df.Filter("sum_energy >= 22.6")
    results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut2"))
    #results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut3"))
    #results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut4"))
    #df = df.Filter("cos_thetat <= 0.74")
    
    


    results.append(df.Histo1D(("jets_e", "", *jet_energy), "jets_e"))
    results.append(df.Histo1D(("RP_e", "", *jet_energy), "RP_e"))
    results.append(df.Histo1D(("dijet_m", "", *dijet_m), "dijet_m"))
    results.append(df.Histo1D(("mass_inv", "", *dijet_m), "mass_inv"))
    results.append(df.Histo1D(("dijet_m_final", "", *dijet_m_final), "dijet_m"))
    results.append(df.Histo1D(("RP_no", "", *bins_count), "RP_no"))
    results.append(df.Histo1D(("electrons", "", *bins_count), "leps_all_no"))
    results.append(df.Histo1D(("electrons_theta", "", *bins_phi), "leps_all_theta"))
    results.append(df.Histo1D(("RP_m", "", *jet_energy), "RP_m"))
    results.append(df.Histo1D(("sum_e", "", *jet_energy), "sum_e"))
    results.append(df.Histo1D(("sum_energy", "", *jet_energy), "sum_energy"))
    results.append(df.Histo1D(("norm_energy", "", *bins_evis), "norm_energy"))
    results.append(df.Histo1D(("et", "", *bins_et), "energy_imbalance_trans"))
    results.append(df.Histo1D(("ep", "", *bins_et), "energy_imbalance_long"))
   
        
    
    
    results.append(df.Histo1D(("visibleMass", "", *visMass), "visibleMass"))    
    results.append(df.Histo1D(("missingEnergy", "", *missEnergy), "missingEnergy"))    
        
    
    return results, weightsum
    
    
    
    
    
    
if __name__ == "__main__":

    baseDir = functions.get_basedir() # get base directory of samples, depends on the cluster hostname (mit, cern, ...)
    import FCCee_spring2021_ecm91_IDEA
    datasets_spring2021_ecm91 = FCCee_spring2021_ecm91_IDEA.get_datasets(baseDir=baseDir) # list of all datasets
    datasets = [] # list of datasets to be run over
 
    if args.flavor == "qq":
        datasets += functions.filter_datasets(datasets_spring2021_ecm91, ["wzp6_ee_qq_ecm91p2", "wzp6_ee_tautau_ecm91p2", "wzp6_ee_mumu_ecm91p2", "wzp6_gaga_qq_5_ecm91p2","kkmc_ee_uu_ecm91p2", "kkmc_ee_dd_ecm91p2", "kkmc_ee_cc_ecm91p2", "kkmc_ee_ss_ecm91p2", "kkmc_ee_bb_ecm91p2", "p8_ee_Zee_ecm91"]) #,"wzp6_ee_qq_ecm89p5","wzp6_ee_tautau_ecm89p5","wzp6_ee_mumu_ecm89p5","wzp6_ee_qq_ecm90p2","wzp6_ee_tautau_ecm90p2","wzp6_ee_mumu_ecm90p2","wzp6_ee_qq_ecm92p0","wzp6_ee_tautau_ecm92p0","wzp6_ee_mumu_ecm92p0","wzp6_ee_qq_ecm93p0","wzp6_ee_tautau_ecm93p0","wzp6_ee_mumu_ecm93p0"]) #"p8_ee_Zuds_ecm91", "p8_ee_Zcc_ecm91", "p8_ee_Zbb_ecm91", "wzp6_ee_qq_ecm91p2"])
        if args.jetAlgo == "kt":
            result = functions.build_and_run(datasets, build_graph_qq, "tmp/output_hadron_xsec_qq_kt.root", maxFiles=args.maxFiles, norm=True, lumi=75000000)
        if args.jetAlgo == "valencia":
            result = functions.build_and_run(datasets, build_graph_qq, "tmp/output_hadron_xsec_qq_valencia.root", maxFiles=args.maxFiles, norm=True, lumi=75000000)
        if args.jetAlgo == "genkt":
            result = functions.build_and_run(datasets, build_graph_qq, "tmp/output_hadron_xsec_qq_genkt.root", maxFiles=args.maxFiles, norm=True, lumi=75000000)
    
