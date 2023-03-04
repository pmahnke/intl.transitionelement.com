#!/usr/bin/perl

use strict;
use utf8::all;
use DBI;
use DateTime::Incomplete;
use URI::Encode qw(uri_encode uri_decode);
use Encode qw(decode encode);
use URI::Escape;
use JSON;

binmode(STDOUT, ":utf8");          #treat as if it is UTF-8
binmode(STDIN, ":encoding(utf8)"); #actually check if it is UTF-8

# database
my $dbh = DBI->connect( "dbi:SQLite:dbname=/home/gartner/html/wltm//wltm.db",
    "", "", { RaiseError => 1, AutoCommit => 1, sqlite_unicode => 1 } );


my (%F);

################################################################
if ( $ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'} ) {

    read(STDIN, my $buffer, $ENV{CONTENT_LENGTH});
    $buffer = $ENV{'QUERY_STRING'} if (!$buffer);

    my @pairs = split(/&/, $buffer);

    foreach my $pair (@pairs) {
     my ($name, $value) = split(/=/, $pair);
      $value = decode("utf-8",uri_unescape($value));

      # decode
      $value =~ s/\%([A-Fa-f0-9]{2})/pack('C', hex($1))/seg;
      $value =~ s/\+/ /g;

      $F{$name} = $value;

    }
}

################################################################
# WHAT TO DO
if ( $F{'a'} eq "make" ) {
    
    &findPerson($F{'id'});

} elsif ($F{'a'} eq"join") {

    &setStatusbyId($F{'id'}, 1);
    &printOutput(qq|You joined WLTM. Welcome!
The \@wltm bot will send you invites to 1-2-1 coffee-chats – as GoogleMeets to your Calendar, and will alert you, with a DM in Mattermost.
Use **find** to set up your first meet.|);
    
} elsif ($F{'a'} eq "snooze") {

    &setStatusbyId($F{'id'}, 2);
    &printOutput(qq|No more invitations from \@wltm for 3 months.|);
    
} elsif ($F{'a'} eq "leave") {

    &setStatusbyId($F{'id'}, 0);
    &printOutput(qq|You have been removed from \@wltm.|);
    
    
} elsif ($F{'a'} eq "info" || $F{'a'} eq "whois") {

    my $id = $F{'id'};
    $id = $F{'person'} if ($F{'person'});
    
    &getInfobyId($id);

} elsif ($F{'a'} eq "bio" || $F{'a'} eq "bios") {

    &setBiobyId($F{'id'}, $F{'bio'});
    &printOutput(qq|Your bio *'$F{'bio'}'* has been added to \@wltm.|);

} elsif ($F{'a'} eq "help") {

    &printOutput(qq~#### Would Like To Meet Help
|Command|Description|
| ----- | --------- |
|**join**|You need to join *wltm*|
|**bio**|You can add your bio for others to see|
|**snooze**|If you want to pause your membership in \@wltm for 3 months|
|**whois** `\@person`|Let's you see a person's info.|
|**leave**|Remove yourself from \@wltm.|
|**status**|Show your status.|
~);
    
} else {

    &setStatusbyId('ya-bo-ng', 1);
    
    &printOutput(qq|Would Like to Meet helps you set up GoogleMeet ‘coffee-chats’ with a random colleague.
When you **join** you will receive invitations to 25 minute meets, up to 6 times a year. **help ** for more.|);
    
#    &setStatusbyId('peterm-ubuntu', 1);
#   &setStatusbyId('tbmb', 1);
#  &setStatusbyId('anasereijo', 1);

# &setBiobyId('peterm-ubuntu','I’m into Schnitzel, Perl and cats.');
#  &setBiobyId('tbmb','I have a moustache and I am crazy');
# &setBiobyId('anasereijo','I am a UXer and I love Portugal');
#    &getInfobyId('peterm-ubuntu');

#    &findPerson('peterm-ubuntu');

}

exit;


sub printOutput {

    print qq |Content-Type: application/json; charset=UTF8\n\n|;

    my $json->{"messages"} = $_[0];
    $json->{"guest_id"} = $_[1] if ($_[1]);
    $json->{"guest_msg"} = $_[2] if ($_[2]);
    
    my $json_text = to_json($json);
    print qq|$json_text|;

    #print qq |'{"message":"$_[0]"}'\n|;
    exit;
    
}

sub getInfobyId {

    # get a user's info by id

    my ($sql, $sth, $id ,$name, $title, $email, $group, $status, $bio ) = "";
    
    $sql = qq |
	SELECT p.launchpad_id, p.name, p.title, p.email, p.group_A, i.status, i.bio
	FROM people as p
	LEFT JOIN tracker as i on p.launchpad_id = i.launchpad_id
	WHERE p.launchpad_id == '$_[0]' 
	|;

    $sth = $dbh->prepare($sql);
    $sth->execute();
    $sth->bind_columns( \$id, \$name, \$title, \$email, \$group, \$status, \$bio );
    
    while ( $sth->fetch ) {

	$status = "active" if ($status == 1);
	$status = "snoozed" if ($status == 2);
	$status = "inactive" if (!$status);
	
	&printOutput(qq ~### Information about $name

|||
|---|---|
|title|$title|
|email|$email|
|group|$group|
|status|$status|
|bio|$bio|
~);	
    }

}


sub findPerson {

    my ( $sql, $sth, $id, $name, $launchpad_id, $bio, $out, $other ) = "";

    &printOutput(qq|**Error** - missing a your id|) if (!$_[0]);
    
    # get the user's main group
    my $group = &getGroupbyId($_[0]);

    # get all current events
     $sql = qq |
     SELECT p.id, p.name, p.launchpad_id, t.bio 
	 FROM people AS p
	 LEFT JOIN tracker AS t ON p.launchpad_id = t.launchpad_id
	 WHERE group_A == '$group' AND p.launchpad_id != '$_[0]' AND t.status == 1
	 ORDER BY RANDOM()
	 LIMIT 1
	  |;

    $sth = $dbh->prepare($sql);
    $sth->execute();
    $sth->bind_columns( \$id, \$name, \$launchpad_id, \$bio );
    
    while ( $sth->fetch ) {

	my $q = $name;
	$q =~ s/ /+/g;
	
	$out .= qq|Would Like to Meet here! I’ve proposed a coffee-chat with $name \@$launchpad_id  [directory](https://directory.canonical.com/search/?query=$q)

Bio: “$bio”

Tentative [GCal](https://www.google.com/calendar/render?action=TEMPLATE&text=WLTM+%E2%98%95+with+$name&details=Here+is+a+Would+Like+to+Meet+for+you+and+$name.&dates=20220307T12000Z%2F20220307T130000Z) Monday, 7 March, 12:00 GMT. You could [chat](\@$launchpad_id) now to say hi, and agree a good time.|;

	$other = qq|Good news from Would Like To Meet has helped \@$_[0] select you for a coffee-chat.  Expect a meeting invitation soon!|;
	
    }
    &printOutput($out, $launchpad_id, $other);
    return();
}


sub getBiobyId {


    # get a user's bio by their launchpad id
    # input launchpad id

    return(0) if (!$_[0]);

    my $sql = qq |select bio from tracker where launchpad_id='$_[0]'|;
    return( $dbh->selectrow_array($sql) );
    
}


sub setStatusbyId {

    # set a user's status by their launchpad id
    # input launchpad id, bio

    &printOutput(qq|**Error** - missing a your id|) if (!$_[0]);

    my ($bio, $sql, $sth) = "";

    $bio = $dbh->selectrow_array( qq|SELECT bio FROM tracker WHERE launchpad_id = '$_[0]'| );
    
    $sql = qq |
	REPLACE INTO tracker (launchpad_id, status, bio)
	VALUES('$_[0]', $_[1], '$bio')
    |;

    $sth = $dbh->prepare($sql);
    $sth->execute();

    return()
}


sub setBiobyId {                                                                                  
    # set a user's bio by their launchpad id                                                         # input launchpad id, bio                                                                                                                                                                     
    &printOutput(qq|**Error** - missing a your id|) if (!$_[0]);

    my ($status, $sql, $sth)="";
                                                                           
    $status = $dbh->selectrow_array( qq|SELECT status FROM tracker WHERE launchpad_id = '$_[0]'| );
    $sql = qq |
	REPLACE INTO tracker (launchpad_id, bio, status) 
	VALUES('$_[0]','$_[1]', '$status')
	|;                                                                                            
    
    $sth = $dbh->prepare($sql);                                                                  
    $sth->execute();                                                                                                                                                                             
    return()                                                                                      
}


sub getGroupbyId {

    # get a user's group by their launchpad id
    # input launchpad id

    return(0) if (!$_[0]);

    my $sql = qq |select group_A from people where launchpad_id='$_[0]'|;
    return( $dbh->selectrow_array($sql) );


}
