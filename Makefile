all : bombycillidae.png

bombycillidae.fasta: $(wildcard *_co1.fasta)
	cat *_co1.fasta > bombycillidae.fasta

bombycillidae.aln: bombycillidae.fasta
	muscle -in bombycillidae.fasta -out bombycillidae.aln

bombycillidae.phy: bombycillidae.aln
	python -c "import Bio.AlignIO as aio; aio.convert('bombycillidae.aln','fasta','bombycillidae.phy','phylip')"

bombycillidae.newick: bombycillidae.phy
	rm RAxML_*.bombycillidae; \
	raxmlHPC -m GTRCAT -n bombycillidae -p 10000 -s bombycillidae.phy; \
	mv RAxML_result.bombycillidae bombycillidae.newick

bombycillidae.png: bombycillidae.newick draw_tree.py
	python draw_tree.py bombycillidae.png