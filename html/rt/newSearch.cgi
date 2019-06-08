#!/usr/bin/perl

#
#  Done
#    13 Aug 2004 - fix urls to work on results
#    13 Aug 2004 - previous searches added
#
#  ToDo
#    * clean up special results like events -- more
#    * previous searches with save option?
#    * make sort more intuitive — currently an error in g.com code preventing this
#    * add additional pages to results
#    * have rss searches log you back in
#    * add or remove the javascript pop-up calls??
#
#

use Carp;
no Carp::Assert;


require ('/home/gartner/html/rt/commonSearch.pl');


# Variables
local $pageOneFlag = "";
#local $URL = "http:\/\/$server.gartner.com\/Search";
local $thisScript = "http://intl.transitionelement.com/rt/newSearch.cgi";


##############################################################
# Get the input from the HTML Form
##############################################################
if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {


    # something submitted

    use CGI::Lite;
    $cgi = new CGI::Lite;

    %FORM = $cgi->parse_form_data;

    foreach $key (keys %FORM) {

	# not required?
	next if ($key eq "PRM");
	$buffer .= "$key\=$FORM{$key}\&";

    }


} else {

    $inputs = "<p\>Username: <input type\=\"text\" name\=\"username\"\ \/\><\/p\>\n";
    &printSearchForm;
    exit;

}


##################################################################################
# MAIN
#
#

#################################
# What to do


if ($FORM{'rss'}) {

    &runQuery;
    &printRSS;
    exit;

} elsif ($FORM{'action'} eq "edit") {

    $inputs = "<input type\=\"hidden\" name\=\"username\" value\=\"$FORM{'username'}\" \/\>\n<input type\=\"hidden\" name\=\"oldname\" value\=\"$FORM{'name'}\" \/\>  $FORM{'username'}\n";
    &printEditForm;
    exit;


} elsif ($FORM{'action'} eq "save") {

    $inputs = "<input type\=\"hidden\" name\=\"username\" value\=\"$FORM{'username'}\" \/\>\n";

    if ($FORM{'oldname'}) {

	# actually saving over an old one
	&saveDB(&readDB($FORM{'username'}, 'edit', $FORM{'oldname'}));

    } else {

	# saving a new one
	&saveDB(&readDB($FORM{'username'}, 'all'));

    }

    $info   = &readDB($FORM{'username'}, 'get');
    &printSearchForm;
    exit;

} elsif ($FORM{'action'} eq "savenew") {

    $inputs = "<input type\=\"hidden\" name\=\"username\" value\=\"$FORM{'username'}\" \/\>\n $FORM{'username'}\n";
    &printEditForm;
    exit;

} elsif ($FORM{'action'} eq "delete") {

    $inputs = "<input type\=\"hidden\" name\=\"username\" value\=\"$FORM{'username'}\" \/\>\n";
    &saveDB(&readDB($FORM{'username'}, 'edit', $FORM{'name'}));
    $info   = &readDB($FORM{'username'}, 'get');
    &printSearchForm;
    exit;


} else {

    &runQuery if ($FORM{'keywords'});
    &prepareHTML;
    &printSearchForm;
    exit;

}

    exit;



################################################################################
sub runQuery {

	# clean up query string
	local $kw = $FORM{'keywords'};
	$kw =~ s/\%/\%25/g;
	$kw =~ s/\"/\%22/g;
	$kw =~ s/\#/\%23/g;
	$kw =~ s/\&/\%26/g;
	$kw =~ s/\'/\%27/g;
	$kw =~ s/\+/\%2B/g;
	$kw =~ s/\,/\%2C/g;
	$kw =~ s/\./\%2E/g;
	$kw =~ s/\//\%2F/g;
	$kw =~ s/\:/\%3A/g;
	$kw =~ s/\;/\%3B/g;
	$kw =~ s/\</\%3C/g;
	$kw =~ s/\=/\%3D/g;
	$kw =~ s/\>/\%3E/g;
	$kw =~ s/\?/\%3F/g;
	$kw =~ s/\@/\%40/g;
	$kw =~ s/\[/\%5B/g;
	$kw =~ s/\]/\%5D/g;
	$kw =~ s/\^/\%5E/g;
	$kw =~ s/\{/\%7B/g;
	$kw =~ s/\|/\%7C/g;
	$kw =~ s/\}/\%7D/g;
	$kw =~ s/\~/\%7E/g;
	$kw =~ s/ /\+/g;

	# clean up outputed string a little
	$FORM{'keywords'} =~ s/\&/\&amp\;/g;
	$FORM{'keywords'} =~ s/\>/\&gt\;/g;
	$FORM{'keywords'} =~ s/\"/\&quot\;/g;
	# $FORM{'keywords'} =~ s///g;

    # Run initial search and get all documents
    local $query = "keywords\=".$kw;
    $query .= "\&op\=73" if ($FORM{'sort'} eq "date");
    $query .= "\&op\=72" if ($FORM{'sort'} eq "relavancy");
    $query .= "\&op\=1"  if (!$FORM{'sort'});

    &getSearchResults($query, 'absPath', 'www');


}

##################################################################################
sub prepareHTML {

    $line = "";

    # get username, or make it hidden
    if (!$FORM{'username'}) {

    	$inputs = "<p\>Username: <input type\=\"text\" name\=\"username\" \/\><\/p\>\n";

    	# turn on BUY flag if there is no username
    	$buy = " \- <a href\=\"\#\"\>buy<\/a\>";

    } else {

    	$inputs = "<input type\=\"hidden\" name\=\"username\" value\=\"$FORM{'username'}\" \/\>\n";
    	$info   = &readDB($FORM{'username'}, 'get');

    	#	$info  .= "\n <li\><a href\=\"$thisScript?action\=savenew\&amp\;username=$FORM{'username'}\&amp\;keywords\=$FORM{'keywords'}\&amp\;terse\=$FORM{'terse'}\"\>save this search<\/a\><\/li\>\n" if ($FORM{'action'} ne "savedsearch" && @url);

    }

    # set checked flags for sorting and terse searching preferences
    local $terse   = "checked\=\"checked\"" if ($FORM{'terse'} eq "true");
    local $ck_rel  = "checked\=\"checked\"" if ($FORM{'sort'}  eq "relavancy");
    local $ck_date = "checked\=\"checked\"" if ($FORM{'sort'}  eq "date");

    # flip sort by date from ascending to descending based on previous selection
    local $st_date = "";
    if ($FORM{'datesortdirection'} eq "up" || $FORM{'sort'} eq "relavancy"  || !$FORM{'sort'}) {
        $st_date = "date <strong\>\&darr\;<\/strong\> <input type\=\"hidden\" name\=\"datesortdirection\" value\=\"down\" \/\>\n";
    } else {
        $st_date = "date <strong\>\&uarr\;<\/strong\> <input type\=\"hidden\" name\=\"datesortdirection\" value\=\"up\" \/\>\n";
    }

    # format searches from this session
    local $prevSearches = &_formatSessionSearches;

    # format information about results
    $resultsDetail =<<EndofHTML if (@url);
<div id="resultsdetail">
  <h2>Current Results</h2>
  <ul>
    <li>Found $results{'total'} results</li>
    <li><input type="checkbox" name="terse" value="true" $terse />simple listings</li>
    <li>sort by <input type="radio" name="sort" value="relavancy" $ck_rel />relavancy <input type="radio" name="sort" value="date" $ck_date />$st_date</li>
    <li><a href="$thisScript?action=savenew&amp;username=$FORM{'username'}&amp;keywords=$FORM{'keywords'}&amp;terse=$FORM{'terse'}&amp;sort=$FORM{'sort'}">Save this search</a></li>
  </ul>

  <h2>Previous Searches</h2>
  <ul>
    $prevSearches
 </ul>

</div>
EndofHTML

		# format Keywords section
    $keywordsDetail =<<EndofHTML if ($results{'keywords'});
<div id="keywordsdetail">
 <h2>Keywords</h2>
 <p>You might also like to try...</p>
 <ul>
  $results{'keywords'}
 </ul>
</div>
EndofHTML

		# format actual results
		foreach $url (@url) {

			# alternate class on each list to allow alternating colors
			if ($c eq "even") {
				$c = "odd";
			} else {
				$c = "even";
			}

			if ($results{'topic'}{$url} !~ /Events/) {

				# NOT an EVENT
				$line .= <<EndofLine;
  <li class="$c">
<a href="$url" class="title">$results{'title'}{$url}</a><br />
$results{'summary'}{$url}<br />

EndofLine

    if (!$FORM{'terse'}) {
	$line .= <<EndofLine;
<div class="detail">
$results{'topic'}{$url} - $results{'date'}{$url} - $results{'pages'}{$url} pages $buy<br />
Written by $results{'authors'}{$url}<br />
Browse Similar Research: $results{'browse'}{$url}
</div>
EndofLine

    } else {

    # terse
    $line .= <<EndofLine;
<div class="detail">
$results{'topic'}{$url} - $results{'date'}{$url} - $results{'pages'}{$url} pages - $results{'tersebrowse'}{$url} $buy<br />
</div>
EndofLine

}
	$line .= <<EndofLine;
</li>

EndofLine


} else {

    # an EVENT
	$eventsDetail .= <<EndofLine;
<div id="eventsdetail">
<h2>$results{'topic'}{$url}</h2>
<ul>
  <li>
<a href="$url"><strong>$results{'title'}{$url}</strong></a><br />
$results{'summary'}{$url}<br />
$results{'date'}{$url}<br />
  </li>
</ul>
</div>
EndofLine

	# undo the alternating cells thingy
	if ($c eq "even") {
	    $c = "odd";
	} else {
	    $c = "even";
	}

}

    }


}



##########################################################################
sub printRSS {

        # put dates into proper RSS 2.0 format
        use DateTime::Format::HTTP;
        my $dt = 'DateTime::Format::HTTP';

	foreach $url (@url) {

	    local ($d, $m, $y) = split(/ /, $results{'date'}{$url});
	    $m = substr($m, 0, 3);

	    local $pubdate = "$d $m $y";

	    local $datestring = $dt->parse_datetime($pubdate, 'GMT');
	    local $dateStr = $dt->format_datetime($datestring);

	    $rss .= "<item>\n  <title><![CDATA[$results{'title'}{$url}]]></title>\n  <description><![CDATA[$results{'summary'}{$url} (resid: $results{'resid'}{$url})]]></description>\n  <pubDate>$dateStr</pubDate>\n  <link><![CDATA[$url]]></link>\n</item>\n";

	#    $rss =~ s/\&(?!amp)/\&amp\;/g;
	}

	$date          = `date +'%a, %d %b %Y %T GMT'`;

	print <<EndofText;
Content-type: text/plain

<?xml version="1.0" ?>
  <rss version="2.0" xmlns:blogChannel="http://backend.userland.com/blogChannelModule">
  <channel>
  <title>Gartner Search -- $FORM{'keywords'}</title>
  <link>$thisScript?username=$FORM{'username'}\&amp\;keywords\=$FORM{'keywords'}\&amp\;terse\=$FORM{'terse'}\&amp\;sort\=$FORM{'sort'}</link>
  <description>Dynamic search of gartner.com based on $FORM{'keywords'} -- there were $results{'total'} results -- brought to you by Gartner, the world's leading IT research and advisory firm.</description>
  <language>en-us</language>
  <copyright>Copyright 2004 Gartner, Inc. and/or its Affiliates. All Rights Reserved. </copyright>
  <lastBuildDate>$date</lastBuildDate>
  <webMaster>peter.mahnke\@gartner.com</webMaster>
  <image>
    <url><![CDATA[http://regionals4.gartner.com/pages/docs/exp/images/dbd/gartner_logo.gif]]></url>
    <width>76</width>
    <height>19</height>
    <link><![CDATA[http://www.gartner.com]]></link>
    <title>Gartner</title>
  </image>
  <ttl>120</ttl>
  <skipDays><day>Saturday</day><day>Sunday</day></skipDays>
  <skipHours><hour>1</hour><hour>2</hour><hour>3</hour><hour>4</hour><hour>5</hour><hour>6</hour><hour>19</hour><hour>20</hour><hour>21</hour><hour>22</hour><hour>23</hour><hour>24</hour></skipHours>
$rss
 </channel>
</rss>
EndofText



}

##############################################################################
sub printSearchForm {

    # clean up ampersands
    $line           =~ s/&(?!\w{2,5};)/&amp;/gm;
    $eventsDetail   =~ s/&(?!\w{2,5};)/&amp;/gm;
    $keywordsDetail =~ s/&(?!\w{2,5};)/&amp;/gm;
    $buffer         =~ s/&(?!\w{2,5};)/&amp;/gm;

    print <<EndofHTML;
Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Language" content="en-us" />

<title>Peter's Simple Search</title>

<link rel="stylesheet" href="/css/newSearch.css" type="text/css" />

<style type="text/css">
</style>

<script type="text/javascript">

</script>

</head>

<body>
    <form method="post" name="frmSearch" action="$thisScript">
<div id="container">

  <div id="searchform">

    $inputs
    <p><img src="http://regionals4.gartner.com/pages/docs/exp/images/dbd/gartner_logo.gif" hspace="20" width="76" height="19" alt="Gartner Logo" />
    <input type="text" size="27" maxlength="400" name="keywords" value="$FORM{'keywords'}" />
    <input type="submit" value="search" class="submit" /><br />
    </p>

  </div><!-- END div search form -->


  <div id="sidebar">

    $resultsDetail

    <div id="info">
      $infoTitle
       <ul>
        $info
        $savethissearch
       </ul>
    </div><!-- END div info -->

    $keywordsDetail

    $eventsDetail

  </div><!-- END div sidebar -->

  <div id="content">
    <ul>
      $line
    </ul>
  </div><!-- END div content -->

  <div id="footer">
<!--
    <p><img src="http://regionals4.gartner.com/pages/docs/exp/images/dbd/gartner_logo.gif" hspace="20" vspace=""width="76" height="19" alt="Gartner Logo" />
    <input type="text" size="27" maxlength="400" name="keywords" value="$FORM{'keywords'}" />
    <input type="submit" style="position:relative;top:2;font:9pt;" value="search" /><br />
    </p>
-->
  </div><!-- END div footer -->


  <p class="buffer">$buffer</p>

</div><!-- END div container -->
  </form>
</body>
</html>
EndofHTML

}



############################################################################################
sub readDB {

	local $info;

	open(FILE, "/home/gartner/html/rt/content/newSearch.db") || die "Can't open db";

	while (<FILE>) {

		chop();

		local ($u, $n, $q) = split(/\t/);

		if ($_[1] eq "get") {

			# display mode

			local $kw = $1 if ($q =~ /keywords=(.[^\&]*)/); # grab keywords
			local $tr = $1 if ($q =~ /terse=(.[^\&]*)/);    # grab terse
			local $st = $1 if ($q =~ /sort=(.[^\&]*)/);     # grab sort

			$info .= "<li\>$n ::
			<a href\=\"$thisScript?$q\&amp\;username=$FORM{'username'}\&amp\;action=savedsearch\" onclick\=\"document.frmSearch.keywords.value\=\'$kw\'\; document.frmSearch.terse.value\=\'$tr\'\; document.frmSearch.sort.value\=\'$st\'\; document.frmSearch.submit(\)\; return(false\)\;\" \>search<\/a\> :
			<a href\=\"$thisScript?$q\&amp\;username=$FORM{'username'}\&amp\;rss\=true\"\>rss<\/a\> :
			<a href\=\"$thisScript?$q\&amp\;name\=$n\&amp\;username=$FORM{'username'}\&amp\;action\=edit\"\>edit<\/a\> :
			<a href\=\"$thisScript?$q\&amp\;name\=$n\&amp\;username=$FORM{'username'}\&amp\;action\=delete\"\>delete<\/a\>
			<\/li\>\n" if ($_[1] eq "get" && $u eq $_[0] && $_[0]);

		} elsif ($_[1] eq "edit") {

			# edit mode -- grab everyting except the one you are editing
			if ($u eq $_[0] && $n eq $_[2] && ($FORM{'oldname'} || $FORM{'action'} eq "delete")) {

				# this is the one you are editing, so ignor
				next;

			} else {

				$info .= "$_\n";

			}

		} else {

			# get all
			$info .= "$_\n";

		}
	}

	close(FILE);

	$infoTitle = "<h2\>Saved Searches<\/h2\>" if ($_[1] eq "get");


	return($info);

}


##################################################################################
sub saveDB {

    # saves the database
    # input is the old database, without the edited listing
    # uses Form inputs for rest

    local $terse = "\&amp\;terse\=true"        if ($FORM{'terse'} eq "true");
    local $sort  = "\&amp\;sort=$FORM{'sort'}" if ($FORM{'sort'});

    open(FILE, ">/home/gartner/html/rt/content/newSearch.db") || die "Can't open db";

    print FILE $_[0];
    print FILE "$FORM{'username'}\t$FORM{'name'}\tkeywords\=$FORM{'keywords'}$terse$sort\n" if ($FORM{'action'} eq "save"); # don't save deleted information

    close(FILE);

    return();

}




##############################################################################
sub printEditForm {

    local $terse = "checked\=\"checked\""   if ($FORM{'terse'} eq "true");
    local $ck_rel  = "checked\=\"checked\"" if ($FORM{'sort'}  eq "relavancy" || !$FORM{'sort'});
    local $ck_date = "checked\=\"checked\"" if ($FORM{'sort'}  eq "date");

    print <<EndofHTML;
Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Language" content="en-us" />

<title>Peter's Simple Search</title>

<link rel="stylesheet" href="/css/newSearch.css" type="text/css" />

<style type="text/css">

</style>

<script type="text/javascript">

</script>

</head>

<body>
<div class="searchform">
<form method="post" name="frmSearch">
$inputs
<p><img src="http://regionals4.gartner.com/pages/docs/exp/images/dbd/gartner_logo.gif" hspace="20" width="76" height="19" alt="Gartner Logo" /></p>
<p>Name: <input type="text" size="27" maxlength="400" name="name" value="$FORM{'name'}" /></p>
<p>Search Term: <input type="text" size="27" maxlength="400" name="keywords" value="$FORM{'keywords'}" /></p>
<p>Terse Listings: <input type="checkbox" name="terse" value="true" $terse /> yes</p>
<p>Sort Listings: <input type="radio" name="sort" value="relavancy" $ck_rel />relavancy <input type="radio" name="sort" value="date" $ck_date />date</p>
<p><input type="submit" style="position:relative;top:2;font:9pt;" name="action" value="save" /></p>
</form>
</div>

<div id="info">
$info
</div>

<p class="buffer">$buffer</p>

</body>
</html>
EndofHTML

}


sub _formatSessionSearches {

	# makes previous session searchs available
	#  nests same searches

	my $kw = "";
	my $tr = "";
	my $st = "";
	my $output = "";
	my $hash = $FORM{'prevqueries'};

	carp "\n\nHASH is $hash\n\n";

	if (!$FORM{'prevqueries'}) {

		# no saved queries, so do nothing

	} elsif ($FORM{'prevqueries'} =~ /keywords=(.[^\&]*)/) {

		# only one saved hash

		$kw = $1 if (/keywords=(.[^\&]*)/); # grab keywords
		$tr = $1 if (/terse=(.[^\&]*)/);    # grab terse
		$st = $1 if (/sort=(.[^\&]*)/);     # grab sort

		$output .= "     <li\><a href\=\"$thisScript?$_\" onclick\=\"document.frmSearch.keywords.value\=\'$kw\'\; document.frmSearch.terse.value\=\'$tr\'\; document.frmSearch.sort.value\=\'$st\'\; document.frmSearch.submit(\)\; return(false\)\;\"\>$kw<\/a\><\/li\>
		<input type\=\"hidden\" name\=\"prevqueries\" value\=\"$_\" \/\>\n" if ($1 ne $FORM{'keywords'});

	} else {

		# more than one saved query

		foreach (@$hash) {

			$kw = $1 if (/keywords=(.[^\&]*)/); # grab keywords
			$tr = $1 if (/terse=(.[^\&]*)/);    # grab terse
			$st = $1 if (/sort=(.[^\&]*)/);     # grab sort

			next if (!$kw);

			$output .= "     <li\><a href\=\"$thisScript?$_\" onclick\=\"document.frmSearch.keywords.value\=\'$kw\'\; document.frmSearch.terse.value\=\'$tr\'\; document.frmSearch.sort.value\=\'$st\'\; document.frmSearch.submit(\)\; return(false\)\;\"\>$kw<\/a\><\/li\>
			<input type\=\"hidden\" name\=\"prevqueries\" value\=\"$_\" \/\>\n" if ($kw ne $FORM{'keywords'});

		}
	}

	$output .= "<li\><a href\=\"$thisScript?username\=$FORM{'username'}\&amp\;keywords\=$FORM{'keywords'}\&amp\;terse\=$FORM{'terse'}\&amp\;sort\=$FORM{'sort'}\" onclick\=\"document.frmSearch.keywords.value\=\'$FORM{'keywords'}\'\; document.frmSearch.terse.value\=\'$FORM{'terse'}\'\; document.frmSearch.sort.value\=\'$FORM{'sort'}\'\; document.frmSearch.submit(\)\; return(false\)\;\"\>$FORM{'keywords'}<\/a\>\n<input type\=\"hidden\" name\=\"prevqueries\" value\=\"username\=$FORM{'username'}\&amp\;keywords\=$FORM{'keywords'}\&amp\;terse\=$FORM{'terse'}\&amp\;sort\=$FORM{'sort'}\" \/\><\/li\>\n";


	return($output);


}
