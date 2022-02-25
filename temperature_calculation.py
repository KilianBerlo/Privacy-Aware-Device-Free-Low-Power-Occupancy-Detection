import math as m
import struct
import numpy as np

## User defined emissivity compensation for IR data of each pixel
EMISSIVITY = 0.95

class temperature_calculation():
    """
    Class that calculates the relative temperature of each pixel
    """
    def __init__(self, deviceParams, ser, figdata):
        """
        Constructor for the class calculating the relative temperature of each pixel
        
        Parameters:
            deviceParams (dict): Dictionary containing all restored EEPROM data
            ser (Serial/int): If live, then "ser" contains the serial connection, if not live then it contains an int with value 0
            figdata (string): The file in which to save the values of the subpages
        """        
        self._pageData = np.empty(451)
        self._frameData = np.zeros(835)
        self._tempData = np.zeros(768)
        self._deviceParams = deviceParams
        self._ser = ser
        self._ADC = 0
        ## For saving frames
        self._save = 0
        self._figdata = figdata

    def getFrameData(self, nr):
        """
        Function that gets the data for both subpages (chess reading pattern) and puts them together in one frame

        Parameters:
            nr (int): Indicates which subpage has to be read for the exemplary dataset
        """  
        if self._ser == 0:
            ## Exemplary data
            page0 = np.array([6.5444e+04, 6.5427e+04, 6.5418e+04, 6.5416e+04, 6.5402e+04, 6.5402e+04
, 6.5396e+04, 6.5396e+04, 6.5394e+04, 6.5395e+04, 6.5395e+04, 6.5400e+04
, 6.5404e+04, 6.5408e+04, 6.5411e+04, 6.5431e+04, 6.5417e+04, 6.5409e+04
, 6.5397e+04, 6.5394e+04, 6.5386e+04, 6.5381e+04, 6.5373e+04, 6.5371e+04
, 6.5370e+04, 6.5377e+04, 6.5372e+04, 6.5381e+04, 6.5376e+04, 6.5389e+04
, 6.5390e+04, 6.5403e+04, 6.5424e+04, 6.5418e+04, 6.5411e+04, 6.5405e+04
, 6.5403e+04, 6.5393e+04, 6.5389e+04, 6.5387e+04, 6.5387e+04, 6.5385e+04
, 6.5388e+04, 6.5393e+04, 6.5397e+04, 6.5397e+04, 6.5404e+04, 6.5416e+04
, 6.5404e+04, 6.5404e+04, 6.5393e+04, 6.5387e+04, 6.5373e+04, 6.5374e+04
, 6.5365e+04, 6.5367e+04, 6.5360e+04, 6.5368e+04, 6.5364e+04, 6.5371e+04
, 6.5371e+04, 6.5378e+04, 6.5380e+04, 6.5387e+04, 6.5425e+04, 6.5415e+04
, 6.5407e+04, 6.5400e+04, 6.5393e+04, 6.5388e+04, 6.5381e+04, 6.5379e+04
, 6.5381e+04, 6.5377e+04, 6.5383e+04, 6.5387e+04, 6.5388e+04, 6.5393e+04
, 6.5400e+04, 6.5404e+04, 6.5400e+04, 6.5397e+04, 6.5383e+04, 6.5383e+04
, 6.5367e+04, 6.5363e+04, 6.5356e+04, 6.5354e+04, 6.5352e+04, 6.5358e+04
, 6.5358e+04, 6.5362e+04, 6.5361e+04, 6.5372e+04, 6.5374e+04, 6.5379e+04
, 6.5414e+04, 6.5408e+04, 6.5401e+04, 6.5393e+04, 6.5382e+04, 6.5380e+04
, 6.5370e+04, 6.5370e+04, 6.5374e+04, 6.5371e+04, 6.5370e+04, 6.5375e+04
, 6.5384e+04, 6.5387e+04, 6.5393e+04, 6.5403e+04, 6.5392e+04, 6.5393e+04
, 6.5378e+04, 6.5372e+04, 6.5360e+04, 6.5360e+04, 6.5347e+04, 6.5347e+04
, 6.5343e+04, 6.5351e+04, 6.5349e+04, 6.5353e+04, 6.5354e+04, 6.5362e+04
, 6.5365e+04, 6.5373e+04, 6.5414e+04, 6.5404e+04, 6.5397e+04, 6.5389e+04
, 6.5377e+04, 6.5372e+04, 6.5368e+04, 6.5367e+04, 6.5363e+04, 6.5367e+04
, 6.5368e+04, 6.5371e+04, 6.5381e+04, 6.5383e+04, 6.5391e+04, 6.5397e+04
, 6.5386e+04, 6.5383e+04, 6.5370e+04, 6.5364e+04, 6.5357e+04, 6.5354e+04
, 6.5347e+04, 6.5343e+04, 6.5339e+04, 6.5340e+04, 6.5342e+04, 6.5346e+04
, 6.5351e+04, 6.5359e+04, 6.5363e+04, 6.5371e+04, 6.5411e+04, 6.5402e+04
, 6.5397e+04, 6.5387e+04, 6.5380e+04, 6.5373e+04, 6.5387e+04, 6.5374e+04
, 6.5366e+04, 6.5362e+04, 6.5365e+04, 6.5367e+04, 6.5373e+04, 6.5377e+04
, 6.5383e+04, 6.5392e+04, 6.5387e+04, 6.5381e+04, 6.5370e+04, 6.5365e+04
, 6.5354e+04, 6.5362e+04, 6.5396e+04, 6.5362e+04, 6.5337e+04, 6.5339e+04
, 6.5342e+04, 6.5346e+04, 6.5345e+04, 6.5352e+04, 6.5362e+04, 6.5365e+04
, 6.5408e+04, 6.5397e+04, 6.5394e+04, 6.5381e+04, 6.5374e+04, 6.5385e+04
, 6.5448e+04, 6.5461e+04, 6.5377e+04, 6.5357e+04, 6.5363e+04, 6.5363e+04
, 6.5368e+04, 6.5378e+04, 6.5381e+04, 6.5395e+04, 6.5383e+04, 6.5378e+04
, 6.5367e+04, 6.5358e+04, 6.5355e+04, 6.5408e+04, 6.5407e+04, 6.5411e+04
, 6.5341e+04, 6.5334e+04, 6.5335e+04, 6.5345e+04, 6.5346e+04, 6.5355e+04
, 6.5358e+04, 6.5365e+04, 6.5400e+04, 6.5397e+04, 6.5387e+04, 6.5381e+04
, 6.5380e+04, 6.5402e+04, 6.5467e+04, 6.5431e+04, 6.5385e+04, 6.5357e+04
, 6.5379e+04, 6.5406e+04, 6.5372e+04, 6.5378e+04, 6.5384e+04, 6.5395e+04
, 6.5379e+04, 6.5372e+04, 6.5362e+04, 6.5361e+04, 6.5353e+04, 6.5406e+04
, 6.5459e+04, 6.5421e+04, 6.5338e+04, 6.5338e+04, 6.5400e+04, 6.5385e+04
, 6.5348e+04, 6.5357e+04, 6.5359e+04, 6.5365e+04, 6.5403e+04, 6.5400e+04
, 6.5391e+04, 6.5382e+04, 6.5380e+04, 6.5393e+04, 6.5482e+04, 6.5447e+04
, 6.5366e+04, 6.5356e+04, 6.5383e+04, 6.5436e+04, 6.5381e+04, 6.5375e+04
, 6.5385e+04, 6.5395e+04, 6.5380e+04, 6.5376e+04, 6.5366e+04, 6.5362e+04
, 6.5353e+04, 6.5410e+04, 6.5449e+04, 6.5365e+04, 6.5334e+04, 6.5337e+04
, 6.5357e+04, 6.5405e+04, 6.5354e+04, 6.5356e+04, 6.5356e+04, 6.5365e+04
, 6.5413e+04, 6.5398e+04, 6.5389e+04, 6.5390e+04, 6.5406e+04, 6.5427e+04
, 6.5461e+04, 6.5430e+04, 6.5380e+04, 6.5363e+04, 6.5366e+04, 6.5418e+04
, 6.5392e+04, 6.5380e+04, 6.5385e+04, 6.5393e+04, 6.5388e+04, 6.5376e+04
, 6.5367e+04, 6.5393e+04, 6.5397e+04, 6.5410e+04, 6.5408e+04, 6.5400e+04
, 6.5369e+04, 6.5345e+04, 6.5360e+04, 6.5399e+04, 6.5355e+04, 6.5357e+04
, 6.5361e+04, 6.5371e+04, 6.5427e+04, 6.5397e+04, 6.5391e+04, 6.5418e+04
, 6.5425e+04, 6.5424e+04, 6.5420e+04, 6.5421e+04, 6.5412e+04, 6.5414e+04
, 6.5412e+04, 6.5428e+04, 6.5388e+04, 6.5380e+04, 6.5386e+04, 6.5398e+04
, 6.5408e+04, 6.5378e+04, 6.5372e+04, 6.5401e+04, 6.5397e+04, 6.5396e+04
, 6.5391e+04, 6.5391e+04, 6.5388e+04, 6.5396e+04, 6.5394e+04, 6.5400e+04
, 6.5357e+04, 6.5357e+04, 6.5366e+04, 6.5372e+04, 6.5428e+04, 6.5429e+04
, 6.5410e+04, 6.5431e+04, 6.5426e+04, 6.5406e+04, 6.5416e+04, 6.5413e+04
, 6.5414e+04, 6.5401e+04, 6.5407e+04, 6.5403e+04, 6.5383e+04, 6.5377e+04
, 6.5386e+04, 6.5392e+04, 6.5401e+04, 6.5399e+04, 6.5394e+04, 6.5404e+04
, 6.5389e+04, 6.5379e+04, 6.5379e+04, 6.5381e+04, 6.5376e+04, 6.5351e+04
, 6.5347e+04, 6.5353e+04, 6.5349e+04, 6.5351e+04, 6.5357e+04, 6.5363e+04
, 1.9685e+04, 6.4820e+03, 3.2767e+04, 6.4820e+03, 3.2767e+04, 6.4800e+03
, 3.2767e+04, 6.4800e+03, 6.5445e+04, 5.2876e+04, 6.0750e+03, 5.5238e+04
, 6.5525e+04, 6.0000e+00, 6.5531e+04, 6.5535e+04, 6.6670e+03, 1.0260e+03
, 6.1700e+02, 3.2767e+04, 6.6660e+03, 1.0260e+03, 6.1700e+02, 3.2767e+04
, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00
, 3.0000e+00, 3.0000e+00, 1.6200e+03, 3.2767e+04, 6.4820e+03, 3.2767e+04
, 6.4820e+03, 3.2767e+04, 6.4800e+03, 3.2767e+04, 6.5453e+04, 6.2794e+04
, 5.3328e+04, 5.5135e+04, 5.0000e+00, 6.5529e+04, 6.5533e+04, 6.5533e+04
, 2.4800e+02, 9.4000e+01, 1.0263e+04, 6.2000e+01, 2.4700e+02, 9.4000e+01
, 1.0263e+04, 6.2000e+01, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00
, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00, 6.5290e+03, 0.0000e+00
, 2.8182e+04])
            page1 = np.array([6.5438e+04, 6.5416e+04, 6.5410e+04, 6.5402e+04, 6.5398e+04, 6.5389e+04
, 6.5386e+04, 6.5375e+04, 6.5384e+04, 6.5381e+04, 6.5384e+04, 6.5384e+04
, 6.5387e+04, 6.5393e+04, 6.5398e+04, 6.5410e+04, 6.5431e+04, 6.5407e+04
, 6.5407e+04, 6.5394e+04, 6.5391e+04, 6.5380e+04, 6.5384e+04, 6.5375e+04
, 6.5385e+04, 6.5374e+04, 6.5384e+04, 6.5383e+04, 6.5394e+04, 6.5391e+04
, 6.5401e+04, 6.5407e+04, 6.5419e+04, 6.5410e+04, 6.5406e+04, 6.5391e+04
, 6.5388e+04, 6.5381e+04, 6.5377e+04, 6.5372e+04, 6.5376e+04, 6.5373e+04
, 6.5375e+04, 6.5379e+04, 6.5380e+04, 6.5382e+04, 6.5390e+04, 6.5389e+04
, 6.5412e+04, 6.5401e+04, 6.5399e+04, 6.5384e+04, 6.5390e+04, 6.5374e+04
, 6.5377e+04, 6.5363e+04, 6.5376e+04, 6.5368e+04, 6.5375e+04, 6.5373e+04
, 6.5385e+04, 6.5383e+04, 6.5395e+04, 6.5395e+04, 6.5417e+04, 6.5405e+04
, 6.5399e+04, 6.5389e+04, 6.5383e+04, 6.5371e+04, 6.5370e+04, 6.5362e+04
, 6.5366e+04, 6.5364e+04, 6.5367e+04, 6.5369e+04, 6.5374e+04, 6.5376e+04
, 6.5386e+04, 6.5381e+04, 6.5410e+04, 6.5396e+04, 6.5396e+04, 6.5380e+04
, 6.5383e+04, 6.5367e+04, 6.5367e+04, 6.5360e+04, 6.5372e+04, 6.5358e+04
, 6.5373e+04, 6.5365e+04, 6.5380e+04, 6.5375e+04, 6.5389e+04, 6.5390e+04
, 6.5413e+04, 6.5403e+04, 6.5395e+04, 6.5383e+04, 6.5378e+04, 6.5368e+04
, 6.5362e+04, 6.5356e+04, 6.5356e+04, 6.5357e+04, 6.5363e+04, 6.5363e+04
, 6.5366e+04, 6.5370e+04, 6.5377e+04, 6.5379e+04, 6.5401e+04, 6.5386e+04
, 6.5390e+04, 6.5374e+04, 6.5371e+04, 6.5356e+04, 6.5357e+04, 6.5352e+04
, 6.5360e+04, 6.5351e+04, 6.5358e+04, 6.5355e+04, 6.5372e+04, 6.5369e+04
, 6.5383e+04, 6.5384e+04, 6.5407e+04, 6.5396e+04, 6.5387e+04, 6.5378e+04
, 6.5375e+04, 6.5362e+04, 6.5362e+04, 6.5350e+04, 6.5353e+04, 6.5351e+04
, 6.5355e+04, 6.5353e+04, 6.5362e+04, 6.5365e+04, 6.5377e+04, 6.5376e+04
, 6.5397e+04, 6.5381e+04, 6.5383e+04, 6.5363e+04, 6.5367e+04, 6.5351e+04
, 6.5353e+04, 6.5345e+04, 6.5351e+04, 6.5344e+04, 6.5356e+04, 6.5350e+04
, 6.5370e+04, 6.5362e+04, 6.5379e+04, 6.5378e+04, 6.5409e+04, 6.5394e+04
, 6.5387e+04, 6.5374e+04, 6.5370e+04, 6.5366e+04, 6.5377e+04, 6.5355e+04
, 6.5353e+04, 6.5347e+04, 6.5356e+04, 6.5350e+04, 6.5360e+04, 6.5359e+04
, 6.5374e+04, 6.5372e+04, 6.5396e+04, 6.5379e+04, 6.5379e+04, 6.5363e+04
, 6.5367e+04, 6.5352e+04, 6.5403e+04, 6.5377e+04, 6.5356e+04, 6.5341e+04
, 6.5352e+04, 6.5346e+04, 6.5357e+04, 6.5359e+04, 6.5374e+04, 6.5374e+04
, 6.5405e+04, 6.5391e+04, 6.5386e+04, 6.5370e+04, 6.5371e+04, 6.5401e+04
, 6.5454e+04, 6.5416e+04, 6.5357e+04, 6.5342e+04, 6.5351e+04, 6.5352e+04
, 6.5360e+04, 6.5363e+04, 6.5371e+04, 6.5372e+04, 6.5391e+04, 6.5375e+04
, 6.5374e+04, 6.5357e+04, 6.5361e+04, 6.5375e+04, 6.5412e+04, 6.5427e+04
, 6.5370e+04, 6.5333e+04, 6.5351e+04, 6.5343e+04, 6.5360e+04, 6.5358e+04
, 6.5373e+04, 6.5376e+04, 6.5402e+04, 6.5387e+04, 6.5384e+04, 6.5372e+04
, 6.5374e+04, 6.5423e+04, 6.5459e+04, 6.5407e+04, 6.5358e+04, 6.5344e+04
, 6.5390e+04, 6.5379e+04, 6.5363e+04, 6.5363e+04, 6.5373e+04, 6.5372e+04
, 6.5380e+04, 6.5371e+04, 6.5370e+04, 6.5355e+04, 6.5362e+04, 6.5376e+04
, 6.5466e+04, 6.5434e+04, 6.5361e+04, 6.5336e+04, 6.5384e+04, 6.5409e+04
, 6.5363e+04, 6.5359e+04, 6.5373e+04, 6.5374e+04, 6.5402e+04, 6.5390e+04
, 6.5388e+04, 6.5377e+04, 6.5373e+04, 6.5415e+04, 6.5474e+04, 6.5393e+04
, 6.5352e+04, 6.5347e+04, 6.5394e+04, 6.5407e+04, 6.5368e+04, 6.5364e+04
, 6.5374e+04, 6.5376e+04, 6.5384e+04, 6.5372e+04, 6.5376e+04, 6.5358e+04
, 6.5367e+04, 6.5378e+04, 6.5465e+04, 6.5405e+04, 6.5348e+04, 6.5335e+04
, 6.5357e+04, 6.5412e+04, 6.5373e+04, 6.5356e+04, 6.5372e+04, 6.5376e+04
, 6.5408e+04, 6.5391e+04, 6.5389e+04, 6.5387e+04, 6.5409e+04, 6.5436e+04
, 6.5457e+04, 6.5395e+04, 6.5365e+04, 6.5349e+04, 6.5372e+04, 6.5406e+04
, 6.5372e+04, 6.5367e+04, 6.5382e+04, 6.5376e+04, 6.5400e+04, 6.5369e+04
, 6.5370e+04, 6.5372e+04, 6.5401e+04, 6.5404e+04, 6.5417e+04, 6.5400e+04
, 6.5392e+04, 6.5349e+04, 6.5359e+04, 6.5394e+04, 6.5377e+04, 6.5362e+04
, 6.5369e+04, 6.5376e+04, 6.5431e+04, 6.5393e+04, 6.5391e+04, 6.5417e+04
, 6.5421e+04, 6.5414e+04, 6.5416e+04, 6.5406e+04, 6.5406e+04, 6.5400e+04
, 6.5407e+04, 6.5416e+04, 6.5375e+04, 6.5369e+04, 6.5381e+04, 6.5381e+04
, 6.5410e+04, 6.5380e+04, 6.5375e+04, 6.5389e+04, 6.5409e+04, 6.5389e+04
, 6.5398e+04, 6.5393e+04, 6.5396e+04, 6.5397e+04, 6.5407e+04, 6.5403e+04
, 6.5369e+04, 6.5355e+04, 6.5375e+04, 6.5378e+04, 6.5441e+04, 6.5422e+04
, 6.5421e+04, 6.5427e+04, 6.5422e+04, 6.5406e+04, 6.5416e+04, 6.5406e+04
, 6.5409e+04, 6.5393e+04, 6.5397e+04, 6.5388e+04, 6.5377e+04, 6.5373e+04
, 6.5387e+04, 6.5383e+04, 6.5400e+04, 6.5389e+04, 6.5394e+04, 6.5392e+04
, 6.5397e+04, 6.5373e+04, 6.5385e+04, 6.5380e+04, 6.5386e+04, 6.5356e+04
, 6.5360e+04, 6.5353e+04, 6.5357e+04, 6.5347e+04, 6.5368e+04, 6.5365e+04
, 1.9685e+04, 6.4850e+03, 3.2767e+04, 6.4850e+03, 3.2767e+04, 6.4830e+03
, 3.2767e+04, 6.4830e+03, 6.5445e+04, 5.2876e+04, 6.0750e+03, 5.5236e+04
, 6.5525e+04, 5.0000e+00, 6.5531e+04, 6.5534e+04, 6.6670e+03, 1.0280e+03
, 6.1700e+02, 3.2767e+04, 6.6660e+03, 1.0280e+03, 6.1700e+02, 3.2767e+04
, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00
, 3.0000e+00, 3.0000e+00, 1.6210e+03, 3.2767e+04, 6.4850e+03, 3.2767e+04
, 6.4850e+03, 3.2767e+04, 6.4830e+03, 3.2767e+04, 6.5454e+04, 6.2794e+04
, 5.3327e+04, 5.5135e+04, 5.0000e+00, 6.5529e+04, 6.5531e+04, 6.5533e+04
, 2.4600e+02, 9.4000e+01, 1.0264e+04, 6.2000e+01, 2.4600e+02, 9.4000e+01
, 1.0264e+04, 6.2000e+01, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00
, 3.0000e+00, 3.0000e+00, 3.0000e+00, 3.0000e+00, 6.5290e+03, 1.0000e+00
, 2.7958e+04])
            if nr == 0:
                self._pageData = page0
            if nr == 1:
                self._pageData = page1
        else:
            read = self._ser.read_until(b'\r\n')
            ## Upon receival, immediately extract the correct hex values
            for i in range(0, len(read) - 4, 2):
                self._pageData[int(i/2)] = (struct.unpack('<H', read[i:i+2])[0])
        
        ## For saving frames
        framefile = open(self._figdata, 'a')
        framefile.write("subpage " + str(self._save) + ":\n" + str(self._pageData))
        framefile.close()
        self._save += 1

        self._ADC = self._pageData[450]
        index = 384
        
        if self._pageData[449] == 0:
            for i in range(index):
                location = (i * 2) + (m.floor(i / 16) % 2)
                self._frameData[location] = self._pageData[i]
        else:
            for i in range(index):
                location = (i * 2) + 1 - (m.floor(i / 16) % 2)
                self._frameData[location] = self._pageData[i]
        for i in range(768, 835):
            self._frameData[i] = self._pageData[index]
            index += 1

        self._frameData = self._frameData.astype(int)

    def getVDD(self):
        """
        Function that calculates the supply voltage value (common for all pixels)
        
        Returns:
            vdd (float): Supply voltage value
        """  
        vdd = self._frameData[810]
        if vdd > 32767:
            vdd -= 65536

        resRAM = (self._frameData[832] & 3072) / 1024
        resCor = pow(2, self._deviceParams['resolutionEE']) / m.pow(2, resRAM)
        vdd = ((resCor * vdd - self._deviceParams['vdd25']) / self._deviceParams['kVdd']) + 3.3

        return vdd

    def getTa(self):
        """
        Function that calculates the ambient temperature (common for all pixels)
        
        Returns:
            ta (float): Ambient temperature value
        """  
        vdd = self.getVDD()
        ptat = self._frameData[800]
        if ptat > 32767:
            ptat -= 65536

        ptatArt = self._frameData[768]
        if ptatArt > 32767:
            ptatArt -= 65536

        ptatArt += (ptat * self._deviceParams['alphaPTAT'])
        ptatArt = (ptat / ptatArt) * 262144

        ta = ptatArt / (1 + self._deviceParams['kvPTAT'] * (vdd - 3.3)) - self._deviceParams['vPTAT25']
        ta = (ta / self._deviceParams['ktPTAT']) + 25

        return ta
    
    def getGain(self):
        """
        Function that calculates the gain parameter (common for all pixels)
        
        Returns:
            gain (float): Gain parameter
        """  
        gain = self._frameData[778]
        if gain > 32767:
            gain -= 65536
        
        gain = self._deviceParams['gainEE'] / gain

        return gain

    def getIRDataCP(self, vdd, ta, gain, mode): 
        """
        Function that calculates the IR data compensation

        Parameters:
            vdd (float): Supply voltage value
            ta (float): Ambient temperature value
            gain (float): Gain parameter
            mode (float): Indicates which mode the sensor uses for its reading pattern (chess or interleaved)

        Returns:
            irDataCP (list): IR data compensation for the compensating pixels for the subpages
        """  
        ## Compensate the gain of the CP pixel
        irDataCP0 = self._frameData[776]
        if irDataCP0 > 32767:
            irDataCP0 -= 65536
        
        irDataCP1 = self._frameData[808]
        if irDataCP1 > 32767:
            irDataCP1 -= 65536
        
        irDataCP0 *= gain
        irDataCP1 *= gain

        ## Compensate the offset, Ta and VDD of the CP pixels
        irDataCP0 = irDataCP0 - self._deviceParams['cpOffset'][0] * (1 + self._deviceParams['cpKta'] * (ta - 25)) * (1 + self._deviceParams['cpKv'] * (vdd - 3.3))
        if mode == self._deviceParams['calibrationModeEE']:
            irDataCP1 = irDataCP1 - self._deviceParams['cpOffset'][1] * (1 + self._deviceParams['cpKta'] * (ta - 25)) * (1 + self._deviceParams['cpKv'] * (vdd - 3.3))
        else:
            irDataCP1 = irDataCP1 - (self._deviceParams['cpOffset'][1] + self._deviceParams['ilChessC'][0]) * (1 + self._deviceParams['cpKta'] * (ta - 25)) * (1 + self._deviceParams['cpKv'] * (vdd - 3.3))
        
        return [irDataCP0, irDataCP1]

    def getPixData(self):        
        """
        Function that gets the relative temperature data for each pixel
        
        Returns:
            _tempData (np.array): Array with the relative temperature data for each pixel
        """  
        for i in range(2):
            self.getFrameData(i)
            subPage = self._frameData[833]
            vdd = self.getVDD()
            ta = self.getTa()
            ## Reflected temperature based on the sensor ambient temperature
            tr = ta - 8
            taTr = m.pow((tr + 273.15), 4) - (m.pow((tr + 273.15), 4) - m.pow((ta + 273.15), 4)) / EMISSIVITY

            ## Sensitivity correction coefficients for each temperature range
            alphaCorrR = []
            alphaCorrR.append(1 / (1 + self._deviceParams['KsTo'][0] * 40))
            alphaCorrR.append(1)
            alphaCorrR.append(1 + self._deviceParams['KsTo'][2] * self._deviceParams['ct'][2])
            alphaCorrR.append(alphaCorrR[2] * (1 + self._deviceParams['KsTo'][3] * (self._deviceParams['ct'][3] - self._deviceParams['ct'][2])))

            gain = self.getGain()
            mode = (self._frameData[832] & 4096) / 32
            irDataCP = self.getIRDataCP(vdd, ta, gain, mode)
            
            for p in range(768):
                ilPattern = m.floor(p / 32) - m.floor(p / 64) * 2
                chessPattern = ilPattern ^ (p - (m.floor(p / 2)) * 2)
                conversionPattern = (m.floor((p + 2) / 4) - m.floor((p + 3) / 4) + m.floor((p + 1) / 4) - m.floor(p / 4)) * (1 - 2 * ilPattern)
                if mode == 0:
                    pattern = ilPattern
                else:
                    pattern = chessPattern    
                if pattern == subPage:
                    ## Calculate the gain compensation on each pixel
                    irData = self._frameData[p]
                    if irData > 32767:
                        irData -= 65536
                    irData = irData * gain

                    ## Calculate the IR data compensation with offset, VDD and Ta
                    irData = irData - self._deviceParams['offset'][p] * (1 + self._deviceParams['kta'][p] * (ta - 25)) * (1 + self._deviceParams['kv'][p] * (vdd - 3.3))

                    #irData = irData - app.structVar.offset(pixelNumber)*(1 + app.structVar.kta(pixelNumber)*(Ta - 25))*(1 + app.structVar.kv(pixelNumber)*(vdd - 3.3));

                    if not (mode == self._deviceParams['calibrationModeEE']):
                        irData = irData + self._deviceParams['ilChessC'][2] * (2 * ilPattern - 1) - self._deviceParams['ilChessC'][1] * conversionPattern
                    ## IR data emmisivity data compensation 
                    irData /= EMISSIVITY 
                    irData = irData - self._deviceParams['tgc'] * irDataCP[subPage] 
                    ## Normalizing to sensitivity
                    alphaCompensated = (self._deviceParams['alpha'][p] - self._deviceParams['tgc'] * self._deviceParams['cpAlpha'][subPage]) * (1 + self._deviceParams['KsTa'] * (ta - 25))
                    
                    sx = m.pow(alphaCompensated, 3) * (irData + alphaCompensated * taTr)
                    sx = self._deviceParams['KsTo'][1] * m.sqrt(m.sqrt(sx))
                    to = m.sqrt(irData / (alphaCompensated * (1 - self._deviceParams['KsTo'][1] * 273.15) + sx) + taTr)
                    to = m.sqrt(to) - 273.15
                    
                    ## Determine the range we are in
                    if to < self._deviceParams['ct'][1]:
                        r = 0
                    elif to < self._deviceParams['ct'][2]:
                        r = 1
                    elif to < self._deviceParams['ct'][3]:
                        r = 2
                    else:
                        r = 3

                    ## Extended To range calculation
                    # to = m.sqrt(m.sqrt(irData / (alphaCompensated * alphaCorrR[r] * (1 + self._deviceParams['KsTo'][r] * (to - self._deviceParams['ct'][r]))) + taTr)) - 273.15
                    
                    ## Relative temperature calculation
                    to = ((irData / alphaCompensated) + taTr) * m.pow(10,-9)
                    self._tempData[p] = to
                    
        return self._tempData