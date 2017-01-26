#!/bin/bash

if test $# != 2; then
        echo "error: bad usage" >&2
        echo "try something like: cat  jobs-56gb.txt | $0 56 /ptmp/sbayrak/fitzefatze/jobs_erdos42" >&2
        exit 1
fi

MEM="${1}gb"
INOUTDIR="$2"
jobdir=z

mkdir -p "$jobdir" || exit
test -n "$(find "$jobdir" -type d -empty)" || echo "warning: '$jobdir is not empty"  >&2

# newline for sed
NL='\n'

jnum=0
while read -r yo cnt sum jobs ;do
	((jnum++))
	jfile=$(printf "job-%04d.cmd" "$jnum")
	echo "$jfile: $cnt $sum"
	i=1
	jobdef="CNT='$cnt'$NL"
	jobdef="${jobdef}MEM_ESTM='$sum'$NL"
	while test "$jobs" != ""; do
		read -r t s mem jobs <<<$jobs
		jobdef="${jobdef}ARGS[$i]='$t $s'$NL"
		((i++))
	done
	#echo "$jobdef"
	sed \
		-e "s/%jobdef%/$jobdef/g" \
		-e "s/%ConsumableCpus%/$cnt/g" \
		-e "s/%ConsumableMemory%/$MEM/g" \
		-e "s@%INOUTDIR%@${INOUTDIR}@g" \
		z.cmd > "$jobdir/$jfile"
done

