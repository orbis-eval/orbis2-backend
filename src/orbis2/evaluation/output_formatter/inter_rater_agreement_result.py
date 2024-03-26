from collections import namedtuple

InterRaterAgreementResult = namedtuple('InterRaterAgreement', 'kappa_micro kappa_macro '
                                                              'average_macro_f1 average_micro_f1')
