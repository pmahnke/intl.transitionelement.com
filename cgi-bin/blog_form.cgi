#!/usr//bin/perl
# marketo to normal html converter
# status
# 2019-10-31 - initial version


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
&parseHTML();
exit;


#####################
sub parseHTML {

    $form = qq |
<form action="https://pages.ubuntu.com/index.php/leadCapture/save" method="post" class="marketo-form" id="mktoForm_$F{'id'}">
  <div class="row">
    <div class="col-4 mktFormReq mktField">
      <label for="FirstName" class="mktoLabel">First Name:</label>
      <input required="" id="FirstName" name="FirstName" maxlength="255" class="mktoField mktoRequired" type="text" aria-label="First Name" style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHklEQVQ4EaVTO26DQBD1ohQWaS2lg9JybZ+AK7hNwx2oIoVf4UPQ0Lj1FdKktevIpel8AKNUkDcWMxpgSaIEaTVv3sx7uztiTdu2s/98DywOw3Dued4Who/M2aIx5lZV1aEsy0+qiwHELyi+Ytl0PQ69SxAxkWIA4RMRTdNsKE59juMcuZd6xIAFeZ6fGCdJ8kY4y7KAuTRNGd7jyEBXsdOPE3a0QGPsniOnnYMO67LgSQN9T41F2QGrQRRFCwyzoIF2qyBuKKbcOgPXdVeY9rMWgNsjf9ccYesJhk3f5dYT1HX9gR0LLQR30TnjkUEcx2uIuS4RnI+aj6sJR0AM8AaumPaM/rRehyWhXqbFAA9kh3/8/NvHxAYGAsZ/il8IalkCLBfNVAAAAABJRU5ErkJggg==&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;">
    </div>
    <div class="col-4 mktFormReq mktField">
      <label for="LastName" class="mktoLabel">Last Name:</label>
      <input required="" id="LastName" name="LastName" maxlength="255" class="mktoField mktoRequired" type="text" aria-label="Last Name">
    </div>
  </div>
  <div class="row">
    <div class="col-4 mktFormReq mktField">
      <label for="Email" class="mktoLabel">Work email:</label>
      <input required="" id="Email" name="Email" maxlength="255" class="mktoField mktoEmailField mktoRequired" type="email" aria-label="Email">
    </div>
    <div class="col-4 mktFormReq mktField">
      <label for="Company" class="mktoLabel">Company Name:</label>
      <input required="" id="Company" name="Company" maxlength="255" class="mktoField mktoRequired" type="text" aria-label="Company Name">
    </div>
  </div>
  <div class="row">
    <div class="col-4 mktFormReq mktField">
      <label for="Title" class="mktoLabel">Job Title:</label>
      <input required="" id="Title" name="Title" maxlength="255" class="mktoField mktoRequired" type="text" aria-label="Job Title">
    </div>
    <div class="col-4 mktFormReq mktField">
      <label for="Phone" class="mktoLabel">Phone Number:</label>
      <input required="" id="Phone" name="Phone" maxlength="255" class="mktoField mktoTelField mktoRequired" type="tel" aria-label="Phone Number">
    </div>
  </div>
  <div class="row">
    <div class="col-4 mktFormReq mktField">
      <input name="canonicalUpdatesOptIn" aria-label="canonicalUpdatesOptIn" id="canonicalUpdatesOptIn" value="yes" class="mktoField" type="checkbox">
      <label for="canonicalUpdatesOptIn" class="mktoLabel">I agree to receive information about Canonical’s products and services.</label>

      <div class="g-recaptcha" data-sitekey="6LfYBloUAAAAAINm0KzbEv6TP0boLsTEzpdrB8if" style="margin: 0rem 0 0.5rem 0;">
      </div>

      <p class="u-no-padding--top">
        In submitting this form, I confirm that I have read and agree to
        <a href="/legal/data-privacy/contact">
          Canonical’s Privacy Notice
        </a> and <a href="/legal/data-privacy">Privacy Policy</a>.
        <input name="RichText" aria-label="RichText" type="hidden">
      </p>
      <button type="submit" class="mktoButton">
        Download
      </button>
      <input type="hidden" aria-hidden="true" aria-label="hidden field" name="munchkinId" class="mktoField" value="066-EOV-335">
      <input name="formid" aria-label="formid" class="mktoField" value="$F{'id'}" type="hidden">
      <input name="formVid" aria-label="formid" class="mktoField" value="$F{'id'}" type="hidden">
      <input type="hidden" name="returnURL" aria-label="returnURL" value="$F{'thank-you'}">
      <input type="hidden" name="retURL" aria-label="retURL" value="$F{'thank-you'}">
      <input type="hidden" aria-hidden="true" aria-label="hidden field" name="return_url" value="$F{'thank-you'}">
      <input name="utm_campaign" aria-label="utm_campaign" class="mktoField mktoFormCol" value="" type="hidden">
      <input name="utm_medium" aria-label="utm_medium" class="mktoField mktoFormCol" value="" type="hidden">
      <input name="utm_source" aria-label="utm_source" class="mktoField mktoFormCol" value="" type="hidden">
      <input name="Consent_to_Processing__c" aria-label="Consent" class="mktoField mktoFormCol" value="Yes" type="hidden">
    </div>
  </div>
</form>
	|;

    &printForm($form);


}


#####################
sub printForm {


    my $display = "u-hide" if (!$_[0]);
    my $safe_form = $_[0];
    $safe_form =~ s/</&lt;/g;
    
    print qq ~Content-type:  text/html
X-XSS-Protection:0

<!doctype html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

    <title>Marketo to html converter</title>

    <!-- stylesheets -->
    <link rel="stylesheet" href="https://assets.ubuntu.com/v1/vanilla-framework-version-2.4.1.min.css" />
</head>

<body>

<div class="wrapper u-no-margin--top">
  <div id="main-content" class="inner-wrapper">

<section class="p-strip--light is-shallow">
  <div class="row">
    <div class="col-8">
      <h1>Marketo to normal html converter</h1>
    </div>
  </div>
    
  <div class="row $display">
    <div class="col-8">
      <h2>Cleaned form raw html</h2>
      <form action="$thisScript" method="POST">
        <fieldset>
          <textarea name="mkto" rows="20">
$safe_form          
          </textarea>
        </fieldset>
      </form>
    </div>
  </div>
    
  <div class="row $display">
    <div class="col-8">
      <h2>cleaned form</h2>
    </div>
  </div>
  <div class="row $display" style="background-color: #fff;">
    <div class="col-8">
      $_[0]
    </div>
  </div>

  <div class="row">
    <div class="col-8">
      <h2>Enter the marketo form details</h2>
      <form action="$thisScript" method="POST">
        <fieldset>
          <label for="thank-you">Form id</label>
          <input type="text" name="id" value="$F{'id'}" />
          <label for="thank-you">Thank you page url</label>
          <input type="text" name="thank-you" value="$F{'thank-you'}" />
          <input class="p-button--positive" type="submit" name="action" value="submit" />
        </fieldset>
      </form>
    </div>
  </div>
</section>
</div>
</div>
</body>
</html>
  ~;



}
