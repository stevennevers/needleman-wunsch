use Entry;

my $row;
my $column;
my @matrix;

package Matrix;

@EXPORT = qw (createMatrix, nextStep);

sub createMatrix {
	my $class = shift;
	my ($rowHeaders, $columnHeaders, $cost) = @_; 
	print "Creating matrix...<br/>\n";

	$row = length($rowHeaders);
	$column = length($columnHeaders);
	
	my $entry;
	my $alignmentScore;
	my $nuc;
	my $up;
	my $left;
	my $diagonal;
	my $source;
	
# 	store entry
	for(my $t = $row; $t >= 0; $t--) {
	
		for(my $l = $column; $l >= 0; $l--){
			$entry = Entry->new();
			if($t == 0){
				$entry->score($cost * $l);
				if($l > 0 ){
					$nuc = substr($columnHeaders,$l-1,1);
					$entry->source($nuc);
				}
				
			}
			if($l == 0){
				$entry->score($cost * $t);
				if($t > 0){
					$nuc = substr($rowHeaders,$t-1,1);
					$entry->source($nuc);
				}
			}
			
			$matrix[$t][$l] = $entry;
		}
	}
	
	for(my $t = 1; $t <= $row; $t++) {
		for(my $l = 1; $l <= $column; $l++){
		
			$up = $matrix[$t-1][$l]->score() + $cost;
			$left = $matrix[$t][$l-1]->score() + $cost;
			#print " up: $up";
			
			#print " left: $left";
			$diagonal = $matrix[$t-1][$l-1]->score();
			
			if($matrix[0][$l]->source() eq $matrix[$t][0]->source()){
				$diagonal += 2;
			} else{
				$diagonal += -1;
			}
			#source is -1 if from up, 0 from diagonal, and 1 from left
			
			$alignmentScore = $up;
			$source = -1;
			if($alignmentScore <= $left){
				$alignmentScore = $left;
				$source = 1;
			}
			if($alignmentScore <= $diagonal){
				$alignmentScore = $diagonal;
				$source = 0;
			}
			
			$matrix[$t][$l]->score($alignmentScore);
			$matrix[$t][$l]->source($source);
		}
	}
	
	print "\n";
	my $i = 0;
	my $j = 0;
	
}

#entry object will have score and source
#source is -1 if from up, 0 from diagonal, and 1 from left
sub nextStep {
	
	print "Performing Alignment...<br/>\n";
	my $i = $row;
	my $j = $column;
	my @align1;
	my @align2;
	my @alignMid;
	my $src = $matrix[$i][$j]->source();
	
	#retracing the matrix
	while($i > 0 || $j >0){	
		
		unshift(@alignMid, '*');
		if($src eq -1){#source is up
			unshift(@align1, $matrix[$i][0]->source());
			unshift(@align2, '-');
			$i--;
			
		}elsif($src eq 1){#source is left
			unshift(@align1, '-');
			unshift(@align2, $matrix[0][$j]->source());
			$j--;
			
		}elsif($src eq 0){#source is diag
			unshift(@align1, $matrix[$i][0]->source());
			unshift(@align2, $matrix[0][$j]->source());
			$i--;
			$j--;
			
		}else{ #source is from edge
			
			if($i eq 0){#source is left
				unshift(@align1, '-');
				unshift(@align2, $matrix[0][$j]->source());
				$j--;
			}elsif($j eq 0){#source is up
				
				unshift(@align1, $matrix[$i][0]->source());
				unshift(@align2, '-');
				$i--;
			}
		
		}
		$src = $matrix[$i][$j]->source();
	}
	
	print "Needleman-Wunsch Alignment: <b>";
	print @align2; print "</b><br/>";
	
	print "Alignment Score: " . $matrix[$row][$column]->score();
}
