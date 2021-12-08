import numpy as np
import pytest

from .pylandtemp.temperature.brightness_temperature import BrightnessTemperatureLandsat


@pytest.fixture
def brightness_temp_output():
    """returns the __call__ output of BrightnessTemperatureLandsat class"""
    sample_band_10 = np.zeros(5, 5)
    out = BrightnessTemperatureLandsat()(sample_band_10)

    return out


def test_output_type(brightness_temp_output):
    assert type(brightness_temp_output()) == tuple


def test_output_size(brightness_temp_output):
    assert brightness_temp_output().shape == (5, 5)
