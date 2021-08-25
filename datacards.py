from kivymd.uix.card import MDCard

class DataCard(MDCard):
    title = 'DataCard'
    def __init__(self,tag,modbusClient,**kwargs):
        self.tag = tag
        self.title = self.tag['description']
        self._modbusClient = modbusClient
        super().__init__(**kwargs)

class CardHoldingRegister(DataCard):
    pass

class CardInputRegister(DataCard):
    pass

class CardCoil(DataCard):
    pass

class CardDiscreto(DataCard):
    pass
