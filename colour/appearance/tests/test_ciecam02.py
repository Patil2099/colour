# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines the unit tests for the :mod:`colour.appearance.ciecam02` module.
"""

import numpy as np
from itertools import permutations

from colour.appearance import (
    VIEWING_CONDITIONS_CIECAM02, InductionFactors_CIECAM02,
    CAM_Specification_CIECAM02, XYZ_to_CIECAM02, CIECAM02_to_XYZ)
from colour.appearance.tests.common import AbstractColourAppearanceModelTest
from colour.utilities import (as_namedtuple, domain_range_scale,
                              ignore_numpy_errors, tsplit, tstack)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'TestCIECAM02ColourAppearanceModelForward',
    'TestCIECAM02ColourAppearanceModelInverse'
]


class TestCIECAM02ColourAppearanceModelForward(
        AbstractColourAppearanceModelTest):
    """
    Defines :mod:`colour.appearance.ciecam02` module unit tests methods for
    *CIECAM02* colour appearance model forward implementation.
    """

    FIXTURE_BASENAME = 'ciecam02.csv'

    OUTPUT_ATTRIBUTES = {
        'J': 'J',
        'C': 'C',
        'h': 'h',
        's': 's',
        'Q': 'Q',
        'M': 'M',
        'H': 'H'
    }

    def output_specification_from_data(self, data):
        """
        Returns the *CIECAM02* colour appearance model output specification
        from given data.

        Parameters
        ----------
        data : list
            Fixture data.

        Returns
        -------
        CAM_Specification_CIECAM02
            *CIECAM02* colour appearance model specification.
        """

        XYZ = tstack([data['X'], data['Y'], data['Z']])
        XYZ_w = tstack([data['X_w'], data['Y_w'], data['Z_w']])

        specification = XYZ_to_CIECAM02(
            XYZ, XYZ_w, data['L_A'], data['Y_b'],
            InductionFactors_CIECAM02(data['F'], data['c'], data['N_c']))

        return specification

    @ignore_numpy_errors
    def test_domain_range_scale_XYZ_to_CIECAM02(self):
        """
        Tests :func:`colour.appearance.cam16.XYZ_to_CIECAM02` definition domain
        and range scale support.
        """

        XYZ = np.array([19.01, 20.00, 21.78])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20.0
        surround = VIEWING_CONDITIONS_CIECAM02['Average']
        specification = XYZ_to_CIECAM02(XYZ, XYZ_w, L_A, Y_b, surround)

        d_r = (
            ('reference', 1, 1),
            (1, 0.01,
             np.array([
                 1 / 100, 1 / 100, 1 / 360, 1 / 100, 1 / 100, 1 / 100, 1 / 400,
                 np.nan
             ])),
            (100, 1, np.array([1, 1, 100 / 360, 1, 1, 1, 100 / 400, np.nan])),
        )
        for scale, factor_a, factor_b in d_r:
            with domain_range_scale(scale):
                np.testing.assert_almost_equal(
                    XYZ_to_CIECAM02(XYZ * factor_a, XYZ_w * factor_a, L_A, Y_b,
                                    surround),
                    specification * factor_b,
                    decimal=7)

    @ignore_numpy_errors
    def test_nan_XYZ_to_CIECAM02(self):
        """
        Tests :func:`colour.appearance.ciecam02.XYZ_to_CIECAM02` definition
        nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = set(permutations(cases * 3, r=3))
        for case in cases:
            XYZ = np.array(case)
            XYZ_w = np.array(case)
            L_A = case[0]
            Y_b = case[0]
            surround = InductionFactors_CIECAM02(case[0], case[0], case[0])
            XYZ_to_CIECAM02(XYZ, XYZ_w, L_A, Y_b, surround)


class TestCIECAM02ColourAppearanceModelInverse(
        AbstractColourAppearanceModelTest):
    """
    Defines :mod:`colour.appearance.ciecam02` module unit tests methods for
    *CIECAM02* colour appearance model inverse implementation.
    """

    FIXTURE_BASENAME = 'ciecam02.csv'

    OUTPUT_ATTRIBUTES = {'X': 0, 'Y': 1, 'Z': 2}

    def output_specification_from_data(self, data):
        """
        Returns the colour appearance model output specification from given
        fixture data.

        Parameters
        ----------
        data : list
            Tested colour appearance model fixture data.

        Notes
        -----
        -   This method is a dummy object.
        """

        pass

    def _XYZ_from_data(self, data, correlates):
        """
        Returns the *CIE XYZ* tristimulus values from given *CIECAM02* colour
        appearance model input data.

        Parameters
        ----------
        data : list
            Fixture data.
        correlates : array_like
            Correlates used to build the input *CIECAM02* colour appearance
            model specification.

        Returns
        -------
        array_like
            *CIE XYZ* tristimulus values
        """

        XYZ_w = tstack([data['X_w'], data['Y_w'], data['Z_w']])

        i, j, k = correlates
        specification = as_namedtuple({
            i: data[i],
            j: data[j],
            k: data[k]
        }, CAM_Specification_CIECAM02)

        XYZ = CIECAM02_to_XYZ(
            specification, XYZ_w, data['L_A'], data['Y_b'],
            InductionFactors_CIECAM02(data['F'], data['c'], data['N_c']))

        return XYZ

    def check_specification_attribute(self, case, data, attribute, expected):
        """
        Tests *CIE XYZ* tristimulus values output from *CIECAM02* colour
        appearance model input data.

        Parameters
        ----------
        case : int
            Fixture case number.
        data : dict.
            Fixture case data.
        attribute : unicode.
            Tested attribute name.
        expected : float.
            Expected attribute value.

        Warnings
        --------
        The method name does not reflect the underlying implementation.
        """

        for correlates in (('J', 'C', 'h'), ('J', 'M', 'h')):
            XYZ = self._XYZ_from_data(data, correlates)
            value = tsplit(XYZ)[attribute]

            error_message = ('Parameter "{0}" in test case "{1}" '
                             'does not match target value.\n'
                             'Expected: "{2}" \n'
                             'Received "{3}"').format(attribute, case,
                                                      expected, value)

            np.testing.assert_allclose(
                value,
                expected,
                err_msg=error_message,
                rtol=0.01,
                atol=0.01,
                verbose=False)

            np.testing.assert_almost_equal(
                value, expected, decimal=1, err_msg=error_message)

    @ignore_numpy_errors
    def test_domain_range_scale_CIECAM02_to_XYZ(self):
        """
        Tests :func:`colour.appearance.cam16.CIECAM02_to_XYZ` definition domain
        and range scale support.
        """

        XYZ_i = np.array([19.01, 20.00, 21.78])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20.0
        surround = VIEWING_CONDITIONS_CIECAM02['Average']
        specification = XYZ_to_CIECAM02(XYZ_i, XYZ_w, L_A, Y_b, surround)
        XYZ = CIECAM02_to_XYZ(specification, XYZ_w, L_A, Y_b, surround)

        d_r = (
            ('reference', 1, 1, 1),
            (1,
             np.array([
                 1 / 100, 1 / 100, 1 / 360, 1 / 100, 1 / 100, 1 / 100, 1 / 400,
                 np.nan
             ]), 0.01, 0.01),
            (100, np.array([1, 1, 100 / 360, 1, 1, 1, 100 / 400, np.nan]), 1,
             1),
        )
        for scale, factor_a, factor_b, factor_c in d_r:
            with domain_range_scale(scale):
                np.testing.assert_almost_equal(
                    CIECAM02_to_XYZ(specification * factor_a, XYZ_w * factor_b,
                                    L_A, Y_b, surround),
                    XYZ * factor_c,
                    decimal=7)

    @ignore_numpy_errors
    def test_raise_exception_CIECAM02_to_XYZ(self):
        """
        Tests :func:`colour.appearance.cam16.CIECAM02_to_XYZ` definition raised
        exception.
        """

        try:
            CIECAM02_to_XYZ(
                CAM_Specification_CIECAM02(
                    41.731091132513917,
                    None,
                    219.04843265831178,
                ),
                np.array([95.05, 100.00, 108.88]),
                318.31,
                20.0,
                VIEWING_CONDITIONS_CIECAM02['Average'],
            )
        except ValueError:
            pass

    @ignore_numpy_errors
    def test_nan_CIECAM02_to_XYZ(self):
        """
        Tests :func:`colour.appearance.ciecam02.CIECAM02_to_XYZ` definition
        nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = set(permutations(cases * 3, r=3))
        for case in cases:
            J = case[0]
            C = case[0]
            h = case[0]
            XYZ_w = np.array(case)
            L_A = case[0]
            Y_b = case[0]
            surround = InductionFactors_CIECAM02(case[0], case[0], case[0])
            CIECAM02_to_XYZ(
                CAM_Specification_CIECAM02(J, C, h), XYZ_w, L_A, Y_b, surround)
