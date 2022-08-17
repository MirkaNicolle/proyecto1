'''
Proyecto 1 - chat usando protocolo existente
Redes 
Miguel Novella - Seccion 10 
Mirka Monzon 18139
'''
#imports
from sheet import clear_screen, enter_para_continuar, obtener_clave, menu, menu_inicio, menu_chat
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET
import threading

class ListClients(slixmpp.ClientXMPP):
    #lista
    def __init__(self, usuario, clave, user=None, msg_precencia=None):
        slixmpp.ClientXMPP.__init__(self, usuario, clave)

        #eventos
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.user_details = None
        self.msg_precencia = msg_precencia

        self.register_plugin('xep_0030') #service Discovery
        self.register_plugin('xep_0199') #XMPP Ping
        self.register_plugin('xep_0045') #mulit-User Chat (MUC)
        self.register_plugin('xep_0096') #jabber Search

    async def start(self, event):
        #envio de mensaje de presencia
        self.send_presencia()
        await self.get_roster()

        user_list = []
        
        try:
            #verifica la lista
            self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: time out')
        
        self.presences.wait(3)

        roster = self.client_roster.groups()

        for group in roster:
            for user in roster[group]:
                details = self.client_roster.presence(user)
                if self.user and self.user == user:
                    
                    user_details = {}
                    status = None
                    show = None
                    priority = None

                    for key, value in details.items():
                        if value['status']:
                            status = value['status'] #status                                         
                        if value['show']:
                            show = value['show'] #show                                             
                        if value['priority']:
                            priority = value['priority'] #prioridad                                   
                    
                    user_details['status'] = status
                    user_details['show'] = show
                    user_details['priority'] = priority

                    self.user_details = user_details

                if "alumchat.fun" in user:
                    user_list.append(user)
        
        self.contacts = user_list

        if self.msg_precencia:
            for contact in self.contacts:
                self.sendPresenceMsg(contact)

        if self.user:
            print("\n" + self.user_details)
        else:
            if len(user_list) == 0:
                print('No tienes contactos')

            for contact in user_list:
                print('Usuario: ' + contact)

        self.disconnect()
    
    def sendPresenceMsg(self, usuario):
        #enviar mensaje

        message = self.Message()
        message['to'] = usuario
        message['type'] = 'chat'
        message['body'] = self.msg_precencia

        try:
            message.send()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: time out')

class SubscribeClient(slixmpp.ClientXMPP):
    #agrerar contacto

    def __init__(self, usuario, clave, new_contact):
        slixmpp.ClientXMPP.__init__(self, usuario, clave)
        self.add_event_handler("session_start", self.start)
        self.new_contact = new_contact

        self.register_plugin('xep_0030') #service Discovery
        self.register_plugin('xep_0199') #XMPP Ping
        self.register_plugin('xep_0045') #mulit-User Chat (MUC)
        self.register_plugin('xep_0096') #jabber Search


    async def start(self, event):
        self.send_presencia()
        await self.get_roster()
        try:
            self.send_presencia_subscription(pto=self.new_contact)
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: time out')
            
        self.disconnect()

class SendMsg(slixmpp.ClientXMPP):
    #envio y recibo de mensajes

    def __init__(self, usuario, clave, to, msg):
        slixmpp.ClientXMPP.__init__(self, usuario, clave)

        self.to = to
        self.msg = msg

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.msg)

        self.register_plugin('xep_0030') #service Discovery
        self.register_plugin('xep_0199') #XMPP Ping
        self.register_plugin('xep_0045') #mulit-User Chat (MUC)
        self.register_plugin('xep_0096') #jabber Search

    async def start(self, event):
        #enviar mensaje de presencia
        self.send_presencia()
        await self.get_roster()

        #enviar mensaje de chat
        self.send_message(mto=self.to,
                        mbody=self.msg,
                        mtype='chat')

        self.disconect()

    def message(self, msg):
        #print mensaje
        if msg['type'] in ('chat'):
            to = msg['to']
            body = msg['body']
            
            #print mensaje y receptor
            print(str(to) +  ": " + str(body))

            #nuevo mensaje
            new_msg = input(">>")

            #enviar mensaje
            self.send_message(mto=self.to,
                            mbody=new_msg)

class MUC(slixmpp.ClientXMPP):
    #chats grupales

    def __init__(self, usuario, clave, rusuario, alias):
        slixmpp.ClientXMPP.__init__(self, usuario, clave)

        self.usuario = usuario
        self.rusuario = rusuario
        self.alias = alias

        #events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.rusuario,
                            self.muc_online)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0199')

    async def start(self, event):
        #envia eventos
        await self.get_roster()
        self.send_presencia()
        self.plugin['xep_0045'].join_muc(self.rusuario,self.alias)

        #mensaje a escribir
        message = input("Escribe el mensaje: ")
        self.send_message(mto=self.rusuario,
                        mbody=message,
                        mtype='groupchat')

    #mensaje MUC 
    def muc_message(self, msg):
        if(str(msg['from']).split('/')[1]!=self.alias):
            print(str(msg['from']).split('/')[1] + ": " + msg['body'])
            message = input("Escribe el mensaje: ")
            self.send_message(mto=msg['from'].bare,
                            mbody=message,
                            mtype='groupchat')

    #Envia mensaje grupal
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.alias:
            self.send_message(mto=presence['from'].bare,
                            mbody="Hello, %s %s" % (presence['muc']['role'],
                                                    presence['muc']['alias']),
                            mtype='groupchat')

class SendFile(slixmpp.ClientXMPP):
    #enviar mensaje 

    def __init__(self, usuario, clave, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, usuario, clave)

        self.receiver = receiver

        self.file = open(filename, 'rb')

        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030') #service Discovery
        self.register_plugin('xep_0065') #SOCKS5 Bytestreams


    async def start(self, event):
        try:
            #abre S5B stream para escritura
            proxy = await self['xep_0065'].handshake(self.receiver)

            #envio del archivo
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)

            #cierre del stream
            proxy.transport.write_eof()
        except (IqError, IqTimeout):
            print('Archivo transeferido fallido')
        else:
            print('Archivo transeferido completado')
        finally:
            self.file.close()
            self.disconnect()

class DeleteAccount(slixmpp.ClientXMPP):
    #borrar cuenta

    def __init__(self, usuario, clave):
        slixmpp.ClientXMPP.__init__(self, usuario, clave)

        self.user = usuario
        #events
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presencia()
        self.get_roster()

        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            #envio del iq borrado
            delete.send(now=True)

        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: time out')
        except Exception as e:
            print(e)  

        self.disconnect()

