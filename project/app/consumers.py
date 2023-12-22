from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
# This is Server Side..

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket Connected...', event)
        print('Channels Layer...', self.channel_layer) # defalut channels layer
        print('Channels Name...', self.channel_name) # defalut channels name
        self.send({
            'type':'websocket.accept'
        })

        #groupname handle here
        self.group = self.scope['url_route']['kwargs']['groupname']
        print('group name..', self.group)

        # this funtion channels layer add in group
        async_to_sync(self.channel_layer.group_add)(
            self.group, self.channel_name) # ('group_name', self.channel_name)

    def websocket_receive(self, event):
        print('Message Recevied from clint..', event)
        print('type of recevied message...', type(event['text']))
        async_to_sync(self.channel_layer.group_send)(self.group, {
            'type':'chat.message', # is comparesaler its type chat message type.
            'message': event['text'] # we send this message to clint is can type as a ticke
        })

    def chat_message(self, event):
        print('EVENT....', event)
        print('Actual Data...', event['message'])
        print('type of data is...', type(event['message']))
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        print('Websocket DisConnected...', event)
        
        #if you are add channels layer in group so you can also group discard also.
        async_to_sync(self.channel_layer.group_discard)(
            self.group, self.channel_name)
        raise StopConsumer()