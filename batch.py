import coef as c

# 2-16 data (k)
# 1-4 parity (m)

for k in xrange(2,17):
    for m in xrange(1,5):
        print "="*80
        print "Matrix for data = {}, parity = {}".format(k, m)
        coef = c.gf_gen_rs_matrix(m, k)
        c.print_matrix(coef)
        print 


