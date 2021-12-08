import numpy as np
import unittest

from pylandtemp.temperature import BrightnessTemperatureLandsat
from pylandtemp.temperature import MonoWindowLST


class TestMonoWindowLST(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    mask = np.random.randint(0, high=1, size=(5, 5), dtype=int)
    mask = mask == 1

    def test_that_output_and_input_size_equal(self):
        output = MonoWindowLST()(
            emissivity_10=self.sample_band_10,
            brightness_temperature_10=self.sample_band_10,
            mask=self.mask,
        )
        self.assertEqual(self.sample_band_10.shape, output.shape)

    def test_that_max_temp_less_than_or_equal_max_earth_temp(self):
        lst_algorithm = MonoWindowLST()
        self.assertEqual(lst_algorithm.max_earth_temp, 273.15 + 56.7)


if __name__ == "__main__":
    unittest.main()
