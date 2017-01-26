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
# @ resources = ConsumableCpus(16)
# @ node_resources = ConsumableMemory(56gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 24:00:00
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

find   /ptmp/sbayrak/fitzefatze/jobs_erdos* -type f -name "acp_w_thr_0.[3-8]*_*_sigma=*tmax=45000.dat" -mmin +2  \
	| sed "s/.dat$//" | while read -r base ; do if ! test -f ${base}_NORM_BOLD_signal.dat || ! test -f ${base}_BOLD_filtered.dat; then  echo "$base.dat" ;fi ;done \
	| \time -v xargs -t -r -P 16 -n 1 python -u 05_bold_activity.py

date "+end time: %F %T"
