import os
import sys

## given a set of EFT points, create the gridpacks for all of them
## an EFT point is a tuple of format
## (kl, kt, c2, cg, c2g)

EFT_points = [
    (1,1,0,0,0),
    (20,1,0,0,0),
    (20,1,0,100,-2),
]

tag = "prova"

force  = True
mg5dir = "../MG5_aMC_v2_6_1/GG_HH_generation"
generate_gpack = True ## set to false if gpack was already generated


###################################################################

###################################################################
############# step 1: create the folder where the production will be saved
print "... working in folder:", tag
if os.path.isdir(tag):
    if force:
        print "** Folder", tag, "is already existing and force option was passed --> deleting it"
        os.system('rm -r %s' % tag)
    else:
        print "** Folder", tag, "already existing, aborting"
        sys.exit()

os.system('mkdir %s' % tag)
os.system('mkdir %s/gridpacks' % tag)
os.system('mkdir %s/configs' % tag)

###################################################################
############# step 2 : create a dictionary for each generation
print "... writing generation log summary for", len(EFT_points), "points to be generated"
flog = open("%s/generation_log.txt" % tag, 'w')
flog.write('{: >15} {: >15} {: >15} {: >15} {: >15} {: >15}\n'.format('ipoint', 'klambda', 'kt', 'c2', 'cg', 'c2g'))
for ipt, EFT_pt in enumerate(EFT_points):
    flog.write('{: >15} {: >15} {: >15} {: >15} {: >15} {: >15}\n'.format(str(ipt), EFT_pt[0], EFT_pt[1], EFT_pt[2], EFT_pt[3], EFT_pt[4]))
flog.close()

###################################################################
############# step 3 : create the gridpacks
if generate_gpack:
    print "... going to prepare the gridpacks"

    # verify the exec is there
    mg5exec = '/'.join((mg5dir,'bin','generate_events'))
    if not os.path.exists(mg5exec):
        print "** Cannot find the MG5 executable at:", mg5exec, "aborting"
        sys.exit()
    else:
        print "... using the executable:", mg5exec

    # generate the scripts
    print "... generating the config scripts"
    scrname_proto = tag+'/configs/point_{0}.txt'
    for ipt, EFT_pt in enumerate(EFT_points):
        scrname = scrname_proto.format(ipt)
        os.system('source ./make_config_ggHH.sh %f %f %f %f %f %s' % (EFT_pt[0], EFT_pt[1], EFT_pt[2], EFT_pt[3], EFT_pt[4], scrname))

    # generate the gpacks
    print "... creating the gridpacks. This could take a while (30s to 1 min per point on polui01)"
    for ipt, EFT_pt in enumerate(EFT_points):
        os.system ('./%s gpack_point_%i < %s' % (mg5exec, ipt, scrname_proto.format(ipt)))