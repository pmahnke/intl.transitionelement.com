#!/usr/bin/perl

if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {
    
    if ($ENV{'CONTENT_LENGTH'}) {
	read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});
	@pairs = split(/&/, $buffer);
    } else {
	@pairs = split(/&/, $ENV{'QUERY_STRING'});
    }
    
    
    foreach $pair (@pairs) {
	
	($name, $value) = split(/=/, $pair);
#	$value =~ s/\@/\\\@/g;
	$FORM{$name} = $value;
	
    }
    
} else {
    
    # nothing submitted
    
}

my $lp_id = "nodata";

my $lp = "";

if ($FORM{'email'}) { 
    $lp = qq~/usr/bin/curl -s 'https://api.launchpad.net/devel/people\?ws.op\=getByEmail\&email\=$FORM{'email'}' | /usr/bin/jq -r '.name' ~;
} else {
    $lp = qq~/usr/bin/curl -s 'https://api.launchpad.net/devel/people\?ws.op\=getByOpenIDIdentifier\&identifier\=$FORM{'id'}' | /usr/bin/jq -r '.name' ~;
}



$lp_id = `$lp`;

print qq|Content-Type: text/html; charset=UTF-8

$lp_id
|;
