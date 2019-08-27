	# gawk profile, created Tue Aug 27 17:23:32 2019

	# BEGIN rule(s)

	BEGIN {
		flag = 1
	}

	# Rule(s)

	/Begin Simulation/ {
		flag = 1 - flag
	}

	flag {
		print $0
	}

