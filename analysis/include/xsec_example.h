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
    
    TLorentzVector sum;
    
    for (int i=0;i<in.size();i++){
        sum = sum+in[i];
    }
    float sum_m = sum.M();
    return sum_m;
}
    
float max_pt(Vec_tlv in){
    float greatest_pt = 0;
    for(int i = 0; i<in.size(); i++){
        if(in[i].Pt()>greatest_pt){
            greatest_pt = in[i].Pt();
        }
    }
    return greatest_pt; 
}
    
Vec_f cos_theta(Vec_f in){
    
    Vec_f vec_cos_theta{cos(in[0]), cos(in[1])};
        
    return vec_cos_theta;
}
}


#endif
