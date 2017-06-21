from random import randint, shuffle
import sys
from unittest import TestCase

from erasure_code import ErasureCode

num_tests = 1000


class TestExhaustiveErasureCode(TestCase):
    def test_k2p1(self):
        self.verify_decode(2, 1)

    def test_k4p1(self):
        self.verify_decode(4, 1)

    @staticmethod
    def combination(n, k):
        """ N Choose K """
        def construct_comb(res, idx):

            # if the res list has k elements, we've found a combination
            if len(res) == k:
                yield res
                return

            # if we've reached the n'th index, return
            if idx >= n:
                return

            # include current index then move to next index
            res.append(idx)
            for i in construct_comb(res, idx + 1):
                yield i

            # exclude current index then move to next index
            res.remove(idx)
            for i in construct_comb(res, idx + 1):
                yield i

        comb = []

        for i in construct_comb(comb, 0):
            yield i

    def verify_decode(self, k, p):
        print 'Testing k = {}, p = {}...'.format(k, p)

        ec = ErasureCode(k, p)
        n = k + p
        passed = 0
        inv_err = 0
        result_err = 0
        iter = 0

        # Generate all combinations of k bytes data
        for i in xrange(2 ** (k * 8)):
            data_in = []

            # Split the bytes
            for byte in xrange(k):
                data_in.insert(0, i >> (8 * byte) & 0xff)

            # Generate parity bytes
            parity = ec.encode(data_in)

            data_out = data_in + parity

            # Check all possible number of lost bytes (1..p)
            for num_loss_bytes in xrange(1, p + 1):

                # For each combination
                for comb in self.combination(n, num_loss_bytes):
                    # Make a copy of data_out
                    data_received = data_out[:]

                    # Set each loss byte to 'None'
                    for idx in comb:
                        data_received[idx] = None

                    try:
                        iter += 1
                        recover = ec.decode(data_received)
                    except ValueError:
                        inv_err += 1
                        continue

                    if recover != data_in:
                        print 'Input was {} but recovered {}'.format(data_in, recover)
                        result_err += 1
                        continue

                    passed += 1

        print 'Completed {} iterations.'.format(iter)
        print '{} passed, {} inv_err, {} result_err'.format(passed, inv_err, result_err)

        if inv_err or result_err:
            self.fail()


class TestRandomErasureCode(TestCase):

    def test_k4p2(self):
        self.verify_decode(4, 2, 1000)

    def test_k4p4(self):
        self.verify_decode(4, 4, 1000)

    def test_k8p2(self):
        self.verify_decode(8, 2, 1000)

    def test_k8p4(self):
        self.verify_decode(8, 4, 1000)

    def test_k8p8(self):
        self.verify_decode(8, 8, 1000)

    def test_k16p2(self):
        self.verify_decode(16, 2, 1000)

    def test_k16p4(self):
        self.verify_decode(16, 4, 1000)

    def test_k16p8(self):
        self.verify_decode(16, 8, 1000)

    def test_k16p16(self):
        self.verify_decode(16, 16, 1000)

    def test_k32p2(self):
        self.verify_decode(32, 2, 1000)

    def test_k32p4(self):
        self.verify_decode(32, 4, 1000)

    def test_k32p8(self):
        self.verify_decode(32, 8, 1000)

    def test_k32p16(self):
        self.verify_decode(32, 16, 1000)

    def test_k32p32(self):
        self.verify_decode(32, 32, 1000)

    def verify_decode(self, k, p, cycles):
        print 'Testing k = {}, p = {}, {} times...'.format(k, p, cycles)

        ec = ErasureCode(k, p)
        passed = 0
        inv_err = 0
        result_err = 0

        for i in xrange(num_tests):
            # Generate k random data_in bytes
            data_in = [randint(0, 255) for _ in xrange(k)]

            # Generate parity bytes
            parity = ec.encode(data_in)

            data_out = data_in + parity

            # Loose p random bytes
            idx = range(k + p)
            shuffle(idx)
            for j in xrange(p):
                data_out[idx[j]] = None

            try:
                recover = ec.decode(data_out)
            except ValueError:
                inv_err += 1
                continue

            if recover != data_in:
                print 'Input was {} but recovered {}'.format(data_in, recover)
                result_err += 1
                continue

            passed += 1

        print '{} passed, {} inv_err, {} result_err'.format(passed, inv_err, result_err)

        if passed != cycles:
            self.fail()