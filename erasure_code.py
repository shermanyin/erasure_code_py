from gf_base2 import gf2

class ErasureCode:
    def __init__(self, k, p):
        """Sets up an object to compute the parity symbols for erasure codes.

        The total number of bytes after the EC process is n = k + m, where

        k: number of source bytes
        m: number of parity bytes to generate
        """
        self.k = k
        self.p = p
        self.n = k + p

        # Using GF(2^8) with 0x11b as g(x)
        self.gf = gf2(8, 283)

        self.encoding_matrix = self.rs_matrix_gen()

    @staticmethod
    def identity_matrix_gen(n):
        res = []
        for r in xrange(n):
            row = [1 if c == r else 0 for c in xrange(n)]
            res.append(row)
        return res

    def rs_matrix_gen(self):
        """Generate an RS matrix to be used as the encoding matrix.
        
        According to Intel's ISA-L code, this matrix is the identity matrix
        followed by an m by k matrix where the values are
            2 ** (r-k * c)
        for r:{k,n-1}, c:{0,k-1}.

        Note there is a descrepency between the header description and code in
        their library.

        Returns an n x k matrix
        """
        # Identity matrix portion
        mat = self.identity_matrix_gen(self.k)

        # Remaining portion
        for r in xrange(self.p):
            row = [self.gf.pow(2, (r * c)) for c in xrange(self.k)]
            mat.append(row)

        return mat

    @staticmethod
    def matrix_print(mat):
        """Prints the given matrix

        mat: matrix to print, in the form of list of rows
        """
        rows = len(mat)
        cols = len(mat[0])

        # Print column header
        print '  ',
        for c in xrange(cols):
            print format(c, '02x'),
        print

        for r in xrange(rows):
            print format(r, '02x'),
            for c in xrange(cols):
                print format(mat[r][c], '02x'),
            print

    def dot_prod(self, a, b, row, col):
        res = 0

        num_terms = len(a[row])
        for i in xrange(num_terms):
            prod = self.gf.mult(a[row][i], b[i][col])
            res = self.gf.add(res, prod)

        return res

    def matrix_mult(self, a, b):
        a_rows = len(a)
        a_cols = len(a[0])
        b_rows = len(b)
        b_cols = len(b[0])

        try:
            res = []

            for r in xrange(a_rows):
                row = []
                for c in xrange(b_cols):
                    row.append(self.dot_prod(a, b, r, c))
                res.append(row)

            return res

        except IndexError:
            msg = (
                'Invaid matrix multiplication. Cannot multiply ({} x {}) '
                'matrix by ({} x {}) matrix.'
                    .format(a_rows, a_cols, b_rows, b_cols)
            )
            raise ValueError(msg)

    @staticmethod
    def matrix_transpose(a):
        # new dimenions
        rows = len(a[0])
        cols = len(a)

        res = []
        for r in xrange(rows):
            row = []
            for c in xrange(cols):
                row.append(a[c][r])
            res.append(row)

        return res

    def encode(self, src):
        """Generate parity bytes for Erasure Code

        src: a list of source bytes, length should be same as k set during
             object initialization.

        returns: a list of p parity bytes, set during object initialization.
        """
        # Take the bottom portion of encoding matrix to generate the parity
        # bytes
        partial_mat = self.encoding_matrix[self.k:]

        # Make src into a matrix (list of lists)
        src_trans = self.matrix_transpose([src])

        parity = self.matrix_mult(partial_mat, src_trans)
        parity_trans = self.matrix_transpose(parity)

        return parity_trans[0]

    @staticmethod
    def matrix_swap_rows(a, row1, row2):
        temp = a[row1]
        a[row1] = a[row2]
        a[row2] = temp

    def matrix_inv(self, a):
        # Make a copy of the matrix so it is not modified
        orig = [row[:] for row in a]
        dimension = len(orig)
        res = self.identity_matrix_gen(dimension)

        for i in xrange(dimension):
            # if the pivot is zero, try to find another row to swap
            if orig[i][i] == 0:
                for j in xrange(i + 1, dimension):
                    if orig[j][i] != 0:
                        self.matrix_swap_rows(orig, i, j)
                        self.matrix_swap_rows(res, i, j)
                        break

            # If there are no rows with non-zero element in ith column
            if orig[i][i] == 0:
                print 'Cannot find inverse for the following matrix:'
                self.matrix_print(a)
                raise ValueError

            # Scale row so pivot is 1
            inv = self.gf.mult_inv(orig[i][i])
            orig[i] = [self.gf.mult(c, inv) for c in orig[i]]
            res[i] = [self.gf.mult(c, inv) for c in res[i]]

            # Zero out the ith column in other rows
            for j in xrange(dimension):
                # Skip the current row
                if j == i:
                    continue

                scale = orig[j][i]
                orig[j] = [self.gf.add(self.gf.mult(scale, e_i), e_j) for e_i, e_j in zip(orig[i], orig[j])]
                res[j] = [self.gf.add(self.gf.mult(scale, e_i), e_j) for e_i, e_j in zip(res[i], res[j])]

        return res

    def decode(self, data):
        """Calculate the original src data.

        data: list of received bytes, in the same order as original EC encoding.
              Lost bytes identified by 'None' in the list. List length must be
              n, which is k + p
        returns: list of original data, length is k. 
        """
        # Create the submatrix to be inversed and the data matrix at the same
        # time.
        mat = []
        ec_data = []
        num_bytes = 0
        for i in xrange(self.n):
            if data[i] is not None:
                # Add the corresponding row from the encoding matrix
                mat.append(self.encoding_matrix[i])
                # construct the n x 1 matrix to multiply
                ec_data.append([data[i]])
                num_bytes += 1

                # We only need first k bytes
                if num_bytes == self.k:
                    break

        if num_bytes < self.k:
            msg = (
                'Not enough received bytes to reconstruct original data. '
                'Only {} bytes received, but requires at least {} bytes.'
                    .format(num_bytes, self.k)
            )
            raise ValueError(msg)

        # Inverse matrix
        mat_inv = self.matrix_inv(mat)

        # Multiply matrix
        orig = self.matrix_mult(mat_inv, ec_data)
        orig_trans = self.matrix_transpose(orig)

        return orig_trans[0]


if __name__ == '__main__':
    #k = int(raw_input("Enter number of source bytes to encode (k): ").strip())
    #p = int(raw_input("Enter number of parity bytes to generate (m): ").strip())

    k = 4
    p = 4
    ec = ErasureCode(k, p)
    #ec.matrix_print(ec.encoding_matrix)
    a = ec.encode([11, 22, 33, 44])
    print a
    b = ec.decode([None, 22, 33, 44, None, 216])
    print b