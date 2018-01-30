import os
import sys

## given a set of EFT points, create the gridpacks for all of them
## an EFT point is a tuple of format
## (kl, kt, c2, cg, c2g)

EFT_points = [
    (1,1,0,0,0),
    (20,1,0,0,0),
]

tag = "prova"

force  = True
mg5dir = "FIXME"

###################################################################


## step 1: create the folder where the production will be saved
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

## step 2 : create a dictionary for each generation
print "... writing generation log summary for", len(EFT_points), "points to be generated"
flog = open("%s/generation_log.txt" % tag, 'w')
flog.write('{: >15} {: >15} {: >15} {: >15} {: >15} {: >15}\n'.format('ipoint', 'klambda', 'kt', 'c2', 'cg', 'c2g'))
for ipt, EFT_pt in enumerate(EFT_points):
    flog.write('{: >15} {: >15} {: >15} {: >15} {: >15} {: >15}\n'.format(str(ipt), EFT_pt[0], EFT_pt[1], EFT_pt[2], EFT_pt[3], EFT_pt[4]))

## step 3 : create the gridpacks
print "... creating the gridpacks. This could take a while"
mg5exec = '/'.join((mg5dir,))
if not os.path.exists(mg5exec):
    print "** Cannot find the MG5 executable at:", mg5exec, "aborting"
    sys.exit()
