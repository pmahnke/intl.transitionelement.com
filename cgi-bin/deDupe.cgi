#!/usr/local/bin/perl

use CGI_Lite;

# Variables



###############################################################
# was something POSTED
if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {

    # something submitted
    &parsePage;


    if ($FORM{'excelFile'}) {
	&printExcel;
	exit;

    } else {
	&results;
	exit;
    }

} else {

    # nothing submitted
    &printStartPage;
    exit;
}



#################################################################
sub parsePage {

    $cgi = new CGI_Lite;
    $cgi->add_timestamp(0);
    $cgi->set_directory ('/home/gartner/html/kelly/');
    %FORM = $cgi->parse_form_data;
    $FORM{'masterEMAILcol'} = $FORM{'masterEMAILcol'} - 1;
    $FORM{'failedEMAILcol'} = $FORM{'failedEMAILcol'} - 1;
    $FORM{'masterMSGcol'} = $FORM{'masterMSGcol'} - 1;
    $FORM{'failedMSGcol'} = $FORM{'failedMSGcol'} - 1;
}

sub printStartPage {

    print <<EndofHeader;
Content-type: text/html;

<HTML>
<BODY>
<h1>INPUT</h1>
<h4>please upload tab delimited files, this will also dedupe</h4>
<form method=post enctype="multipart/form-data">
<table width=600>
 <tr>
  <td>master file</td>
  <td><input type=file size=30 name=masterFile></td>
 </tr>
 <tr>
  <td>master file's email column</td>
  <td><input type=text name=masterEMAILcol size=2></td>
 </tr>
 <tr>
  <td>master file's message column</td>
  <td><input type=text name=masterMSGcol size=2></td>
 </tr>

 <tr>
  <td>failure file</td>
  <td><input type=file size=30 name=failedFile></td>
 </tr>
 <tr>
  <td>failure file's email column</td>
  <td><input type=text name=failedEMAILcol size=2></td>
 </tr>
 <tr>
  <td>failure file's message column</td>
  <td><input type=text name=failedMSGcol size=2></td>
 </tr>

 <tr>
  <td>timestamp</td>
  <td><input type=text name=ts size=10></td>
 </tr>

 
 <tr>
  <td></td>
  <td><input type=submit></td>
 </tr>
</table>
<p>
</body>
</html>

EndofHeader

    exit;

}


sub results {
    

    # read removed email file
    %DEL = &openFile($FORM{'failedFile'}, $FORM{'failedEMAILcol'}, $FORM{'failedMSGcol'}, 'failed');

    # read master email list
    %MASTER = &openFile($FORM{'masterFile'}, $FORM{'masterEMAILcol'}, $FORM{'masterMSGcol'}, 'master');

    foreach $key (keys %MASTER) {
    
	if ($DEL{$key}) {
	    
	    $msg .= "found dupe $key master $master{$key} failed $failed{$key}";
	    if ($master{$key} =~ /failed/i && $failed{$key} eq "Email Failed") {
		
		# person already failed once and failed again
		$msg .= " \- failed again ";
		$deDuped{$key} = "FAILED TWICE\tfailed x 2 $FORM{'ts'}\t".$MASTER{$key};
		delete $MASTER{$key};
		
	    } elsif ($master{$key} !~ /failed/i && $failed{$key} eq "Email Failed") {
		
		# person already failed once and failed again
		$msg .= " \- failed again ";
		$failedMASTER{$key} = "FAILED ONCE\tfailed x 1 $FORM{'ts'}\t".$MASTER{$key};
		delete $MASTER{$key};
		
	    } elsif ($failed{$key} eq "User Has Unsubscribed") {
		
		# user unsubscribed
		$msg .= " \- user unsubscribed ";
		$deDuped{$key} = "UNSUB\tunsub $FORM{'ts'}\t".$MASTER{$key};
		delete $MASTER{$key};
		
	    }
	    
	    # remove any removed names from the additions list
	    #$deDuped{$key} = $MASTER{$key};
	    #$delete $MASTER{$key};
	    #$deleteCount++;

	    $msg .= " <br>\n";
	}
	
    }
    
    # now should be clean

    ###################################################
    # save good file
    $goodOutputFile = "/home/gartner/html/kelly/good.txt";
    $goodHTMLFile = "/kelly/good.txt";
    open (GOODOUTPUT, ">$goodOutputFile") || die "can't write good file: $goodOutputFile\n\n";
    foreach $key (sort keys %MASTER) {
	print GOODOUTPUT "GOOD\t\t$MASTER{$key}\n";
	$totalCount++;
    }
    foreach $key (sort keys %failedMASTER) {
	print GOODOUTPUT "$failedMASTER{$key}\n";
	$totalCount++;
    }

    close (GOODOUTPUT);

    ################################################### 
    # save bad file
    $badOutputFile = "/home/gartner/html/kelly/bad.txt";
    $badHTMLFile = "/kelly/bad.txt";
    open (BADOUTPUT, ">$badOutputFile") || die "can't write bad file: $badOutputFile\n\n";
    foreach $key (sort keys %deDuped) {
	$deDuped{$key} =~ s/\n//g;
#	$DEL{$key} =~ s/\n//g;
	print BADOUTPUT "$deDuped{$key}\n";   # \t$DEL{$key}\n";
	$badCount++;
    }
    close (BADOUTPUT);

    $msg .= "\nDeleted List $deleteCount for a total of $totalCount good. <br\> \n\n Done. <p\>\n\n";

    print <<EndofHeader;
Content-type: text/html

<HTML>
<head>


</head>
<BODY>
<h1>RESULTS</h1>

<table width=600>
 <tr>
  <td>good file</td>
  <td><a href="?excelFile=$goodOutputFile&fn=good.xls" target="good">open tab delimited file</td>
 </tr>
 <tr>
  <td>bad file</td>
  <td><a href="?excelFile=$badOutputFile&fn=bad.xls" target="bad">open tab delimited file</td>
 </tr>
</table>
<p>
<h4>messages</h4>
$msg

</body>
</html>

EndofHeader

    exit;
}

sub printExcel {

    open (FILE, "$FORM{'excelFile'}");
    while (<FILE>) {
	$listing .= $_;
    }
    close (FILE);

    print <<EndofHTML;
Content-Type: bad/type
Content-Disposition: attachment; filename=$FORM{'fn'}

$listing

EndofHTML
}

#################################################################################
sub openFile {

    # pass it 2 variables, filename and column of email address

    local $file = "/home/gartner/html/kelly/".$_[0];
    open (FILE, "$file") || die "\n\Can't open file: $file\n\n";
    
    while (<FILE>) {

	chop();
	
	s/\n//g;
	s/\r//g;
	
	local @line = split (/\t/);
	
	local $email = $line[$_[1]];
	local $status = $line[$_[2]];

#	$msg .= "$_[3] \- $status <br \>";

	local $c = 0;
	local $line = "";
	local $bit = "";
	foreach $bit (@line) {
	    next if ($c < 2);
	    $msg .= "$bit ";
	    $line .= "\t$bit";
	    $c++;
	}
	next if (!$email);
	$msg .= "line $line<br\>";

	
	$email =~ tr/[A-Z]/[a-z]/; # make emails all lowercase
	$email =~ s/\'//g; # remove '
	$hash{$email} = $_;
	local $sts = $_[3];
	$$sts{$email} = $status;

	$fileCount++;
		
    }
    close(FILE);
    $msg .= "$fileCount lines in $_[0] <br\>\n";
    return(%hash);
}
