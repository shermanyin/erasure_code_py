from random import randint, shuffle
from unittest import TestCase

from erasure_code import ErasureCode

num_tests = 1000

class TestErasureCode(TestCase):
    def test_random(self):
        for k in [4, 8, 12, 16, 32]:
            for p in [2, 4, 8]:

                print 'Testing k = {}, p = {}.'.format(k, p)

                ec = ErasureCode(k, p)
                passed = 0

                for i in xrange(num_tests):
                    # Generate k random input bytes
                    input = [randint(0, 255) for _ in xrange(k)]

                    # Generate parity bytes
                    parity = ec.encode(input)

                    code = input + parity

                    # Loose p random bytes
                    idx = range(k + p)
                    shuffle(idx)
                    for j in xrange(p):
                        code[idx[j]] = None

                    recover = ec.decode(code)

                    if (recover != input):
                        print 'Input was {} but recovered {}'.format(input, recover)
                        print '{} of {} passed up to this point.'.format(passed, num_tests)
                        raise AssertionError

                    passed += 1

                print '{} of {} tests passed.'.format(passed, num_tests)