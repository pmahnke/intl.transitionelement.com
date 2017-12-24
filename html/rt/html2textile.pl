#!/usr/local/bin/perl

# html2textil parser

# this is not at all complete

# started 25 May 2007





sub html2textile {


    my $flag  = 0;
    my $count = 1;
    my $out;
    my $list_type;

    my @lines = split (/\n/, $_[0]);
    foreach (@lines) {
        
        chomp();
        s/\r/\n/g;
        # s/\l/\n/g;
        
        if (!$_ && $flag) {
	    $flag = 0;
	    next;
        } elsif (!$_ || length($_) < 2) {
	    $count++;
        }
        
        if ($count > 1) {
	    $count = 1;
	    next;
        }
        
        $flag = 1 if (/<li>/i);
        
        s/<h(\d)>(.[^<]*)<\/h\d>/h$1. $2/i;

        # lists
        
        $list_type = "ul" if (/<ul>/i);
        $list_type = "ol" if (/<ol>/i);
        $list_type = ""   if (/<\/(o|u)l>/i);
        
        s/<\/ul>//gi;   
        s/<ul>/\n\n/gi; 
        s/<\/li>\n\n/<\/li>\n/mi;
        s/<\/li>//gi;
	if (/<li>/ && !$list_type) {
	    $list_type = "ul";
	    $_ = "\n\n".$_;
	}
        s/<li>/\* /gi if ($list_type ne "ol");
        s/ \* /\* /g if ($list_type ne "ol");
        s/<li>/\# /gi if ($list_type eq "ol");
        s/ \# /\# /g if ($list_type eq "ol");
        
        s/\s+<\/(b|strong)>/<\/strong>/gi;
        s/<(b|strong)>\s+(.[^<]*)<\/(b|strong)>/\*$2\* /gi;
        s/<(b|strong)>(.[^<]*)\s+<\/(b|strong)>/\*$2\* /gi;
        s/<(b|strong)>(.[^<]*)<\/(b|strong)>/\*$2\* /gi;
        s/<(i|em)>(.[^<]*)<\/(i|em)>/_$2_/gi;
        s/<p>(.[^<]*)<\/p>/$1/gi;
        s/<p>/\n\n/gi;
        s/<\/p>/\n\n/gi;
        s/\&amp\;ndash\;/\-/gi;       
        s/\&mdash\;/\-\-/gi;
        s/\n\n\n/\n\n/g;
        
        
        $out .= "$_\n";
        
    }

    $out =~ s/\n\n\n/\n\n/g;
    $out =~ s/ \n/\n/g;

    $out = "\n$out\n";

    return($out);
}

1;
