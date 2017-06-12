class gf2:
    def __init__(self, m, g):
        """ Initialize object for GF(2^m) calculations.

        m: degree of GF field (usually number of bits)
        g: irreducible polynomial g(x) for multiplication reduction.  Specify
           the coefficients only.  eg. 11 for m=3 (x^3+x+1), or 283 for m=8.
           Highest degree must be m.
        """
        self.m = m
        self.g = g

        # g(x) must be of degree m
        if ((g >> m) != 1):
            print 'Incorrect g(x)={} for degree m={}:'.format(g, m)
            print 'Initialization failed.'
            exit(1)

    def add(self, x, y):
        return x ^ y

    def mult(self, x, y):
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
