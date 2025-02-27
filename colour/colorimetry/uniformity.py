# -*- coding: utf-8 -*-
"""
Spectral Uniformity
===================

Defines the objects to compute the *spectral uniformity*
(or *spectral flatness*) of spectral distributions.

References
----------
-   :cite:`David2015a` : David, A., Fini, P. T., Houser, K. W., Ohno, Y.,
    Royer, M. P., Smet, K. A. G., Wei, M., & Whitehead, L. (2015). Development
    of the IES method for evaluating the color rendition of light sources.
    Optics Express, 23(12), 15888. doi:10.1364/OE.23.015888
"""

import numpy as np

from colour.colorimetry import sds_and_msds_to_msds

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['spectral_uniformity']


def spectral_uniformity(sds):
    """
    Computes the *spectral uniformity* (or *spectral flatness*) of given
    spectral distributions.

    Parameters
    ----------
    sds : array_like or MultiSpectralDistributions
        Spectral distributions or multi-spectral distributions to
        compute the spectral uniformity of. `sds` can be a single
        :class:`colour.MultiSpectralDistributions` class instance, a list
        of :class:`colour.MultiSpectralDistributions` class instances or a
        list of :class:`colour.SpectralDistribution` class instances.

    Returns
    -------
    ndarray
        Spectral uniformity.

    Warnings
    --------
    The spectral distributions must have the same spectral shape.

    References
    ----------
    :cite:`David2015a`

    Examples
    --------
    >>> from colour.quality.datasets import SDS_TCS
    >>> spectral_uniformity(SDS_TCS.values())  # doctest: +ELLIPSIS
    array([  9.5514285...e-06,   1.1482142...e-05,   1.8784285...e-05,
             2.8711428...e-05,   3.1971428...e-05,   3.2342857...e-05,
             3.3850000...e-05,   3.9925714...e-05,   4.1333571...e-05,
             2.4002142...e-05,   5.7621428...e-06,   1.4757142...e-06,
             9.7928571...e-07,   2.0057142...e-06,   3.7157142...e-06,
             5.7678571...e-06,   7.5557142...e-06,   7.4635714...e-06,
             5.7492857...e-06,   3.8692857...e-06,   3.5407142...e-06,
             4.4742857...e-06,   5.6435714...e-06,   7.6371428...e-06,
             1.0171428...e-05,   1.2254285...e-05,   1.4810000...e-05,
             1.6517142...e-05,   1.5430714...e-05,   1.4536428...e-05,
             1.4037857...e-05,   1.1587857...e-05,   1.0743571...e-05,
             1.0979285...e-05,   1.0398571...e-05,   8.2971428...e-06,
             6.3057142...e-06,   5.0942857...e-06,   4.8500000...e-06,
             5.5371428...e-06,   6.4128571...e-06,   7.2592857...e-06,
             7.7750000...e-06,   7.1607142...e-06,   6.6635714...e-06,
             6.7328571...e-06,   7.5307142...e-06,   1.0733571...e-05,
             1.6234285...e-05,   2.2570714...e-05,   2.7056428...e-05,
             2.7781428...e-05,   2.5025714...e-05,   1.7966428...e-05,
             1.0505000...e-05,   5.9657142...e-06,   3.6421428...e-06,
             2.1664285...e-06,   1.2935714...e-06,   8.3642857...e-07,
             7.2500000...e-07,   6.3928571...e-07,   6.6285714...e-07,
             8.5571428...e-07,   1.4507142...e-06,   2.2542857...e-06,
             3.4142857...e-06,   4.9864285...e-06,   6.4907142...e-06,
             7.8928571...e-06,   9.1664285...e-06,   9.9521428...e-06,
             9.7664285...e-06,   9.3150000...e-06,   8.9092857...e-06,
             8.1578571...e-06,   6.8935714...e-06,   5.5721428...e-06,
             4.4592857...e-06,   3.4778571...e-06,   2.7650000...e-06,
             2.3114285...e-06,   1.7092857...e-06,   1.1771428...e-06,
             9.8428571...e-07,   8.8285714...e-07,   7.4142857...e-07,
             7.0142857...e-07,   7.0857142...e-07,   6.6642857...e-07,
             7.5928571...e-07,   8.7000000...e-07,   8.2714285...e-07,
             7.1714285...e-07,   6.6000000...e-07])
    """

    msds = sds_and_msds_to_msds(sds)

    interval = msds.shape.interval

    r_i = np.gradient(np.transpose(msds.values), axis=1) / interval

    return np.mean(r_i ** 2, axis=0)
