#!/usr/bin/awk -f

function basekey()
{
	return substr(FILENAME,0,14)
}

# old awk does not has BEGINFILE ...
{
	if (lastfile != FILENAME) {
		key = basekey()
		c[key]++
		if (!exitstatus[key]) exitstatus[key] = "u"
		if (!term[key]) term[key] = "-"
		if (!oom[key]) oom[key] = "-"
		lastfile = FILENAME
	}
}

/Maximum resident/{
	thr = basekey()
	mem=$6;
	if (maxmem[thr] < mem){
		maxmem[thr] = mem
	}
}

/User time/{
	thr = basekey()
	usertm = $4
	if (maxusertm[thr] < usertm){
		maxusertm[thr] = usertm
	}
}

/Exit status:/{
	es = $3
	if (es != "0" ) {
		exitstatus[key] = "e"
	} else if (exitstatus[key] == "u" && es == "0") {
		exitstatus[key] = "0"
	}
}

/terminated by signal/{
	term[key] = "T"
}

/triggered an out of memory condition/{
	oom[key] = "oom"
}

END{
	for (key in c){
		printf("%20s %3s %7.2fG %6.0fs %s %4s %s\n", key,c[key],maxmem[key]/1024/1024,maxusertm[key],exitstatus[key],oom[key],term[key]) | "sort"
	}
}
