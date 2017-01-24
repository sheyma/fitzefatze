# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = /ptmp/$(user)/LOG-ALL/$(jobid).log
# @ output = /ptmp/$(user)/LOG-ALL/$(jobid).log
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
	ORIG_LOG="$INOUTDIR/lljob-$(basename "$LOADL_STEP_OUT")"
	echo "link logfile to $ORIG_LOG"
	ln -f "$LOADL_STEP_OUT" "$ORIG_LOG"
else
	echo "warning: unknown load leveler log file (dryrun?)"
	ORIG_LOG="unknown"
fi

# add backgound jobs in parallel ...


# The jobdef macro below will be expanded like
#CNT='2'
#ARGS[1]='0.34 0.010'
#ARGS[2]='0.82 0.020'

%jobdef%

#DRYRYUN="1"

echo "## start $CNT backround jobs"
for i in $(seq 1 $CNT); do
	read thr sigma <<<${ARGS[$i]}
	tmax=45000
	velocity=30.0
	JOB_BASE_NAME="$INOUTDIR/acp_w_thr_${thr}_erdos_sigma=${sigma}_D=0.05_v=${velocity}_tmax=${tmax}"
	BLOG="${JOB_BASE_NAME}.jobout"

	test -z "$DRYRYUN" || BLOG="test-$i.log"

	bj="bj $i:" # just a log prefix ...

	echo "$bj starting backround job $i with args ${ARGS[$i]}"
	test -f "$BLOG" && echo "$bj warning: logfile already exists (repeated job?): '$BLOG'"

	rm -f "$BLOG"
	echo "### background job $i with args ${ARGS[$i]}(${ARGS[$i]}), , original LL logfile is $ORIG_LOG" > "$BLOG"
	cmd="/usr/bin/time -v  python -u 04_fhn_time_delays.py "$INOUTDIR/acp_w_thr_${thr}_erdos.dat" data/fib_length.dat $sigma $velocity $tmax"

	echo "$bj run command: $cmd >> "$BLOG" 2>&1 &"
	echo "run command: $cmd >> "$BLOG" 2>&1 &" >> "$BLOG"

	if test -z "$DRYRYUN"; then
		$cmd >> "$BLOG" 2>&1 &
	else
		/usr/bin/time -v  sh -c "echo 'test output'; sleep '$i'" >> "$BLOG" 2>&1 &
	fi
done

echo "# review shell jobs"
jobs
date "+waiting for jobs...: %F %T"
wait

# TODO print exit status of all the processes


date "+end time: %F %T"
