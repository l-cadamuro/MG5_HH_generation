# MG5_HH_generation
Utilities to generate LHE files of HH samples using aMC_@NLO

# Instructions to install
```
## get CMSSW environment
cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src/
cmsenv
git clone https://github.com/l-cadamuro/MG5_HH_generation
## download MG5
wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.1.tar.gz
tar zxvf MG5_aMC_v2.6.1.tar.gz
## install the BSM_gg_hh model in the release
cd MG5_aMC_v2_6_1/models
wget https://cms-project-generators.web.cern.ch/cms-project-generators/BSM_gg_hh.tar
tar -xvf BSM_gg_hh.tar
cd ..
```
