#!/usr/bin/perl

# interactive get-in-touch form builder
# status
# 2020-05-26 - initial build

use CGI::Lite;

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
&parseForm();
exit;

########################################
sub parseForm {

  my $output = qq |
  <div class="p-modal" id="contact-modal">
    <div class="p-modal__dialog" role="dialog" aria-labelledby="modal-title" aria-describedby="modal-description">
      <header class="p-modal__header" style="display: block; border-bottom: 0;">
        <button class="p-modal__close" aria-label="Close active modal" style="margin-left: -1rem">Close</button>
        <h2 class="p-modal__title u-sv1" id="modal-title">$F{'title'}</h2>
      </header>
      <div class="js-pagination js-pagination--1">
        <p id="modal-description" class="u-no-max-width u-no-margin--bottom">$F{'description'}</p>
  |;

  $output .= &processQ($F{'q1'}, $F{'q1-code'}, $F{'q1-answers'}, $F{'q1-other'} );

  $output .= &processQ($F{'q2'}, $F{'q2-code'}, $F{'q2-answers'}, $F{'q2-other'} );

  $output .= qq |
<div class="pagination">
  <a class="p-button--positive pagination__link--next" href="">Next</a>
</div>
</div>

<div class="js-pagination js-pagination--2 u-hide">
  |;


  $output .= &processQ($F{'q3'}, $F{'q3-code'}, $F{'q3-answers'}, $F{'q3-other'} );
  
  $output .= &processQ($F{'q4'}, $F{'q4-code'}, $F{'q4-answers'}, $F{'q4-other'} ) if ($F{'q4'});

  $output .= qq |
<div class="pagination">
  <a class="pagination__link--previous p-button--neutral" href="">Previous</a>
  <a class="pagination__link--next p-button--positive" href="">Next</a>
</div>
</div>

<div class="js-pagination js-pagination--3 u-hide">
  |;

  $output .= qq |
  <h3 class="p-heading--five">How should we get in touch?</h3>
  <div class="row u-no-padding">
    <div class="col-6">
      <form action="https://pages.ubuntu.com/index.php/leadCapture/save" method="post" id="mktoForm_%% formid %%" class="modal-form marketo-form">
        <ul class="p-list">
          <li class="mktFormReq mktField p-list__item">
            <label for="FirstName" class="mktoLabel">First name:</label>
            <input required id="FirstName" name="FirstName" maxlength="255" type="text" class="mktoField mktoRequired" />
          </li>
          <li class="mktFormReq mktField p-list__item">
            <label for="LastName" class="mktoLabel">Last name:</label>
            <input required id="LastName" name="LastName" maxlength="255" type="text" class="mktoField mktoRequired" />
          </li>
          <li class="mktFormReq mktField p-list__item">
            <label for="Email" class="mktoLabel">Work email:</label>
            <input required id="Email" name="Email" maxlength="255" type="email" class="mktoField mktoEmailField mktoRequired" />
          </li>
          <li class="mktField p-list__item">
            <input class="mktoField" value="yes" id="canonicalUpdatesOptIn" name="canonicalUpdatesOptIn" type="checkbox" />
            <label class="mktoLabel mktoHasWidth" for="canonicalUpdatesOptIn">I agree to receive information about Canonical’s products and services.</label>
          </li>
          <li class="p-list__item">In submitting this form, I confirm that I have read and agree to <a href="/legal/data-privacy/contact">Canonical&rsquo;s Privacy Notice</a> and <a href="/legal/data-privacy">Privacy Policy</a>.</li>
          <li class="p-list__item">
            <div class="g-recaptcha" data-sitekey="{{ CAPTCHA_TESTING_API_KEY }}"></div>
          </li>
        </ul>

        <div class="u-hide">
          <h3>Your comments</h3>
          <ul class="p-list">
            <li class="mktFormReq mktField p-list__item">
              <label for="Comments_from_lead__c" class="mktoLabel">What would you like to talk to us about?</label>
              <textarea id="Comments_from_lead__c" name="Comments_from_lead__c" rows="5" class="mktoField" maxlength="2000"></textarea>
            </li>
          </ul>
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="formValidation" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="formid" class="mktoField" value="%% formid %%" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="formVid" class="mktoField" value="%% formid %%" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="lpId" class="mktoField" value="%% lpId %%" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="subId" class="mktoField" value="30" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="munchkinId" class="mktoField" value="066-EOV-335" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="lpurl" class="mktoField" value="%% lpurl %%?cr={creative}&amp;kw={keyword}" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="cr" class="mktoField" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="kw" class="mktoField" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="q" class="mktoField" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="returnURL" value="%% returnURL %%" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="retURL" value="%% returnURL %%" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="Consent_to_Processing__c" value="yes" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="productContext" id="product-context" value="{{ product }}" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_campaign" class="mktoField" id="utm_campaign" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_medium" class="mktoField" id="utm_medium" value="" />
          <input type="hidden" aria-hidden="true" aria-label="hidden field" name="utm_source" class="mktoField" id="utm_source" value="" />
        </div>

        <div class="pagination">
          <a class="pagination__link--previous p-button--neutral" href="">Previous</a>
          <button type="submit" class="pagination__link--next p-button--positive mktoButton" aria-label="Submit">Let's discuss</button>
        </div>
      </form>
    </div>
  </div>
</div>

<div class="js-pagination js-pagination--4 u-hide">
  <div class="row u-no-padding">
    <div class="u-equal-height">
      <div class="col-7">
        <h3 class="p-heading--two">$F{'ty-title'}</h3>
        <p class="p-heading--four">$F{'ty-text'}</p>
      </div>
      <div class="col-5 u-vertically-center u-align--center u-hide--small">
        <img src="https://assets.ubuntu.com/v1/cbae9a60-thank_you_orange_cmyk.svg" alt="smile" width="200" height="200" loading="auto">
      </div>
    </div>
  </div>
  <a class="js-close p-button--neutral" href="">Close</a>
</div>
</div>
</div>
  |;

  my $output_pre = $output;
  $output_pre =~ s/</&lt;/g;
  
  $output = qq |
  <section class="p-strip">
    <div class="row">
      <div class="col-8">
        $doutput
      </div>
    </div>
    <div class="row">
      <div class="col-8">
        <pre style="font-size: small;">
$output_pre
        </pre>
      </div>
    </div>
  </section>
  |;

  &printForm($output);
  exit;
}


########################################
sub processQ {

  my $title = $_[0];
  my $code = $_[1];
  my @options = split (/\n/, $_[2]);
  my $mod = int(scalar @options / 3) + 1;
  my $other = $_[3];
  my ($i, $output) = "";
  
  $output = qq |
  <div class="js-formfield">
    <h3 class="p-heading--five">$title</h3>
    <div class="row u-no-padding">
      <div class="col-4 u-sv3">
  |;
  
  foreach (@options) {

      my $opt = $_;
      $opt =~ s/\s+$//; #=~ s/\n//g;
      
      my $id = &cleanId($opt, $code);

      $output .= qq |          </div>
	  <div class="col-4 u-sv3">\n| if ($i % $mod == 0 && $i);
      $m = $i % $mod;
      $output .= qq |	    <input type="checkbox" id="$id">\n	    <label for="$id">$opt</label>\n|;

      $i++;
     

   }

  # optional Other
  if ($other) {

      my $id = &cleanId("-other", $code);

      $output .= qq |
	<div class="js-other-container">
	  <input type="checkbox" class="js-other-container__checkbox" id="$id">
	  <label for="$id">Other</label>
	  <input type="text" id="$id-specified" class="js-other-container__input" placeholder="Please specify" style="opacity: 0; margin-top: .25rem;" aria-label="$other">
        </div>
	|;
    }

    $output .= qq |
         </div>
       </div>
     </div>
      |;  

  return($output);
  
}


sub cleanId {

    my $id = "";
    $id = $_[1]."-".$_[0];
    $id =~ tr/[A-Z]/[a-z]/;
    $id =~ s/ /-/g;
    $id =~ s/\.//g;
    $id =~ s/\s//g;
    return($id)
}

########################################
sub printForm {

    print qq ~Content-type: text/html\n\n  
<!doctype html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Interactive get-in-touch form builder</title>
    <link rel="stylesheet" href="https://assets.ubuntu.com/v1/vanilla-framework-version-2.12.0.min.css" />
  </head>
  <body>
    <div class="wrapper">
      <div id="main-content" class="inner-wrapper">

	<section class="p-strip--light is-shallow">
    <div class="row">
      <div class="col-8">
        <h1>Interactive get-in-touch form builder</h1>
      </div>
    </div>
  </section>

$_[0]

  <section class="p-strip--light">
  <div class="row">
  <div class="col-8">
  
  <form action="https://intl.transitionelement.com/modal/index.cgi" method="GET">
  <label for="title">Title</label>
  <input id="title" type="text" name="title" value="$F{'title'}">
  
  <label for="description">Description</label>
  <input id="description" type="text" name="description" value="$F{'description'}">
  
  <label for="q1">Question 1</label>
  <input id="q1" type="text" name="q1" value="$F{'q1'}">
  <label for="q1-answers">answers</label>
  <textarea id="q1-answers" name="q1-answers" rows="8" cols="80">$F{'q1-answers'}</textarea>
  <label for="q1-code">code</label>
  <input id="q1-code" type="text" name="q1-code" value="$F{'q1-code'}">
  <label for="q1-other">other</label>
  <input id="q1-other" type="text" name="q1-other" value="$F{'q1-other'}" />
  
  <label for="q2">Question 2</label>
  <input id="q2" type="text" name="q2" value="$F{'q2'}">
  <label for="q2-answers">answers</label>  
  <textarea id="q2-answers" name="q2-answers" rows="8" cols="80">$F{'q2-answers'}</textarea>
  <label for="q2-code">code</label>
  <input id="q2-code" type="text" name="q2-code" value="$F{'q2-code'}">
  <label for="q2-other">other</label>
  <input id="q2-other" type="text" name="q2-other" value="$F{'q2-other'}" />
  
  <label for="q3">Question 3</label>
  <input id="q3" type="text" name="q3" value="$F{'q3'}">
  <label for="q3-answers">answers</label>  
  <textarea id="q3-answers" name="q3-answers" rows="8" cols="80">$F{'q3-answers'}</textarea>
  <label for="q3-code">code</label>
  <input id="q3-code" type="text" name="q3-code" value="$F{'q3-code'}">
  <label for="q3-other">other</label>
  <input id="q3-other" type="text" name="q3-other" value="$F{'q3-other'}" />
  
  <label for="q4">Question 4</label>
  <input id="q4" type="text" name="q4" value="$F{'q4'}">
  <label for="q4-answers">answers</label>  
  <textarea id="q4-answers" name="q4-answers" rows="8" cols="80">$F{'q4-answers'}</textarea>
  <label for="q4-code">code</label>
  <input id="q4-code" type="text" name="q4-code" value="$F{'q4-code'}">
  <label for="q4-other">other</label>
  <input id="q4-other" type="text" name="q4-other" value="$F{'q4-other'}" />
  
  <label for="title">Open question</label>
  <input id="question" type="text" name="question" value="$F{'question'}">
  
  <label for="ty-title">Thank you title</label>
  <input id="ty-title" type="text" name="ty-title" value="$F{'ty-title'}">
  
  <label for="ty-text">Thank you message</label>
  <textarea id="ty-text" name="ty-text" rows="8" cols="80">$F{'ty-text'}</textarea>

  <label for="form-id">Form id</label>
  <input id="form-id" type="text" name="form-id" value="$F{'form-id'}">
  
  <input type="submit" class="p-button" name="a" value="build">
  
  </form>
  </div>
  </section>
  
      </div>
    </div>
  </body>
</html>

~;
  
  exit();
}
