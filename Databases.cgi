#!/usr/local/bin/perl

use CGI qw/:standard/;
use Bio::Perl;
use DBI;
use Bio::Tools::SeqStats;
use Bio::Tools::SeqWords;
use Matrix;
use Alignment;


print header;
print start_html("DNA Database");
print "<h1>DNA Database Tools</h1>\n";
&print_prompt();
&do_work();
&print_tail();
print end_html;

sub print_prompt {
	print start_form;
	print "<b>Insert into Database</b><br>";
	print "<em>Species Name:</em>";
	print textfield('name');
	print "<br>";
	print "<em>Sequence:</em>";
	print textfield('sequence');
	print "<br>";
	print submit('Action','Insert');
	print "<br><br>";

	print "<b>Show Sequences Database</b><br>";
	print "<em>Show all sequences in database</em><br>";
	print submit('Action','Select Sequences');
	print submit('Action','Show database');
	print "<br><br>";

	print "<b>Search Database</b><br>";
	print "<em>Query:</em>";
	print textfield('query');
	print "<br>";
	print submit('Action','Search Species');
	print submit('Action','Search Sequence');
	print "<br><br>";

	print "<b>Sequence Alignment</b><br>";
	print "Enter the common names of two species to do a Needleman-Wunsch alignment<br>";
	print "<em>Species 1</em>";
	print textfield('species1');
	print "<br>";
	print "<em>Species 2</em>";
	print textfield('species2');
	print "<br>";
	print submit('Action','Align');	

	print "<hr>\n";
	print endform;
}

sub do_work {

	if(param('Action') eq 'Insert'){

		my $name = param('name');
		my $sequence = param('sequence');

		if($name eq '' || $sequence eq ''){
			print "<b>Missing species name or sequence</b>";
			exit;
		}

		$dbh = DBI->connect("dbi:mysql:database=sequences_nevers;host=psoda2.cs.byu.edu","phylo","") 
			or die("Couldn't connect");

		# insert the data
		$SQL = "insert into seqs values('".$name."','".$sequence."');";

		print "The sql statement is [".$SQL."]",p;

		$Select = $dbh->prepare($SQL);
		$Select->execute();

		$dbh->disconnect();

		print em("Your data has been added to the database.<br>"),p;
	}

	if(param('Action') eq 'Select Sequences'){
		$dbh = DBI->connect("dbi:mysql:database=sequences_nevers;host=psoda2.cs.byu.edu","phylo","") 
			or die("Couldn't connect");

		$SQL = "select * from seqs";

		$Select = $dbh->prepare($SQL);
		$Select->execute();

		print em("Below are all of the sequences from the database:<br><br>");

		while($Row=$Select->fetchrow_hashref){
			print "$Row->{sequence}",p;
		}
		
		$dbh->disconnect();
	}

	if(param('Action') eq 'Show database'){
		$dbh = DBI->connect("dbi:mysql:database=sequences_nevers;host=psoda2.cs.byu.edu","phylo","") 
			or die("Couldn't connect");

		$SQL = "select * from seqs";

		$Select = $dbh->prepare($SQL);
		$Select->execute();

		print em("Below are all of the sequences from the database:<br><br>");

		while($Row=$Select->fetchrow_hashref){
			print "name $Row->{name}, sequence $Row->{sequence}",p;
		}
		
		$dbh->disconnect();
	}


	if(param('Action') eq 'Search Species'){
		
		my $query = param('query');
		$dbh = DBI->connect("dbi:mysql:database=sequences_nevers;host=psoda2.cs.byu.edu","phylo","") 
			or die("Couldn't connect");

		$SQL = "select * from seqs where name like '".$query."%'";

		print "The sql statement is [".$SQL."]",p;


		$Select = $dbh->prepare($SQL);
		$Select->execute();

		print em("Below are your search results:<br><br>");

		while($Row=$Select->fetchrow_hashref){
			print "$Row->{name}",p;
		}

		$dbh->disconnect();
	}

	if(param('Action') eq 'Search Sequence'){

		my $query = param('query');

		$dbh = DBI->connect("dbi:mysql:database=sequences_nevers;host=psoda2.cs.byu.edu","phylo","") 
			or die("Couldn't connect");

		$SQL = "select * from seqs where sequence like '".$query."%'";

		print "The sql statement is [".$SQL."]",p;

		$Select = $dbh->prepare($SQL);
		$Select->execute();

		print em("Below are your search results:<br><br>");

		while($Row=$Select->fetchrow_hashref){
			print "$Row->{sequence}",p;
		}

		$dbh->disconnect();
	}

	if(param('Action') eq 'Align') {

		my $dbh;
                $dbh = DBI->connect("dbi:mysql:database=sequences_nevers;host=psoda2.cs.byu.edu","phylo","")
                        or die("Couldn't connect");
                my $SQL;
                my $select;
                my $sequence;
                
                $SQL= "select sequence from seqs where name='".param('species1')."';";
                $select = $dbh->prepare($SQL);
                $select->execute();
                $select->bind_columns(undef, \$sequence);
                $sequence =~ s/(^\s+|\s+$)//g;

                while($select->fetch()) {
                        print "Sequence 1: $sequence <br />";
                }

                my $SQL2;
                my $select2;
                my $sequence2;
                $SQL2= "select sequence from seqs where name='".param('species2')."';";
                $select2 = $dbh->prepare($SQL2);
                $select2->execute();
                $select2->bind_columns(undef, \$sequence2);

                $sequence2 =~ '/s{\s+}{}gxms/';
                while($select2->fetch()) {
                        print "Sequence 2: $sequence2 <br />";
                }

                if($sequence && $sequence2){

                        Alignment->gapcost(-2);
                        Alignment->align($sequence, $sequence2);
                }	
    }
}

sub print_tail {
	print "";
}
