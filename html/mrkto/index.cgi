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

	# OUT OF A ROW
	if (/<div class="mktoClear">/ && $FLAGrow) {
	    $FLAGrow = 0;
	    $o .= &processRow($field, $FLAGreq);
	    ($field, $FLAGreq) = "";
	    next;
	}
	
        # IN A ROW
        if (/<(input|button|select|textarea|label|div class="mktoHtmlText)/) {
            $FLAGrow = 1;
        }
        
        
        if ($FLAGrow) {
            $field    .= $_;
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

    return if ($_[0] =~ /(hidden|canonicalUpdatesOptIn|button)/);
    
    # sets class based on required or not
    $class = qq | class="p-list__item"|;
    $class = qq | class="p-list__item"| if ($_[1]);
    $class .= qq | id="comments"| if ($_[0] =~ /Comments_from_lead__c/);

    my $in = $_[0];
    
    $in =~ s/style="(.[^"]*)"//g; # remove inline styles
    $in =~ s/\*//g; # remove Asterix for required fields
    $in =~ s/class="(.[^"]*?)"//g; #TextField|mktoHasWidth|mktoFieldDescriptor|mktoHasWidth|mktoField|mktoEmailField|mktoRequired|mktoInvalid|mktoFormCol|mktoLabel)//g; # removing random classes
    $in =~ s/<span (.[^>?]*)>//g;
    $in =~ s/<\/span>//g;
    $in =~ s/ class="\s*"//g;
    $in =~ s/<div\s*>//g;
    $in =~ s/<\/div>//g;
    $in =~ s/:<\/label>/ (optional):<\/label>/g if (!$_[1]); # add span if required
    $in =~ s/<(input|textarea|select)/<$1 required /g if ($_[1]); # add html5 required

    if ($in =~ /In submitting this form, I confirm that I have read and agree to <a href="https:\/\/www.ubuntu.com\/legal\/dataprivacy" target="_blank"  id="">Canonical's Privacy Policy<\/a>/) {
	$in = qq |

              <input value="yes" id="canonicalUpdatesOptIn" name="canonicalUpdatesOptIn" type="checkbox" />
              <label for="canonicalUpdatesOptIn">I agree to receive information about Canonical's products and services.</label>

              <p>
                In submitting this form, I confirm that I have read and agree to <a href="/legal/data-privacy/contact">Canonical's Privacy Notice</a> and <a href="/legal/data-privacy">Privacy Policy</a>.
              </p>
            
              {# These are honey pot fields to catch bots #}
              <div class="u-off-screen">
                <label class="website" for="website">Website:</label>
                <input name="website" type="text" class="website" autocomplete="off" value="" id="website" tabindex="-1" />
                <label class="name" for="name">Name:</label>
                <input name="name" type="text" class="name" autocomplete="off" value="" id="name" tabindex="-1" />
              </div>
            {# End of honey pots #}
|;
	}
        
    # formatting clean-ups
    $in =~ s/<\/option><option/<\/option>\r<option/g; # prepend space to options
    $in =~ s/<\/label></<\/label>\r</g; # format labels
    $in =~ s/</&lt;/g; # convert < to &lt;

    $out = qq |        $in\n\n|;
    $out =~ s/<div\s*>//g;
    $out =~ s/<\/div>//g;
    return($out);

}


############################################################################
sub printForm {

    # set a class to hide the results if this is running the first time
    my $display;
    $display = qq | style="display: none;" | if (!$_[0]);
    
    my $formTag = qq |<form action="/marketo/submit" method="post" id="$_[1]">|;
    
    my $form = qq |
<!-- MARKETO FORM -->
      $formTag 
        <fieldset class="u-no-margin--bottom">
$_[0]
          <!-- hidden fields -->
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="formid" value="{{formid}}" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="returnURL" value="{{returnURL}}" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="Consent_to_Processing__c" value="yes" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_campaign" id="utm_campaign" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_medium" id="utm_medium" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_source" id="utm_source" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_content" id="utm_content" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_term" id="utm_term" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="GCLID__c" id="GCLID__c" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="FBCLID__c" id="FBLID__c" value="" />
          <button type="submit" class="p-button--positive" onclick="dataLayer.push({'event' : 'GAEvent', 'eventCategory' : 'Form', 'eventAction' : 'contact-us', 'eventLabel' : '{{product}}', 'eventValue' : undefined });">Submit</button>
        </fieldset>
      </form>
<!-- /MARKETO FORM -->

|;

    $form =~ s/button><\/span>/button>/g;
    $form =~ s/&(?!#?[xX]?(?:[0-9a-fA-F]+|\w+);)/&amp;/g; # amputator
    $form =~ s/\}\&/\}\&amp;/g;
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
