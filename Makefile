all : bombycillidae_co1.png bombycillidae_cytb.png

clean :
	rm RAxML_* *.aln *.phy *.phy.reduced *.newick *.png

.SECONDEXPANSION:
bombycillidae_%.fasta: $$(wildcard *_$$*.fasta)
	cat $^ > $@

bombycillidae_%.aln: bombycillidae_%.fasta
	muscle -in $< -out $@

bombycillidae_%.phy: bombycillidae_%.aln
	python -c "import Bio.AlignIO as aio; aio.convert('$<','fasta','$@','phylip')"

bombycillidae_%.newick: bombycillidae_%.phy
	rm RAxML_*.bombycillidae_$*; \
	raxmlHPC -m GTRCAT -n bombycillidae_$* -p 10000 -s $<; \
	mv RAxML_result.bombycillidae_$* $@

bombycillidae_%.png: bombycillidae_%.newick draw_tree.py
	python draw_tree.py $* $@