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
cd ../..
```

# Prepare the folder for the generation
```
cd MG5_aMC_v2_6_1
./bin/mg5_aMC < ../MG5_HH_generation/prepare_MG5_generation.txt
cd ..
```
which will create a folder ``MG5_aMC_v2_6_1/GG_HH_generation``

# For an interactive generation (one point at a time!)
1. `` cd MG5_aMC_v2_6_1``
2. set the number of events, energy etc.. by editing ``GG_HH_generation/Cards/run_card.dat``
3. run the generation interactively as ``./GG_HH_generation/bin/generate_events |output_name|``
**note:** you can script the generation by doing
``./GG_HH_generation/bin/generate_events |output_name| < |script_name|``
where ``script_name`` is a file that contains the following lines:
```
0
set  ctr 1.0
set  cy  1.0
set  c2  1.0
set  a1  1.0
set  a2  1.0
0
```
you can also generate the config file with MG5_HH_generation/make_config_ggHH.sh

# For a gridpack generation (single core, but can be sent to cluster or grid)
1. In ``GG_HH_generation/Cards/run_card.dat`` set ``True = gridpack``
