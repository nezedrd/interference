import numpy as np

class Values:
    __wl = 532        #.10e-6m  # Wavelength in nanometers
    __c  = 299.792458 #.10e6m/s # Speed of light
    __d  = 100        #.10e-6m  # Distance between both sources in nanometers
    __D  = 30E4       #.10e-6m  # Distance to the screen in nanometers (30cm)
    __D_og = 'cm'     #
    __D_og_choices = {'cm': 1e4, 'nm': 1}

    """
    d is the distance between coherent sources
    """
    @classmethod
    def get_inter_source_distance(cls):
        return cls.__d

    @classmethod
    def print_inter_source_distance(cls,s=None):
        text = 'Distance between sources is {:.4g} nanometers.'.format(cls.__d)
        if s is None:
            print(text)
        else:
            s.write('{:}\n'.format(text))

    @classmethod
    def set_inter_source_distance(cls,value):
        assert(value > 50 and value < 1000)
        cls.__d = value

    """
    wl(λ) is the wavelenth of the sources
    """
    @classmethod
    def get_wavelength(cls):
        return cls.__wl

    @classmethod
    def print_wavelength(cls,s=None):
        text = 'Sources wavelength is {:.4g} nanometers.'.format(cls.__wl)
        if s is None:
            print(text)
        else:
            s.write('{:}\n'.format(text))

    @classmethod
    def set_wavelength(cls,value):
        assert(value >= 400 and value < 800)
        cls.__wl = value

    """
    D is the distance from the sources to the screen
    """
    @classmethod
    def get_screen_distance(cls):
        return cls.__D

    @classmethod
    def print_screen_distance(cls,s=None):
        verb_unit = {'cm': 'centimeters', 'nm': 'nanometers'}
        text = 'Distance to the screen is {:.4g} {:}.'.format(
                cls.__D/cls.__D_og_choices[cls.__D_og],
                verb_unit[cls.__D_og])
        if s is None:
            print(text)
        else:
            s.write('{:}\n'.format(text))

    @classmethod
    def set_screen_distance(cls,value):
        value = value*cls.__D_og_choices[cls.__D_og]
        assert(value > 50 and value < 10e6)
        cls.__D = value

    @classmethod
    def set_screen_distance_unit(cls,value):
        assert(value in cls.__D_og_choices)
        cls.__D_og = value

    """
    Point O(x,y)
    Point A(-d,0) is the first source
    Point B(d,0) is the second source
    """
    @classmethod
    def get_left_distance(cls,x,y):
        return np.sqrt(np.square(x+cls.__d)+np.square(y))

    @classmethod
    def get_left_distance_1d(cls,xr,y):
        yr = y*np.ones(xr.shape)
        return cls.get_left_distance(xr,yr)

    @classmethod
    def get_left_distance_2d(cls,xr,yr):
        x = np.copy(xr).reshape(-1,1)
        y = np.copy(yr).reshape(1,-1)
        return cls.get_left_distance(np.ones(y.shape)*x,
                np.ones(x.shape)*y)

if __name__=='__main__':
    xr = np.arange(-110,-80,10).reshape(-1,1)
    yr = np.arange(50,110,10).reshape(1,-1)
    print(Values.get_left_distance_2d(xr,yr))
