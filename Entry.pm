package Entry;

@EXPORT = qw (new, score, source);

sub new {
	my $class = shift;
	my $self = {};
	$self->{SCORE} = undef;
	$self->{SOURCE} = undef;
	bless($self,$class);
	return $self;
}

#return score for that place in matrix
sub score {
	my $self = shift;
	if (@_) { $self->{SCORE} = shift }
	return $self->{SCORE};
}

# return source of matrix
# 1 from up, 0 from diagonal, -1 from left
sub source {
	my $self = shift;
	if (@_) { $self->{SEQUENCE} = shift }
	return $self->{SEQUENCE};
}
