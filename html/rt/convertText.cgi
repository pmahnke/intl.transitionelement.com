#!/usr/local/bin/perl

# test text converter

use Text::Textile;
use CGI::Lite;

require ("/home/gartner/html/rt/common.pl");
#require ("/home/gartner/html/rt/replaceChars.pl");
require ("/home/gartner/html/rt/SmartyPants.pl");
#require ("/home/gartner/cgi-bin/Textile.pm");
#require ("/home/gartner/html/rt/uiStrings.pl");
#require ("/home/gartner/html/rt/acronym.pl");
require ("/home/gartner/html/rt/html2textile.pl");
require ("/home/stmargarets/cgi-bin/common_text.pl");


##############################################################
# Variables


##############################################################
if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {
    
    
    sub null {
    
    # old school post!
    
    local $buffer = "";
    read(STDIN,$buffer,$ENV{CONTENT_LENGTH});
    
    @pairs = split(/&/, $buffer);
    foreach $pair (@pairs) {

	($name, $value) = split(/=/, $pair);
	$value =~ s/\+/ /g; # spaces
	
	$value =~ s/%0D%0A/\n/g; # newlines?
	
	# $value =~ s/\&lt\;/\</g; # less thans
	# $value =~ s/\&amp\;/\&/g; # ampersans
	$value =~ s/%26(.[^%]*)%3B/\&amp\;$1\;/g; # nbsp
	$value =~ s/%(..)/pack("c",hex($1))/ge; # rest

	$value =~ s/\302\240//g;
	$value =~ s/\302\243/{L-}/g;

	$value =~ s/\305™/&#x159;/g;
	$value =~ s/\303\240/{a'}/g;

	$value =~ s/\342\200[\230\231]/'/g;
	$value =~ s/\342\200\246/.../g;
	$value =~ s/\342\200\223/-/g;
	$value =~ s/\342\200\224/--/g;
	$value =~ s/\342\200[\234\235]/"/g;
	
	$FORM{$name} = $value;
    }
    } # end sub null
    
    # something submitted
    $cgi = new CGI::Lite;
    %FORM = $cgi->parse_form_data;
    
    &getSelect;
    &processText;
	
} else {

	$FORM{'locale'} = "emea";
	$FORM{'charset'} = "utf-8";
	$FORM{'flavor'} = "xhtml1";
	&getSelect;
	&processText; #printInitialForm;
	exit;
	
}


exit;



################################################################################
sub processText {

    &getDocType;
    
    $output = $FORM{'input'};

    if ($FORM{'textile'}) {

		$output = &clean4textile($output); # clean funny characters
	
		$textile = new Text::Textile (
				      charset => $FORM{'charset'},
				      flavor => $FORM{'flavor'}
				      );
		$output  = $textile->process($output);
	
	}
    
    $output = &SmartyPants ($output, 1)            if ($FORM{'smarty'});
    $output = &noHang($output, $FORM{'noHang'})    if ($FORM{'noHang'});
    $output = &html2textile($output)               if ($FORM{'html2textile'});
    
    $preoutput = $output;
    
    $preoutput =~ s/\&amp\;/\&/g;
    $preoutput =~ s/\&/\&amp\;/g;
    $preoutput =~ s/</&lt\;/g;
    $preoutput =~ s/>/&gt\;/g;
    

    $preFull = $docType."<title>add title<\/title\>\n\n<\/head\>\n\n<body\>\n\n".$output."\n<\/body\>\n<\/html\>\n";
    $preFull =~ s/\&amp\;/\&/g;
    $preFull =~ s/\&/\&amp\;/g;
    $preFull =~ s/</&lt\;/g;
    $preFull =~ s/>/&gt\;/g;


    #$output =~ s/\n/<br \/\>\n/g;
    $output =~ s/\&amp\;/\&/g;

    $fS = "checked=\"checked\"" if ($FORM{'smarty'});
    $fT = "checked=\"checked\"" if ($FORM{'textile'});
    $fH = "checked=\"checked\"" if ($FORM{'html2textile'});   
 
    print <<EndofHTML;
Content-type:  text/html

$docType
<title>convertText - $ENV{'REMOTE_ADDR'}</title>
<link rel="stylesheet" href="http://mahnke.net/css/blueprint/blueprint/screen.css" type="text/css" media="screen, projection"> 
<link rel="stylesheet" href="http://mahnke.net/css/blueprint/blueprint/print.css" type="text/css" media="print">    
<!--[if IE]><link rel="stylesheet" href="http://mahnke.net/css/blueprint/blueprint/ie.css" type="text/css" media="screen, projection"><![endif]--> 
 
</head>
<body>
<div class="container" >
<div id="content" class="span-23 last"> 

<h1>Convert Text</h1>
<h2>Output</h2>
<p>
$output
</p>

<form method="post" enctype="application/x-www-form-urlencoded">

<p>
<textarea rows="10" cols="80">
$preoutput
</textarea></p>

<h2>Input</h2>
<p><textarea name="input" rows="15" cols="80">$FORM{'input'}</textarea></p>

<p>
 <ul>
  <li> Textile: <input type="checkbox" name="textile" value="on" $fT/> <a href="/rt/mtmanual_textile2.html" target="_blank">?</a> char set <select name="charset">$selChar</select> format: <select name="flavor">$selFlavor</select> </li>
  <li> Smarty: <input type="checkbox" name="smarty" value="on" $fS/> </li>
  <li> Hang: <input type="text" name="noHang" value="$FORM{'noHang'}" /> <em>0 or nothing for no hang</em></li>
  <li> html 2 textile: <input type="checkbox" name="html2textile" value="on" $fH /></li>
 </ul>
</p>
<p>charset: <input type="hidden" name="_charset_" />$FORM{'_charset_'} $decoder</p>

<p><input type="submit" /></p>

</form>

<h3>code with doctype</h3>
<pre>
$preFull
</pre>


<h3>messages</h3>
<p>$msg</p>
<h3>buffer</h3>
<p>$buffer</p>

</div> 
</div> 
</body>
</html>

EndofHTML

}

################################################################################
sub printInitialForm {
    

    print <<EndofHTML;
Content-type:  text/html

$docType
<title>convertText - $ENV{'REMOTE_ADDR'}</title>
<style type="text/css">
h1,h2,h3,ol,li,body {	font-family: Verdana, Arial, Sans;	}
h1	{		font-size: 14pt;	}
h2	{		font-size: 12pt; clear:both;	}
h3	{		font-size: 10pt;	}
li,p,td	{		font-size: 9pt;	        }
</style>
</head>
<body>

<h1>Convert Text</h1>

<form method="post" enctype="application/x-www-form-urlencoded">

<p><textarea name="input" rows="15" cols="80"></textarea></p>

<p>
 <ul>
  <li>Textile: <input type="checkbox" name="textile" value="on" /> <a href="/rt/mtmanual_textile2.html" target="_blank">?</a> char set <select name="charset">$selChar</select> format: <select name="flavor">$selFlavor</select> </li>
  <li> Smarty: <input type="checkbox" name="smarty" value="on" /> </li>
  <!-- <li> Replace Chars: <input type="checkbox" name="chars" value="on" /> </li> -->
  <li> Hang: <input type="text" name="noHang" /> <em>0 or nothing for no hang</em> </li>
  <!-- <li> Acronyms: <input type="checkbox" name="acronym" value="on" /> <em>Gartner Acronyms</em></li>
  <li> UI Translate: <input type="checkbox" name="ui" value="on" $fU /> from: <select name="from">$select to: <select name="to">$select</li>-->
 </ul>
</p>

<p><input type="submit" /></p>

</form>
</body>
</html>

EndofHTML
}


################################################################################
sub getDocType {

    if ($FORM{'charset'} eq "iso-8859-1") {
	$CHAR = "iso-8859-1";
    } else {
	$CHAR = "utf-8";
    }

    if ($FORM{'flavor'} eq "xhtml1") {

	$docType=<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<?xml version="1.0" encoding="$CHAR"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=$FORM{'charset'}" ></meta>

EOF
    } elsif ($FORM{'flavor'} eq "xhtml1.1") {

	$docType =<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml11.dtd">
<?xml version="1.0" encoding="$CHAR"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=$FORM{'charset'}"></meta>

EOF

    } elsif ($FORM{'flavor'} eq "xhtml2") {

	$docType=<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 2.0//EN"
        "http://www.w3.org/TR/xhtml2/DTD/xhtml2.dtd">

<?xml version="1.0" encoding="$CHAR"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=$FORM{'charset'}"></meta>

EOF

    } else {

	$docType=<<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=$FORM{'charset'}">

EOF

    }

}


################################################################################
sub getSelect {


    if ($FORM{'charset'} eq "utf-8") {
	$selUTF8 = "selected\=\"selected\"";
    } else {
	$selISO = "selected\=\"selected\"";
    }

    if ($FORM{'flavor'} eq "xhtml1") {
	$selX1 = "selected\=\"selected\"";
    } elsif ($FORM{'flavor'} eq "xhtml1.1") {
	$selX11 = "selected\=\"selected\"";
    } elsif ($FORM{'flavor'} eq "xhtml2") {
	$selX2 = "selected\=\"selected\"";
    } else {
	$selH = "selected\=\"selected\"";
    }


    $selChar =<<EOF;
  <option value="utf-8" $selUTF8>utf-8</option>
  <option value="iso-8859-1" $selISO>iso-8859-1</option>
EOF

    $selFlavor =<<EOF;
  <option value="xhtml1" $selX1>XHTML 1.0</option>
  <option value="xhtml1.1" $selX11>XHTML 1.1</option>
  <option value="html/css" $selH>HTML/CSS</option>
  <option value="html" $selHC>HTML</option>
EOF

#   <option value="xhtml2" $selX2>XHTML 2</option> NOT CURRENTLY SUPPORTED


}

