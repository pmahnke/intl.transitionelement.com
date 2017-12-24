#!/usr/local/bin/perl

# getNODocument3.pl has a differnt way to handle authors.... than getNODocument.pl

#require ("/home/gartner/cgi-bin/glogin_regionals.pl");
require ("/home/gartner/cgi-bin/gNOlogin2.pl");


################################################
sub getResearchDetail {

    # Variables
    local $text = "";
    local $Output = "";

    # action
    local @docDetails = &parseResearchDetailPage(&getGARTNERpage($_[0]));
    return (@docDetails);

}

################################################
sub parseResearchDetailPage {


    # local @output = split (/\>/, $_[0]);
    local @output = split (/\n/, $_[0]);
    local ($title, $pubDate, $summary, $resId, $auth, $authFlag, $body, $bodyFlag, $summaryFlag, $toc, $pages, $tocFlag, $lineNumber, $keywords, $path, $fileName, $fileSize) = "";

    foreach (@output) {

	# $_ .= "\>";

        $_ =~ s/<span CLASS\=hiliteText\>//gi;
        $_ =~ s/<\/span\>//gi;


	while (/<META NAME\=\"(.[^\"]*)\" CONTENT\=\"(.[^\"\>]*)\"\>/gi) {
	    $getNOdocmsg .= "META $1 is $2 <br\>\n";
	}
	# $getNOdocmsg .= "$lineNumber \t $_\n";

	$lineNumber++;

	#Table of Contents

	$tocFlag = 0  if (/Begin Body/i  || /<TABLE WIDTH\=\"100%\" HEIGHT\=\"1\" CELLSPACING\=\"0\" CELLPADDING\=\"0\" BORDER\=\"0\">/ && $tocFlag);
	$tocFlag = 1 if (/begin table of contents/|| /<table BORDER\=0 CELLSPACING\=0 CELLPADDING\=0 WIDTH\=\"650\" \>/);
	$toc .= "$_\n" if ($tocFlag);

	# PRICE
	# <B>Price:</B> US $ 1,495.00
	$price = $1 if (/US+\$(.[^\.]*)\./);
#	$price = $_ if (/<B\>Price\: <\/B\>(.*)/i);

#	$price = $_ if (/Price/);

	# TITLE
	$title = $1 if (/<META NAME\=\"TITLE\" CONTENT\=\"(.[^\"\>]*)\"\>/i);

	# PUBDATE GGPUBDT
	$pubDate = $1 if (/<META NAME\=\"GGPUBDT\" CONTENT\=\"(.[^\"\>]*)\"\>/i);

	# RESID
	$resId   = $1 if (/<META NAME\=\"GGRESID\" CONTENT\=\"(.[^\"\>]*)\"\>/i);

	# NOTE NUMBER
	$noteNumber = $1 if (/<META NAME\=\"GGNOTENUM\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# DOC TYPE
	$docType = $1 if (/<META NAME\=\"GGDOCTYPE\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# GGCONTENT
	$contentType = $1 if (/<META NAME\=\"GGCONTENT\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# GGFOLDER
	$folderType =  $1 if (/<META NAME\=\"GGFOLDER\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# GGGEO
	$geo =  $1 if (/<META NAME\=\"GGGEO\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# GGINDUSTRY
	$industry =  $1 if (/<META NAME\=\"GGINDUSTRY\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# GGINFOTYPE
	$infoType =  $1 if (/<META NAME\=\"GGINFOTYPE\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# GGORGSZ
	$orgInfo =  $1 if (/<META NAME\=\"GGORGSZ\" CONTENT=\"(.[^\"\>]*)\"\>/i);

	# GGDOCCD
	$docCd =  $1 if (/<META NAME\=\"GGDOCCD\" CONTENT=\"(.[^\"\>]*)\"\>/i);



	# KEYWORDS
	$keywords .= " $1" if (/<META NAME\=\"GGINDUSTRY\" CONTENT=\"(.[^\"\>]*)\"\>/i
			       || /<META NAME\=\"GGPROVFOC\" CONTENT=\"(.[^\"\>]*)\"\>/i
			       );


	# FILENAME, PATH
	# <a class="rightColText" href="/resources/121200/121277/united_kingdom_.pdf">united_kingdom_.pdf</a>
	if (/a class\=\"rightColText\" href\=\"\/resources\/(.[^\"]*)\"\>(.[^<]*)</) {
	    $path     = "\/resources\/".$1;
	    $fileName = $2;
	}

	# FILESIZE
	# <span class="rightColTextPlain"> (26.3KB)</span>
	$fileSize = $1 if (/rightColTextPlain\"\> \((.[^\)]*)\)</);



	# SUMMARY
	#if (/GGSUMMARY/) {
	#    $summary = $1 if (/CONTENT\=\"(.[^\>]*)\>/);
	#    chop ($summary);
	#}

	$summary = $1 if (/<META NAME\=\"GGSUMMARY\" CONTENT\=\"(.*)/i); # catch all... don't know why I needit

	$summary = $1 if (/<META NAME\=\"GGSUMMARY\" CONTENT\=\"(.[^\">]*)\">/i);


	if (/<META NAME\=\"GG PRM SUMMARY\" CONTENT\=\"(.*)/i || $summaryFlag) {

	    if (!$summaryFlag) {
		$summary .= $1;
		$summaryFlag = 1;
	    } else {
		$summary .= $_;
	    }

	    if ($summary =~ /\"\>/) {

		# there is the end tag
		$summaryFlag = 0;
		$summary =~ s/\"\>//;

	    }
	}

	# PAGES
	$pages .= $1 if (/<B\>Pages\: <\/B\>(.*)/);

	# AUTHOR
	if (/<TD class\=\"authors/i) {

	    $authFlag = 1;
	    next;

	} elsif ($authFlag) {

	    if (/<\/td\>/i) { # look for ending </td>

		$authFlag = 0;
		$auth =~ s/  //g;
		chop($auth) if (!$multiAuthFlag);
		next;

	    }


	    s/\r//g;
	    s/\n//g;

	    if ($authFlag == 2) {

		# author name on this line
		$auth .= "$_";
		$auth .= " \| " if ($authCount);
		$authFlag = 1;
#		print "\n\nFOUND MULTI LINE AUTHOR NAME $_\n\n";
	    }


	    if (/openBio\(\'\/(AnalystBiography\?authorId\=.*[^<\/A\>])<\/A\>/) {

		$auth .= "<a href\=\"javascript:void\(null\)\" class\=\"linkTextSmall\" onclick\=\"openBio\(\'\/".$1."<\/a\>,  ";
		# $auth .= "$1, ";


	    } elsif (/\'\/AnalystBiography\?authorId\=(.[^\'\)\"\>]*)\'\)\"\>/) {

		# multiLine Author

		$multiAuthFlag = 1;
	$authCount++;

		$auth .= "<a href\=\"javascript:void\(null\)\" class\=\"linkTextSmall\" onclick\=\"openBio\(\'\/AnalystBiography\?authorId\=".$1."\'\)\"\>";
#		print "\n\nFOUND MULTI LINE AUTHOR LINK $1\n\n";
		$authFlag = 2;
	    }

	    next;
	}


	# BODY
	if (/Begin Body/) {

	    $bodyFlag = 1;
	    next;

	} elsif ($bodyFlag) {

	    if (/class\=\"footer\"/) {

		$bodyFlag = 0;
		next;

	    }

	    s/<.[^\>]*\>//g; # remove all HTML tags
	    s/\r//g;
	    s/\n\n/\n/g;

	    $body .= $_;
	}

    }

    if ($multiAuthFlag) {
	$auth =~ s/ \| $//;
	$auth =~ s/ <\/a\>/<\/a\>/gi;
    }

	# clean up summary, from catch all grab
	$summary = substr ($summary, 0, index ($summary, "\">") ) if ($summary =~ /\">/);

    # clean up toc
    $toc = &cleanToc($toc);

	# clean up author
	$auth =~ s/<a(.[^>]*)>//g;
	$auth =~ s/\|/,/g;
	chop($auth);

	# deal with missing contentType
	$contentType = $folderType if (!$contentType);


    # clean up $pubDate
    $pubDate =~ s/\-/ /g;
    $pubDate =~ s/^0//;
    $pubDate =~ s/Jan/January/;
    $pubDate =~ s/Feb/February/;
    $pubDate =~ s/Mar/March/;
    $pubDate =~ s/Apr/April/;
    $pubDate =~ s/Jun/June/;
    $pubDate =~ s/Jul/July/;
    $pubDate =~ s/Aug/August/;
    $pubDate =~ s/Sep/September/;
    $pubDate =~ s/Oct/October/;
    $pubDate =~ s/Nov/November/;
    $pubDate =~ s/Dec/December/;


    $getNODOCmsg .= "getNOdocument3: $title, $pubDate, $summary, $resId, $auth, $body, $noteNumber, $price, $pages\n";
    return ($title, $pubDate, $summary, $resId, $auth, $body, $noteNumber, $toc, $price, $pages, $docType, $contentType, $folderType, $keywords, $path, $fileName, $fileSize, $geo, $industry, $infoType, $orgInfo, $docCd);


}

sub cleanToc {

	local undef @list;
 	local ($t, $tbls, $figs, $ret) = "";
	local $tocType = "";
	local ($inTOC, $inTable, $inFigs) = "";


	push @list, "List of Tables" if (/List of Tables/);

	push @list, $1 if (/<\/a>(List of Figures)<\/TD>/);

	# gets the TOC and TABLES from DPRO
	while($_[0] =~ /(<P CLASS=\"dv_docHead1\">|<SPAN CLASS=\"dv_doc1Level\">|<P CLASS=\"dv_doc1level\">)(.[^<\/]*)/gi ) {
		push @list, $2;
		$getNOdocmsg .= "toc dpro\t$1\t$2\n";
		$tocType = 0;
	}



	# gets the TABLE OF CONTENTS section in the table type of form
	if ($_[0] =~ /Table of Contents<\/td><\/tr><tr> <td>(.*)<\/td>/i) {

		local $toclist = $1;

		$toclist = substr ($toclist, 0, index ($toclist, "<\/td>") - 1);
		$toclist =~ s/<BR> (\w)/<\/li>\n    <li>$1/gi;
		$toclist =~ s/<BR> </<\/li>\n </gi;
		$toclist =~ s/<UL> (\w)/<ul>\n    <li>$1/gi;
		$toclist =~ s/<\/UL>/<\/ul>\n    <li>/gi;

		$toclist = substr ($toclist, 0, length($toclist) - 4);

		# $t = "<div class\=\"toc\" alt\=\"table type\">\n    <p> Table of Contents </p>\n    <ul>\n    $toclist\n</ul>\n\n";
		$t = "<div class\=\"toc\" alt\=\"table type\">\n    <p> Table of Contents </p>\n    $toclist\n\n";

		$getNOdocmsg .= "toc table\t$1\t$2\t$3\n";

		$tocType = 1;

	}


	# get's all 3 sections in the <P type of form
	while ($_[0] =~ /(<P CLASS=\"header3\">|<P>)(.[^<\/P>]*)/g) {

		push @list, $2;

		$getNOdocmsg .= "toc para\t$1\t$2\n";

		$tocType = 0;

	}

	# gets the LIST OF TABLES and LIST OF FIGURES in the table type of form
	while ($_[0] =~ /<td(.[^>]*)>(.[^<]*)<\/td>.<td>(.[^<]*)<\/td>/gi) {

		push @list, "$2 $3";

		$getNOdocmsg .= "toc table\t$1\t$2\t$3\n";

		$tocType = 1;

	}




	foreach (@list) {

		$inTOC = "t" if (!$inTOC && $tocType);

		$inTable = 1 if (/Table/ && !$inTable && $tocType);
		$inFigs = 1 if (/Figure/ && !$inFigs && $tocType);

		# put Headings in and divisions between
		if (/Table of Contents/) {
			$inTOC = "t";
			$$inTOC .= "<div class\=\"toc\">\n    <p> Table of Contents </p>\n    <ul>\n";
			next; # if (!$inTOC);
		} elsif (/List of Tables/ || $inTable == 1) {
			$$inTOC .= "</ul>\n\n";
			$inTOC = "tbls";
			$$inTOC .= "    </ul>\n</div>\n\n\n<div class\=\"listoftables\">\n    <p> List of Tables </p>\n    <ul>\n";
			$inTable = 2;
			next if (!$inTable);
		} elsif (/List of Figures/ || $inFigs == 1) {
			$$inTOC .= "</ul>\n\n";
			$inTOC = "figs";
			$$inTOC .= "    </ul>\n</div>\n\n\n<div class\=\"listoffigs\">\n    <p> List of Figures </p>\n    <ul>\n";
			$inFigs = 2;
			next if (!$inFigs);
		}

		$$inTOC .= "    <li> $_ </li>\n";


	}
	$$inTOC .= "    </ul>\n</div>\n\n";

	$ret = "$t\n\n$tbls\n\n$figs\n\n";
	return($ret);
}

1; # return true




