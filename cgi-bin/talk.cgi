#!/usr/local/bin/perl


# CREATE TABLE conversation (id integer primary key autoincrement, title text);
# CREATE TABLE message (id integer primary key autoincrement, date date, time time, message text, conversation_id integer, user_id integer);
# CREATE TABLE user (id integer primary key autoincrement, name text);
# CREATE TABLE tracker (id integer primary key autoincrement, user_id integer, conversation_id integer, date date, time time);

require ("/home/gartner/html/rt/SmartyPants.pl");
require ("/home/gartner/cgi-bin/Textile.pm");

use CGI::Lite;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=/home/mahnke/cgi-bin/chat.db","","",{ PrintError => 1, AutoCommit => 0 });

my $date = `date +'%Y-%m-%d';`;
my $time = `date +'%T'`;
chop($date);
chop($time);

my $thisScript = qq |http://intl.transitionelement.com/cgi-bin/talk.cgi|;

my ($msg, $h); 


if ($ENV{'CONTENT_LENGTH'} || $ENV{'QUERY_STRING'}) {

    $cgi = new CGI::Lite;
    %FORM = $cgi->parse_form_data;
    
    
} else {

	&name();
	
}

# hour changes for datetime functions
if ($FORM{'name'} =~ /Peter/i) {
	$h = "+7 hours";
} else {
	# most people are EST
	$h = "+2 hours";
}

#############################################################################
# what to do
if ($FORM{'action'} eq "start") {

	&conversation();
	
} elsif ($FORM{'action'} eq "join") {

	&name();
	
} elsif ($FORM{'action'} eq "delete conversation") {

	&print(&delete_converstation());

} elsif ($FORM{'action'} eq "update") {

	my $out = &get_conv($FORM{'conversation_id'});
	print "Content-type: text/html\;\n\n";
	print $out;
	exit;

} elsif ($FORM{'action'} eq "who") {

	&print(&get_conversation_list);

} else {

	&chat();

}
exit;



#############################################################################
sub tracker {

	# track the person's last check of a conversation
	# only get it if there is new stuff....

	my ($sql, $sth, $test, $t_id, $d, $t, $limit);
	

	# does the person already have a tracker id for this conversation
	$sql = qq | SELECT id 
				FROM tracker 
				WHERE user_id=$FORM{'user_id'} 
					AND conversation_id=$FORM{'conversation_id'}
			  |;

	$t_id = $dbh->selectrow_array($sql);

	return($t_id);
	
}


#############################################################################
sub tracker_update {

	my ($sql, $sth, $test, $t_id, $d, $t, $limit);
	

	# does the person already have a tracker id for this conversation
	$sql = qq | SELECT id 
				FROM tracker 
				WHERE user_id=$FORM{'user_id'} 
					AND conversation_id=$FORM{'conversation_id'}
			  |;

	$t_id = $dbh->selectrow_array($sql);
	
	
	if ($t_id) {
	
		# tracker is tracking this conversation for the user
		# test is last update
		$sql = qq | SELECT t.id 
					FROM tracker AS t
					LEFT JOIN message AS m ON t.conversation_id=m.conversation_id 
						AND m.conversation_id=$FORM{'conversation_id'}
					WHERE t.id=$t_id 
						AND m.date>=t.date 
						AND m.time>t.time
				  |;
	
		$test = $dbh->selectrow_array($sql);
		
		$sql =~ s/(\n|\t|  )/ /g;
		#print STDERR "tracker  $FORM{'name'} test is $test\n$sql\n";


	
		# update the tracker table with current time and date
		$sql = qq | UPDATE 
					tracker
					SET 
					date = ?, time = ?
					WHERE
					id = ?
		  		|;

		$sth = $dbh->prepare($sql);
		$sth->execute($date, $time, $t_id);
		$dbh->commit();
		
		return($t_id);
			

	} else {
	
		# new person... create the tracker record
		$sql = qq | INSERT INTO 
					tracker 
					(user_id, conversation_id, date, time )
					VALUES (?,?,?,?) 
			  	|;

		$sth = $dbh->prepare($sql);
		$sth->execute($FORM{'user_id'}, $FORM{'conversation_id'}, $date, $time);
		$dbh->commit();
		
		return();

	}

}


#############################################################################
sub insert_message {

	my ($sql, $sth, $out);

	$sql = qq |	
	
		INSERT INTO message 
			(message, date, time, conversation_id, user_id)
		VALUES (?, ?, ?, ?, ?)
	|;

	
	$sth = $dbh->prepare($sql);

	$sth->execute($FORM{'message'}, $date, $time, $FORM{'conversation_id'}, $FORM{'user_id'});

	$dbh->commit();
	
	return();

}


#############################################################################
sub get_conversation_list {

	my ($out, $sql, $sth, $limit);
	
	$limit = " AND u.id = $FORM{'user_id'} " if ($FORM{'name'} !~ /peter/i);

	$sql = qq |
	
		SELECT c.title, u.name, c.id
			FROM tracker            t
			LEFT JOIN conversation  c  ON  c.id=t.conversation_id
			LEFT JOIN user          u  ON  u.id=t.user_id
			WHERE t.date > (select time ('now', '-6 hours')) $limit
			GROUP BY c.title, u.name
			ORDER BY c.title, u.name
	|;
	
	$sth = $dbh->prepare($sql);

	$sth->execute();

	$sth->bind_columns (\$c, \$n, \$i);

	$out = "<table>\n<tr><th>Conversation</th><th>Who</th></tr>";
	
	while ( $sth->fetch ) {
	
		my $t = $dbh->selectrow_array("SELECT max (time (time, '$h')) FROM message WHERE conversation_id=$i AND date=(select date('now')) AND user_id<>$FORM{'user_id'}");
	
		$out .= "<tr><td><a href\=\"$thisScript?action\=jump&amp\;conversation\=$c&amp\;conversation_id\=$i&amp\;name\=$FORM{'name'}&amp\;user_id\=$FORM{'user_id'}\">$c<\/a> $t";
		$out .= "  ( <a href\=\"$thisScript?action\=delete conversation&amp\;conversation\=$c&amp\;conversation_id\=$i&amp\;name\=$FORM{'name'}&amp\;user_id\=$FORM{'user_id'}\">del</a> ) " if ($FORM{'name'} =~ /peter/i);
		$out .= "</td><td>$n</td></tr>\n";

	}
	$out .= "</table>\n\n";
	return($out);	
}


#############################################################################
sub get_user_list {

	my ($out, $sql, $sth);

	$sql = qq |
	
		SELECT u.name, count(distinct m.message), max(m.date), max (m.time)
			FROM message  m
			LEFT JOIN user     u   ON u.id = m.user_id
			WHERE m.conversation_id = ?
			GROUP BY name
			ORDER BY name
	|;
	
	$sth = $dbh->prepare($sql);

	$sth->execute($FORM{'conversation_id'});

	$sth->bind_columns (\$n, \$c, \$d, \$t);

	$out = "<table>\n<tr><th>Who</th><th>No.</th><th>When</th></tr>";
	
	while ( $sth->fetch ) {
	
		$out .= "<tr><td>$n</td><td>$c</td><td>$d $t</td></tr>\n";

	}
	$out .= "</table>\n\n";
	return($out);	
}


#############################################################################
sub get_conv {

	my ($limit, $sql, $sth, $out, $note);

	my $tracker_id = &tracker if ($FORM{'action'} eq "update");
	
	#return() if (!$tracker_id);
	
	#print STDERR "get_conv $FORM{'name'} limit is $limit\n";

	if ($tracker_id && $FORM{'action'} eq "update") {

		$sql = qq |	SELECT  u.name, m.message, date(m.date, '$h'), time(m.time, '$h')
					FROM message  m
					LEFT JOIN user    u  ON  u.id = m.user_id
					WHERE 
					m.conversation_id = ? AND 
					m.date>=(select date from tracker where id=?) AND 
					m.time>(select time from tracker where id=?);	
				|;
				
		$sth = $dbh->prepare($sql);
		$sth->execute($FORM{'conversation_id'}, $tracker_id, $tracker_id);
		#$note .= "tracker id $tracker_id and update on \n";
	
	} else {
	
		$sql = qq |
	
			SELECT u.name, m.message, date(m.date, '$h'), time(m.time, '$h')
			FROM message          AS m
				LEFT JOIN user    AS u   ON u.id = m.user_id
			WHERE conversation_id = ?
			$limit
			ORDER BY date, time
	
		|;

		$sth = $dbh->prepare($sql);
		$sth->execute($FORM{'conversation_id'});
		#$note .= "getting whole list\n"
	}
	
	#$sql =~ s/\n/ /g;
	#print STDERR "$FORM{'action'} $FORM{'name'} $sql $FORM{'user_id'}, $FORM{'conversation_id'} $tracker_id \n $note \n";

	$sth->bind_columns (\$n, \$msg, \$d, \$t);
	
	while ( $sth->fetch ) {

		#print STDERR "\n$sql\n\n";
	
		if ($n eq $FORM{'name'}) {
			$out .= "<li class\=\"me\">$msg <span class\=\"name\">$n</span><span class\=\"date\"><br />$t</span></li>\n";
		} else {
			$out .= "<li class\=\"you\"><span class\=\"name\">$n</span> $msg<span class\=\"date\"><br />$t</span></li>\n";
		}
	
	}

	&tracker_update;

	#print STDERR "output $out\n" if ($tracker_id);

	return($out);

}


#############################################################################
sub delete_converstation {

	my ($sql);

	$sql = qq |
DELETE FROM
message
WHERE
conversation_id=$FORM{'conversation_id'}
	|;
	$dbh->do($sql);
	$sql =~ s/\n/ /g;
	print STDERR "$sql\n";
	my $out = $sql;

	$sql = qq |
DELETE FROM
tracker
WHERE
conversation_id=$FORM{'conversation_id'}
	|;
	$dbh->do($sql);
	$sql =~ s/\n/ /g;
	print STDERR "$sql\n";
	$out .= $sql;
	
	$sql = qq |
DELETE FROM
conversation
WHERE
id=$FORM{'conversation_id'}
	|;
	$dbh->do($sql);
	$sql =~ s/\n/ /g;
	print STDERR "$sql\n";
	$out .= $sql;

	$dbh->commit();
	
	return('deleted conversation... '.$FORM{'conversation'}.$out);

}


#############################################################################
sub email {

	my $out =<<EndofHTML;

You are invited to a talk by $FORM{'name'}

  <$thisScript?action=join&conversation=$FORM{'conversation'}&conversation_id=$FORM{'conversation_id'}>


EndofHTML
	
	my $subject = "Join me for a talk: ".$FORM{'conversation'};
	
	use MIME::Lite;
	MIME::Lite->send("sendmail", "/var/qmail/bin/sendmail -t >& /dev/null");
   	my $mail = MIME::Lite->new(
                           From    =>'talk2me@mahnke.net',
                           To      =>$FORM{'email'},
                           Subject =>$subject,
                           Data    =>$out
                           );
   	$mail->send;

	#print STDERR "\nemail\n$out\n\n";		

	return('email sent to '.$FORM{'email'});
	
}

#############################################################################
sub get_user_id {
	
	my $user_id = $dbh->selectrow_array("SELECT id FROM user WHERE name='$FORM{'name'}'");
	return($user_id);
	
}

#############################################################################
sub create_user_id {

	my ($sql, $sth, $out);

	$sql = qq |	INSERT INTO user
				(name)
				VALUES (?)
			  |;
	
	$sth = $dbh->prepare($sql);
	$sth->execute($FORM{'name'});
	$dbh->commit();
	return();

}

#############################################################################
sub chat {

	my ($sql, $sth, $out, $conv, $users);

	my $t_id = $FORM{'conversation_id'};
	
	if (!$FORM{'user_id'}) {
		
		# user has no user_id... so get or create...
		$FORM{'user_id'} = &get_user_id;
		if (!$FORM{'user_id'}) {
			# none, so create one...
			&create_user_id;
			$FORM{'user_id'} = &get_user_id;
		}
	}
	
	# send an email invite if a real email was submitted
	$mesg .= &email() if ($FORM{'email'} && $FORM{'email'} ne "email");
	
	if (!$t_id) {
	
		# test it
		$t_id = $dbh->selectrow_array("SELECT id FROM conversation WHERE title='$FORM{'conversation'}'");
	
		if (!$t_id) {
			# insert it
			$sql = qq | INSERT INTO conversation (title) VALUES (?) |;
			$sth = $dbh->prepare($sql);
    	    $sth->execute($FORM{'conversation'});
       	 	$dbh->commit();
        }
        
    } else {

		&insert_message() if ($FORM{'message'});
    	$conv = &get_conv($t_id);

   	}
    
	$FORM{'conversation_id'} = $dbh->selectrow_array("SELECT id FROM conversation WHERE title='$FORM{'conversation'}'");

	# get list of users in a conversation
	$users = &get_user_list;

	$coversations = &get_conversation_list; # if ($FORM{'name'} eq "Peter");

	$out =<<EndofHTML;

	<input type="hidden" name="name" value="$FORM{'name'}" />
	<input type="hidden" name="user_id" value="$FORM{'user_id'}" />
	<input type="hidden" name="conversation" value="$FORM{'conversation'}" />
	<input type="hidden" name="conversation_id" value="$FORM{'conversation_id'}" />
	<input type="hidden" name="action" value="message" />

<div id="log">	
<ul>
	$conv
</ul>
</div>

<div id="input">
<p><fieldset><input type="text" name="message" id="message" tabindex="1" size="40" /><input type="submit" name="action" value="go"  tabindex="2"/></p>
<p><input type="submit" name="action" value="reload"  tabindex="3"/></fieldset></p>
</div>

<div id="email">
<p><fieldset><input type="text" name="email" value="email"  tabindex="4"/> <input type="submit" name="action" value="invite"  tabindex="5" /></fieldset></p>
</div>

</div><!-- end DIV content -->
<div id="navigation">

<div id="users">
$users
</div>

<div id="conversations">
$coversations
</div>

</div>
	
EndofHTML

	&print ($out, 'Your talk: '.$FORM{'conversation'});

}




#############################################################################
sub conversation {

	my ($sql, $sth, $out);

	my $u_id = $dbh->selectrow_array("SELECT id FROM user WHERE name='$FORM{'name'}'");

	if (!$u_id) {
	
		# insert it
		$sql = qq | INSERT INTO user (name) VALUES (?) |;
		$sth = $dbh->prepare($sql);
        $sth->execute($FORM{'name'});

		#print STDERR "$sql $FORM{'name'}\n";
        $dbh->commit();
    }
	$u_id = $dbh->selectrow_array("SELECT id FROM user WHERE name='$FORM{'name'}'");


	$out =<<EndofHTML;

	<input type="hidden" name="name" value="$FORM{'name'}" />
	<input type="hidden" name="user_id" value="$u_id" />
	
	$FORM{'name'}
	
	conversation: <input name="conversation" value="$FORM{'conversation'}" />
	<input type="submit" name="action" value="conversation" />
	
	</div><!-- end DIV content -->
	
EndofHTML

	&print ($out, 'Your conversation?');

}



#############################################################################
sub name {

	my ($action, $out);
	
	$action = "start";
	$action = "start chat" if ($FORM{'conversation_id'});
	
	$out =<<EndofHTML;

	<input type="hidden" name="conversation" value="$FORM{'conversation'}" />
	<input type="hidden" name="conversation_id" value="$FORM{'conversation_id'}" />
	
	name: <input name="name" value="$FORM{'name'}" />
	<input type="submit" name="action" value="$action" />

	</div><!-- end DIV content -->
	
EndofHTML

	&print ($out, 'Your name?');

}




#############################################################################
sub print {

	my $out;

	my $textile = new Text::Textile (
                                   charset => $FORM{'charset'},
                                   flavor => $FORM{'flavor'}
                                      );
    $out  = $textile->process($_[0]);

    $out  = &SmartyPants ($out, 1);

	
	$out =<<EndofHTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" ></meta>
<title>talk2me</title>

<script type="text/javascript" src="/prototype.js"></script>

<style type="text/css">


  body     {  font-family: verdana, arial, sans-serif;  }
  ul       {  width: 95%; margin:  0.25em; padding: 0.5em;                  }
  li       {  list-style-type: none;          }
  .you     {  color: red; text-align: left;   }
  .me      {  color: blue; text-align: right; } 
  .msg     {  color: grey;                    }
  li:hover {  background-color: #eee;         }
  .name    {  font-size: 0.75em; margin: 0 -1.5em; padding: 0 2em; }
  .date    {  font-size: 0.75em; margin: 0 -1.5em; padding: 0 2em; }
  #log     {  overflow-y: scroll; overflow-x: hidden; height: 15em; width: 100%;  }
  #users   {  clear: left; float: right;  }
  #conversations {  clear: both; float: right;  }
  fieldset {  border: 0;  }
  textarea {  font-family: verdana; color: blue;  }
  #content, #navigation { float: left;  padding: 1em;  }
  #content    {  background-color: #eee; width: 55%;  } 
  #navigation {  width: 35%; background-color: #ce9; border: 1px solid #ccc; } 
  #input      {  background-color: #cee;  border: 1px solid #ccc;  }
  #email      {  background-color: lightyellow; border: 1px solid #ccc; }
  td          {  font-size: 0.75em;  }

</style>

<script type="text/javascript">

	
/* $('talk').request(
	{
  		method: 'get',
  		parameters: { action: go, name: '$FORM{'name'}', user_id: $FORM{'user_id'}, conversation_id: $FORM{'conversation_id'}, date: '$date', time: '$time' },
    	onSuccess: function scroll() {
	   		e.scrollTop=e.scrollHeight;
    	}
  	});
*/
	new Ajax.PeriodicalUpdater('log', '/cgi-bin/talk.cgi',
  	{
    	method: 'get',
   	 	parameters: {action: 'update', name: '$FORM{'name'}', user_id: $FORM{'user_id'}, conversation_id: $FORM{'conversation_id'}, date: '$date', time: '$time'},
	    insertion: Insertion.Bottom,
    	frequency: 3,
    	decay: 1,
    	onSuccess: function scroll() {
    		e = document.getElementById('log');
	    	e.scrollTop=e.scrollHeight;
    	}
  	});

 function startup () {

	document.talk.message.focus();
 	e = document.getElementById('log');
	e.scrollTop=e.scrollHeight;

 }

</script>

</head>
<body onload="startup();">

<div id="container">
	<div id="content">

<h1>Talk to me&#8230;</h1>

<h2>$_[1]</h2>

<p class="msg">$mesg</p>

<form method="post" name="talk" id="talk" action="talk.cgi">

$out

</form>

</div>

</body>
</html>
EndofHTML


	print "Content-type: text/html\n\n$out\n";

	exit;


}
