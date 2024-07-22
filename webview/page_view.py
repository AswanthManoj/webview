import numpy as np
import asyncio, json, uuid
from .config import Config
from .utils import ensure_event_loop
from typing import Callable, Optional
from fastapi import WebSocket, WebSocketDisconnect
import struct



class HTMLUpdater:
    def __init__(self):
        self.config = None
        self.html_content = ""
        self.change_detected = True
        self.client: WebSocket = None
        
    def bind_config(self, config: Config):
        self.config=config 

    def update_view(self, new_html: str):
        loop = ensure_event_loop()
        loop.run_until_complete(self.async_update_view(new_html))
        
    async def async_update_view(self, new_html: str): 
        if self.client:
            await self.client.send_text(new_html)
            if self.config and self.config.debug:
                print("Webview: View updated")
        elif self.config and self.config.debug:
            print("Webview: Client is not available for UI updates")
           
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected to html updater")
        try:
            while True:
                await websocket.receive_text()
        finally:
            self.client = None
  
     
            
class AudioPlayer:
    
    def __init__(self):
        self.config = None
        self.client: WebSocket = None
        self.audio_queue = asyncio.Queue()
        self.pending_audios: dict[str, bool] = {}
        
    def bind_config(self, config: Config):
        self.config=config    
        
    def play_audio(self, audio_data: str, delay: float) -> str:
        loop = ensure_event_loop()
        return loop.run_until_complete(self.async_play_audio(audio_data, delay))   
         
    async def async_play_audio(self, audio_data: str, delay: float) -> str:
        audio_id: str = str(uuid.uuid4())
        if self.client:
            await self.audio_queue.put((audio_id, audio_data, delay))
            self.pending_audios[audio_id] = True
        while True:
            if audio_id not in self.pending_audios:
                return audio_id
            
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected to audio player")
        try:
            while True:
                audio_id, audio_data, delay = await self.audio_queue.get()
                await websocket.send_text(json.dumps({
                    "type": "audio",
                    "id": audio_id,
                    "data": audio_data,
                    "delay": delay
                }))
                message = await websocket.receive_text()
                data = json.loads(message)
                
                if data['type'] == 'playback_complete':
                    if self.config and self.config.debug:
                        print(f"Audio playback completed for ID: {data['id']}")
                    del self.pending_audios[data['id']]
        finally:
            self.client = None
          
          
            
class AudioRecorder:

    def __init__(self) -> None:
        self.is_recording: bool = False
        self.config: Optional[Config] = None
        self.client: Optional[WebSocket] = None
        self.audio_processor: Optional[Callable[[bytes], None]] = None
        
    def bind_config(self, config: Config):
        self.config=config 
        
    def start_recording(self, audio_processor: Callable[[bytes], None]) -> bool:
        loop = ensure_event_loop()
        return loop.run_until_complete(self.async_start_recording(audio_processor))
        
    async def async_start_recording(self, audio_processor: Callable[[bytes], None]) -> bool:
        self.audio_processor = audio_processor
        if self.client:
            await self.client.send_json({"command": "start_recording"})
            self.is_recording = True
            return True
        else:
            return False
        
    def stop_recording(self) -> bool:
        loop = ensure_event_loop()
        return loop.run_until_complete(self.async_stop_recording())

    async def async_stop_recording(self) -> bool:
        if self.client:
            await self.client.send_json({"command": "stop_recording"})
            self.is_recording = False
            return True
        return False
    
    async def process_audio(self, audio_data: bytes):
        if self.is_recording:
            audio_np = np.frombuffer(audio_data, dtype=np.float32)
            audio_bytes = (audio_np * 32767).astype(np.int16).tobytes()
            if self.audio_processor:
                self.audio_processor(audio_bytes)
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected to audio recorder")
        try:
            while True:
                data = await websocket.receive_text()
                audio_data = json.loads(data)
                if audio_data['type'] == "audio_data":
                    # Convert the list of floats to bytes
                    float_list = audio_data['data']
                    byte_data = struct.pack(f'{len(float_list)}f', *float_list)
                    await self.process_audio(byte_data)
        finally:
            self.client = None
    


html_updater = HTMLUpdater()
audio_player = AudioPlayer()
audio_recorder = AudioRecorder()