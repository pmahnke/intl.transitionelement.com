#!/usr/local/bin/perl

require ("/home/gartner/html/rt/getNODocument3.pl");

###############################################################
#
# commonSearch.pl
#
#  runs a search on gartner.com and returns the results in a Hask
#
#  INPUTS
#    query string, absolute path flag <optional>, server prefix (i.e. www3, www4) <optional>
#
#  TODO
#    make more objecty
#
#
###################################################################



my $absPath = "";
my $server = "www3";

sub getSearchResults {

    if ($_[1]) {
    	# set absolut URL path if requested
    	$absPath = "http:\/\/".$server.".gartner.com\/";
    }


    if ($_[2]) {
    	# set server if passed
    	$server = "$_[2]";
    }
    my $URL = "http:\/\/".$server.".gartner.com\/Search\?".$_[0];


    carp "GETTING QUERY: $URL\n\n";
    $Page = &getGARTNERpage($URL, $server);
    &_parseResultsPage($Page);

    return (@url);
}


##################################################################################
sub _parseResultsPage {

	my $uri;
	my $resid;
	my $target;
	my $title;
	my $pages;
	my $flagPages;
	my $topic;
	my $summary;
	#my $authors;
	my $totalResults;

	local @output = split (/\n/, $_[0]);

	START: foreach (@output) {

		# last
		last if (/end document loop/);


		# ADDITIONAL SEARCH RESULTS PAGES
		if (!$pageOneFlag && /Search\?/) {

			while (/Search\?(.[^\"]*)\"/g) {

				push @URLS, $1;
				$msg .= "new FOUND ADDITIONAL RESULTS PAGE $1<p\>\n\n";

			}

			# only get other search result URLs once
			$pageOneFlag = 1;
		}

		# get total number of results
		$totalResults = $1 if (/matches\&nbsp\;(.[^\&]*)\&/ && !$totalResults);

		# deal with results
		if ($flagLast) {

			$flagLast = 0;
			push @url, $uri;
			$results{'resid'}{$uri}       = $resid;
			$results{'target'}{$uri}       = $target;
			$results{'title'}{$uri}        = $title;
			$results{'date'}{$uri}         = $date;
			$results{'topic'}{$uri}        = $topic;
			$results{'summary'}{$uri}      = $summary;
			$results{'pages'}{$uri}        = $pages;
			chop ($authors);
			chop ($authors);
			$results{'authors'}{$uri}      = $authors;
			chop ($browse);
			chop ($browse);
			chop ($browse);
			$results{'browse'}{$uri}       = $browse;
			chop ($tersebrowse);
			$results{'tersebrowse'}{$uri}  = $tersebrowse;
			$results{'total'}              = $totalResults;
			($uri, $resid, $target, $title, $date, $topic, $summary, $pages, $authors, $browse, $tersebrowse) = "";

		}


		# get URL, target  and Title
		if (/openDoc\(\'(.[^\']*)\'\,\'(.[^\']*)\'\)\" class\=\"resultTitleLink\"\>(.[^<]*)</) {

			$uri     = "$absPath$1";
			$target  = $2;
			$title   = $3;
			$resid   = $1 if ($uri =~ /id\=(.*)/);

			# carp "found info: $uri, $title\n";
		}

		# get date
		$date = $1 if (/entry2\"\>(.*)/);

		# get topic
		if ($flagTopic && /(.[^<]*)</) {
			$topic = $1;
			$flagTopic = 0;
		}
		if (/<td class\=\"entry2\" width\=\"610\"\>/) {
			$flagTopic = 1;
			next;
		}


		# get pages
		if ($flagPages && /(.[^\&]*)/) {
			$pages = $1;
			$flagPages = 0;
		}

		if (/Pages:\&nbsp\;/) {
			$flagPages = 1;
		}

		# get Keywords
		while (/changeKeyword\(\'(.[^\)]*)\)\" class\=\"pageLinkNormal\"\>\"(.[^\"]*)\"/g) {

			#	carp "got keyword: $2 $1\n";
			$results{'keywords'} .= "<li\><a href\=\"?username\=$FORM{'username'}\&keywords\=\&quot\;$2\&quot\;\" onclick\=\"changeKeyword\(\'$absPath$1\);return(false\)\;\"\>$2<\/a\><\/li\>\n";

		}

		# get Authors
		while (/authorId\=(.[^\']*)\'\)\" class\=\"resultAuthorLink\"\>(.[^<]*)</g) {

			local $id = $1;
			local $name = $2;

			# push @authorId,   $id;
			# $authorName{$id} = $name;

			$authors .= "<a href\=\"$absPath\/AnalystBiography?authorId\=$id\" onclick\=\"openAuthorBio\(\'$absPath\/AnalystBiography?authorId\=$id\'\)\"\>$name<\/a\>, ";

			if ($_ =~ /<br\>/) {
				$flagSummary = 1;
				last;
			}

		}



		# get Summary
		if ($flagSummary == 1) {
			$flagSummary = 2;
			next;
		}

		if ($flagSummary == 2) {

			# how to exit summary
			if (/<br\>/) {

				$flagSummary = 0;
				$summary .= $`;
				$summary =~ s/<(.[^>]*)>//g; # remove tags
				next;
			}

			$summary .= $_;

		}



		# get Browse information
		while (/bn\((.[^\)]*)\)\" class\=\"resultNodeLink\"\>(.[^<]*)</g) {

			# push @browseNode, $1;
			# push @browseName, $2;

			# carp "BROWSE: $2 $1\n$browse\n\n";

	    $browse .= <<EOF;
<a href="$absPath/7_search/Body2Frame.jsp?bc=1&op=15&bop=4&v=0&node=$1&n=$1&simple1=0&archived=0&resultsPerSearch=0" onclick="bn($1); return false;">$2</a>;
EOF

    	$tersebrowse .= <<EOF if (!$tersebrowse);
<a href="$absPath/7_search/Body2Frame.jsp?bc=1&op=15&bop=4&v=0&node=$1&n=$1&simple1=0&archived=0&resultsPerSearch=0" onclick="bn($1); return false;">similar pages</a>
EOF

	   	if ($_ =~ /<br\>/) {
	   		$flagLast = 1;
	   		last;
	    }

	  }

	} # end foreach

}

1; # return true

