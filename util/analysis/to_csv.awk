	# gawk profile, created Tue Aug 27 18:48:01 2019

	# Rule(s)

	{
		cols[$1] = $2
	}

	# END rule(s)

	END {
		n = asorti(cols, stat)
		for (i = 1; i < n; i++) {
			printf "%s,", stat[i]
		}
		printf "%s\n", stat[n]
		for (i = 1; i < n; i++) {
			printf "%s,", cols[stat[i]]
		}
		print cols[stat[i]]
	}

