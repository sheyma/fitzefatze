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
# @ resources = ConsumableCpus(1)
# @ node_resources = ConsumableMemory(56gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 02:00:00
# @ notification = error
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

date "+start time: %F %T"

cd ~/devel/fitzefatze || exit
export TMPDIR="/ptmp/sbayrak/TMP"
mkdir -p "$TMPDIR"

if test -z "$SKIP_LL_INFO"; then
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
fi

## finally we do do our real stuff ...
echo "####  here we go"

INOUTDIR="/ptmp/sbayrak/fitzefatze/jobs1"

JOB_BASE_NAME="$INOUTDIR/acp_w_thr_%threshold%_sigma=%sigma%_D=0.05_v=%velocity%_tmax=%tmax%"

if test -n "$LOADL_STEP_OUT"; then
	ln -f "$LOADL_STEP_OUT" "${JOB_BASE_NAME}.jobout"
else
	echo "warning: don't link log file (dryrun?)"
fi

/usr/bin/time -v  python -u 04_fhn_time_delays.py "$INOUTDIR/acp_w_thr_%threshold%.dat" data/fib_length.dat "%sigma%" "%velocity%" "%tmax%"


date "+end time: %F %T"
