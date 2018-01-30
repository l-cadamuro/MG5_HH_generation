# produces a config that instructs MG5 to configure its parameters
# usage:
# source make_config_ggHH.sh kl kt c2 cg c2g output_LFN

if [ "$#" -ne 6 ]; then
    echo "Illegal number of parameters"
    echo "Usage:"
    echo "source make_config_ggHH.sh kl kt c2 cg c2g output_LFN"
    return
fi

## create the file
OFILE=$6
touch $OFILE
## clear the file if existing
> $OFILE
echo "0"            >> $OFILE
echo "set  ctr $1"  >> $OFILE
echo "set  cy  $2"  >> $OFILE
echo "set  c2  $3"  >> $OFILE
echo "set  a1  $4"  >> $OFILE
echo "set  a2  $5"  >> $OFILE
echo "0"            >> $OFILE