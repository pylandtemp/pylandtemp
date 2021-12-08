import numpy as np
import unittest

from pylandtemp.temperature import BrightnessTemperatureLandsat
from pylandtemp.temperature import (
    SplitWindowJiminezMunozLST,
    SplitWindowKerrLST,
    SplitWindowMcMillinLST,
    SplitWindowPriceLST,
    SplitWindowSobrino1993LST,
)


class TestSplitWindowSobrino1993LST(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    mask = np.random.randint(0, high=1, size=(5, 5), dtype=int)
    mask = mask == 1

    def test_that_output_and_input_size_equal(self):
        output = SplitWindowSobrino1993LST()(
            emissivity_10=self.sample_band_10,
            emissivity_11=self.sample_band_10,
            brightness_temperature_10=self.sample_band_10,
            brightness_temperature_11=self.sample_band_10,
            mask=self.mask,
        )
        self.assertEqual(self.sample_band_10.shape, output.shape)

    def test_that_max_temp_less_than_or_equal_max_earth_temp(self):
        lst_algorithm = SplitWindowSobrino1993LST()
        self.assertEqual(lst_algorithm.max_earth_temp, 273.15 + 56.7)


class TestSplitWindowJiminezMunozLST(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    mask = np.random.randint(0, high=1, size=(5, 5), dtype=int)
    mask = mask == 1

    def test_that_output_and_input_size_equal(self):
        output = SplitWindowJiminezMunozLST()(
            emissivity_10=self.sample_band_10,
            emissivity_11=self.sample_band_10,
            brightness_temperature_10=self.sample_band_10,
            brightness_temperature_11=self.sample_band_10,
            mask=self.mask,
        )
        self.assertEqual(self.sample_band_10.shape, output.shape)

    def test_that_max_temp_less_than_or_equal_max_earth_temp(self):
        lst_algorithm = SplitWindowJiminezMunozLST()
        self.assertEqual(lst_algorithm.max_earth_temp, 273.15 + 56.7)


class TestSplitWindowKerrLST(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    mask = np.random.randint(0, high=1, size=(5, 5), dtype=int)
    mask = mask == 1

    def test_that_output_and_input_size_equal(self):
        output = SplitWindowKerrLST()(
            brightness_temperature_10=self.sample_band_10,
            brightness_temperature_11=self.sample_band_10,
            ndvi=self.sample_band_10,
            mask=self.mask,
        )
        self.assertEqual(self.sample_band_10.shape, output.shape)

    def test_that_max_temp_less_than_or_equal_max_earth_temp(self):
        lst_algorithm = SplitWindowKerrLST()
        self.assertEqual(lst_algorithm.max_earth_temp, 273.15 + 56.7)


class TestSplitWindowKerrLST(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    mask = np.random.randint(0, high=1, size=(5, 5), dtype=int)
    mask = mask == 1

    def test_that_output_and_input_size_equal(self):
        output = SplitWindowKerrLST()(
            brightness_temperature_10=self.sample_band_10,
            brightness_temperature_11=self.sample_band_10,
            ndvi=self.sample_band_10,
            mask=self.mask,
        )
        self.assertEqual(self.sample_band_10.shape, output.shape)

    def test_that_max_temp_less_than_or_equal_max_earth_temp(self):
        lst_algorithm = SplitWindowKerrLST()
        self.assertEqual(lst_algorithm.max_earth_temp, 273.15 + 56.7)


class TestSplitWindowMcMillinLST(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    mask = np.random.randint(0, high=1, size=(5, 5), dtype=int)
    mask = mask == 1

    def test_that_output_and_input_size_equal(self):
        output = SplitWindowMcMillinLST()(
            brightness_temperature_10=self.sample_band_10,
            brightness_temperature_11=self.sample_band_10,
            mask=self.mask,
        )
        self.assertEqual(self.sample_band_10.shape, output.shape)

    def test_that_max_temp_less_than_or_equal_max_earth_temp(self):
        lst_algorithm = SplitWindowMcMillinLST()
        self.assertEqual(lst_algorithm.max_earth_temp, 273.15 + 56.7)


class TestSplitWindowPriceLST(unittest.TestCase):
    sample_band_10 = np.zeros((5, 5))
    mask = np.random.randint(0, high=1, size=(5, 5), dtype=int)
    mask = mask == 1

    def test_that_output_and_input_size_equal(self):
        output = SplitWindowPriceLST()(
            emissivity_10=self.sample_band_10,
            emissivity_11=self.sample_band_10,
            brightness_temperature_10=self.sample_band_10,
            brightness_temperature_11=self.sample_band_10,
            mask=self.mask,
        )
        self.assertEqual(self.sample_band_10.shape, output.shape)

    def test_that_max_temp_less_than_or_equal_max_earth_temp(self):
        lst_algorithm = SplitWindowPriceLST()
        self.assertEqual(lst_algorithm.max_earth_temp, 273.15 + 56.7)


if __name__ == "__main__":
    unittest.main()
