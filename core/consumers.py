import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SeatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = f'event_{self.event_id}'

        # Únete al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print('WebSocket conectado:', self.channel_name)

    async def disconnect(self, close_code):
        # Sal del grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('WebSocket desconectado:', self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        seat_id = data['seat_id']
        status = data['status']

        print('Mensaje recibido:', data)

        # Envia el mensaje a la sala del grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'seat_status',
                'seat_id': seat_id,
                'status': status
            }
        )

    async def seat_status(self, event):
        seat_id = event['seat_id']
        status = event['status']

        print('Actualizando asiento:', seat_id, 'a', 'reservado' if status else 'disponible')

        # Envia el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'seat_id': seat_id,
            'status': status
        }))
