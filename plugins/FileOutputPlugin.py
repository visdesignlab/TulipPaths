from tulip import *
import os.path


class FileOutputPlugin(tlp.Algorithm):
    """ Base class for a Tulip plugin algorithm which saves output to a file """

    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)

        self._outputFileLabel = 'file::Output File'

        # Create an empty output file if none exists
        self._outputFilepath = self.defaultOutputFilepath()
        if not os.path.isfile(self._outputFilepath):
            outputFile = open(self._outputFilepath, 'w')
            outputFile.close()

        # Let the user specify the output file as a parameter, defaulting to
        # the file we just created
        self.addStringParameter(self._outputFileLabel, "", self._outputFilepath)

    def check(self):
        return True

    def run(self):
        return True


    def outputFilepath(self, filename):
        """ Return the full filepath of a file with the given name,
        placing it in the home directory
        """
        return os.path.expanduser('~') + '/' + filename

    def defaultOutputFilepath(self):
        """ Return a default file path for output """
        return self.outputFilepath('TulipOutput.txt')

    def beginFileOutput(self):
        """ Open the output file for writing and prepare to record output """
        self._outputFilepath = self.dataSet[self._outputFileLabel]
        self._outputFile = open(self._outputFilepath, 'w')

    def endFileOutput(self):
        """ Close the output file, saving whatever has been written """
        self._outputFile.close()

    def printToFile(self, message=''):
        """ Print a message to the output file followed by a newline. Assumes
        beginFileOutput() has been called
        """
        self._outputFile.write(str(message) + '\n')
