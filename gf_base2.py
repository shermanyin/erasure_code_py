class gf2:
    def __init__(self, m, g):
        """ Initialize object for GF(2^m) calculations.

        m: degree of GF field (usually number of bits)
        g: irreducible polynomial g(x) for multiplication reduction.  Specify
           the coefficients only.  eg. 11 for m=3 (x^3+x+1), or 283 for m=8.
           Highest degree must be m.
        """
        # g(x) must be of degree m
        if ((g >> m) != 1):
            msg = (
                'Incorrect value for g(x) = {}.  Highest degree of g(x) must '
                'be equal to m ({}). Initialization failed.'.format(g, m)
            )
            raise ValueError(msg)

        self.m = m
        self.g = g
        self.order = 2 ** m

        # Using log and exp tables for calculations is faster, but would require
        # the knowledge of a generator for the particular m.  Here we just
        # calculate the multiplication table manually.
        self.mult_tbl = [
            [self.long_mult(row, col) for col in xrange(self.order)]
            for row in xrange(self.order)
        ]

        # Multiplicative inverses.  Inverse for 0 is undefined but we record a
        # 'None' here to make indexing more intuitive.
        self.mult_inv_tbl = [ None ]
        for row in xrange(1, self.order):
            self.mult_inv_tbl.append(self.mult_tbl[row].index(1))

    def add(self, x, y):
        return x ^ y

    def mult(self, x, y):
        return self.mult_tbl[x][y]

    def add_inv(self, x):
        return x

    def mult_inv(self, x):
        return self.mult_inv_tbl[x]

    def long_mult(self, x, y):
        prod = 0

        # Multiply
        while x:
            if x & 1:
                prod ^= y
            x >>= 1
            y <<= 1

        # Reduce by g(x)
        g_msb = 1 << self.m

        for i in xrange(self.m - 2, -1, -1):
            if (prod & g_msb << i):
                prod ^= self.g << i

        return prod
