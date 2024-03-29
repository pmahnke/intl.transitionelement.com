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
  <button id="showModal" aria-controls="contact-modal">Show modal…</button>
  <div class="p-modal" id="contact-modal">
    <div class="p-modal__dialog" role="dialog" aria-modal="true" aria-labelledby="modal-title" aria-describedby="modal-description">
      <header class="p-modal__header" style="display: block; border-bottom: 0;">
        <h2 class="p-modal__title u-sv1" id="modal-title">$F{'title'}</h2>
        <button class="p-modal__close" aria-label="Close active modal" aria-controls="modal">Close</button>
      </header>
      <div class="js-pagination js-pagination--1">
        <p id="modal-description" class="u-no-max-width u-no-margin--bottom">$F{'description'}</p>
  |;

  $output .= &processQ($F{'q1'}, $F{'q1-code'}, $F{'q1-answers'}, $F{'q1-other'}, $F{'q1-type'} );

  $output .= &processQ($F{'q2'}, $F{'q2-code'}, $F{'q2-answers'}, $F{'q2-other'}, $F{'q2-type'} );

  $output .= qq |
<div class="pagination">
  <a class="p-button--positive pagination__link--next" href="">Next</a>
</div>
</div>

<div class="js-pagination js-pagination--2 u-hide">
  |;


  $output .= &processQ($F{'q3'}, $F{'q3-code'}, $F{'q3-answers'}, $F{'q3-other'}, $F{'q3-type'} );
  
  $output .= &processQ($F{'q4'}, $F{'q4-code'}, $F{'q4-answers'}, $F{'q4-other'}, $F{'q4-type'} ) if ($F{'q4'});

  $output .= qq |
      <div class="u-sv3 js-formfield">
        <h3 class="p-heading--five">$F{'question'}</h3>
        <textarea id="open-question" name="open-question" aria-label="$F{'question'}" placeholder="$F{'question-helptext'}" rows="3"></textarea>
      </div>
      |;
  
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
          <input type="hidden" aria-hidden="true" name="formid" class="mktoField" value="%% formid %%" />
          <input type="hidden" aria-hidden="true" name="formVid" class="mktoField" value="%% formid %%" />
          <input type="hidden" aria-hidden="true" name="lpId" class="mktoField" value="%% lpId %%" />
          <input type="hidden" aria-hidden="true" name="subId" class="mktoField" value="30" />
          <input type="hidden" aria-hidden="true" name="munchkinId" class="mktoField" value="066-EOV-335" />
          <input type="hidden" aria-hidden="true" name="lpurl" class="mktoField" value="%% lpurl %%?cr={creative}&amp;kw={keyword}" />
          <input type="hidden" aria-hidden="true" name="cr" class="mktoField" value="" />
          <input type="hidden" aria-hidden="true" name="kw" class="mktoField" value="" />
          <input type="hidden" aria-hidden="true" name="q" class="mktoField" value="" />
          <input type="hidden" aria-hidden="true" name="returnURL" value="%% returnURL %%" />
          <input type="hidden" aria-hidden="true" name="retURL" value="%% returnURL %%" />
          <input type="hidden" aria-hidden="true" name="Consent_to_Processing__c" value="yes" />
          <input type="hidden" aria-hidden="true" name="productContext" id="product-context" value="{{ product }}" />
          <input type="hidden" aria-hidden="true" name="utm_campaign" class="mktoField" id="utm_campaign" value="" />
          <input type="hidden" aria-hidden="true" name="utm_medium" class="mktoField" id="utm_medium" value="" />
          <input type="hidden" aria-hidden="true" name="utm_source" class="mktoField" id="utm_source" value="" />
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
      <div class="col-12">
        $output
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
  my $type = $_[4];
  my ($i, $output) = "";
  
  $output = qq |
  <div class="js-formfield">
    <h3 class="p-heading--five">$title</h3>
    <div class="row u-no-padding">
      <div class="col-3 u-sv3">
  |;
  
  foreach (@options) {

      my $opt = $_;
      $opt =~ s/\s+$//; #=~ s/\n//g;
      
      my $id = &cleanId($opt, $code);

      $output .= qq |          </div>
	  <div class="col-3 u-sv3">\n| if ($i % $mod == 0 && $i);
      $m = $i % $mod;
      
      if ($type eq "radio") {
	  my $radio_id = &cleanId($code);
	  $output .= qq |
	      <label class="p-radio" for="$id">
  	        <input class="p-radio__input" type="radio" aria-labelledby="$radio_id" value="$opt">
	        <span  class="p-radio__label" id="$radio_id">$opt</span>
	      </label>
	      |;

      } else {
	  
	  $output .= qq |
	      <label class="p-checkbox" aria-labelledby="$id">
	        <input class="p-checkbox__input" type="checkbox">
	        <span class="p-checkbox__label" id="$id">$opt</span>
	      </label>
	      |;
      
      }
	  $i++;
     

   }

  # optional Other
  if ($other) {

      my $id = &cleanId("-other", $code);

      $output .= qq |
	<div class="js-other-container">
	  <label class="p-checkbox" aria-labelledby="$id">
	    <input class="p-checkbox__input js-other-container__checkbox" id="$id" type="checkbox">
	    <span class="p-checkbox__label" id="$id">Other</span>
	    <input type="text" id="$id-specified" class="js-other-container__input" placeholder="Please specify" style="opacity: 0; margin-top: .25rem;" aria-label="$other">
	  </label>
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

    my $id = $_[0];
    $id = $_[1]."-".$_[0] if ($_[1]);
    $id =~ tr/[A-Z]/[a-z]/;
    $id =~ s/ /-/g;
    $id =~ s/\.//g;
    $id =~ s/\s//g;
    $id =~ s/('|’)//g;
    $id =~ s/,//g;
    $id =~ s/(\(|\))//g;
    return($id)
}

########################################
sub printForm {

    $F{'q1-type-checked'} = "checked" if ($F{'q1-type'} eq "radio");
    $F{'q2-type-checked'} = "checked" if ($F{'q2-type'} eq "radio");
    $F{'q3-type-checked'} = "checked" if ($F{'q3-type'} eq "radio");
    $F{'q4-type-checked'} = "checked" if ($F{'q4-type'} eq "radio");
    
    print qq ~Content-type: text/html\n\n  
<!doctype html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Interactive get-in-touch form builder</title>
    <link rel="stylesheet" href="https://assets.ubuntu.com/v1/vanilla-framework-version-3.1.1.min.css" />
    <script src="https://ubuntu.com/static/js/dist/main.js?v=597d458" defer=""></script>
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
  <input id="q1-type" type="checkbox" name="q1-type" value="radio" $F{'q1-type-checked'}>
  <label for="q1-type">Radio? (<em>default is checkbox</em>)</label>
  <label for="q1-other">other</label>
  <input id="q1-other" type="text" name="q1-other" value="$F{'q1-other'}" />
  
  <label for="q2">Question 2</label>
  <input id="q2" type="text" name="q2" value="$F{'q2'}">
  <label for="q2-answers">answers</label>  
  <textarea id="q2-answers" name="q2-answers" rows="8" cols="80">$F{'q2-answers'}</textarea>
  <label for="q2-code">code</label>
  <input id="q2-code" type="text" name="q2-code" value="$F{'q2-code'}">
  <input id="q2-type" type="checkbox" name="q2-type" value="radio" $F{'q2-type-checked'}>
  <label for="q2-type">Radio? (<em>default is checkbox</em>)</label>
  <label for="q2-other">other</label>
  <input id="q2-other" type="text" name="q2-other" value="$F{'q2-other'}" />
  
  <label for="q3">Question 3</label>
  <input id="q3" type="text" name="q3" value="$F{'q3'}">
  <label for="q3-answers">answers</label>  
  <textarea id="q3-answers" name="q3-answers" rows="8" cols="80">$F{'q3-answers'}</textarea>
  <label for="q3-code">code</label>
  <input id="q3-code" type="text" name="q3-code" value="$F{'q3-code'}">
  <input id="q3-type" type="checkbox" name="q3-type" value="radio" $F{'q3-type-checked'}>
  <label for="q3-type">Radio? (<em>default is checkbox</em>)</label>
  <label for="q3-other">other</label>
  <input id="q3-other" type="text" name="q3-other" value="$F{'q3-other'}" />
  
  <label for="q4">Question 4</label>
  <input id="q4" type="text" name="q4" value="$F{'q4'}">
  <label for="q4-answers">answers</label>  
  <textarea id="q4-answers" name="q4-answers" rows="8" cols="80">$F{'q4-answers'}</textarea>
  <label for="q4-code">code</label>
  <input id="q4-code" type="text" name="q4-code" value="$F{'q4-code'}">
  <input id="q4-type" type="checkbox" name="q4-type" value="radio" $F{'q4-type-checked'}>
  <label for="q4-type">Radio? (<em>default is checkbox</em>)</label>
  <label for="q4-other">other</label>
  <input id="q4-other" type="text" name="q4-other" value="$F{'q4-other'}" />
  
  <label for="question">Open question</label>
  <input id="question" type="text" name="question" value="$F{'question'}">
  
  <label for="question-helptext">Open question help text</label>
  <input id="question-helptext" type="text" name="question-helptext" value="$F{'question-helptext'}">
  
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
  <script>
  // This is an example modal implementation inspired by
  // https://www.w3.org/TR/wai-aria-practices/examples/dialog-modal/dialog.html

(function () {
  // This is not a production ready code, just serves as an example
  // of how the focus should be controlled within the modal dialog.
  var currentDialog = null;
  var lastFocus = null;
  var ignoreFocusChanges = false;
  var focusAfterClose = null;

  // Traps the focus within the currently open modal dialog
  function trapFocus(event) {
    if (ignoreFocusChanges) return;

    if (currentDialog.contains(event.target)) {
      lastFocus = event.target;
    } else {
      focusFirstDescendant(currentDialog);
      if (lastFocus == document.activeElement) {
        focusLastDescendant(currentDialog);
      }
      lastFocus = document.activeElement;
    }
  }

  // Attempts to focus given element
  function attemptFocus(child) {
    if (child.focus) {
      ignoreFocusChanges = true;
      child.focus();
      ignoreFocusChanges = false;
      return document.activeElement === child;
    }

    return false;
  }

  // Focuses first child element
  function focusFirstDescendant(element) {
    for (var i = 0; i < element.childNodes.length; i++) {
      var child = element.childNodes[i];
      if (attemptFocus(child) || focusFirstDescendant(child)) {
        return true;
      }
    }
    return false;
  }

  // Focuses last child element
  function focusLastDescendant(element) {
    for (var i = element.childNodes.length - 1; i >= 0; i--) {
      var child = element.childNodes[i];
      if (attemptFocus(child) || focusLastDescendant(child)) {
        return true;
      }
    }
    return false;
  }

  /**
    Toggles visibility of modal dialog.
    @param {HTMLElement} modal Modal dialog to show or hide.
    @param {HTMLElement} sourceEl Element that triggered toggling modal
    @param {Boolean} open If defined as `true` modal will be opened, if `false` modal will be closed, undefined toggles current visibility.
  */
  function toggleModal(modal, sourceEl, open) {
    if (modal && modal.classList.contains('p-modal')) {
      if (typeof open === 'undefined') {
        open = modal.style.display === 'none';
      }

      if (open) {
        currentDialog = modal;
        modal.style.display = 'flex';
        focusFirstDescendant(modal);
        focusAfterClose = sourceEl;
        document.addEventListener('focus', trapFocus, true);
      } else {
        modal.style.display = 'none';
        if (focusAfterClose && focusAfterClose.focus) {
          focusAfterClose.focus();
        }
        document.removeEventListener('focus', trapFocus, true);
        currentDialog = null;
      }
    }
  }

  // Find and hide all modals on the page
  function closeModals() {
    var modals = [].slice.apply(document.querySelectorAll('.p-modal'));
    modals.forEach(function (modal) {
      toggleModal(modal, false, false);
    });
  }

  // Add click handler for clicks on elements with aria-controls
  document.addEventListener('click', function (event) {
    var targetControls = event.target.getAttribute('aria-controls');
    if (targetControls) {
      toggleModal(document.getElementById(targetControls), event.target);
    }
  });

  // Add handler for closing modals using ESC key.
  document.addEventListener('keydown', function (e) {
    e = e || window.event;

    if (e.code === 'Escape') {
      closeModals();
    } else if (e.keyCode === 27) {
      closeModals();
    }
  });

  // init the dialog that is initially opened in the example
  toggleModal(document.querySelector('#modal'), document.querySelector('[aria-controls=modal]'), true);
})();
  </script>

</html>

~;
  
  exit();
}
