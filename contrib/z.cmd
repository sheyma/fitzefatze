# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = /ptmp/$(user)/LOG-ALL/$(jobid).out
# @ output = /ptmp/$(user)/LOG-ALL/$(jobid).out
# @ job_type = serial
# @ node_usage = not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(10)
# @ node_resources = ConsumableMemory(120gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 02:00:00
# @ notification = error
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

date "+start time: %F %T"
export TMPDIR="/ptmp/sbayrak/TMP"

## print host info for debugging or reproducing later
echo "#### begin machine info ####"
echo -n "## whoami: "
whoami
echo -n "## hostname: "
hostname -f
echo -n "## uname: "
uname -a
echo "## free:"
free
echo "## ulimit:"
ulimit  -a
echo "## lscpu:"
cat /proc/cpuinfo | grep -m1 "model name"
lscpu
echo "#### end machine info ####"

echo "#### begin python info ####"
myversions 2>&1
echo "#### end python info ####"

echo "#### begin module info ####"
module list
echo "#### end module info ####"

echo "#### begin env ####"
env | sort
echo "#### end env ####"

echo "#### begin original job setup ####"
grep "^# @ " "$0"
echo "#### end original job setup ####"

## finally we do do our real stuff ...
echo "####  here we go"

INOUTDIR="/ptmp/sbayrak/fitzefatze/jobs_erdos39"

JOB_BASE_NAME="$INOUTDIR/acp_w_thr_%threshold%_erdos_sigma=%sigma%_D=0.05_v=%velocity%_tmax=%tmax%"

if test -n "$LOADL_STEP_OUT"; then
	#ln -f "$LOADL_STEP_OUT" "${JOB_BASE_NAME}.jobout"
	ORIG_LOG="$LOADL_STEP_OUT"
else
	echo "warning: don't link log file (dryrun?)"
	ORIG_LOG="unknown"
fi

# add backgound jobs in parallel ...


# expanded like
#CNT='2'
#ARGS[0]='0.34 0.030'
#ARGS[1]='0.82 0.005'

%jobdef%

for i in $(seq 1 $CNT); do
	read thr sigma <<<${ARGS[$i]}
	tmax=45000
	velocity=30.0
	JOB_BASE_NAME="$INOUTDIR/acp_w_thr_${thr}_erdos_sigma=${sigma}_D=0.05_v=${velocity}_tmax=${tmax}"
	BLOG="${JOB_BASE_NAME}.jobout"
	echo "starting backround job $i with args ${ARGS[$i]}"
	echo "### background job (${ARGS[$i]}), original logfile is $(basename "$ORIG_LOG")" to "$BLOG"
	#/usr/bin/time -v  python -u 04_fhn_time_delays.py "$INOUTDIR/acp_w_thr_${thr}_erdos.dat" data/fib_length.dat ${ARGS[$i]} $tmax \
	#    >> "$BLOG" 2>&1 &

	echo /usr/bin/time -v  python -u 04_fhn_time_delays.py "$INOUTDIR/acp_w_thr_${thr}_erdos.dat" data/fib_length.dat ${ARGS[$i]} $tmax und...
done

wait

date "+end time: %F %T"
