#!/usr/local/bin/perl


$FILE = "/home/gartner/logs/access\*";

use CGI::Lite;


if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {

    $cgi = new CGI::Lite;
    %FORM = $cgi->parse_form_data;

    &printPAGE(&search);
    exit;

} else {

    # nothing submitted... so PANIC!!!
	&printPAGE();
	exit;

}


sub search {


    #82.43.120.39 - - [25/May/2005:06:39:19 -0500] "GET /cgi-bin/directory.cgi HTTP/1.1" 200 6918 "http://stmgrts.org.uk/" "Mozilla/5.0 (Windows; U; Windows NT 5.0;en-GB; rv:1.7.8) Gecko/20050511 Firefox/1.0.4"
    
    my @input = `zgrep \"$FORM{'date'}\" $FILE \| grep "$FORM{'pattern'}\"`;
    
    foreach (@input) {
	my ($ip, $null, $null, $date, $tz, $method, $url, $null, $status, $size, $refer, $browser, $null) = split (/ /,$_, 13); 

	next if ($url !~ /$FORM{'pattern'}/);
	$$url{$ip}++;
	$counturl{$url}++;
    }

    foreach (sort { $counturl{$b} <=> $counturl{$a} } keys %counturl) {
	
	undef my $ipcount;
	foreach (keys %$_) {
	    $ipcount++;
	}

	$trim = substr ($_, 0, 80);
	$output .= "<tr><td class\=\"script\"><a href\=\"http://intl.transitionelement.com$_\" target\=\"new\">$trim</a></td><td>$counturl{$_}</td><td>$ipcount</td></tr>\n";
	
    }
    return ($output);

}

sub printFORM {

	my $line =<<EndofFORM;

<form method="post" action="/cgi-bin/log.cgi">

<ul>
  <li>Date: <input type="text" name="date" value="$FORM{'date'}" /></li>
  <li>URL: <input type="text" name="pattern" value="$FORM{'pattern'}" /></li>
  <li><input type="submit" /></li>
</ul>


</form>

EndofFORM

    return($line);
}


sub printPAGE {

    my $form = &printFORM();
    
    print <<EndofHTML;
Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org\tR/xhtml1/DTD/xhtml1-transitional.dtd">
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <meta http-equiv="Content-Type"       content="text/html; charset=utf-8" />
        <title>intl.transitionelement.com log parser </title>

        <style type="text/css">
            #twocolcenter  {width: 700px;}
	    table {table-layout: fixed; }
    td {overflow: hidden; text-overflow: ellipsis;}
        </style>

        <script type="text/javascript" language="javascript">

        </script>

   </head>

    <body>

        <div id="container">

        <div id="banner">
            <h1 id="logo">Scholastic Log Parser</h1>
        </div><!-- end div banner -->

                <div id="content">

                    <h2>Log Parser</h2>

$form

<table>
<col id="col1" width="250"></col><col id="col2"></col>
<tr><th>url</th><th>hits</th><th>ips</th></tr>
$_[0]
</table>

<p>$help</p>

<p>$msg</p>

                </div><!-- end div content -->

            </div><!-- end div twocolcenter -->

        <div style="clear: both;">&#160;</div>

$footer

        </div><!-- end div container -->



    </body>
</html>
EndofHTML


}

