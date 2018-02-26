# prepare many process folders (for parallel generation)
# usage:
# source prepare_MG5_VBF_many.sh nfolders

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage:"
    echo "source prepare_MG5_VBF_many.sh nfolders"
    return
fi
for i in $(seq 1 $1); do \
   cp MG5_HH_generation/prepare_MG5_VBFgeneration.txt MG5_HH_generation/prepare_MG5_VBFgeneration_${i}.txt
   sed -i -e "s/VBF_HH_generation/VBF_HH_generation_${i}/g" MG5_HH_generation/prepare_MG5_VBFgeneration_${i}.txt
   cd MG5_aMC_v2_6_1
   ./bin/mg5_aMC < ../MG5_HH_generation/prepare_MG5_VBFgeneration_${i}.txt
   cd ..
   rm MG5_HH_generation/prepare_MG5_VBFgeneration_${i}.txt
done
