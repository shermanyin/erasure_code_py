from gf_base2 import gf2

def print_tbl(rows, cols, val):
    """Prints a table of values given in val.
    
    rows: num of rows
    cols: num of cols
    val:  values to print in the form of list of lists
    """
    # Print column header
    print '  ',
    for c in xrange(cols):
        print format(c, '02x'),
    print

    for r in xrange(rows):
        print format(r, '02x'),
        for c in xrange(cols):
            print format(val[r][c], '02x'),
        print

if __name__ == "__main__":
    desc = ('This program calculates the addition and multiplication tables '
            'for GF(2^m) with the given generating polynomial, g(x). e.g., '
            'g(x) might be 11 for m=3 (x^3+x+1), or 283 for m=8.')

    print desc
    m = int(raw_input("Enter degree of GF field (m):").strip())
    g = int(raw_input("Enter coefficients of g(x):").strip())

    order = 2 ** m
    
    gf = gf2(m, g)

    """
    # Quick heck for doing mult in CLI
    while (1):
        a = int(raw_input("a:").strip())
        b = int(raw_input("b:").strip())
        print gf_mult(a,b)
    """
    add_tbl = [
        [gf.add(row, col) for col in xrange(order)]
        for row in xrange(order)
    ]
    print "Addition table:"
    print_tbl(order, order, add_tbl)
    print

    mult_tbl = [
        [gf.mult(row, col) for col in xrange(order)]
        for row in xrange(order)
    ]
    print "Multiplication table:"
    print_tbl(order, order, mult_tbl)
    print

    mult_inv = [0]
    for r in xrange(1, order):
        mult_inv.append(mult_tbl[r].index(1))
    print "Multiplicative inverses:"
    for i in xrange(1, order):
        print '{:02x}: {:02x}'.format(i, mult_inv[i])

