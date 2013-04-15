#!/usr/bin/perl



#input for the FASTA file to be analyzed
my $file = $ARGV[0];
my $fileName = $ARGV[1];

#open the file input from the command line
open (INPUT, $file) || die "could not open file";

#read all the lines and store into an array and then close the file
@linesArray = <INPUT>;
close(INPUT);

foreach $line (@linesArray){
	#print "$line";
	if($line =~ /\>/){
		#print $line;
		@aNum = split(/gb\||emb\||dbj\|/, $line);
		@aNum = split(/\|/, $aNum[1]);
		
		$name= $aNum[1];
		#print $name;
		$name = join( '.', split(/\s/, $name, 4));
		@name = split(/\s/, $name);
		$fastaName = join('',$aNum[0],$name[0], "\n");
		$fastaName=join('','>',$fastaName);
		$line = $fastaName;
		}
}

$outFileStr = ">" . $fileName;
open(OUTFILE, $outFileStr);
print OUTFILE @linesArray;
