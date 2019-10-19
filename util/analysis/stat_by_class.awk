    # gawk profile, created Tue Aug 27 18:35:42 2019

    # BEGIN rule(s)

    BEGIN {
        FS = "[:_]|[ ]+";
        pat = "[.]"stat"[_]"
    }

    # Rule(s)

    $0~pat {
        print $3 "," $5 "," $6
    }

