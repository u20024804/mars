#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2018 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

from .... import operands
from .core import TensorRandomOperandMixin, handle_array


class TensorNoncentralChisquare(operands.NoncentralChisquare, TensorRandomOperandMixin):
    __slots__ = '_df', '_nonc', '_size'
    _input_fields_ = ['_df', '_nonc']

    def __init__(self, size=None, state=None, dtype=None, gpu=None, **kw):
        dtype = np.dtype(dtype) if dtype is not None else dtype
        super(TensorNoncentralChisquare, self).__init__(_size=size, _state=state, _dtype=dtype,
                                                        _gpu=gpu, **kw)

    def __call__(self, df, nonc, chunks=None):
        return self.new_tensor([df, nonc], None, raw_chunks=chunks)


def noncentral_chisquare(random_state, df, nonc, size=None, chunks=None, gpu=None, **kw):
    r"""
    Draw samples from a noncentral chi-square distribution.

    The noncentral :math:`\chi^2` distribution is a generalisation of
    the :math:`\chi^2` distribution.

    Parameters
    ----------
    df : float or array_like of floats
        Degrees of freedom, should be > 0.
    nonc : float or array_like of floats
        Non-centrality, should be non-negative.
    size : int or tuple of ints, optional
        Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
        ``m * n * k`` samples are drawn.  If size is ``None`` (default),
        a single value is returned if ``df`` and ``nonc`` are both scalars.
        Otherwise, ``mt.broadcast(df, nonc).size`` samples are drawn.
    chunks : int or tuple of int or tuple of ints, optional
        Desired chunk size on each dimension
    gpu : bool, optional
        Allocate the tensor on GPU if True, False as default

    Returns
    -------
    out : Tensor or scalar
        Drawn samples from the parameterized noncentral chi-square distribution.

    Notes
    -----
    The probability density function for the noncentral Chi-square
    distribution is

    .. math:: P(x;df,nonc) = \sum^{\infty}_{i=0}
                           \frac{e^{-nonc/2}(nonc/2)^{i}}{i!}
                           \P_{Y_{df+2i}}(x),

    where :math:`Y_{q}` is the Chi-square with q degrees of freedom.

    In Delhi (2007), it is noted that the noncentral chi-square is
    useful in bombing and coverage problems, the probability of
    killing the point target given by the noncentral chi-squared
    distribution.

    References
    ----------
    .. [1] Delhi, M.S. Holla, "On a noncentral chi-square distribution in
           the analysis of weapon systems effectiveness", Metrika,
           Volume 15, Number 1 / December, 1970.
    .. [2] Wikipedia, "Noncentral chi-square distribution"
           http://en.wikipedia.org/wiki/Noncentral_chi-square_distribution

    Examples
    --------
    Draw values from the distribution and plot the histogram

    >>> import matplotlib.pyplot as plt
    >>> import mars.tensor as mt
    >>> values = plt.hist(mt.random.noncentral_chisquare(3, 20, 100000).execute(),
    ...                   bins=200, normed=True)
    >>> plt.show()

    Draw values from a noncentral chisquare with very small noncentrality,
    and compare to a chisquare.

    >>> plt.figure()
    >>> values = plt.hist(mt.random.noncentral_chisquare(3, .0000001, 100000).execute(),
    ...                   bins=mt.arange(0., 25, .1).execute(), normed=True)
    >>> values2 = plt.hist(mt.random.chisquare(3, 100000).execute(),
    ...                    bins=mt.arange(0., 25, .1).execute(), normed=True)
    >>> plt.plot(values[1][0:-1], values[0]-values2[0], 'ob')
    >>> plt.show()

    Demonstrate how large values of non-centrality lead to a more symmetric
    distribution.

    >>> plt.figure()
    >>> values = plt.hist(mt.random.noncentral_chisquare(3, 20, 100000).execute(),
    ...                   bins=200, normed=True)
    >>> plt.show()
    """
    if 'dtype' not in kw:
        kw['dtype'] = np.random.RandomState().noncentral_chisquare(
            handle_array(df), handle_array(nonc), size=(0,)).dtype
    size = random_state._handle_size(size)
    op = TensorNoncentralChisquare(size=size, state=random_state._state, gpu=gpu, **kw)
    return op(df, nonc, chunks=chunks)
