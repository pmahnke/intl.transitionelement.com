
################################################################################
#
# common.pl
#
#   written:  01 Dec 2003 by Peter Mahnke
#   modified: 21 Jan 2004 by Peter Mahnke
#
#   require script, called from most regional scripts
#
#   DESCRIPTION OF SUBROUTINES
#
#	 noHang
#	   takes a line of text and breaks it at a certain length,
#	   making sure there are no "widows"
#
#
#	 uppercase
#	   turns a title into a properly Capitalized version
#	   ignoring the obvious articles (e.g. 'the', 'of', etc.)
#
#
#
################################################################################



sub noHang {

	# three inputs
	# 1. text
	# 2. where to wrap
	# 3. delimiter (optional-defaults to <br />

	undef my @words;
	my $charCount = 0;
	my $noHang = "";
	my $wordNumber = 0;

	my $delim = "<br \/\>\n";
	$delim = "\n" if ($_[2] =~ /no/i);

	@words = split (" ", $_[0]);

	foreach (@words) {

		my $len = length($_);
		my $len1 = $charCount + $len;
		my $len2 = $charCount + $len + length($words[$wordNumber + 1]);

		if ($len2 > $_[1] && $wordNumber == $#words-1 ) {

			# if chars in current line + this word and the next are > $_[1]
			# and its the third last word, break

			$noHang .= " $delim $_ $words[$wordNumber + 1] $words[$wordNumber + 2]";
			last;

		} elsif ($len1 >= $_[1] && $wordNumber == $#words ) {

			# if chars in current line + this word > $_[1]
			# and its the second last word, break

			$noHang .= " $delim $_ $words[$wordNumber + 1]";
			last;

		} elsif ($charCount + $len < $_[1] ) {

			$charCount = $charCount + $len + 1;
			$noHang .= " $_";

		} else {

			$noHang .= " $delim$_";
			$charCount = $len;

		}

		$wordNumber++;
	}

	$noHang =~ s/^ //; # remove leading space
	$noHang =~ s/\<br \/\> /\<br \/\>/g; # remove trailing space

	return($noHang);

}




#################################################################
sub uppercase {

	# properly capitalize the titles, ignoring the obvious articles (e.g. 'the', 'of', etc.)
	# appends to global variable $msg for any messages....

	undef my $ucTitle;
	undef my $wordCount;

	@words = split (" ", $_[0]);

	foreach (@words) {

		$msg .= "title word: \|$_\|\n";

		# skip first word
		if (!$wordCount) {
			$wordCount = 1;
		}

		# DON'T capitalize the following 'special' words...
		# _in reverse logic to make it harder to read_
		if ($_ ne "the" &&
			$_ ne "of"  &&
			$_ ne "a"   &&
			$_ ne "in"  &&
			$_ ne "to"  &&
			$_ ne "an"  &&
			$_ ne "and")
		{

			$_ = ucfirst($_);
			$msg .= " capping $_ ";

		} else {

			$msg .= " skiping $_ ";

		}

		$ucTitle .= "$_ ";
		$wordCount++;
		$msg .= "now: $_ <br\>\n";
	}

	return($ucTitle);

}

sub clean_ascii {

    # ascii equivalent replacements
    my $s = $_[0];
    $s =~ s/\342\200[\230\231]/\'/g;
    $s =~ s/\342\200\246/.../g;
    $s =~ s/\342\200\223/-/g;
    $s =~ s/\342\200\224/--/g;
    $s =~ s/\342\200[\234\235]/\"/g;
    return($_[0]);

}

1;
















