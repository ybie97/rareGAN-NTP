#/bin/bash

proto=$1
budget=$2
thresh=$3


echo "Available Options: ntp_pvt"
echo "Available Budget: 20000, 200000"
echo "Available Thresholds: 5, 10, 15, 20, 999"

if [[ "$proto" != "ntp_pvt" ]]
then
  echo "wrong protocol"

else
  echo "Running" $proto $budget $thresh
    python rad_others.py $proto $budget $thresh
fi 
