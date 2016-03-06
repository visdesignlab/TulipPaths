import sys
from os.path import expanduser


def defaultOutputFile(filename):
    """ Return an appropriate default filename for plugin output on the current operating system """

    platform = sys.platform

    # On Windows, output to the root of the C: drive
    if platform == 'win32':
        return 'C:\\' + filename + '.txt'
    else:
        homeDirectory = expanduser('~')
        return homeDirectory + '/' + filename + '.txt'
