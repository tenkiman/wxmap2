from w2base import *

class W2(W2Base):

    def __init__(self,
                 W2BaseDirDat=None,
                 ):


        self.W2BaseDirDat=W2BaseDirDat

        self.initW2LocalVars()
        self.initW2GlobalVars()
        self.initW2VarsSwitches()
        self.initW2VarsModule()
        self.initW2VarsEnv()
        self.initW2VarsAll()
        self.initW2VarsNwp2()
        self.initW2VarsClimo()

