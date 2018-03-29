#!/usr/bin/env python
"""
Tests for sa_library.imagecorrelation
"""
import numpy
import matplotlib
import matplotlib.pyplot as pyplot
import tifffile

import storm_analysis.sa_library.imagecorrelation as imgCorr
import storm_analysis.simulator.draw_gaussians_c as dg


def test_align3d_1():
    """
    Test on uniform images.
    """
    image = numpy.ones((10,12,14))
    a3d = imgCorr.Align3D(image, xy_margin = 1, z_margin = 1)
    a3d.setOtherImage(image)

    # Check for the same value regardless of displacement.
    val = a3d.fn(0.0, 0.0, 0.0)
    assert(abs(val - a3d.fn(0.0, 0.0, 0.1)) < 1.0e-6)
    assert(abs(val - a3d.fn(0.0, 0.1, 0.0)) < 1.0e-6)
    assert(abs(val - a3d.fn(0.0, 0.1, 0.1)) < 1.0e-6)
    assert(abs(val - a3d.fn(0.1, 0.0, 0.1)) < 1.0e-6)
    assert(abs(val - a3d.fn(0.1, -0.1, 0.0)) < 1.0e-6)
    assert(abs(val - a3d.fn(0.1, -0.1, 0.1)) < 1.0e-6)

    # Check that derivatives are zero.
    for elt in [-0.1, 0.0, 0.1]:
        assert(abs(a3d.dfn_dx(elt, 0.0, 0.0)) < 1.0e-6)
        assert(abs(a3d.dfn_dy(0.0, elt, 0.0)) < 1.0e-6)
        assert(abs(a3d.dfn_dz(0.0, 0.0, elt)) < 1.0e-6)


def test_align3d_2():
    """
    Test displacement
    """
    image1 = dg.drawGaussiansXYZ((12,13,14),
                                 numpy.array([6.0]),
                                 numpy.array([6.5]),
                                 numpy.array([7.0]))
    a3d = imgCorr.Align3D(image1, xy_margin = 1, z_margin = 1)
    a3d.setOtherImage(image1)
    val = a3d.fn(0.0, 0.0, 0.0)
    
    image2 = dg.drawGaussiansXYZ((12,13,14),
                                 numpy.array([6.1]),
                                 numpy.array([6.6]),
                                 numpy.array([6.9]))    
    a3d.setOtherImage(image2)

    assert(a3d.fn(0.0, 0.0, 0.0) < (val - 0.01))
    assert(a3d.fn(0.1, 0.1, -0.1) < (val - 0.01))
    assert(abs(a3d.fn(-0.1, -0.1, 0.1) - val) < 1.0e-4)


def test_align3d_3():
    """
    Test on Gaussians.
    """
    image = dg.drawGaussiansXYZ((12,13,14),
                                numpy.array([6.0]),
                                numpy.array([6.5]),
                                numpy.array([7.0]))
    
    a3d = imgCorr.Align3D(image, xy_margin = 1, z_margin = 1)
    a3d.setOtherImage(image)

    # Check X derivatives.
    for elt in [-0.1, 0.0, 0.1]:
        dx = 1.0e-6
        f1 = a3d.fn(elt + dx, 0.0, 0.0)
        f2 = a3d.fn(elt, 0.0, 0.0)
        val = (f1-f2)/dx
        assert(abs(a3d.dfn_dx(elt, 0.0, 0.0) - val) < 1.0e-4)
    

if (__name__ == "__main__"):
#    test_align3d_1()
#    test_align3d_2()
    test_align3d_3()

    
