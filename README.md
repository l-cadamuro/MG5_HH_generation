# MG5_HH_generation
Utilities to generate LHE files of HH samples using aMC_@NLO

[Instructions to install](#instructions-to-install)  
[Prepare the folder for the generation](#prepare-the-folder-for-the-generation)  
[For an interactive generation (one point at a time!)](#for-an-interactive-generation-one-point-at-a-time)  
[For a gridpack generation (single core but can be sent to cluster or grid)](#for-a-gridpack-generation-single-core-but-can-be-sent-to-cluster-or-grid)  
[Running on the llr tier3](#running-on-the-llr-tier3)  
[Cluster mode](#cluster-mode)  
[Disable browser opening](#disable-browser-opening)  
[NMSSM generation](#nmssm-generation)

# Instructions to install
```
## get CMSSW environment
cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src/
cmsenv
git clone https://github.com/l-cadamuro/MG5_HH_generation
## download MG5
#wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.1.tar.gz
#tar zxvf MG5_aMC_v2.6.1.tar.gz
#MG5VERS=MG5_aMC_v2.6.5.tar.gz
MG5VERS=MG5_aMC_v2.6.6.tar.gz
wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/${MG5VERS}
tar zxvf ${MG5VERS}
## install the BSM_gg_hh model in the release
#cd MG5_aMC_v2_6_1/models
# this transforms the tar.gz into the MG5 version folder name
MG5FLDR=$MG5VERS
MG5FLDR="${MG5FLDR/.tar.gz/}"
MG5FLDR="${MG5FLDR//./_}"
cd ${MG5FLDR}/models
wget https://cms-project-generators.web.cern.ch/cms-project-generators/BSM_gg_hh.tar
tar -xvf BSM_gg_hh.tar
cd ../..
## install also the VBF HH model
#cd MG5_aMC_v2_6_1/models
cd ${MG5FLDR}/models
wget https://cms-project-generators.web.cern.ch/cms-project-generators/SM_HEL_UFO_noLightYukawa_HH_VBF.tar.gz
tar zxvf SM_HEL_UFO_noLightYukawa_HH_VBF.tar.gz
cd ../..
```

# Prepare the folder for the generation
**Gluon fusion**
```
cd ${MG5FLDR}
./bin/mg5_aMC < ../MG5_HH_generation/prepare_MG5_generation.txt
cd ..
```
which will create a folder ``${MG5VERS}/GG_HH_generation``.

**Vector boson fusion**
```
cd ${MG5FLDR}
./bin/mg5_aMC < ../MG5_HH_generation/prepare_MG5_VBFgeneration.txt
cd ..
```
which will create a folder ``${MG5VERS}/VBF_HH_generation``.

*Generating multiple folders*
The scripts ``prepare_MG5_many.sh`` and ``prepare_MG5_many.sh`` will simply call the above multiple time (call them from ``CMSSW/src``).
However, it is much faster to generate one output folder, and then simply do
```
cd ${MG5FLDR}
FLD_NAME=GG_HH_generation # or VBF_HH_generation
for i in {1..HOW_MANY_YOU_WANT}; do cp -r $FLD_NAME ${FLD_NAME}_${i}; done
```
which avoid re-running the diagrams every time.

# For an interactive generation (one point at a time!)
1. `` cd ${MG5FLDR}``
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

# For a gridpack generation (single core but can be sent to cluster or grid)
1. In ``GG_HH_generation/Cards/run_card.dat`` set ``True = gridpack``

# Running on the llr tier3
MadGraph code uses the condor submission commands, which will not work for the LLR Tier3 cluster.  
To make it work, one needs to modify the file ``madgraph/various/cluster.py`` to add the following lines (thanks Andrea!).  
NOTE: this file is copied to the working directory when generating a process. If you have already generated a working directory, you can edit only its own script at ``VBF_HH_generation/bin/internal`` (replace ``VBF_HH_generation`` with the working dir name).  
The modified script is also copied in [llr/cluster.py](llr/cluster.py), from MG5_aMC_v2_6_1

1. in class ``CondorCluster(Cluster)``, function ``submit`` (approx. line 860) replace the block ``text = """ `` with
```
        # A.S: changed to make it compliant with submission at llr 
        text = """Executable = %(prog)s
                  output = %(stdout)s
                  error = %(stderr)s
                  log = %(log)s
                  %(argument)s
                  environment = CONDOR_ID=$(Cluster).$(Process)
                  Universe = vanilla
                  notification = Error
                  Initialdir = %(cwd)s
                  %(requirement)s
                  getenv=True

                  accounting_group = cms
                  concurrency_limits_expr = strcat(T3Queue,":",RequestCpus," ",AcctGroupUser,":",RequestCpus)

                  +T3Queue="short"
                  +T3Group="cms"
                  +T3Submit=true

                  queue 1
               """
```

2. in class ``CondorCluster(Cluster)``, function ``submit2`` (approx. line 920) replace the block ``text = """ `` with
```
        # A.S: changed to make it compliant with submission at llr        
        text = """Executable = %(prog)s
                  output = %(stdout)s
                  error = %(stderr)s
                  log = %(log)s
                  %(argument)s
                  should_transfer_files = YES
                  when_to_transfer_output = ON_EXIT
                  transfer_input_files = %(input_files)s
                  %(output_files)s
                  Universe = vanilla
                  notification = Error
                  Initialdir = %(cwd)s
                  %(requirement)s
                  getenv=True

                  accounting_group = cms
                  concurrency_limits_expr = strcat(T3Queue,":",RequestCpus," ",AcctGroupUser,":",RequestCpus)

                  +T3Queue="short"
                  +T3Group="cms"
                  +T3Submit=true

                  queue 1
               """
```

# Cluster mode
Genearation defaults to multicore on a single machine. To use the cluster mode (jobs sent to cluster), before generating the process, you must edit ``input/mg5_configuration.txt``, uncomment run_mode and set it to 1:
```
#! Default Running mode
#!  0: single machine/ 1: cluster / 2: multicore
# run_mode = 2
```
If the process was already generated, edit the card in ``PROCESS_FOLDER/Cards/me5_configuration.txt``  
To run on the LLR cluster see [the corresponding section](#running-on-the-llr-tier3)

# Disable browser opening
Before generating the output, open the file ``input/mg5_configuration.txt`` and set
```
# Allow/Forbid the automatic opening of the web browser (on the
status page)
#when launching MadEvent [True/False]
automatic_html_opening = False
```
If the process was already generated, edit the card in ``PROCESS_FOLDER/Cards/me5_configuration.txt``  
See also [this link](https://answers.launchpad.net/mg5amcnlo/+faq/1943)

# NMSSM generation
A custom model by Yiming Zhong is used. It is a modified version of the NSSM model used in [this card](https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/ggh01_M125_Toa01a01_M5_Tomumutautau_proc_card.dat), where couplings to the H02 and H03 to gluons have been added to generate g g > H03.
```
cp MG5_HH_generation/NMSSM/NMSSMHET_UFO.zip ${MG5FLDR}/models
cd ${MG5FLDR}/models
unzip NMSSMHET_UFO.zip
```

To prepare the folder
```
./bin/mg5_aMC < ../MG5_HH_generation/NMSSM/prepare_MG5_NMSSM_generation.txt
```
