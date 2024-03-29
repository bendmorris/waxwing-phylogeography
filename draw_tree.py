''' 
Usage: python draw_tree.py [image_file.png]

If run without arguments, the result will be printed to stdout instead of 
saving as an image file.
'''
import Bio.Phylo as bp
import sys

try:
    gene = sys.argv[1]
    filename = sys.argv[2]
    draw_to_file = True

    def draw(x, y=''):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12,6))
        axes = plt.axes(frameon=False)
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        bp.draw(x, do_show=False, axes=axes)
        base, extension = '.'.join(filename.split('.')[:-1]), filename.split('.')[-1]
        plt.savefig(base + y + '.' + extension)
except:
    gene = 'co1'
    draw = lambda x, y='': bp.draw_ascii(x)
    draw_to_file = False

samples = {}
locations = {}
with open('bombycillidae_%s.fasta' % gene) as input_file:
    for line in input_file:
        if line[0] == '>':
            parts = line[1:].strip().split('.')
            sample_name = '.'.join(parts[:2])
            species_name = ' '.join(parts[2:])
            samples[sample_name] = species_name
with open('sample_locations') as input_file:
    for line in input_file:
        line = line.strip()
        if not line: continue
        sample_name, _, location = line.split(':')[:3]
        locations[sample_name] = location


with open('bombycillidae_%s.newick' % gene) as tree_file:
    tree_string = tree_file.read()

for sample, name in samples.iteritems():
    tree_string = tree_string.replace(sample, "'%s'" % (name + 
        (' (%s)' % (locations[sample]) if sample in locations 
                                       else '')))

tree = bp.NewickIO.Parser.from_string(tree_string).parse().next()
tree.name = 'Bombycillidae'
tree.root_at_midpoint()
draw(tree)

for subtree_name, extn in (('Bombycilla cedrorum', '_cedar'), ('Bombycilla garrulus', '_bohemian')):
    matches = tree.find_elements(lambda x: x.name.startswith(subtree_name))
    subtree = bp.Newick.Tree(root=tree.common_ancestor(matches))
    subtree.name = subtree_name
    subtree.root.branch_length = 0
    subtree.root_at_midpoint()
    draw(subtree, extn)
