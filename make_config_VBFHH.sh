# produces a config that instructs MG5 to configure its parameters
# usage:
# source make_config_VBFHH.sh CV C2V C3 output_LFN

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage:"
    echo "source make_config_VBFHH.sh CV C2V C3 output_LFN"
    return
fi

### in the card
#Block new
#    1 1.000000e-01 # CV
#    2 1.000000e-01 # C2V
#    3 1.000000e-01 # C3

## create the file
OFILE=$4
touch $OFILE
## clear the file if existing
> $OFILE
echo "0"            >> $OFILE
echo "set ptj  2"   >> $OFILE     ## from VBF CMS card
echo "set etaj -1"  >> $OFILE     ## from VBF CMS card
echo "set drjj 0.0001" >> $OFILE  ## from VBF CMS card
echo "set  CV  $1"  >> $OFILE
echo "set  C2V $2"  >> $OFILE
echo "set  C3  $3"  >> $OFILE
echo "0"            >> $OFILE
