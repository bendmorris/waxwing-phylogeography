all : bombycillidae.png

.PHONY : clean
clean :
	-rm -f RAxML_* bombycillidae.*

.SECONDARY:

.SECONDEXPANSION:
bombycillidae.fasta: *_co1.fasta
	cat $^ > $@

bombycillidae.aln: bombycillidae.fasta
	muscle -in $< -out $@

bombycillidae.phy: bombycillidae.aln
	python -c "import Bio.AlignIO as aio; aio.convert('$<','fasta','$@','phylip')"

bombycillidae.newick: bombycillidae.phy
	rm -f RAxML_*.bombycillidae; \
	raxmlHPC -m GTRCAT -n bombycillidae -p 10000 -s $<; \
	mv RAxML_result.bombycillidae $@

bombycillidae.png: bombycillidae.newick draw_tree.py sample_locations bombycillidae.fasta
	python draw_tree.py $@