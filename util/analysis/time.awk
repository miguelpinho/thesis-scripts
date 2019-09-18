    # gawk profile, created Tue Aug 27 18:35:42 2019

    # BEGIN rule(s)

    BEGIN {
        t = 0
    }

    # Rule(s)

    /final_tick/ {
        print t++ "," $2
    }

