"""
for developers: manual (console) wesen programming
"""

from ...defaultwesensource import DefaultWesenSource
import re
import readline
import sys


class WesenSource(DefaultWesenSource):

    def __init__(self, infoAllSource):
        DefaultWesenSource.__init__(self, infoAllSource)
        self.exitPattern = re.compile("^(x|q|quit|exit)$")
        self.commands = ["x", "q", "quit", "exit"]
        readline.set_completer(Completer(self.commands).complete)
        readline.parse_and_bind("tab: complete")

    def getInput(self):
        """pull a string from somewhere - usually raw_input()"""
        return eval(input("\n> "))

    def main(self):
        while(True):
            try:
                userInput = self.getInput()
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            else:
                if(self.exitPattern.match(userInput)):
                    sys.exit()
                else:
                    exec(userInput)


class Completer:

    def __init__(self, commands):
        self.commands = [command + "()" for command in commands]

    def complete(self, text, state):
        matches = self.method_matches(text)
        try:
            return matches[state]
        except:
            return None

    def method_matches(self, text):
        matches = []
        if(len(text) == 0):
            return self.commands
        n = len(text)
        for command in self.commands:
            if(command[:n] == text):
                matches.append(command)
        return matches
