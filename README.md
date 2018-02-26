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
## install also the VBF HH model
cd MG5_aMC_v2_6_1/models
wget https://cms-project-generators.web.cern.ch/cms-project-generators/SM_HEL_UFO_noLightYukawa_HH_VBF.tar.gz
tar zxvf SM_HEL_UFO_noLightYukawa_HH_VBF.tar.gz
cd ../..
```

# Prepare the folder for the generation
```
cd MG5_aMC_v2_6_1
./bin/mg5_aMC < ../MG5_HH_generation/prepare_MG5_generation.txt
cd ..
```
which will create a folder ``MG5_aMC_v2_6_1/GG_HH_generation``.

If you want to generate VBF HH, use the script ``../MG5_HH_generation/prepare_MG5_VBFgeneration.txt`` that created the folder `MG5_aMC_v2_6_1/VBF_HH_generation``

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


