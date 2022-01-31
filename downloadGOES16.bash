#!/bin/bash
 
 
echo "retrieving GOES"
 
#########################################
# CONFIGURACION
#
# YEAR OF INTEREST
YEARS='2022'
 
# DAYS OF THE YEAR
DAYS="001"
 
# CHANNEL
CHANNELS='C13'
 
# PRODUCTO
PRODUCTS='L1b-RadF'


#########################################
 

for PRODUCT in $PRODUCTS; do
for YEAR in $YEARS; do
for DAY in $DAYS; do
 
aws s3 --no-sign-request ls --recursive noaa-goes16/ABI-$PRODUCT/$YEAR/$DAY/ | awk '{print $3";"$4}' >> list.txt
 
done
done
done
 
#
Selecciono C13
for CHANNEL in $CHANNELS; do
grep $CHANNEL list.txt >> wanted.txt
done
#########################################
 
#########################################
# DOWNLOAD
#
 
for x in $(cat wanted.txt);
do
SIZE=$(echo $x | cut -d";" -f1)
FULLNAME=$(echo $x | cut -d";" -f2)
NAME=$(echo $x | cut -d"/" -f5)
 
echo "Processing file $NAME of size $SIZE"
if [ -f $NAME ]; then
 echo "This file exists locally"
 LOCALSIZE=$(du -sb $NAME | awk '{ print $1 }')
 if [ $LOCALSIZE -ne $SIZE ]; then
 echo "The size of the file is not the same as the remote file. Downloading again..."
 aws s3 --no-sign-request cp s3://noaa-goes16/$FULLNAME ./
 else
 echo "The size of the file matches the remote file. Not downloading it again."
 fi
else
 echo "This file does not exists locally, downloading..."
 aws s3 --no-sign-request cp s3://noaa-goes16/$FULLNAME ./
fi
 
done
#########################################
 
echo Program ending.
