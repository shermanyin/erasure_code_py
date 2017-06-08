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

def gf_add(x, y):
    return x ^ y

def gf_mult(x, y, m, g):
    """Multiplication in GF(2^m)

    x: operand
    y: operand
    m: degree of GF
    g: generating polynomial used for reduction. Must be degree m.
    """
    prod = 0

    # Multiply
    while x:
        if x & 1:
            prod ^= y
        x >>= 1
        y <<= 1

    # Reduce by g(x)
    g_msb = 1 << m

    for i in xrange(m-2, -1, -1):
        if (prod & g_msb << i):
            prod ^= g << i

    return prod


if __name__ == "__main__":
    desc = ('This program calculates the addition and multiplication tables '
            'for GF(2^m) with the given generating polynomial, g(x). e.g., '
            'g(x) might be 11 for m=3 (x^3+x+1), or 283 for m=8.')

    print desc
    m = int(raw_input("Enter degree of GF field (m):").strip())
    g = int(raw_input("Enter coefficients of g(x):").strip())

    num_elements = 2 ** m
    
    # g(x) must be of degree m
    if ((g >> m) != 1):
        print 'Incorrect g(x)={} for degree m={}:'.format(g, m)
        exit(1)

    """
    # Quick heck for doing mult in CLI
    while (1):
        a = int(raw_input("a:").strip())
        b = int(raw_input("b:").strip())
        print gf_mult(a,b)
    """
    add_tbl = [
        [gf_add(row, col) for col in xrange(num_elements)]
        for row in xrange(num_elements)
    ]
    print "Addition table:"
    print_tbl(num_elements, num_elements, add_tbl)
    print

    mult_tbl = [
        [gf_mult(row, col, m, g) for col in xrange(num_elements)]
        for row in xrange(num_elements)
    ]
    print "Multiplication table:"
    print_tbl(num_elements, num_elements, mult_tbl)
    print

    mult_inv = [0]
    for r in xrange(1, num_elements):
        mult_inv.append(mult_tbl[r].index(1))
    print "Multiplicative inverses:"
    for i in xrange(1, num_elements):
        print '{:02x}: {:02x}'.format(i, mult_inv[i])

