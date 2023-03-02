import numpy as np


def kappa_metric(table):
    """A modified Kappa for text annotation tasks based on statsmodels.stats.

    Parameters:
        table : array_like, 2-D
            assumes subjects in rows, and categories in columns

    Return:
        kappa : float
            A modified version of the Fleiss' Kappa which does not correct for random agreement among raters (which
            is highly unlikely in text annotation tasks.

    References
    ----------
    Wikipedia https://en.wikipedia.org/wiki/Fleiss%27_kappa
    """
    # avoid integer division
    table = 1.0 * np.asarray(table)
    n_sub, n_cat = table.shape
    n_total = table.sum()
    n_rater = table.sum(1)
    n_rat = n_rater.max()
    # assume fully ranked
    assert n_total == n_sub * n_rat

    # marginal frequency  of categories
    p_cat = table.sum(0) / n_total

    table2 = table * table
    p_rat = (table2.sum(1) - n_rat) / (n_rat * (n_rat - 1.))
    return p_rat.mean()
