# This file is part of the pyMOR project (http://www.pymor.org).
# Copyright Holders: Rene Milk, Stephan Rave, Felix Schindler
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function

import numpy as np

from pymor.core.defaults import defaults


@defaults('raise_negative', 'tol')
def induced_norm(product, raise_negative=True, tol=1e-10):
    """The induced norm of a scalar product.

    The norm of a vector (an array of vectors) U is calculated by
    calling ::

        product.apply2(U, U, mu=mu, pairwise=True)

    In addition, negative norm squares of absolute value smaller
    than `tol` are clipped to `0`.
    If the `raise_negative` is `True`, a :exc:`ValueError` exception
    is raised if there are still negative norm squares afterwards.

    Parameters
    ----------
    product
        The scalar product for which the norm is to be calculated,
        given as a linear |Operator|.
    raise_negative
        If `True`, raise an exception if calcuated norm is negative.
    tol
        See above.

    Returns
    -------
    norm
        A function `norm(U, mu=None)` taking a |VectorArray| `U`
        as input together with the |Parameter| `mu` which is
        passed to the product.
    """

    def norm(U, mu=None):
        norm_squared = product.apply2(U, U, mu=mu, pairwise=True)
        if tol > 0:
            norm_squared = np.where(np.logical_and(0 > norm_squared, norm_squared > - tol),
                                    0, norm_squared)
        if raise_negative and np.any(norm_squared < 0):
            raise ValueError('norm is negative (square = {})'.format(norm_squared))
        return np.sqrt(norm_squared)

    return norm


def cat_arrays(vector_arrays):
    vector_arrays = list(vector_arrays)
    total_length = sum(map(len, vector_arrays))
    cated_arrays = vector_arrays[0].empty(vector_arrays[0].dim, reserve=total_length)
    for a in vector_arrays:
        cated_arrays.append(a)
    return cated_arrays
