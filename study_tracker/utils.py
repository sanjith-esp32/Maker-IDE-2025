import platform
import os

def create_beep_function():
    """
    Create an appropriate beep function based on the platform
    """
    if platform.system() == 'Linux':
        return lambda: os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
    else:
        return lambda: print('\a')
