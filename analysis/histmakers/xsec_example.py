
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
args = parser.parse_args()

functions.set_threads(args)

# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (10000, 0, 100) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins
bins_en = (1000, 0, 100)
bins_n = (2,0,2)

bins_theta = (200, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)

bins_cos = (100, -1, 1)

def build_graph_ll(df, dataset):

    print("build graph", dataset.name)
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Lepton0", "Muon#0.index")

    # gen muons
    df = df.Define("gen_muons", "FCCAnalyses::get_gen_pdg(Particle, 13)") # muon pdg index=13
    df = df.Define("gen_muons_p", "FCCAnalyses::MCParticle::get_p(gen_muons)")
    df = df.Define("gen_muons_theta", "FCCAnalyses::MCParticle::get_theta(gen_muons)")
    df = df.Define("gen_muons_phi", "FCCAnalyses::MCParticle::get_phi(gen_muons)")
    df = df.Define("gen_muons_no", "FCCAnalyses::MCParticle::get_n(gen_muons)")
    
    results.append(df.Histo1D(("gen_muons_p", "", *bins_p_mu), "gen_muons_p"))
    results.append(df.Histo1D(("gen_muons_theta", "", *bins_theta), "gen_muons_theta"))
    results.append(df.Histo1D(("gen_muons_phi", "", *bins_phi), "gen_muons_phi"))
    results.append(df.Histo1D(("gen_muons_no", "", *bins_count), "gen_muons_no"))
    
    results.append(df.Histo1D(("evts_initial", "", *bins_count), "weight"))
    
    
    # get the leptons leptons
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_p", "FCCAnalyses::ReconstructedParticle::get_p(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    df = df.Define("leps_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps_all)")
    df = df.Define("leps_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps_all)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")
    
    
    
    # construct Lorentz vectors of the leptons
    df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(leps_all)")
    df = df.Define("m_inv", "FCCAnalyses::inv_mass(leps_tlv)")
    df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(91., ReconstructedParticles)")
    df = df.Define("emiss", "missingEnergy[0].energy")
    df = df.Define("muon_leading", "(leps_all_p[0] > leps_all_p[1]) ? leps_all_p[0] : leps_all_p[1]")
    df = df.Define("muon_subleading", "(leps_all_p[0] < leps_all_p[1]) ? leps_all_p[0] : leps_all_p[1]")
    df = df.Define("one_pt", "FCCAnalyses::one_pt(leps_tlv)")
    df = df.Define("cos_theta", "FCCAnalyses::cos_theta(leps_all_theta)")
    df = df.Define("cut0", "0")
    df = df.Define("cut1", "1")
    df = df.Define("cut2", "2")
    df = df.Define("cut3", "3")
    df = df.Define("cut4", "4")
    df = df.Define("cut5", "5")
    df = df.Define("acol","FCCAnalyses::acolinearity(leps_all)")

    
    # initial 
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))
    
    # Filter
    df = df.Filter("leps_all_no==2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1")) 
    
    #df = df.Filter("m_inv>51.6525")
    #df = df.Filter("emiss<22.45")
    df = df.Filter("muon_leading > 27.3")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))
    df = df.Filter("one_pt > 3")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))
    df = df.Filter("leps_all_theta[0] > 0.2003348423 and leps_all_theta[0] < 2.941257811")
    df = df.Filter("leps_all_theta[1] > 0.2003348423 and leps_all_theta[1] < 2.941257811")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))
    
    df = df.Filter("acol<1.57079632679")
    
    # final
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))

    df = df.Define("visibleEnergy", "FCCAnalyses::visibleEnergy(ReconstructedParticles)")
    
    results.append(df.Histo1D(("cos_theta", "", *bins_theta), "cos_theta"))
    results.append(df.Histo1D(("acol", "", *bins_phi), "acol"))
    results.append(df.Histo1D(("muon_leading", "", *bins_p_mu), "muon_leading"))
    results.append(df.Histo1D(("leps_all_p", "", *bins_p_mu), "leps_all_p"))
    results.append(df.Histo1D(("leps_all_theta", "", *bins_theta), "leps_all_theta"))
    results.append(df.Histo1D(("leps_all_phi", "", *bins_phi), "leps_all_phi"))
    results.append(df.Histo1D(("leps_all_q", "", *bins_charge), "leps_all_q"))
    results.append(df.Histo1D(("leps_all_no", "", *bins_count), "leps_all_no"))
    results.append(df.Histo1D(("m_inv", "", *bins_m_ll), "m_inv"))
    results.append(df.Histo1D(("emiss", "", *bins_en), "emiss"))
    
    results.append(df.Histo1D(("m_inv", "", *bins_m_ll), "m_inv"))
    results.append(df.Histo1D(("visibleEnergy", "", *bins_m_ll), "visibleEnergy"))
    
    df = df.Define("theta_plus", "(leps_all_q[0] > 0) ? leps_all_theta[0] : leps_all_theta[1]")
    df = df.Define("theta_minus", "(leps_all_q[0] < 0) ? leps_all_theta[0] : leps_all_theta[1]")
    df = df.Define("cos_theta_plus", "cos(theta_plus)")
    df = df.Define("cos_theta_minus", "cos(theta_minus)")
    df = df.Define("cosThetac", "(sin(theta_plus-theta_minus))/(sin(theta_plus)+sin(theta_minus))")
    
    results.append(df.Histo1D(("theta_plus", "", *bins_theta), "theta_plus"))
    results.append(df.Histo1D(("theta_minus", "", *bins_theta), "theta_minus"))
    results.append(df.Histo1D(("cos_theta_plus", "", *bins_cos), "cos_theta_plus"))
    results.append(df.Histo1D(("cos_theta_minus", "", *bins_cos), "cos_theta_minus"))
    
    
    results.append(df.Histo1D(("cosThetac", "", *bins_cos), "cosThetac"))
    
    
    results.append(df.Histo1D(("evts_final", "", *bins_count), "weight"))
    return results, weightsum
    
 
    
   

if __name__ == "__main__":

    baseDir = functions.get_basedir() # get base directory of samples, depends on the cluster hostname (mit, cern, ...)
    import FCCee_spring2021_ecm91_IDEA
    datasets_spring2021_ecm91 = FCCee_spring2021_ecm91_IDEA.get_datasets(baseDir=baseDir) # list of all datasets
    datasets = [] # list of datasets to be run over

    datasets += functions.filter_datasets(datasets_spring2021_ecm91, ["p8_ee_Zmumu_ecm91"])
    datasets += functions.filter_datasets(datasets_spring2021_ecm91, ["p8_ee_Ztautau_ecm91"])
    datasets += functions.filter_datasets(datasets_spring2021_ecm91, ["wzp6_gaga_mumu_5_ecm91p2"])
    result = functions.build_and_run(datasets, build_graph_ll, "tmp/output_xsec_example.root", maxFiles=args.maxFiles, norm=True, lumi=150000000)

    
