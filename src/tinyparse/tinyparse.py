# the tinyparse library version 0.1
# 
# Copyright (c) 2022 MP Prabhanand
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# In case someone tries to execute this as a binary for some reason.
if __name__ == '__main__':
    raise Exception("Oh you silly goose, you can't run this as a binary!")

# Temporary arrays to store all values (like a RAM stick)
options    = [] 
Oshortflags = []
Olongflags  = []
Oflags = []
Fflags = []
Flongflags = []
Fshortflags = []
args = []
optionValues = []

# This is how 
def KeepTrackofOperations(type: str, help: str, name: str, longFlag = "", shortFlag = ""):
    """
    Register a(n) argument/flag/option.
    """
    # A dictionary of this form is used as a way to keep track of all arguments to parse.
    # {"type": typ, "name": aname, "help": help, "longFlag": longFlag, "shortFlag": shortFlag}
    # where, `type` can only be of three types:
    #   * `opt` - for options
    #   * `arg` - for arguments
    #   * `flg` - for flags

    opt = {"type": type, "name": name, "help": help, "longFlag": longFlag, "shortFlag": shortFlag}

    if type == 'opt':
        # Append types.
        Oshortflags.append(shortFlag)
        Oflags.append(shortFlag)
        Oflags.append(longFlag)
        Olongflags.append(longFlag)
    elif type == 'flg':
        Fshortflags.append(shortFlag)
        Fflags.append(shortFlag)
        Fflags.append(longFlag)        
        Flongflags.append(longFlag)        

    options.append(opt)


# This exception is used when a flag already exists.
class FlagInUse(Exception):
    """
    An exception that occurs when a flag is already under use.
    """
    pass


# The main class.
class ArgumentParser():
    """
    Initialise an argument parser.
    """
    def __init__(self, description: str, argv: list[str], name: str = None) -> None:
        self.desc = description

        # in case the program name isn't defined for some godforsaken reason
        if name:
            self.name = name
        else:
            self.name = argv[0]
        self.argv = argv

    
    def Argument(self, aname: str, help: str,  type: type):
        """
        An argument is any positional value that is  
        """
        if aname: 
            for i in self.argv:
                # and modern problems require modern solutions. 
                if i not in Oflags and i not in Fflags and i not in args and i not in optionValues and i != self.argv[0]: 
                    args.append(i)
                    return type(i)
    
    def Flag(self, aname: str, help: str, customShort = "", customLong = "", longAndShort = False, shortOnly = False) -> bool:
        
        # By default, Flag() takes the name of the flag to generate both long and short flags.
        # longAndShort enables both long and short flags.
        # As of now, I still haven't implemented the short-only flag.

        # "Auto-generate" flag names
        if customShort:
            # If a custom name is defined.
            shortFlag = f"-{customShort}"
            if shortFlag in Fshortflags:
                raise FlagInUse("Short flag already in use")
        else:
            shortFlag = f"-{list(aname)[0]}"
            if shortFlag in Fshortflags:
                shortFlag = f"-{list(aname)[2]}"

        if customLong:
            # If a custom name is defined.
            longFlag = f"--{customLong}"
            if longFlag in Flongflags:
                raise FlagInUse("Long flag already in use")

        else:
            longFlag = f"--{aname}"
            if longFlag in Flongflags:
                raise FlagInUse("Long flag already in use")

        # After defining short and long flags, register it.
        KeepTrackofOperations(type="flg", help=help, name=aname, longFlag=longFlag, shortFlag=shortFlag)

        
        # Parse arguments and return a boolean value. 

        if longAndShort:
            
            if longFlag in self.argv or shortFlag in self.argv:
                return True
            else:
                return False

        elif shortOnly:
            
            if shortFlag in self.argv:
                return True
            else:
                return False

        else:

            if longFlag in self.argv:
                return True
            else:
                return False

    
    def Option(self, aname: str, help: str, type: type, long = "", short = ""):
        """An option is a flag which can store a value."""        
        
        # check if a custom long flag is not defined.
        if not long: 
            long = f"--{aname}"
        if long in Olongflags:
            # If there is already a flag
            raise FlagInUse(f"Long flag {long} already in use")

        # check if a custom short flag is not defined.
        if short and short in Oshortflags: raise FlagInUse(f"Short flag {short} already in use") 
        
        if not short: 
            # "Auto-generate a short flag"
            short = f"-{list(aname)[0]}"
            if short in Oshortflags:
                # if the auto-gen'd flag is already in the short flags list
                short = f"-{list(aname)[2]}"

        # Register the options.
        KeepTrackofOperations(type="opt", help=help, name=aname, longFlag=long, shortFlag=short)

        # Parse the option.
        if long in self.argv:
            flagIndex = self.argv.index(long)
        elif short in self.argv:
            flagIndex = self.argv.index(short)
            
        val = self.argv[flagIndex+1]
        optionValues.append(val)
        try:
            return type(val)
        except Exception as e:
            print(f'Exception: {e}')