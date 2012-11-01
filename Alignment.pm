use Matrix;

package Alignment;

@EXPORT = qw (new, gapcost, align);
#my $cost;

sub new {
	my $class = shift;
	my $self = {};
	$self->{GAPCOST} = undef;
	bless($self,$class);
	return $self;
}

sub gapcost {
	my $self = shift;
	if (@_) { $self->{GAPCOST} = shift }
	#print "\nIn GapCost: $cost<br/>\n";
	return $self->{GAPCOST};
}

sub align {
	my $self = shift;
	my ($sequence1, $sequence2) = @_; 

	my $cost = $self->{GAPCOST};
	my @matrix = Matrix->createMatrix($sequence1, $sequence2, $cost);
	Matrix->nextStep();
	
	return $sequence1 . "<br/>\n" . $sequence2 . "<br/>\n";
}
