# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = /ptmp/$(user)/LOG-ALL/$(jobid).out
# @ output = /ptmp/$(user)/LOG-ALL/$(jobid).out
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(1)
# @ node_resources = ConsumableMemory(1gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 00:05:00
# @ notification = complete
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

date "+start time: %F %T"


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

JOB_BASE_NAME="/ptmp/sbayrak/fitzefatze/hehe"

if test -n "$LOADL_STEP_OUT"; then
	ln "$LOADL_STEP_OUT" "${JOB_BASE_NAME}.jobout"
else
	echo "warning: don't link log file (dryrun?)"
fi

# /usr/bin/time -v python ${HOME}/devel/eigen_decomp/hcp_embed.py /ptmp/sbayrak/hcp/984472 --hem full --thr -o /ptmp/sbayrak/

date "+end time: %F %T"
