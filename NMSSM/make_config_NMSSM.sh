# produces a config that instructs MG5 to configure its parameters
# usage:
# source make_config_ggHH.sh kl kt c2 cg c2g output_LFN

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "Usage:"
    echo "source make_config_NMSSM.sh mh03 mh02 output_LFN"
    return
fi

## create the file
OFILE=$3
touch $OFILE
## clear the file if existing
> $OFILE
echo "0"                >> $OFILE
echo "set  MH03 $1"     >> $OFILE
echo "set  MH02 $2"     >> $OFILE
echo "set  MH01 125"    >> $OFILE
echo "set  WH03 0.001"  >> $OFILE
echo "set  WH02 0.001"  >> $OFILE
echo "set  WH01 0.004"  >> $OFILE
echo "0"                >> $OFILE