"""Compute barcodes for an easy example.
"""
import homology as hom
import simpcells as sc
import points_to_complex as ptc


# compute cells:
a = sc.cell('a', [])
b = sc.cell('b', [])
c = sc.cell('c', [])
d = sc.cell('d', [])

ab = sc.cell('ab', [a, b])
bc = sc.cell('bc', [b, c])
cd = sc.cell('cd', [c, d])
ad = sc.cell('ad', [a, d])
ac = sc.cell('ac', [a, c])

acd = sc.cell('acd', [ac, cd, ad])
abc = sc.cell('abc', [ab, bc, ac])

# cell list:
K = [a, b, c, d, bc, ad, cd, ab, ac, acd, abc]

# add order:
a.order = 0
b.order = 0

c.order = 1
d.order = 1

bc.order = 1
ad.order = 1

cd.order = 2
ab.order = 2

ac.order = 3

acd.order = 4

abc.order = 5

# add dimension:
a.dimension = 0
b.dimension = 0
c.dimension = 0
d.dimension = 0

bc.dimension = 1
ad.dimension = 1
cd.dimension = 1
ab.dimension = 1
ac.dimension = 1

acd.dimension = 2
abc.dimension = 2

# sort cell list by order:
K = ptc.sort_by_order(K)  # should always be done if we work with the order

# compute homology:
hom.compute_homology(K, step2=False)

# get barcodes:
homology_list, gen = hom.get_barcodes(K)
print(homology_list)
for g in gen:
    for g2 in g[1]:
        print(g2.basisel)

# draw barcodes:
while True:
    number_dim = int(input('Which homology should be printed?'))
    hom.draw_barcode(homology_list, number_dim, K)
