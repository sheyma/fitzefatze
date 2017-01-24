#!/bin/bash

NL=$'\n'
NL='\n'

jnum=0
while read -r yo cnt sum jobs ;do
	((jnum++))
	jfile=$(printf "job-%04d.cmd" "$jnum")
	echo "job $jfile: $sum"
	i=1
	jobdef="CNT='$cnt'$NL"
	while test "$jobs" != ""; do
		read -r t s mem jobs <<<$jobs
		jobdef="${jobdef}ARGS[$i]='$t $s'$NL"
		((i++))
	done
	#echo "$jobdef"
	sed "s/%jobdef%/$jobdef/g" z.cmd > "z/$jfile"
done

exit

tmax=45000
thresholds="0.34 0.38 0.42 0.46 0.50 0.54 0.58 0.62 0.66 0.70 0.74 0.78 0.82"
thresholds="0.50 0.54 0.58 0.62 0.66 0.70 0.74"
sigmas="0.005 0.010 0.015 0.020 0.025 0.030 0.035 0.040 0.045 0.050"
sigmas="0.005"
velocities="30"

for t in $thresholds; do
for s in $sigmas;do
for v in $velocities; do
	t=$(printf "%.2f" "$t")
	s=$(printf "%.3f" "$s")
	v=$(printf "%.1f" "$v")
	sed -e "s/%threshold%/$t/g" -e "s/%sigma%/$s/g" -e "s/%velocity%/$v/g" -e "s/%tmax%/$tmax/g" x.cmd > tmp-$t-$s-$v.cmd
done
done
done
