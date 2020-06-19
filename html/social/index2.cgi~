#!/usr/bin/perl

use CGI::Lite;

my (%F, $script) = "";


#############################################################################
# parse get/post
if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {

    my $cgi = new CGI::Lite;
    %F = $cgi->parse_form_data;

} else {

    # if the user didn't post anything...
    &printForm();
    exit;
}

#############################
# WHAT TO DO
if ($F{'a'} eq "go") {
    &printForm();
} else {
    &printForm();
}

sub printForm {

    $F{'h1'}    = qq |Embracing the open source mandate| if (!$F{'h1'});
    $F{'h4'}    = qq |85% of enterprises have an open source mandate, preference or are exploring| if (!$F{'h4'} && !$F{'h1'});
    $F{'class'} = qq |p-engage-banner--grad| if (!$F{'class'});
    my $selection = qq |<option value="" disabled="disabled" selected="">Select an option</option>|;
    $selection = qq |<option value="$F{'class'}" selected="">$F{'class'}</option>\n<option value="" disabled="disabled"></option>| if ($F{'class'});

    $F{'image'} = qq |https://assets.ubuntu.com/v1/5096c143-451-research-vector-white-logo.svg| if (!$F{'image'});

    $script = qq |
	<script>
	window.onload = function() {
    var ubuntu = document.getElementById("ubuntulogo");
    var img = document.getElementById("logo");
    var neww = 250;
    if (newh >= neww) {
      neww=200;
    }
    var newh = (img.height/img.width * neww);
    |;

    my $canvasFacebook = &makeCanvas('facebook', 1200, 628, 'wide', 'big');
    my $canvasFacebookmobile = &makeCanvas('facebookmobile', 1080, 1080, 'square', 'big');
    my $canvasFacebook916 = &makeCanvas('facebook916', 400, 500, 'tall');
    my $canvasTwitter = &makeCanvas('twitter', 800, 418, 'tall');
    my $canvasTwittersquare = &makeCanvas('twittersquare', 800, 800, 'square');

    $script .= qq |
	};
    </script>
    |;

    
    print qq~Content-type: text/html;

<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" type="text/css" media="screen" href="https://ubuntu.com/static/css/styles.css?v=66d95f5">
  <link rel="shortcut icon" href="https://assets.ubuntu.com/v1/49a1a858-favicon-32x32.png" type="image/x-icon">
  <link rel="apple-touch-icon" href="https://assets.ubuntu.com/v1/17b68252-apple-touch-icon-180x180-precomposed-ubuntu.png">

  <link rel="preload" as="font" type="font/woff2" href="https://assets.ubuntu.com/v1/e8c07df6-Ubuntu-L_W.woff2" crossorigin="">
  <link rel="preload" as="font" type="font/woff2" href="https://assets.ubuntu.com/v1/7f100985-Ubuntu-Th_W.woff2" crossorigin="">
  <link rel="preload" as="font" type="font/woff2" href="https://assets.ubuntu.com/v1/f8097dea-Ubuntu-LI_W.woff2" crossorigin="">
  <link rel="preload" as="font" type="font/woff2" href="https://assets.ubuntu.com/v1/fff37993-Ubuntu-R_W.woff2" crossorigin="">
</head>
<body>

<div class="wrapper u-no-margin--top">
  <div id="main-content" class="inner-wrapper">

    <img id="ubuntulogo" src="https://assets.ubuntu.com/v1/f263d9c4-logo-ubuntu-white.svg" alt="Ubuntu" width="143" height="32" loading="auto" style="display: none;">
    <img id="logo" src="$F{'image'}?w=250" alt="" width="250" loading="auto" style="dispklay: none;">

    <section class="p-strip">
    <div class="u-fixed-width">

    <h4>Facebook &amp; LinkedIn - 1200 x 628</h4>
    $canvasFacebook

    <h4>Facebook mobile - 1080 x 1080</h4>
    $canvasFacebookmobile
    
    <h4>Facebook 9:16 - 400 x 500</h4>
    $canvasFacebook916

    <h4>Twitter wide - 800 x 418</h4>
    $canvasTwitter

    <h4>Twitter square - 800 x 800</h4>
    $canvasTwittersquare

    </div>
  </div>


<section class="p-strip--light">
  <div class="row">
    <div class="col-8">
      <form method="GET">
        <label for="h1">Title</label>
        <input type="text" id="h1" name="h1" value="$F{'h1'}">                                                                                                                                                                                                                                              
        <label for="h4">Sub-heading</label>
        <input type="text" id="h4" name="h4" value="$F{'h4'}">                                       

        <label for="image">Image</label>
        <input type="text" id="image" name="image" value="$F{'image'}">                                       
                                                                                                                                                             
        <label for="class">Background</label>                                                                                                                        
        <select name="class" id="class">
          $selection
          <option>p-engage-banner--dark</option>
          <option>p-engage-banner--grad</option>
          <option>p-engage-banner--k8s</option>
          <option>p-engage-banner--aqua</option>
          <option>p-engage-banner--snapcraft</option>
        </select>                                                                                                                                                                                                                                                                     
        <button class="p-button--positive u-float-right">Go</button>  
      </form>   
     </div>
    </div>
   </section>
</div>
</div>
   $script
  </body>
</html>
    ~;

    return();
}


sub makeCanvas {

    # inputs - 0 - name, 1 - canvas width, 2 - canvas height, 3 - wide or tall, 4 - h1 size
    
    my ($h1, $line) = "";
    my $logox = 0.6 * $_[1];
    my $midy = 0.35 * $_[2];
    $midy =  $midy - 50 if (length($F{'h1'}) > 60 && $_[3] eq 'tall' && $_[0] ne 'facebook916');
    $midy =  $midy - 10 if (length($F{'h1'}) > 40 && $_[0] ne 'facebook916');
    $midy =  $midy + 30 if (length($F{'h1'}) > 40 && $_[3] eq 'square');
    my $height = $midy + 42;
    
    my $leftm = 30; # left margin
    my $h1size = "36px"; # h1 font size
    my $h1lh = 48; # line height
    
    if ($_[4] eq 'big') {
	# make big images have more space;
	$leftm = 100;
	$h1size = "46px";
	$h1lh = 53;
    }
	
    
    my @h1 = split(/ /, $F{'h1'});
    foreach (@h1) { 
	$line .= "$_ ";
	if (length($line) > 18) {
	    $height += $h1lh;
	    $h1 .= qq |ctx$_[0].fillText("$line", $leftm, $height);|;
	    $line = "";
	}
    }
    $height += $h1lh;
    $h1 .= qq |ctx$_[0].fillText("$line", $leftm, $height);| if (length($line) > 0);
    
    my ($h4, %stop, $class) = "";
    $line = "";
    $height += 53;
    my @h4 = split(/ /, $F{'h4'});
    foreach (@h4) { 
	$line .= "$_ ";
	if (length($line) > 25) {
	    $h4 .= qq |ctx$_[0].fillText("$line", $leftm, $height);|;
	    $line = "";
	    $height += 32;
	}
    }
    $h4 .= qq |ctx$_[0].fillText("$line", $leftm, $height);| if (length($line) > 0);

    $stop{'p-engage-banner--grad'}{1} = "#2c001e";
    $stop{'p-engage-banner--grad'}{2} = "#772953";
    $stop{'p-engage-banner--grad'}{3} = "#e95420";

    $stop{'p-engage-banner--dark'}{1} = "#111111";
    $stop{'p-engage-banner--dark'}{2} = "#333333";
    $stop{'p-engage-banner--dark'}{3} = "#4e4e4e";
    
    $stop{'p-engage-banner--k8s'}{3} = "#326de6";
    $stop{'p-engage-banner--k8s'}{2} = "#173d8b";
    $stop{'p-engage-banner--k8s'}{1} = "#173d8b";
    
    $stop{'p-engage-banner--aqua'}{1} = "#2b585d";
    $stop{'p-engage-banner--aqua'}{2} = "#47919a";
    $stop{'p-engage-banner--aqua'}{3} = "#47919a";
    
    $stop{'p-engage-banner--snapcraft'}{3} = "#83bfa1";
    $stop{'p-engage-banner--snapcraft'}{2} = "#83bfa1";
    $stop{'p-engage-banner--snapcraft'}{1} = "#2d6162";

    $class = $F{'class'};
    
    my $addlogo = qq |ctx$_[0].drawImage(img, $logox, ($_[2]-newh)/2, neww, newh);|;
    $addlogo = qq |ctx$_[0].drawImage(img, $leftm, 50, 100/(img.height/img.width), 100);| if ($_[0] eq 'facebook916'); 

    my $canvas = qq |

	<canvas id="$_[0]" width="$_[1]" height="$_[2]">
	Your browser does not support the HTML5 canvas tag.
	</canvas>
	|;

    $script .= qq |
    var canvas$_[0] = document.getElementById("$_[0]");
    var ctx$_[0] = canvas$_[0].getContext("2d");

    // Create gradient
    var grd$_[0] = ctx$_[0].createLinearGradient(0, 0, $_[1], $_[2]);
    grd$_[0].addColorStop(0, "$stop{$class}{1}");
    grd$_[0].addColorStop(.42, "$stop{$class}{2}");
    grd$_[0].addColorStop(.94, "$stop{$class}{3}");
    // Fill with gradient
    ctx$_[0].fillStyle = grd$_[0]; 
    ctx$_[0].fillRect(0, 0, $_[1], $_[2]);
    
    // add ubuntu logo
    ctx$_[0].drawImage(ubuntu, $leftm, $midy, 143, 32);

    // add logo
    $addlogo

    // add text
    // h1
    ctx$_[0].font = "normal 100 $h1size Ubuntu";
    ctx$_[0].fillStyle = "#ffffff";
    $h1
    // h4
    ctx$_[0].font = "normal 300 20.8979px Ubuntu";
    $h4
    |;
	
    return($canvas);

}
