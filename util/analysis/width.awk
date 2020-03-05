    # gawk profile, created Tue Aug 27 18:35:42 2019

    # BEGIN rule(s)

    BEGIN {
        print "fu used,total width"
    }

    # Rule(s)

    /totalSimdFUUsed/ {
        printf $2
    }
    /totalSimdWidthUsed/ {
        print "," $2
    }

