import numpy as np 
from pylandtemp.general_utils import fractional_vegetation_cover


class SplitWindowParentLST:

      # A comparison of all the methods can be found here:
      # https://link.springer.com/article/10.1007/s40808-020-01007-1/tables/3
      def __init__(self):
            pass
      

      def __call__(self, dict_):
            return self._compute_lst(dict_)
      
      def _compute_lst(self, dict_):

            raise NotImplementedError("Concrete method yet to be implemented")
      
class SplitWindowJiminezMunozLST(SplitWindowParentLST):
      def __init__(self):
            """
            Method references:


            For all data:
            Jiménez-Muñoz, Juan-Carlos, and José A. Sobrino. "Split-window coefficients for land surface
            temperature retrieval from low-resolution thermal infrared sensors." IEEE geoscience and 
            remote sensing letters 5.4 (2008): 806-809.

            For landsat:

            """
            self.cwv = 0.013

      def _compute_lst(self, dict_):
            """

            Returns:
                  np.ndarray: Land surface tem perature
            """

            # TODO: Assertions for size (suqal and single band) and that band 10 is not none


            tb_10 = dict_['brightness_temperature_10']
            tb_11 = dict_['brightness_temperature_11']
            emissivity_10 = dict_['emissivity_10']
            emissivity_11 = dict_['emissivity_11']
            mask = dict_['mask']

            mean_e = (emissivity_10 + emissivity_11) / 2
            diff_e = emissivity_10 - emissivity_11

            diff_tb = tb_10 - tb_11

            assert tb_10.shape == tb_11.shape == emissivity_10.shape == emissivity_11.shape, "All images  (temperature and emissivity) should have the same shape and size"

            lst = (tb_10 + 
                  (1.387 * diff_tb) + 
                  (0.183 * (diff_tb**2)) - 
                   0.268 + ((54.3 - (2.238 * self.cwv)) * 
                  (1 - mean_e)) + ((-129.2 + (16.4 * self.cwv)) * diff_e))

            lst[mask] = np.nan 
            return lst

class SplitWindowKerrLST(SplitWindowParentLST):
      def __init__(self):

            super().__init__()
            """
            Method reference:

            Kerr Y, Lagouarde J, Nerry F, Ottlé C (2004) Land surface temperature
            retrieval techniques and applications: case of the AVHRR. Thermal remote 
            sensing in land surface processing. CRC Press, New York, pp 55–131


            """
            self.cwv = 0.013

      def _compute_lst(self, dict_):
            """[summary]
            Returns:
                  np.ndarray: Land surface temperature
            """

            # TODO: Assertions for size (suqal and single band) and that band 10 is not none


            tb_10 = dict_['brightness_temperature_10']
            tb_11 = dict_['brightness_temperature_11']
            ndvi = dict_['ndvi']
            mask = dict_['mask']
   
            pv = fractional_vegetation_cover(ndvi)

            lst = (
                  (tb_10 * 
                  ((0.5 * pv)+ 3.1)) +
                  (tb_11 *
                  ((-0.5 * pv) - 2.1)) -
                  ((5.5 * pv) + 3.1)
            )
            lst[mask] = np.nan 

            return lst

class SplitWindowMcMillinLST(SplitWindowParentLST):
      """
      Method reference:

      McMillin LM (1975) Estimation of sea surface temperatures 
      from two infrared window measurements with different absorption. 
      J Geophys Res 80(36):5113–5117. https://doi.org/10.1029/JC080i036p05113


      """

      def _compute_lst(self, dict_):
            """

            Returns:
                  np.ndarray: Land surface temmperature
            """

            # TODO: Assertions for size (suqal and single band) and that band 10 is not none


            tb_10 = dict_['brightness_temperature_10']
            tb_11 = dict_['brightness_temperature_11']
            mask = dict_['mask']
   
      
            lst = (1.035 * tb_10) + (3.046 * (tb_10 - tb_11)) - 10.93

            lst[mask] = np.nan 

            return lst


class SplitWindowPriceLST(SplitWindowParentLST):
      """
      Method reference:

      Price JC (1984) Land surface temperature measurements from the split window 
      channels of the NOAA advanced very high-resolution radiometer. J Geophys Res 89:7231–7237. 
      https://doi.org/10.1029/JD089iD05p07231

      """
      def _compute_lst(self, dict_):
            """[summary]

            Returns:
                  np.ndarray: Land surface temmperature
            """

            # TODO: Assertions for size (suqal and single band) and that band 10 is not none


            tb_10 = dict_['brightness_temperature_10']
            tb_11 = dict_['brightness_temperature_11']
            emm_10 = dict_['emissivity_10']
            emm_11 = dict_['emissivity_11']
            mask = dict_['mask']
   
      
            lst = (
                  (tb_10 + 3.33 * (tb_10 - tb_11)) * 
                  ((3.5 * emm_10) / 4.5) + 
                  (0.75 * tb_11 * (emm_10 * emm_11))
            )

            lst[mask] = np.nan 

            return lst

class SplitWindowSobrino1993LST(SplitWindowParentLST):
      """
      Method reference:

      Sobrino JA, Caselles V, Coll C (1993) Theoretical split window algorithms 
      for determining the actual surface temperature. I1Nuovo Cimento 16:219–236. 
      https://doi.org/10.1007/BF02524225

      """
      def _compute_lst(self, dict_):
            """[summary]

            Returns:
                  np.ndarray: Land surface temmperature
            """

            # TODO: Assertions for size (equal and single band) and that band 10 is not none


            tb_10 = dict_['brightness_temperature_10']
            tb_11 = dict_['brightness_temperature_11']
            emm_10 = dict_['emissivity_10']
            emm_11 = dict_['emissivity_11']
            mask = dict_['mask']
   

            diff_tb = tb_10 - tb_11
            diff_e = emm_10 - emm_11 

            lst = (
                  tb_10 + (1.06 * (diff_tb)) +
                  (0.46 * diff_tb**2) +
                  (53 * (1 -  emm_10)) -
                  (53 * (emm_10 - emm_11))
            )

            lst[mask] = np.nan 

            return lst


class SplitWindowCollCasellesLST(SplitWindowParentLST):
      """
      Method reference:

      Coll C, Caselles V (1997) A split-window algorithm for land surface temperature 
      from advanced very high-resolution radiometer data: validation and algorithm comparison. 
      J Geophys Res 102(16697–16):713. https://doi.org/10.1029/97JD00929

      """
      def _compute_lst(self, dict_):
            """[summary]

            Returns:
                  np.ndarray: Land surface temmperature
            """

            # TODO: Assertions for size (equal and single band) and that band 10 is not none


            tb_10 = dict_['brightness_temperature_10']
            tb_11 = dict_['brightness_temperature_11']
            mask = dict_['mask']
   

            lst = (
                  (0.39 * tb_10**2) +
                  (2.3 * tb_10) -
                  (0.78 * tb_10 * tb_11) -
                  (1.34 * tb_11) -
                  (1.34 * tb_11) +
                  (0.39 * tb_11**2) +
                  1.56
            )

            lst[mask] = np.nan 

            return lst

      
