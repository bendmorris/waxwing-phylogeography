gene = cytb

all : bombycillidae_$(gene).png

.PHONY : clean
clean :
	-rm -f RAxML_* bombycillidae_*.aln bombycillidae_*.phy bombycillidae_*.newick

.SECONDARY:

.SECONDEXPANSION:
bombycillidae_$(gene).fasta: *_$(gene).fasta
	cat $^ > $@

bombycillidae_$(gene).aln: bombycillidae_$(gene).fasta
	muscle -in $< -out $@

bombycillidae_$(gene).phy: bombycillidae_$(gene).aln
	python -c "import Bio.AlignIO as aio; aio.convert('$<','fasta','$@','phylip')"

bombycillidae_$(gene).newick: bombycillidae_$(gene).phy
	rm -f RAxML_*.bombycillidae; \
	raxmlHPC -m GTRCAT -n bombycillidae -p 10000 -s $<; \
	mv RAxML_result.bombycillidae $@

bombycillidae_$(gene).png: bombycillidae_$(gene).newick draw_tree.py sample_locations bombycillidae_$(gene).fasta
	python draw_tree.py $(gene) $@

filled_sample_locations: sample_locations get_location.py fill_sample_locations.py
	python fill_sample_locations.py > filled_sample_locations

sample_map.png: filled_sample_locations sample_map.py
	python sample_map.py sample_map.png
