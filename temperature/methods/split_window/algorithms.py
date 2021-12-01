import numpy as np 
from getemp.general_utils import compute_proportion_vegetation_cover

#def SplitWindowSobrino(t1, t2, e1, e2, cwv=0.013, mask=None):
#      #REFERENCE: Skokovic D, Sobrino JA, Jiménez Muñoz JC, SoriaG, Julien Y,Mattar C, Cristóbal J (2014)
#      """
#      t1 = TOA brightness temperature band 10
#      t2 = TOA brightness temperature band 11
#      e1 = Emissivity band 10
#      e2 = Emissivity band 11
#      cwv = Column water vapour
#      """
#
#      # TODO: Implement mask. If mask, compute for only non masked locations. 
#      # TODO: Optimize code performance. Don't precompute mean_e and diff_e
#      # TODO: Move assertion test into a different function 
#      # TODO: Move function class with __call__ method 
#
#      mean_e = (e1 + e2) / 2
#      diff_e = np.subtract(e1, e2)
#
#      assert t1.shape == t2.shape == e1.shape == e2.shape == cwv.shape, "Images should have the same size"
#
#      lst = (t1 + (1.387 * (t1 - t2)) + (0.183 * ((t1 - t2)**2))
#            - 0.268 + ((54.3 - (2.238 * cwv))* (1 - mean_e)) + ((-129.2 + (16.4 * cwv)) * diff_e))
#
#      return lst

class SplitWindowParentLST:
      # https://link.springer.com/article/10.1007/s40808-020-01007-1/tables/3
      def __init__(self):
            pass
      

      def __call__(self, dict_):
            return self._compute_lst(dict_)
      
      def _compute_lst(self, dict_):

            raise NotImplementedError("Concrete method yet to be implemented")
      
class SplitWindowSobrinoLST(SplitWindowParentLST):
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
            """[summary]
            dict_ should contain the following keys
            dict_ keys:
                  brightness_temperature_10 (np.ndarray): Landsat 8 image band 10  (converted to brightness temperature). 
                  emissivity (np.ndarray): The emmisivity image derived from computing emissivity

            Returns:
                  np.ndarray: Land surface temmperature
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

            lst = (t1 + 
                  (1.387 * diff_tb) + 
                  (0.183 * (diff_tb**2)) - 
                   0.268 + ((54.3 - (2.238 * self.cwv)) * 
                  (1 - mean_e)) + ((-129.2 + (16.4 * self.cwv)) * diff_e))

            land_surface_temp[mask] = np.nan 
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
   
            pv = compute_proportion_vegetation_cover(ndvi)

            lst = (
                  (tb_10 * 
                  ((0.5 * pv)+ 3.1)) +
                  (tb_11 *
                  ((-0.5 * pv) - 2.1)) -
                  ((5.5 * pv) + 3.1)
            )
            lst[mask] = np.nan 

            return lst
      
      



class SplitWindowMcClainLST(SplitWindowParentLST):
      """
      Method reference:

      McMillin LM (1975) Estimation of sea surface temperatures 
      from two infrared window measurements with different absorption. 
      J Geophys Res 80(36):5113–5117. https://doi.org/10.1029/JC080i036p05113


      """

      def _compute_lst(self, dict_):
            """[summary]

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
