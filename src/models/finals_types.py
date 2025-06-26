class Finals_Types:
    
    types = {
        1: "Elimination Final",
        2: "Qualifying Final",
        3: "Preliminary Final",
        4: "Semi Final",
        5: "Grand Final"
    }

    def __init__(self, name):
        self.name = name
        self.id = None
        if name is None:
            return
        for fid, type in self.types.items():
            if type.lower() == name.lower():
                self.id = fid
                break