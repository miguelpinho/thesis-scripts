    # gawk profile, created Tue Aug 27 18:35:42 2019

    # BEGIN rule(s)

    BEGIN {
        print "sim seconds,clk cycles"
    }

    # Rule(s)

    /sim_seconds/ {
        printf $2
    }
    /system.switch_cpus.numCycles/ {
        print "," $2
    }

