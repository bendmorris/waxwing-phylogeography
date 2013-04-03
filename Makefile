all : bombycillidae.newick

bombycillidae.fasta: bombycilla.fasta phainopepla.fasta phainoptila.fasta
	cat bombycilla.fasta phainopepla.fasta phainoptila.fasta > bombycillidae.fasta

bombycillidae.aln: bombycillidae.fasta
	muscle -in bombycillidae.fasta -out bombycillidae.aln

bombycillidae.phy: bombycillidae.aln
	python -c "import Bio.AlignIO as aio; aio.convert('bombycillidae.aln','fasta','bombycillidae.phy','phylip')"

bombycillidae.newick: bombycillidae.phy
	rm RAxML_*.bombycillidae; \
	raxmlHPC -m GTRCAT -n bombycillidae -p 10000 -s bombycillidae.phy; \
	mv RAxML_result.bombycillidae bombycillidae.newick