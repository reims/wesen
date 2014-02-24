"""Example code, don't call.

For more examples, see the subfolders of the sources folder.

For more information on the interface,
take a look at Wesen.PutInterface in wesen.py"""

from Wesen.defaultwesensource import DefaultWesenSource


class WesenSource(DefaultWesenSource):

    """this is a template to your own wesen sources."""

    def __init__(self, infoAllSource):
        """Do all initialization stuff."""
        DefaultWesenSource.__init__(self, infoAllSource)

    def __str__(self):
        """Give yourself an awesome string representation,
        which will only show up in debug information."""
        return "<unspecified WesenSource>"

    def getDescriptor(self):
        """If you use some other GUI than the standard,
        this descriptive information might show up there.
        Usually, you can just omit this method."""
        return {}

    def Receive(self, message):
        """called when the wesen listens to a message.

        message should be a dictionary,
        but there is no unified protocol.
        """
        pass

    def main(self):
        """A.I. code here, this method is run every turn.
        Please try to write code with low runtime complexity.
        """
        pass
