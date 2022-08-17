'''
Proyecto 1 - chat usando protocolo existente
Redes 
Miguel Novella - Seccion 10 
Mirka Monzon 18139
'''
#imports
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

class Registro(slixmpp.ClientXMPP):

    def __init__(self, usuario, clave):
        slixmpp.ClientXMPP.__init__(self, usuario, clave)

        self.add_event_handler("session_start", self.start)

        self.add_event_handler("register", self.register)

        self.register_plugin('xep_0030') #service Discovery
        self.register_plugin('xep_0004') #data forms
        self.register_plugin('xep_0066') #out-of-band Data
        self.register_plugin('xep_0077') #in-band Registration

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()

    async def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundusuario.user
        resp['register']['password'] = self.clave

        try:
            await resp.send()
            print("\nAccount created: ", self.boundusuario, "\n")
        except IqError as e:
            print("\nCould not register account: ", e.iq['error']['text'], "\n")
            self.disconnect()
        except IqTimeout:
            print("\nNo response from server.")
            self.disconnect()