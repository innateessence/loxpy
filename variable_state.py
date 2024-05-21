"""
I want all variables to store some metadata in a very performant way that's easily portable to C
"""

# https://ruby-doc.com/docs/ProgrammingRuby/html/taint.html#:~:text=Tainted%20Objects,shown%20in%20the%20code%20below.
# Reference $SAFE levels in Ruby
# Consider using a similar approach to Ruby's taint mechanism. But providing a more simplistic interface for the developer.

from enum import Enum


class BinaryEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return 1 << count


class VariableMetadata(BinaryEnum):
    UNKNOWN = 1  # This variable safety level is unknown (e.g. not initialized / not specified) This is the default
    TAINTED = 2  # This variable has been tainted (e.g. by user input)
    TRUSTED = 4  # This variable is trusted (e.g. by a security check)


class VariableMetaTraits:
    """This class is a wrapper around the metadata of a variable. It allows us to easily interact with the metadata of a variable"""

    def __init__(self):
        self.metadata = 0

    def has_property(self, property):
        return self.metadata & property == property

    def add_property(self, property):
        self.metadata |= property

    def remove_property(self, property):
        if self.has_property(property):
            self.metadata -= property

    def reset_properties(self):
        self.metadata = 0

    def __repr__(self):
        return "<VariableMetadata %r>" % self.metadata
