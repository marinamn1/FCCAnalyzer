import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=100)
parser.add_argument("--limitingTheta", type=float, help="Limiting Theta angle (size of the hole, radians)", default=0.00)
parser.add_argument("--flavor", type=str, choices=["ee", "mumu", "qq"], help="Flavor (ee, mumu, qq)", default="qq")
parser.add_argument("--jetAlgo", type=str, choices=["kt", "valencia", "genkt"], default="kt", help="Jet clustering algorithm")
args = parser.parse_args()

functions.set_threads(args)

# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (20000, 0, 300) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins

bins_theta = (315, 0, 3.15)
bins_phi = (500, -5, 5)
bins_cut = (6,0,6)

bins_count = (60, 0, 120)
mc_count = (150, 0, 300)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_jets = (10,0,10)
bins_iso = (500, 0, 5)
bins_et = (100,0,1)
bins_evis = (220, 0, 2.2)
bins_norm = (115, 0, 1.15)

bins_resolution = (10000, 0.95, 1.05)


jet_energy = (1000, 0, 100) # 100 MeV bins
dijet_m = (2000, 0, 200) # 100 MeV bins
bins_rapidity = (200,-10,10)
visMass = (2000, 0, 200) # 100 MeV bins
missEnergy  = (2000, 0, 200) # 100 MeV bins

dijet_m_final = (500, 50, 100) # 100 MeV bins
    
def build_graph_qq(df, dataset):

    print("build graph", dataset.name)
    results = []
    limit = args.limitingTheta

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Lepton0", "Electron#0.index")
    df = df.Alias("Lepton1","Muon#0.index")
    df = df.Define("VisibleParticles", "FCCAnalyses::VisibleParticles(%f,ReconstructedParticles)"%(limit))
    df = df.Define("MCVisibleParticles", "FCCAnalyses::MCVisibleParticles(%f,Particle)"%(limit))
    df = df.Define("NonVisibleParticles", "FCCAnalyses::NonVisibleParticles(%f,ReconstructedParticles)"%(limit))
    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
    df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get(Lepton1, ReconstructedParticles)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_iso", "FCCAnalyses::coneIsolation(0.01, 0.4)(muons, ReconstructedParticles)")
    df = df.Define("electrons_iso", "FCCAnalyses::coneIsolation(0.01, 0.4)(electrons, ReconstructedParticles)")
    df = df.Define("high_muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons)")
    df = df.Define("high_electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons)")
    df = df.Define("high_muons_iso", "FCCAnalyses::coneIsolation(0.01, 0.4)(high_muons, ReconstructedParticles)")
    df = df.Define("isolated_muons", "FCCAnalyses::sel_iso(0.25)(high_muons, high_muons_iso)")
    df = df.Define("high_electrons_iso", "FCCAnalyses::coneIsolation(0.01, 0.4)(high_electrons, ReconstructedParticles)")
    df = df.Define("isolated_electrons", "FCCAnalyses::sel_iso(0.25)(high_electrons, high_electrons_iso)")
    
    # results.append(df.Histo1D(("muons_iso", "", *bins_iso), "muons_iso"))
    # results.append(df.Histo1D(("high_muons_iso", "", *bins_iso), "high_muons_iso"))
    # results.append(df.Histo1D(("electrons_iso", "", *bins_iso), "electrons_iso"))
    # results.append(df.Histo1D(("high_electrons_iso", "", *bins_iso), "high_electrons_iso"))
    
    df = df.Define("RP_charged", "FCCAnalyses::charged(VisibleParticles)")
    df = df.Define("MC_charged", "FCCAnalyses::mc_charged(MCVisibleParticles)")
    df = df.Define("RP_neutral", "FCCAnalyses::neutral(ReconstructedParticles)")
    df = df.Define("n_charged", "FCCAnalyses::ReconstructedParticle::get_n(RP_charged)")
    df = df.Define("mc_n_charged", "FCCAnalyses::MCParticle::get_n(MC_charged)")
    df = df.Define("n_neutral", "FCCAnalyses::ReconstructedParticle::get_n(RP_neutral)")
    
    df = df.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
    df = df.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
    df = df.Define("RP_pz", "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
    df = df.Define("RP_e",  "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df = df.Define("MC_e",  "FCCAnalyses::MCParticle::get_e(MCVisibleParticles)")
    df = df.Define("RP_e_charged",  "FCCAnalyses::ReconstructedParticle::get_e(RP_charged)")
    df = df.Define("MC_e_charged",  "FCCAnalyses::MCParticle::get_e(MC_charged)")
    df = df.Define("RP_e_vis",  "FCCAnalyses::ReconstructedParticle::get_e(VisibleParticles)")
    df = df.Define("RP_e_NonVisible",  "FCCAnalyses::ReconstructedParticle::get_e(NonVisibleParticles)")
    df = df.Define("RP_p", "FCCAnalyses::ReconstructedParticle::get_p(ReconstructedParticles)")
    df = df.Define("RP_pt", "FCCAnalyses::ReconstructedParticle::get_pt(ReconstructedParticles)")
    df = df.Define("MC_pt", "FCCAnalyses::MCParticle::get_pt(Particle)")
    df = df.Define("MC_pt_charged", "FCCAnalyses::MCParticle::get_pt(MC_charged)")
    df = df.Define("RP_pt_charged", "FCCAnalyses::ReconstructedParticle::get_pt(RP_charged)")
    df = df.Define("RP_m",  "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
    df = df.Define("RP_q",  "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
    df = df.Define("RP_no", "FCCAnalyses::ReconstructedParticle::get_n(ReconstructedParticles)")
    df = df.Define("MC_no", "FCCAnalyses::MCParticle::get_n(Particle)")
    df = df.Define("RP_no_vis", "FCCAnalyses::ReconstructedParticle::get_n(VisibleParticles)")
    df = df.Define("RP_no_NonVisible", "FCCAnalyses::ReconstructedParticle::get_n(NonVisibleParticles)")
    df = df.Define("RP_theta_NonVisible", "FCCAnalyses::ReconstructedParticle::get_theta(NonVisibleParticles)")
    df = df.Define("RP_theta_vis", "FCCAnalyses::ReconstructedParticle::get_theta(VisibleParticles)")
    df = df.Define("RP_theta", "FCCAnalyses::ReconstructedParticle::get_theta(ReconstructedParticles)")
    df = df.Define("MC_theta", "FCCAnalyses::MCParticle::get_theta(Particle)")
    df = df.Define("visibleMass", "FCCAnalyses::visibleMass(ReconstructedParticles)") # scalar
    df = df.Define("missingEnergy_vec", "FCCAnalyses::missingEnergy(91.1, ReconstructedParticles)") # returns a vector
    df = df.Define("missingEnergy", "FCCAnalyses::ReconstructedParticle::get_e(missingEnergy_vec)")
    df = df.Define("sum_energy", "FCCAnalyses::sum_energy(RP_e)")
    df = df.Define("MC_sum_energy", "FCCAnalyses::norm_energy(MC_e)")
    df = df.Define("sum_energy_charged", "FCCAnalyses::norm_energy(RP_e_charged)")
    df = df.Define("MC_sum_energy_charged", "FCCAnalyses::norm_energy(MC_e_charged)")
    df = df.Define("norm_RP_e_vis", "FCCAnalyses::norm_RP_e(RP_e_vis)")
    df = df.Define("norm_MC_e", "FCCAnalyses::norm_RP_e(MC_e)")
    df = df.Define("norm_RP_e_NonVisible", "FCCAnalyses::norm_RP_e(RP_e_NonVisible)")
    #df = df.Define("norm_energy", "FCCAnalyses::norm_energy(RP_e)")
    df = df.Define("norm_energy_vis", "FCCAnalyses::norm_energy(RP_e_vis)")
    df = df.Define("norm_energy_NonVisible", "FCCAnalyses::norm_energy(RP_e_NonVisible)")
    df = df.Define("energy_imbalance", "FCCAnalyses::energy_imbalance(ReconstructedParticles)")
    df = df.Define("energy_imbalance_tot", "energy_imbalance[0]")
    df = df.Define("energy_imbalance_trans", "energy_imbalance[1]/energy_imbalance[0]")
    df = df.Define("energy_imbalance_long", "energy_imbalance[2]/energy_imbalance[0]")
    df = df.Define("thrust_function", "FCCAnalyses::cos_thetat(ReconstructedParticles)")
    df = df.Define("thrust", "thrust_function[0]")
    df = df.Define("cos_thetat", "abs(thrust_function[3])")
    #df = df.Define('EVT_thrust',     'FCCAnalyses::Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
    #df = df.Define('RP_thrustangle', 'FCCAnalyses::Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')
    #results.append(df.Histo1D(("cos_thetat", "", *bins_theta), "RP_thrustangle"))
    #results.append(df.Histo1D(("thrust", "", *bins_theta), "EVT_thrust"))
    
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
    
    
    
    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    if args.jetAlgo == "kt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets)")
    elif args.jetAlgo == "valencia":
        df = df.Define("clustered_jets", "JetClustering::clustering_valencia(0.5, 1, 2, 0, 0, 1., 1.)(pseudo_jets)")
    elif args.jetAlgo == "genkt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_genkt(1.5, 2, 2, 0, 0, -1)(pseudo_jets)")
          


    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_p", "FCCAnalyses::JetClusteringUtils::get_p(jets)")
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
    # results.append(df.Histo1D(("e_ratio", "", *jet_energy), "e1_e2"))
    # results.append(df.Histo1D(("e1", "", *jet_energy), "e1"))
    # results.append(df.Histo1D(("e2", "", *jet_energy), "e2"))
    results.append(df.Histo1D(("cos_theta1", "", *bins_theta), "cos_theta1"))
    results.append(df.Histo1D(("cos_theta2", "", *bins_theta), "cos_theta2"))
    
        
    df = df.Define("njets", "jets_e.size()")
    results.append(df.Histo1D(("njets", "", *bins_jets), "njets"))
        
    # reconstruct resonance (jets are pT ordered)
    df = df.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df = df.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df = df.Define("jet1_e", "jet1.E()")
    df = df.Define("jet2_e", "jet2.E()")
    df = df.Define("dijet", "jet1+jet2")
    df = df.Define("dijet_m", "dijet.M()")
    df = df.Define("rapidity", "dijet.Y()")
    df = df.Define("jets_acol", "3.14159265359-jet1.Theta()-jet2.Theta()")
    results.append(df.Histo1D(("jet1_e", "", *dijet_m), "jet1_e"))
    results.append(df.Histo1D(("jet2_e", "", *dijet_m), "jet2_e"))
    results.append(df.Histo1D(("jets_acol", "", *bins_theta), "jets_acol"))
    results.append(df.Histo1D(("rapidity", "", *bins_rapidity), "rapidity"))

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
    df1 = df
    df2 = df
    df3 = df
    #df = df.Filter("njets >= 2")
    #df = df.Filter("RP_no_vis >= 10")
    #df = df.Filter("n_charged >= 4")
    #df = df.Filter("mc_n_charged >= 4")
    df1 = df1.Filter("RP_no_vis < 14")
    results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut1"))
    #df = df.Filter("norm_energy_vis >= 0.247752")
    #df = df.Filter("norm_energy_vis >= 0.52")
    #df = df.Filter("MC_sum_energy >= 0.52")
    df2 = df2.Filter("norm_energy_vis < 0.4")
    results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut2"))
    df3 = df3.Filter("RP_no_vis < 14 || norm_energy_vis < 0.4")
    #df3 = df3.Filter("norm_energy_vis >= 0.877")
    #results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut3"))
    #results.append(df.Histo1D(("cutFlow", "", *bins_cut), "cut4"))
    #df = df.Filter("cos_thetat <= 0.74")
    
    
    #######
    ### CUTS FROM LEP COMPARISON
    #######
    df = df.Define("lep", "FCCAnalyses::sel_LEP(ReconstructedParticles)")
    df = df.Define("lep_mc", "FCCAnalyses::sel_LEP_mc(Particle)")
    df = df.Define("lep_charged", "FCCAnalyses::charged(lep)")
    df = df.Define("lep_charged_mc", "FCCAnalyses::mc_charged(lep_mc)")
    df = df.Define("lep_n_charged", "FCCAnalyses::ReconstructedParticle::get_n(lep_charged)")
    df = df.Define("lep_n_charged_mc", "FCCAnalyses::MCParticle::get_n(lep_charged_mc)")
    df = df.Define("lep_RP_e_charged",  "FCCAnalyses::ReconstructedParticle::get_e(lep_charged)")
    df = df.Define("lep_MC_e_charged",  "FCCAnalyses::MCParticle::get_e(lep_charged_mc)")
    df = df.Define("lep_energy_charged", "FCCAnalyses::norm_energy(lep_RP_e_charged)")
    df = df.Define("lep_energy_charged_mc", "FCCAnalyses::norm_energy(lep_MC_e_charged)")
    df = df.Define("lep_RP_px", "FCCAnalyses::ReconstructedParticle::get_px(lep)")
    df = df.Define("lep_RP_py", "FCCAnalyses::ReconstructedParticle::get_py(lep)")
    df = df.Define("lep_RP_pz", "FCCAnalyses::ReconstructedParticle::get_pz(lep)")
    df = df.Define('EVT_sphericity','FCCAnalyses::Algorithms::minimize_sphericity("Minuit2","Migrad")(lep_RP_px,lep_RP_py, lep_RP_pz)')
    #df = df.Define('RP_sphericityangle', 'FCCAnalyses::Algorithms::getAxisCosTheta(EVT_sphericity, lep_RP_px, lep_RP_py, lep_RP_pz)')
    df = df.Define('sphe_x',   "EVT_sphericity.at(0)")
    df = df.Define('sphe_y',   "EVT_sphericity.at(1)")
    df = df.Define('sphe_z',   "EVT_sphericity.at(2)")
    df = df.Define('EVT_sphericity_mag', "sqrt(sphe_x*sphe_x+sphe_y*sphe_y+sphe_z*sphe_z)")
    df = df.Define('EVT_sphericity_val', "EVT_sphericity.at(3)")
    df = df.Define("sphericity_angle", "sphe_z/EVT_sphericity_mag")
    #df = df.Filter("lep_n_charged > 4")
    #df = df.Filter("lep_energy_charged > 0.1645")
    #df = df.Filter("lep_n_charged_mc > 4")
    #df = df.Filter("lep_energy_charged_mc > 0.1645")
    #df = df.Filter("sphericity_angle > -0.819 && sphericity_angle < 0.819")
    results.append(df.Histo1D(("lep_n_charged", "", *bins_count), "lep_n_charged"))
    results.append(df.Histo1D(("lep_n_charged_mc", "", *bins_count), "lep_n_charged_mc"))
    


    results.append(df.Histo1D(("jets_e", "", *jet_energy), "jets_e"))
    results.append(df.Histo1D(("jets_p", "", *jet_energy), "jets_p"))
    results.append(df.Histo1D(("norm_RP_e", "", *bins_norm), "RP_e"))
    results.append(df.Histo1D(("RP_e_vis", "", *jet_energy), "RP_e_vis"))
    results.append(df.Histo1D(("RP_pt", "", *dijet_m), "RP_pt"))
    results.append(df.Histo1D(("RP_pt_charged", "", *dijet_m), "RP_pt_charged"))
    results.append(df.Histo1D(("MC_pt", "", *dijet_m), "MC_pt"))
    results.append(df.Histo1D(("MC_pt_charged", "", *dijet_m), "MC_pt_charged"))
    results.append(df1.Histo1D(("discard1RP_e_vis", "", *bins_norm), "norm_RP_e_vis"))
    results.append(df2.Histo1D(("discard2RP_e_vis", "", *bins_norm), "norm_RP_e_vis"))
    results.append(df3.Histo1D(("discard3RP_e_vis", "", *bins_norm), "norm_RP_e_vis"))
    results.append(df.Histo1D(("RP_e_NonVisible", "", *jet_energy), "RP_e_NonVisible"))
    results.append(df.Histo1D(("RP_p", "", *jet_energy), "RP_p"))
    results.append(df.Histo1D(("dijet_m", "", *dijet_m), "dijet_m"))
    results.append(df.Histo1D(("mass_inv", "", *dijet_m), "mass_inv"))
    results.append(df.Histo1D(("dijet_m_final", "", *dijet_m_final), "dijet_m"))
    results.append(df.Histo1D(("RP_no", "", *bins_count), "RP_no"))
    results.append(df.Histo1D(("MC_no", "", *mc_count), "MC_no"))
    results.append(df.Histo1D(("RP_no_vis", "", *bins_count), "RP_no_vis"))
    results.append(df1.Histo1D(("discard1RP_no_vis", "", *bins_count), "RP_no_vis"))
    results.append(df2.Histo1D(("discard2RP_no_vis", "", *bins_count), "RP_no_vis"))
    results.append(df3.Histo1D(("discard3RP_no_vis", "", *bins_count), "RP_no_vis"))
    results.append(df.Histo1D(("RP_no_NonVisible", "", *bins_count), "RP_no_NonVisible"))
    results.append(df.Histo1D(("n_charged", "", *bins_count), "n_charged"))
    results.append(df.Histo1D(("n_neutral", "", *bins_count), "n_neutral"))
    results.append(df.Histo1D(("mc_n_charged", "", *bins_count), "mc_n_charged"))
    results.append(df.Histo1D(("RP_q", "", *bins_charge), "RP_q"))
    results.append(df.Histo1D(("electrons_no", "", *bins_count), "electrons_no"))
    results.append(df.Histo1D(("electrons_theta", "", *bins_theta), "electrons_theta"))
    results.append(df.Histo1D(("muons_no", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_theta", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("RP_theta", "", *bins_theta), "RP_theta"))
    results.append(df.Histo1D(("MC_theta", "", *bins_theta), "MC_theta"))
    results.append(df.Histo1D(("RP_theta_vis", "", *bins_theta), "RP_theta_vis"))
    results.append(df1.Histo1D(("discard1RP_theta", "", *bins_theta), "RP_theta_vis"))
    results.append(df2.Histo1D(("discard2RP_theta", "", *bins_theta), "RP_theta_vis"))
    results.append(df3.Histo1D(("discard3RP_theta", "", *bins_theta), "RP_theta_vis"))
    results.append(df.Histo1D(("RP_theta_NonVisible", "", *bins_theta), "RP_theta_NonVisible"))
    results.append(df.Histo1D(("RP_m", "", *jet_energy), "RP_m"))
    results.append(df.Histo1D(("sum_e", "", *dijet_m), "sum_e"))
    results.append(df.Histo1D(("sum_energy", "", *dijet_m), "sum_energy"))
    results.append(df.Histo1D(("MC_sum_energy", "", *dijet_m), "MC_sum_energy"))
    results.append(df.Histo1D(("MC_sum_energy_charged", "", *dijet_m), "MC_sum_energy_charged"))
    results.append(df1.Histo1D(("discard1norm_energy", "", *bins_norm), "norm_energy_vis"))
    results.append(df2.Histo1D(("discard2norm_energy", "", *bins_norm), "norm_energy_vis"))
    results.append(df3.Histo1D(("discard3norm_energy", "", *bins_norm), "norm_energy_vis"))
    results.append(df.Histo1D(("norm_RP_e_vis", "", *bins_norm), "norm_RP_e_vis"))
    results.append(df.Histo1D(("norm_MC_e", "", *bins_norm), "norm_MC_e"))
    results.append(df.Histo1D(("norm_RP_e_NonVisible", "", *bins_norm), "norm_RP_e_NonVisible"))
    results.append(df.Histo1D(("norm_energy_vis", "", *bins_norm), "norm_energy_vis"))
    results.append(df.Histo1D(("norm_energy_NonVisible", "", *bins_norm), "norm_energy_NonVisible"))
    results.append(df.Histo1D(("et", "", *bins_et), "energy_imbalance_trans"))
    results.append(df.Histo1D(("ep", "", *bins_et), "energy_imbalance_long"))
    results.append(df1.Histo1D(("discard1cos_thetat", "", *bins_norm), "cos_thetat"))
    results.append(df1.Histo1D(("discard1thrust", "", *bins_norm), "thrust"))
    results.append(df3.Histo1D(("discard3cos_thetat", "", *bins_norm), "cos_thetat"))
    results.append(df3.Histo1D(("discard3thrust", "", *bins_norm), "thrust"))
   
        
    
    
    results.append(df.Histo1D(("visibleMass", "", *visMass), "visibleMass"))    
    results.append(df.Histo1D(("missingEnergy", "", *missEnergy), "missingEnergy"))    
        
    
    return results, weightsum
    
    
    
    
    
    
if __name__ == "__main__":

    baseDir = functions.get_basedir() # get base directory of samples, depends on the cluster hostname (mit, cern, ...)
    import FCCee_spring2021_ecm91_IDEA
    import FCCee_winter2023_IDEA_ecm240
    datasets_spring2021_ecm91 = FCCee_spring2021_ecm91_IDEA.get_datasets(baseDir=baseDir) # list of all datasets
    datasets_winter2023_ecm240 = FCCee_winter2023_IDEA_ecm240.get_datasets(baseDir=baseDir)
    datasets = [] # list of datasets to be run over
 
    if args.flavor == "qq":
        datasets += functions.filter_datasets(datasets_spring2021_ecm91, ["wzp6_ee_tautau_ecm91p2", "wzp6_ee_mumu_ecm91p2", "wzp6_gaga_qq_5_ecm91p2", "p8_ee_Zee_ecm91"])# "wzp6_ee_qq_ecm91p2","kkmc_ee_uu_ecm91p2", "kkmc_ee_dd_ecm91p2", "kkmc_ee_cc_ecm91p2", "kkmc_ee_ss_ecm91p2", "kkmc_ee_bb_ecm91p2", "p8_ee_Zee_ecm91", "p8_ee_Zmumu_ecm91", "p8_ee_Ztautau_ecm91"])
        datasets += functions.filter_datasets(datasets_winter2023_ecm240, ["wz3p8_ee_uu_ecm91p2", "kkmc_ee_uu_ecm91p2"]) #"p8_ee_Zuu_ecm91p2_noBES_noISR", "kkmc_ee_uu_ecm91p2_noBES_noISR", "wz3p8_ee_uu_ecm91p2_noBES_noISR", "wzp6_ee_uu_ecm91p2"])
        if args.jetAlgo == "kt":
            result = functions.build_and_run(datasets, build_graph_qq, "tmp/output_hadron_xsec_gen.root", maxFiles=args.maxFiles, norm=True, lumi= 75000000)
        if args.jetAlgo == "genkt":
            result = functions.build_and_run(datasets, build_graph_qq, "tmp/output_hadron_xsec.root", maxFiles=args.maxFiles, norm=True, lumi= 75000000)
    
