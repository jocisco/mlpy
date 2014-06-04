#!/bin/bash

sda1=`df -H /dev/sda1 | sed '1d' | awk '{print $5}' | cut -d'%' -f1`
sdb1=`df -H /dev/sdb1 | sed '1d' | awk '{print $5}' | cut -d'%' -f1`

mem=`top -bn1 | head | awk '/Mem/ { printf "%.2f",$4*100/$2}'`

# 5 min cpu load avg
num_cpu=`grep 'model name' /proc/cpuinfo | wc -l`
cpu=`cat /proc/loadavg | awk '{printf "%.2f", $2/'$num_cpu'*100}'`

# computing jvm mem %
diag=`curl -sk https://admin:cariden@172.29.104.113:8443/matelive/services/diag/sysinfo`
used=`echo $diag | egrep -o "JVM memory current usage=[^ ]+" | sed 's/.*=\(.*\)/\1/'`
total=`echo $diag | egrep -o "JVM max memory=[^ ]+" | sed 's/.*=\(.*\)/\1/'`
jvm=`bc <<< "scale=2; $used*100/$total"`

jdbconn=`netstat -ant | grep 9088 | grep EST | wc -l`
dsmem=`top -bn1m | grep oninit | awk '{sum += $10} END {print sum}'`

# outputing tsv file
echo -e "server\tsda1\tsdb1\tmem\tcpu\tjvm\tjdbconn\tdsmem"
echo -e "mldev01\t${sda1}\t${sdb1}\t${mem}\t${cpu}\t$jvm\t${jdbconn}\t${dsmem}"
