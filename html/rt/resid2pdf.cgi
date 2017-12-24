#!/usr/local/bin/perl

require ("/home/gartner/html/rt/getNODocument3.pl");

# input is a resid
# output is a path to the pdf

use CGI::Lite;

################################################################
#
# Get the input from the HTML Form
#
if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {

    # something submitted
    $cgi = new CGI::Lite;
    %FORM = $cgi->parse_form_data;


} else {

    # nothing submitted
	print <<EOF;
Content-type: text/plain;

0
EOF
    exit;
}

my $resId = _commify($FORM{'id'});
my ($docCd, $title) = &readDB($resId);
($docCd, $title) = &getfromGartner($FORM{'id'}) if (!$docCd); # lookup by getting g.com document if not in the database

my $path = substr ($docCd, 0, 4);

$title = substr ($title, 0, 15);
$title =~ tr/[A-Z]/[a-z]/;
$title =~ s/ /_/g;

$path = "\/resources\/$path"."00\/$docCd\/$title\.pdf";

print <<EOF;
Content-type: text/plain;

$path
EOF

exit;





##################################################################################
sub readDB {

    my $line = `grep $_[0] /home/gartner/html/rt/content/Resid2doccd2notenum.db`;

	$line =~ s/\"//g;
	$line =~ s/,//g;


	my ($resId, $title, $date, $docCd, $noteNum) = split (/\t/, $line);

    return(0) if (!$line);

    return($docCd, $title);

}

##################################################################################
sub saveDB {

        open (OUT, ">>/home/gartner/html/rt/content/Resid2doccd2notenum.db");
        print OUT $_[0];
        close (OUT);
        return();

}

##################################################################################
sub getfromGartner {


	my $url = "http:\/\/www4.gartner.com\/DisplayDocument\?id\=$_[0]\&ref\=g_search";

    my ($title, $pubDate, $summary, $resId, $auth, $body, $noteNumber, $toc, $price, $pages, $docType, $contentType, $folderType, $keywords, $path, $fileName, $fileSize, $geo, $industry, $infoType, $orgInfo, $docCd);

    ($title, $pubDate, $summary, $resId, $auth, $body, $noteNumber, $toc, $price, $pages, $docType, $contentType, $folderType, $keywords, $path, $fileName, $fileSize, $geo, $industry, $infoType, $orgInfo, $docCd) = &getResearchDetail($url);

	return(0) if (!$title);

	$resId = &_commify($resId);

	my $db = "$resId\t$title\t$pubDate\t$docCd\t$noteNumber\n";

	&saveDB($db) if ($db);

	return($docCd, $title);

}



##############################################
sub _commify {
   local $_  = shift;
   1 while s/^(-?\d+)(\d{3})/$1,$2/;
   return $_;
}



#http://www4.gartner.com/resources/119200/119206/119206.pdf

#http://www4.gartner.com/resources/420900/420985/420985.pdf