from mafia_engine.base import GameObject

class Role(GameObject):
    """Denotes a game role, e.g. "mafioso" or "doctor".
    Roles consist of:
        - an Alignment (which determines WinCons (win conditions) and such);
        - Abilities (which are potential Actions);
        - Status
        - TODO: Other stuff (such as ActionPoint restrictions?)
    """
    
    def __init__(self, **kwargs):
        """
        Keys: name, alignment, abilities, status
        """
        super().__init__(self, **kwargs)
        #TODO Add local members.
        self.name = kwargs.get("name","")
        self.aligment = kwargs.get("alignment",None)
        self.abilities = kwargs.get("abilities",[]) # [Ability]
        self.status = kwargs.get("status",{})       # name : value

        pass


    pass