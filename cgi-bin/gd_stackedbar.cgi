#!c:/perl/bin/perl.exe

use CGI::Lite;
use GD::Graph::bars;
use GD::Text;
use Math::Round;


if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {

 	$cgi = new CGI::Lite;
    %FORM = $cgi->parse_form_data;


} else {
	exit;
}

    @Clables   = &_makearray($FORM{'Clables'})  if ($FORM{'Clables'});
    @Cdata1    = &_makearray($FORM{'Cdata1'})   if ($FORM{'Cdata1'});
    @Cdata2    = &_makearray($FORM{'Cdata2'})   if ($FORM{'Cdata2'});
    @Cdata3    = &_makearray($FORM{'Cdata3'})   if ($FORM{'Cdata3'});
	@Clegend   = &_makearray($FORM{'Clegend'})  if ($FORM{'Clegend'});

    $Clables   = &_makeserial($FORM{'Clables'},1)  if ($FORM{'Clables'});
    $Cdata1    = &_makeserial($FORM{'Cdata1'})     if ($FORM{'Cdata1'});
    $Cdata2    = &_makeserial($FORM{'Cdata2'})     if ($FORM{'Cdata2'});
    $Cdata3    = &_makeserial($FORM{'Cdata3'})     if ($FORM{'Cdata3'});
	$Clegend   = &_makeserial($FORM{'Clegend'},1)  if ($FORM{'Clegend'});


	#my @mydata = ([$Clables], [$Cdata1], [$Cdata2], [$Cdata3]);
	my @mydata = ([@Clables], [@Cdata1], [@Cdata2], [@Cdata3]);
	#my @mydata = (["25-Sep-04","26-Sep-04","27-Sep-04","28-Sep-04","29-Sep-04","30-Sep-04","01-Oct-04","02-Oct-04"],[1360,2053,9561,8855,9062,8871,7513,270],[2,8,27,16,31,40,9,0],[37,144,491,408,448,462,266,4]);

#&null;
sub null {
	print <<EndofHTML;
Content-type: text/html

<pre>
@Clegend
@Clables
@Cdata1
@Cdata2
@Cdata3

$Clegend
$Clables
$Cdata1
$Cdata2
$Cdata3

</pre>
EndofHTML
exit;
}

my $graph = new GD::Graph::bars(400,300);

# figure out max x-axis
$max = int ($max * 1 + 1000);
$max = nearest(1000, $max);
$graph->set( y_max_value => $max);
$graph->set( y_min_value => 0);


# set fonts
$graph->set_title_font('c:/windows/fonts/trebuc.ttf', 12);
$graph->set_legend_font('c:/windows/fonts/trebuc.ttf', 10);
$graph->set_x_axis_font('c:/windows/fonts/trebuc.ttf', 6);
$graph->set_y_axis_font('c:/windows/fonts/trebuc.ttf', 6);
$graph->set_x_label_font('c:/windows/fonts/trebuc.ttf', 10);
$graph->set_y_label_font('c:/windows/fonts/trebuc.ttf', 10);

$graph->set(
    x_label         => $FORM{'xaxis'},
    y_label         => $FORM{'yaxis'},
    title           => $FORM{'Ctitle'},
    bar_spacing     => 3,
	long_ticks      => 0,
    cumulate        => 1,
	y_long_ticks    => 1,
    y_label_skip    => 0,
    accentclr       => "white",
    accent_treshold => 10,
    shadow_depth    => 0,
)
or warn $graph->error;


# set COLORS
$graph->set( dclrs        => [ qw(dblue dgreen dred) ] );
$graph->set( labelclr     => "dgray" );
$graph->set( axislabelclr => "dgray" );
$graph->set( legendclr    => "dgray" );
$graph->set( valuesclr    => "dgray" );
$graph->set( textclr      => "dgray" );
$graph->set( fgclr        => "black" );


$graph->set_legend(@Clegend);

$graph->plot(\@mydata) or die $graph->error;

binmode STDOUT;
select(STDOUT);
$| = 1;
undef $/;
print "Content-type: image/png\n\n";
print $graph->gd->png();

exit;


sub _makearray {

	my @array = split (/\|/, $_[0]);
	return(@array);

}

sub _makeserial {

	my $serial;
	my $intramax;
	my @array = split (/\|/, $_[0]);
	foreach (@array) {
		$serial .= "$_,"     if (!$_[1]); # numbers
		$serial .= "\"$_\"," if ($_[1]); # text
		if ($_ !~ /\D/) {
			$intramax = $_   if ($_ > $intramax);
		}
	}
	$max += $intramax;
	chop($serial);
	return ($serial);

}