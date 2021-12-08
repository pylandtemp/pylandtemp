import numpy as np
import unittest

from pylandtemp.temperature import BrightnessTemperatureLandsat


class TestBrightnessTemoperature(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    output = BrightnessTemperatureLandsat()(sample_band_10)

    def test_that_method_returns_tuple(self):
        self.assertIsInstance(self.output, tuple)

    def test_that_output_and_input_size_equel(self):
        self.assertEqual(self.sample_band_10.shape, self.output[0].shape)


if __name__ == "__main__":
    unittest.main()
