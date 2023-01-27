#ifndef XSEC_EXAMPLE_H
#define XSEC_EXAMPLE_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"

#include "ReconstructedParticle2MC.h"

namespace FCCAnalyses {
  
using Vec_f = ROOT::VecOps::RVec<float>;

Vec_tlv makeLorentzVectors(Vec_rp in) {
	
	Vec_tlv result;
	for (auto & p: in) {
		TLorentzVector tlv;
		tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
		result.push_back(tlv);
	}
	return result;
}

float inv_mass(Vec_tlv in){
    
    TLorentzVector result;
    for (int i =0; i< in.size(); i++){
        result = result + in[i];
    }
    float M = result.M();
    return M;
}

float one_pt(Vec_tlv in){
    
    float result;
    if (in[0].Pt() > in[1].Pt()){
        result = in[0].Pt();
    }
    
    else{
         result = in[0].Pt();
        
    }
    
    
    return result;
    
}

Vec_f cos_theta(Vec_f in){
    Vec_f cos_theta{cos(in[0]),cos(in[1])};
    return cos_theta;
}
    
}

#endif
