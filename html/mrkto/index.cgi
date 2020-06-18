#!/usr//bin/perl
# marketo to normal htmlconverter
# status
# 2015-11-18 - change jquery.validation to add http:// as defauls protocal on url fields


use CGI::Lite;

my $testscript = qq |

  \$(function(){\$("#comments").hide()});

  \$('#Ubuntu_User__c').on('change',function(){

   var selection = \$(this).val();
   if(selection == 'Commercially only') {
      \$('#comments').show();
   } else {
      \$('#comments').hide();
   }
  });
|;

##############################################################
# Variables

# better formatted newsletter opt-in with checkbox on the left
#my $thisScript = qq |/mrkto|;

my $goodOptin = qq |
    <li  class="mktField">    
        <input class="mktoField" value="yes" id="NewsletterOpt-In" name="NewsletterOpt-In" type="checkbox">
        <label  class="mktoLabel mktoHasWidth" for="NewsletterOpt-In">I would like to receive occasional news from Canonical by email.</label>        
    </li>
    <li>All information provided will be handled in accordance with the Canonical <a href="http://www.ubuntu.com/legal" target="_blank">privacy policy</a>.</li>
        |;

# add good state province code?
my $goodState = qq |
    <li class="mktoPlaceholder mktoPlaceholderState">
        <label for="State" class="mktoLabel mktoHasWidth">State:</label>
        <select id="State" name="State" class="mktoField  mktoRequired mktFReq">
        <optgroup label="Select Province" value="SelectProvince">
<option value="AB">Alberta</option><option value="BC">British Columbia</option><option value="MB">Manitoba</option><option value="NB">New Brunswick</option><option value="NF">Newfoundland</option><option value="NT">Northwest Territories</option><option value="NS">Nova Scotia</option><option value="NU">Nunavut</option><option value="ON">Ontario</option><option value="PE">Prince Edward Island</option><option value="QC">Quebec</option><option value="SK">Saskatchewan</option><option value="YT">Yukon Territory</option>
        </optgroup>
        <optgroup label="Select State" value="SelectState">
        <option value="AK">Alaska</option><option value="AL">Alabama</option><option value="AR">Arkansas</option><option value="AZ">Arizona</option><option value="CA">California</option><option value="CO">Colorado</option><option value="CT">Connecticut</option><option value="DC">District of Columbia</option><option value="DE">Delaware</option><option value="FL">Florida</option><option value="GA">Georgia</option><option value="HI">Hawaii</option><option value="IA">Iowa</option><option value="ID">Idaho</option><option value="IL">Illinois</option><option value="IN">Indiana</option><option value="KS">Kansas</option><option value="KY">Kentucky</option><option value="LA">Louisiana</option><option value="MA">Massachusetts</option><option value="MD">Maryland</option><option value="ME">Maine</option><option value="MI">Michigan</option><option value="MN">Minnesota</option><option value="MO">Missouri</option><option value="MS">Mississippi</option><option value="MT">Montana</option><option value="NC">North Carolina</option><option value="ND">North Dakota</option><option value="NE">Nebraska</option><option value="NH">New Hampshire</option><option value="NJ">New Jersey</option><option value="NM">New Mexico</option><option value="NV">Nevada</option><option value="NY">New York</option><option value="OH">Ohio</option><option value="OK">Oklahoma</option><option value="OR">Oregon</option><option value="PA">Pennsylvania</option><option value="PR">Puerto Rico</option><option value="RI">Rhode Island</option><option value="SC">South Carolina</option><option value="SD">South Dakota</option><option value="TN">Tennessee</option><option value="TX">Texas</option><option value="UT">Utah</option><option value="VA">Virginia</option><option value="VT">Vermont</option><option value="WA">Washington</option><option value="WI">Wisconsin</option><option value="WV">West Virginia</option><option value="WY">Wyoming</option>
    </optgroup>
        </select>
    </li>
        |;



# parse the post input
##############################################################
if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {

    # something submitted
    $cgi = new CGI::Lite;
    %F = $cgi->parse_form_data;
    
} else {
    
    # nothing sent
    &printForm();
    exit;
       
}
&parseHTML();
exit;


##############################################################
sub parseHTML {


    &printForm() if (!$F{'mkto'});
    $F{'mkto'} =~ s/>/>\r/g;
    my @html = split(/\r/, $F{'mkto'});
    
    my ($FLAGform, $FLAGrow, $FLAGreq, $FLAGstate, $field, $formId, $o);
    
    foreach (@html){

        # in the form, so set the flag to start working
        if (/<form/ && /id="(mktoForm_.[^"]*)"/) {
$FLAGform = 1; 
$formId = $1;
        }
        next if (!$FLAGform); # skip if not in the form
        
        #print STDERR "looking at $_ \n";
        #print STDERR qq |opt: $_\n| if (/NewsletterOpt/);


        # stop processing if at end of the form
        if ($FLAGform && /<\/form>/) {
$o .= &processRow($field, $FLAGreq);
$FLAGform = 0;
next;
        }
        
        
        # SKIP THE MKTOCLEAR EMPTY DIVS    
        if ($FLAGclear) {

#skip the closing div and reset the flag
$FLAGclear = 0;
next;

        }
        $FLAGclear = 1 if (/<div class="mktoClear">/);
        
        # IN A ROW
        if (/<div class="(mktoFormRow|mktoFieldWrap|mktoButtonRow)">/) {

            if ($field =~ /NewsletterOpt-In/) {
                $o .= $goodOptin; # override
            } elsif ($field =~ /"State"/) {
                print STDERR qq |found state $field|;
                $o .= $goodState;
            } else {       
                $o .= &processRow($field, $FLAGreq);
            }
            
            ($field, $FLAGreq) = "";
            $FLAGrow = 1;
        
        }
        
        
        if ($FLAGrow) {
        
            $field    .= $_ if (!/(<div|<\/div|<span)/);
            $FLAGreq   = 1 if (/mktoRequiredField/);
       
        }           
    
    }
    
    &printForm($o, $formId);

}

############################################################################
sub processRow {

    # translates marketo rows into vanilla format
					
    my ($out, $class) = "";
    return() if (!$_[0]);
    
    # sets class based on required or not
    $class = qq | class="p-list__item mktField"|;
    $class = qq | class="p-list__item mktFormReq mktField"| if ($_[1]);
    $class .= qq | id="comments"| if ($_[0] =~ /Comments_from_lead__c/);

    my $in = $_[0];
    
    $in =~ s/style="(.[^"]*)"//g; # remove inline styles
    $in =~ s/\*//g; # remove Asterix for required fields
    $in =~ s/(mktoTextField|mktoHasWidth|mktoFieldDescriptor|mktoHasWidth)//g; # removing random classes
    $in =~ s/:<\/label>/ (optional):<\/label>/g if (!$_[1]); # add span if required
    $in =~ s/<(input|textarea|select)/<$1 required /g if ($_[1]); # add html5 required
        
    # formatting clean-ups
    $in =~ s/\n//g; # remove extra newlines
    $in =~ s/<\/option><option/<\/option>\r<option/g; # prepend space to options
    $in =~ s/<\/label></<\/label>\r</g; # format labels
    $in =~ s/</&lt;/g; # convert < to &lt;
    
    $out = qq |
        <li $class>    
$in
        </li>
    |; # wrap fields in list
    
    return($out);

}


############################################################################
sub printForm {

    # set a class to hide the results if this is running the first time
    my $display;
    $display = qq | style="display: none;" | if (!$_[0]);
    
    my $formTag = qq |<form action="https://pages.ubuntu.com/index.php/leadCapture/save" method="post" id="$_[1]" class="marketo-form">|;
    
    my $form = qq |
<!-- MARKETO FORM -->
<script src="//assets.ubuntu.com/v1/37b1db88-jquery.min.js"></script>
<script  src="//assets.ubuntu.com/v1/d55f58bb-jquery.validate.js"></script>
<script src="//assets.ubuntu.com/v1/6ce35d3e-jquery-ui.min.js"></script>‌​
    
$formTag 
<fieldset>
    <ul class="p-list">          
$_[0]
    </ul>
</fieldset>
</form>
<script>
\$("\#$_[1]").validate({
    errorElement: "span",
    errorClass: "mktFormMsg mktError",
    onkeyup: false,
    onclick: false,
    onblur: false
});
$testscript
</script>
<script  src="//assets.ubuntu.com/v1/f97fa297-stateCountry.js"></script>

<!-- /MARKETO FORM -->

|;

    $form =~ s/button><\/span>/button>/g;
    $form =~ s/&(?!#?[xX]?(?:[0-9a-fA-F]+|\w+);)/&amp;/g; # amputator
    $form =~ s/\}\&/\}\&amp;/g;
    $form =~ s/<\/form>/\n<input type="hidden" name="returnURL" value="$F{'thank-you'}" \/>\n<input type="hidden" name="retURL" value="$F{'thank-you'}" \/>\n<\/form>/;

    $form =~ s/&lt;/</g;
    
    my $safeForm = $form;
    $safeForm =~ s/</&lt;/g;
    
    $F{'mkto'} =~ s/</&lt;/g;
    
    print qq ~Content-type:  text/html
X-XSS-Protection:0

<!doctype html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

    <title>Marketo to html converter</title>

    <!-- stylesheets -->
    <link rel="stylesheet" type="text/css" media="screen"    href="//assets.ubuntu.com/sites/guidelines/css/responsive/latest/ubuntu-styles.css" />
    <link rel="stylesheet" type="text/css" media="screen" href="http://assets.ubuntu.com/sites/ubuntu/1418/u/css/styles.css" />
    <link rel="stylesheet" type="text/css" media="screen" href="http://assets.ubuntu.com/sites/ubuntu/1418/u/css/beta/global-responsive.css" />
    <link rel="stylesheet" type="text/css" media="print" href="http://assets.ubuntu.com/sites/ubuntu/1418/u/css/core-print.css" />

</head>

<body>

<div class="wrapper">
<div id="main-content" class="inner-wrapper">

    <div class="row no-border no-margin-bottom">
        <h1>Marketo to normal html converter</h1>
    </div>
    
    <div class="row no-border" $display>

	    <div class="eight-col">
	    
	        <h2>Cleaned form raw html</h2>

            <form action="$thisScript" method="POST">
                <fieldset>
                    <ul>
                        <li>
                            <textarea name="mkto" rows="20">
$safeForm          
                            </textarea>
                        </li>
                    </ul>
                </fieldset>
            </form>
        </div>
    </div>
    

    <div class="row no-border" $display>
	    <div class="eight-col">

            <h2>cleaned form</h2>

$form

        </div>
    </div>

    <div class="row no-border">
	    <div class="eight-col">

            <h2>Enter the marketo form</h2>

            <form action="$thisScript" method="POST">
                <fieldset>
                    <ul>
                        <li><textarea name="mkto" rows="20">$F{'mkto'}</textarea></li>
                        <li>
                            <label for="thank-you">Thank you page url</label>
                            <input type="text" name="thank-you" value="$F{'thank-you'}" />
                        <li>
                        <li>
                            <input type="submit" name="action" value="submit" />
                        <li>
                    </ul>
                </fieldset>
            </form>
        </div>
    </div>



</div></div>
</body>
</html>
  
    ~;
    exit;

}
