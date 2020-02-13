    # gawk profile, created Tue Aug 27 18:35:42 2019

    # BEGIN rule(s)

    BEGIN {
        FS = "[:]|[*]";
        print "tick,fu used,issued,extra,width"
    }

    # Rule(s)

    /TotalSimdFU/ {
        print $1 "," $5 "," $8 "," $14 "," $11
    }

