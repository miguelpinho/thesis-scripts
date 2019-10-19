    # gawk profile, created Tue Aug 27 18:35:42 2019

    # BEGIN rule(s)

    BEGIN {
        print "clk cycles"
    }

    # Rule(s)

    /system.switch_cpus.numCycles/ {
        print $2
    }

