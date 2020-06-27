#!/usr/bin/perl

# test text converter
use utf8::all;
use Encode qw(decode encode);
use Text::Textile;
use URI::Escape;
use Markdent::Simple::Document;

binmode(STDOUT, ":utf8");          #treat as if it is UTF-8
binmode(STDIN, ":encoding(utf8)"); #actually check if it is UTF-8

require ("/home/gartner/html/rt/common.pl");
require ("/home/gartner/html/rt/SmartyPants.pl");
require ("/home/gartner/html/rt/html2textile.pl");
require ("/home/stmargarets/cgi-bin/common_text.pl");


##############################################################
# Variables


##############################################################
if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {


  read(STDIN,$buffer,$ENV{CONTENT_LENGTH});

  @pairs = split(/&/, $buffer);
  foreach $pair (@pairs) {

    ($name, $value) = split(/=/, $pair);

    $msg = "<br />raw: $value ".Encode::is_utf8($value) if ($name eq "input");
    $value = decode("utf-8",uri_unescape($value));
    $msg .= "<br />decode: $value ".Encode::is_utf8($value) if ($name eq "input");
    $FORM{$name} = &urldecode($value);
    $msg .= "<br />urldecode: $value ".Encode::is_utf8($value) if ($name eq "input");

  }

  &getSelect;
  &processText;

} else {

  $FORM{'locale'} = "emea";
  $FORM{'charset'} = "UTF-8";
  $FORM{'flavor'} = "xhtml1";
  &getSelect;
  &processText; #printInitialForm;
  exit;

}


exit;

################################################################################
sub urlencode {
  my $s = $_[0];
  $s =~ s/ /+/g;
  $s =~ s/([^A-Za-z0-9\+-])/sprintf("%%%02X", ord($1))/seg;
  return $s;
}

################################################################################
sub urldecode {
  my $s = $_[0];
  $msg .= "<br />in sub $_[0]";
  $s =~ s/\%([A-Fa-f0-9]{2})/pack('C', hex($1))/seg;
  $s =~ s/\+/ /g;
  return $s;
}


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
    if ($FORM{'markdown'}) {
      $output = &clean4markdown($output);
      my $mds  = Markdent::Simple::Document->new();
      $output = $mds->markdown_to_html(
        title    => 'My Document',
        markdown => $output,
        dialect => 'github'
        );
      }
      $output = &clean4markdown($output)             if ($FORM{'clean'});
      $output = &SmartyPants ($output, 1)            if ($FORM{'smart'});
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

      $fC = "checked=\"checked\"" if ($FORM{'clean'});
      $fM = "checked=\"checked\"" if ($FORM{'markdown'});
      $fS = "checked=\"checked\"" if ($FORM{'smarty'});
      $fT = "checked=\"checked\"" if ($FORM{'textile'});
      $fH = "checked=\"checked\"" if ($FORM{'html2textile'});
      $fCite = "checked=\"checked\"" if ($FORM{'cite'});


      # date logic for yaml
      my $d = qq |-d='$FORM{'date'}'| if ($FORM{'date'});

      # date
      my $date = `date $d +'%Y-%m-%d'`;
      chop($date);

      # yaml date
      my $slash_date = `date $d +'/archives/%Y/%m/filename.html'`;
      chop($slash_date);

      my $long_date = `date $d +'%Y-%m-%d-filename'`;
      chop($long_date);

      my $rfc_date = `date $d +'%F %T'`;
      chop($rfc_date);

      my $pr_date = `date $d +'%-d %B %Y'`;
      chop($pr_date);

      my $yaml =  qq~---
layout: post
title: ""
permalink: $slash_date
commentfile: $long_date
category: news|around_town|editorial
date: $rfc_date
image: ""
excerpt: |

---
~;

    my $pr = qq|<cite>-- from a Richmond Council press release - $pr_date</cite>| if ($FORM{'cite'});



      $out = qq~
$docType
<title>convertText - $ENV{'REMOTE_ADDR'}</title>
<link rel="stylesheet" href="https://mahnke.net/css/blueprint/blueprint/screen.css" type="text/css" media="screen, projection">
<link rel="stylesheet" href="https://mahnke.net/css/blueprint/blueprint/print.css" type="text/css" media="print">
<!--[if IE]><link rel="stylesheet" href="https://mahnke.net/css/blueprint/blueprint/ie.css" type="text/css" media="screen, projection"><![endif]-->
</head>
<body>
  <div class="container" >
  <div id="content" class="span-23 last">

  <h1>Convert Text</h1>
  <h2>Output</h2>
  <div>
  $yaml
  $output
  $cite
  </div>

  <form method="post" enctype="application/x-www-form-urlencoded">

  <p>
  <textarea rows="10" cols="80">
  $preoutput
  </textarea></p>

  <h2>Input</h2>
  <p><textarea name="input" rows="15" cols="80">$FORM{'input'}</textarea></p>

  <p>
  <ul>
  <li> Textile: <input type="checkbox" name="textile" value="on" $fT/> <a href="/rt/mtmanual_textile2.html" target="_blank">?</a> format: <select name="flavor">$selFlavor</select> </li>
  <li> Markdown: <input type="checkbox" name="markdown" value="on" $fM/> </li>
  <li> Clean: <input type="checkbox" name="clean" value="on" $fC/> </li>
  <li> Smarty: <input type="checkbox" name="smarty" value="on" $fS/> </li>
  <li> Hang: <input type="text" name="noHang" value="$FORM{'noHang'}" /> <em>0 or nothing for no hang</em></li>
  <li> html 2 textile: <input type="checkbox" name="html2textile" value="on" $fH /></li>
  <li> date: <input type="text" name="date" value="$date" placeholder="$date" /></li>
  <li> lbrut cite?: <input type="checkbox" name="cite" value="on" $fCite /></li>
  </ul>
  </p>

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
      ~;

      binmode STDOUT, ":utf8";
      print "Content-type: text/html; charset=utf-8\n\n$out\n";


}

################################################################################
sub printInitialForm {

  # date
  my $date = `date $d +'%Y-%m-%d'`;
  chop($date);


  my $out = qq~
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
      <ul>
        <li>Textile: <input type="checkbox" name="textile" value="on" /> <a href="/rt/mtmanual_textile2.html" target="_blank">?</a> format: <select name="flavor">$selFlavor</select> </li
        <li> Markdown: <input type="checkbox" name="markdown" value="on" /> </li>
        <li> Clean: <input type="checkbox" name="clean" value="on" /> </li>
        <li> Smarty: <input type="checkbox" name="smarty" value="on" /> </li>
        <!-- <li> Replace Chars: <input type="checkbox" name="chars" value="on" /> </li> -->
        <li> Hang: <input type="text" name="noHang" /> <em>0 or nothing for no hang</em> </li>
        <!-- <li> Acronyms: <input type="checkbox" name="acronym" value="on" /> <em>Gartner Acronyms</em></li>
        <li> UI Translate: <input type="checkbox" name="ui" value="on" $fU /> from: <select name="from">$select to: <select name="to">$select</li>-->
        <li> date: <input type="text" name="date" value="$date" placeholder="$date" /></li>
        <li> lbrut cite?: <input type="checkbox" name="cite" value="on" $fCite /></li>
      </ul>

      <p><input type="submit" /></p>

    </form>
  </body>
</html>
  ~;
  binmode STDOUT, ":utf8";
  print "Content-type: text/html; charset=utf-8\n\n$out\n";

}


################################################################################
sub getDocType {

  $docType= qq|
<!doctype html>

<html lang="en">
  <head>
    <meta charset="UTF-8" />

  |;

}


################################################################################
sub getSelect {


  if ($FORM{'flavor'} eq "xhtml1") {
    $selX1 = "selected\=\"selected\"";
  } elsif ($FORM{'flavor'} eq "xhtml1.1") {
    $selX11 = "selected\=\"selected\"";
  } elsif ($FORM{'flavor'} eq "xhtml2") {
    $selX2 = "selected\=\"selected\"";
  } else {
    $selH = "selected\=\"selected\"";
  }


  $selFlavor = qq|
  <option value="xhtml1" $selX1>XHTML 1.0</option>
  <option value="xhtml1.1" $selX11>XHTML 1.1</option>
  <option value="html/css" $selH>HTML/CSS</option>
  <option value="html" $selHC>HTML</option>
  |;


}
