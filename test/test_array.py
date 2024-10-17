from quspin_core._bindings.array import Array
import numpy as np


def test_quspin_array():
    npy_array = np.array([1, 2, 3, 4, 5], dtype=np.float64)
    quspin_array = Array(npy_array)

    assert npy_array.dtype == quspin_array.dtype
    assert npy_array.shape == quspin_array.shape
    assert npy_array.strides == quspin_array.strides
    assert npy_array.ndim == quspin_array.ndim
    assert npy_array.size == quspin_array.size
    assert np.array_equal(npy_array, quspin_array)
