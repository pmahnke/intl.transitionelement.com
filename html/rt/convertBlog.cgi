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

    if ($ENV{'CONTENT_LENGTH'}) {
	read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});
	@pairs = split(/&/, $buffer);
    } else {
	@pairs = split(/&/, $ENV{'QUERY_STRING'});
    }


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

  $FORM{'input'} =~ s/^\d{5}//;
  $FORM{'input'} =~ s/CTA - \[\]\(\)//;

  
  # remove link to press release
  my $richlink ="";
  if ($FORM{'input'} =~ /https:\/\/www.richmond.gov.uk\/\/news\/(.*)/) {
      $richlink = $&;
      $FORM{'input'} =~ s/$richlink//;
  }

  $output = $FORM{'input'};

  my $image = $1 if ($output =~ /img src="(.[^"]*)"/);
  my $imagefull = $& if ($output =~/<img(.[^>]*?)>/);
  
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
  
  if ($imagefull) {
      $preoutput =~ s/$imagefull//;
      $imagefull =~ s/alt=""//;
  }
  $preoutput =~ s/\&amp\;/\&/g;
  $preoutput =~ s/\&/\&amp\;/g;
  $preoutput =~ s/</&lt\;/g;
  $preoutput =~ s/>/&gt\;/g;
  $preoutput =~ s/\n/\n\n/g;
  $preoutput =~ s/\n\n\n/\n\n/g;
  $preoutput =~ s/\n\n\n/\n\n/g;
  $preoutput =~ s/- (.[^\n]*)\n\n- /- $1\n- /g;
  
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
  $fCite_MP = "checked=\"checked\"" if ($FORM{'cite_MP'});
  $fCite_Martyn = "checked=\"checked\"" if ($FORM{'cite_Martyn'});

  my $filename = $FORM{'title'};
  $filename = "lbrut-".$filename if ($FORM{'cite'});
  $filename = "mp-".$filename if ($FORM{'cite_MP'});
  $filename =~ tr/[A-Z]/[a-z]/;
  $filename =~ s/( |'|"|:|,)/-/g;
  $filename =~ s/----/-/g;
  $filename =~ s/---/-/g;
  $filename =~ s/--/-/g;

  my $excerpt = "";
  my @excerpt = (split /\n/, $preoutput);
  foreach (@excerpt) { 
      next if(!$_);
      $excerpt=$_;
      last if ($excerpt);
  }

  
      # date logic for yaml
      my $d = qq |-d '$FORM{'date'} 10:00:00'| if ($FORM{'date'});

      # date
      my $date = `date $d +'%Y-%m-%d'`;
      chop($date);

      # yaml date
      my $slash_date = `date $d +'/archives/%Y/%m/$filename.html'`;
      chop($slash_date);

      my $long_date = `date $d +'%Y-%m-%d-$filename'`;
      chop($long_date);

      my $rfc_date = `date $d +'%F %T'`;
      chop($rfc_date);

      my $pr_date = `date $d +'%-d %B %Y'`;
  chop($pr_date);

  # stmg my $cat = qq~around_town|news|editorial~;
  my $cat = qq~travel|culture|life in the UK|on technology|about|of interest|on food & drink~;
  my $pr = "";
  if ($FORM{'cite'}) {
      $cat = qq~news|around_town~;
      $pr = qq|<cite>-- from a Richmond Council press release - $pr_date</cite>|;
      $pr = qq|<cite>-- from a [Richmond Council press release - $pr_date]($richlink)</cite>| if ($richlink);
      $pr =~ s/\/\/news/\/news/g;

  } elsif ($FORM{'cite_MP'}) {
      $cat = qq~news~;
      $pr = qq|<cite>-- from a Munira Wilson, MP for Twickenham press release - $pr_date</cite>|;
  } elsif ($FORM{'cite_Martyn'}) {
      $cat = qq~around_town~;
      $pr = qq|<cite>-- from Martyn Day</cite>|;
  }
  
  my $yaml =  qq~---
layout: post
title: "$FORM{'title'}"
permalink: $slash_date
commentfile: $long_date
category: $cat
date: $rfc_date
image: "$image"
excerpt: |
    $excerpt
---
~;


      $out = qq~
$docType
<title>convertText - $ENV{'REMOTE_ADDR'}</title>
  <link rel="stylesheet" type="text/css" media="screen" href="https://assets.ubuntu.com/v1/vanilla-framework-version-2.19.3.min.css">
</head>
<body>
    <div class="wrapper u-no-margin--top">
      <div id="main-content" class="inner-wrapper">
        <section class="p-strip--light">
	  <div class="row">
            <div class="col-8">
              <h1>Convert Text</h1>
              <h2>Output</h2>
              <div>
<pre>
$yaml
$output
$pr
</pre>
              </div>
            </div>
	  </div>
	</section>

        <section class="p-strip">
          <div class="row">
	    <div class="col-8">
	    <form method="post" enctype="application/x-www-form-urlencoded">

	  <textarea rows="10" cols="80">
$yaml
$imagefull

$preoutput
$pr
	  </textarea>

	  <label>
	  <h2 id="inputh">Input</h2>
	  </label>
	  <textarea labeledby="inputh" id="input" name="input" rows="15" cols="80">$FORM{'input'}</textarea></p>

	  <label for="flavor">format</label>
	  <select id="flavor" name="flavor">$selFlavor</select> 

	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelT" name="textile" value="on" $fT/>
	  <span class="p-checkbox__label" id="checkboxLabelT">Textile <a href="/rt/mtmanual_textile2.html" target="_blank">?</a></span>
	  </label>
	  
	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelM" name="markdown" value="on" $fM/>
	  <span class="p-checkbox__label" id="checkboxLabelM">Markdown</span>
	  </label>

	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelC" name="clean" value="on" $fC/> 
	  <span class="p-checkbox__label" id="checkboxLabelC">Clean</span>
	  </label>
	  
	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelS" name="smarty" value="on" $fS/> 
	  <span class="p-checkbox__label" id="checkboxLabelS">Smarty</span>
	  </label>
	  
	  <!--<label class="p-checkbox">
	  <input type="text" name="noHang" value="$FORM{'noHang'}" />
	  <span class="p-checkbox__label" id="checkboxLabel0">hang <em>0 or nothing for no hang</em></span>
	  </label>-->
	  
	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelH" name="html2textile" value="on" $fH />
	  <span class="p-checkbox__label" id="checkboxLabelH">html 2 textile</span>
	  </label>
	  
	  <label for="title">title<label>
	  <input type="text" id="title" name="title" value="$FORM{'title'}" />

	  <label for="date">date</label>
	  <input type="text" id="date" name="date" value="$date" placeholder="$date" />
	  
	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelCite" name="cite" value="on" $fCite />
	  <span class="p-checkbox__label" id="checkboxLabelCite">lbrute cite?</span>
	  </label>
	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelCite_MP" name="cite_MP" value="on" $fCite_MP />
	  <span class="p-checkbox__label" id="checkboxLabelCite_MP">MP cite?</span>
	  </label>
	  <label class="p-checkbox">
	  <input type="checkbox" class="p-checkbox__input" labelledby="checkboxLabelCite_Martyn" name="cite_Martyn" value="on" $fCite_Martyn />
	  <span class="p-checkbox__label" id="checkboxLabelCite_Martyn">Martyn Day cite?</span>
	  </label>
	  
	  <input class="p-button--positive" type="submit" />
	  
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
</section>
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
	  <li> title: <input type="text" name="title" value="$FORM{'title'}" /></li>
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
