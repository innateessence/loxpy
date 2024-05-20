"""
I want all variables to store some metadata in a very performant way that's easily portable to C
"""


class SafetyMetadata:
    UNKNOWN = 1  # This variable safety level is unknown (e.g. not initialized / not specified) This is the default
    TAINTED = 2  # This variable has been tainted (e.g. by user input)
    TRUSTED = 4  # This variable is trusted (e.g. by a security check)

class VariableMetadata:
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
