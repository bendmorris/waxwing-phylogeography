import Bio.Phylo as bp

samples = {}

with open('bombycillidae.fasta') as input_file:
    for line in input_file:
        if line[0] == '>':
            parts = line[1:].strip().split('.')
            sample_name = '.'.join(parts[:2])
            species_name = ' '.join(parts[2:])
            samples[sample_name] = species_name


with open('bombycillidae.newick') as tree_file:
    tree_string = tree_file.read()

for sample, name in samples.iteritems():
    tree_string = tree_string.replace(sample, "'%s'" % name)

tree = bp.NewickIO.Parser.from_string(tree_string).parse().next()
bp._utils.draw_ascii(tree)

cedars = tree.find_elements('Bombycilla cedrorum')
cedar_root = bp.Newick.Tree(root=tree.common_ancestor(cedars))
cedar_root.root.branch_length = 0
bp._utils.draw_ascii(cedar_root)

bohemians = tree.find_elements('Bombycilla garrulus')
bohemian_root = bp.Newick.Tree(root=tree.common_ancestor(bohemians))
bohemian_root.root.branch_length = 0
bp._utils.draw_ascii(bohemian_root)