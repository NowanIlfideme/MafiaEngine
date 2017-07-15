
class Role(object):
    """Denotes a game role, e.g. "mafioso" or "doctor".
    Roles consist of:
        - an Alignment (which determines WinCons (win conditions) and such);
        - Abilities (which are potential Actions);
        - Status
        - TODO: Other stuff (such as ActionPoint restrictions?)
    """
    
    def __init__(self, alignment):
        #TODO Add local members.
        self.alignment = alignment
        self.status = {}    # name : value
        self.abilities = {} # name : Ability

        pass


    pass