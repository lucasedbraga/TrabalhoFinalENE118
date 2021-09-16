from kivymd.uix.card import MDCard

class DataCard(MDCard):
    title = 'DataCard'
    def __init__(self,tag,modbusClient,**kwargs):

        self.tag = tag
        self.wait = False
        self.title = self.tag['description']
        self._modbusClient = modbusClient
        super().__init__(**kwargs)
        

    def update_data(self):
        try:
            if self._modbusClient.is_open():
                if self.wait == False:
                    self.value = self.set_data((self._read_data(self.tag['address'],1)[0])/self.tag['mult'])
                    return self.value

        except Exception as e:
            print(f"Erro na Leitura do dado {self.tag['name']} ",e.args)

    def write_data(self):
        try:
            if self._modbusClient.is_open():
                self._write_data_fcn(self.tag['address'],self.get_data())
                self.wait = False

        except Exception as e:
            print(f"Erro na escrita do dado {self.tag['name']} ",e.args)


class CardHoldingRegister(DataCard):
    def __init__(self, tag, modbusClient, **kwargs):
        super().__init__(tag,modbusClient,**kwargs)
        self._read_data = self._modbusClient.read_holding_registers
        self._write_data_fcn = self._modbusClient.write_single_register

    def set_data(self,data):
        if self.wait == False:
            value = str(data)
            self.ids.textfield.text = value
            return value

    def get_data(self):
        mult = int(self.tag['mult'])
        return int(self.ids.textfield.text)*mult

class CardInputRegister(DataCard):
    def __init__(self, tag, modbusClient, **kwargs):
        super().__init__(tag,modbusClient,**kwargs)
        self._read_data = self._modbusClient.read_input_registers

    def set_data(self,data):
        value = str(data)
        self.ids.label.text = value
        return value


class CardCoil(DataCard):
    def __init__(self, tag, modbusClient, **kwargs):
        super().__init__(tag,modbusClient,**kwargs)
        self._read_data = self._modbusClient.read_coils
        self._write_data_fcn = self._modbusClient.write_single_coil

    def set_data(self,data):
        value = data
        self.ids.switch.active = value
        return value

    def get_data(self):
        return self.ids.switch.active

