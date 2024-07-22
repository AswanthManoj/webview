import time
from .app import start_app
from .config import config, Config
from typing import Callable, Optional
from .page_view import html_updater, HTMLUpdater, audio_player, AudioPlayer, AudioRecorder, audio_recorder

class WebView:
    """
    WebView class for managing the web-based user interface.

    This class provides a high-level interface for configuring, starting,
    and updating a web-based view. It encapsulates the configuration and
    HTML updating functionality, offering a simplified API for users.

    Attributes:
        config (Config): Configuration object for the WebView.
        html_updater (HTMLUpdater): Object responsible for updating the HTML content.
        audio_player (AudioPlayer): Object responsible for handling audio playback.

    Example:
    ```python
        from webview import webview
        webview.configure(host="localhost", port=5000, debug=True)
        webview.start_webview()
        webview.update_view("<h1>Hello, World!</h1>")
    ```
    """
    def __init__(self, config: Config, html_updater: HTMLUpdater, audio_player: AudioPlayer, audio_recorder: AudioRecorder):
        """
        Initialize a WebView instance.

        Args:
            config (Config): Configuration object for the WebView.
            html_updater (HTMLUpdater): Object responsible for updating the HTML content.
            audio_player (AudioPlayer): Object responsible for handling audio playback.
            audio_recorder (AudioRecorder): Object responsible for handling audio record control and stream.
        """
        self.config  = config
        self.html_updater = html_updater
        self.audio_player = audio_player
        self.audio_recorder = audio_recorder

    def configure(self, title="Webview App", host: str="127.0.0.1", port: int=8080, debug: bool=True, log_level: str="warning", custom_browser=False):
        """
        Configure the WebView settings.

        Args:
            title (str, optional): The title to be shown on the browser tab.
            host (str, optional): The host address for the server.
            port (int, optional): The port number for the server.
            debug (bool, optional): Whether to enable debug mode.
            log_level (str, optional): The logging verbosity for the fastapi server.
            custom_browser (bool, optional): Whether to use a custom browser implementation.
            
        Example:
        ```python
            from webview import webview
            webview.configure(title="Webview App", host="0.0.0.0", port=3000, debug=False, custom_browser=True)
            webview.start_webview()
        ```
        """
        self.config.set(title, host, port, debug, log_level, custom_browser)
    
    def update_view(self, html: str):
        """
        Update the HTML content of the WebView.

        This method can be called from a synchronous context.

        Args:
            html (str): The new HTML content to set.

        Example:
        ```python
            from webview import webview
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            
            webview.update_view("<div>New content</div>")
        ```
        """
        self.html_updater.update_view(html)
        
    async def async_update_view(self, html: str):
        """
        Asynchronously update the HTML content of the WebView.

        This method should be called from an asynchronous context.

        Args:
            html (str): The new HTML content to set.

        Example:
        ```python
            import asyncio
            from webview import webview
            
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            
            async def update():
                ...
                await Webview.async_update_view("<div>Async update</div>")
                
            asyncio.run(update())
        ```
        """
        await self.html_updater.async_update_view(html)
        
    def play_audio(self, audio_data: str, delay: float=None) -> str:
        """
        Play audio data in the WebView.

        This method can be called from a synchronous context.

        Args:
            audio_data (str): The audio data to play.
            delay (float): A delay to start the audio play.

        Returns:
            str: The unique ID of the audio task.

        Example:
        ```python
            from webview import webview
            from webview.utils import read_and_encode_mp3
            
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            
            audio = read_and_encode_mp3("sample/sample_audio1.mp3")
            audio_id = webview.play_audio(audio)
        ```
        """
        return self.audio_player.play_audio(audio_data, delay)
        
    async def async_play_audio(self, audio_data: str, delay: float=None) -> str:
        """
        Asynchronously play audio data in the WebView.

        This method should be called from an asynchronous context.

        Args:
            audio_data (str): The audio data to play.
            delay (float): A delay to start the audio play.

        Returns:
            str: The unique ID of the audio task.

        Example:
        ```python
            import asyncio
            from webview import webview
            from webview.utils import read_and_encode_mp3
            
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            
            async def play():
                ...     
                audio = read_and_encode_mp3("sample/sample_audio1.mp3")
                audio_id = await webview.async_play_audio(audio)
            asyncio.run(play())
        ```
        """
        return await self.audio_player.async_play_audio(audio_data, delay)
    
    def start_recording(self, audio_processor: Callable[[bytes], None]) -> bool:
        """
        Start recording audio in the WebView.

        This method can be called from a synchronous context.

        Args:
            audio_processor (Callable[[bytes], None]): A callback function to process the recorded audio data.

        Returns:
            bool: True if the recording was successfully started, otherwise False.

        Example:
        ```python
            from webview import webview
            
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            
            def process_audio(audio_bytes):
                print("Audio data received:", audio_bytes)
            
            webview.start_recording(process_audio)
        ```
        """
        return self.audio_recorder.start_recording(audio_processor)    
    
    async def async_start_recording(self, audio_processor: Callable[[bytes], None]) -> bool:
        """
        Asynchronously start recording audio in the WebView.

        This method should be called from an asynchronous context.

        Args:
            audio_processor (Callable[[bytes], None]): A callback function to process the recorded audio data.

        Returns:
            bool: True if the recording was successfully started, otherwise False.

        Example:
        ```python
            import asyncio
            from webview import webview
            
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            
            async def start_recording():
                def process_audio(audio_bytes):
                    print("Audio data received:", audio_bytes)
                    
                await webview.async_start_recording(process_audio)
            
            asyncio.run(start_recording())
        ```
        """
        return await self.audio_recorder.async_start_recording(audio_processor)   
        
    def stop_recording(self) -> bool:
        """
        Stop recording audio in the WebView.

        This method can be called from a synchronous context.

        Returns:
            bool: True if the recording was successfully stopped, otherwise False.

        Example:
        ```python
            from webview import webview
            
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            
            ...
            webview.stop_recording()
        ```
        """
        return self.audio_recorder.stop_recording()
    
    async def async_stop_recording(self) -> bool:
        """
        Asynchronously stop recording audio in the WebView.

        This method should be called from an asynchronous context.

        Returns:
            bool: True if the recording was successfully stopped, otherwise False.

        Example:
        ```python
            import asyncio
            from webview import webview
            
            webview.configure(host="localhost", port=5000, debug=True)
            webview.start_webview()
            ...
            async def stop_recording():
                await webview.async_stop_recording()
                
            asyncio.run(stop_recording())
        """
        return await self.audio_recorder.async_stop_recording()
    
    def start_webview(self) -> bool:
        """
        Start the WebView application.

        This method starts the FastAPI application in a separate thread and
        waits for 2 seconds to allow the server to initialize.

        Returns:
            bool: True if the WebView was successfully started.

        Example:
        ```python
            from webview import webview
            
            webview.configure(host="localhost", port=5000, debug=True)
            success = webview.start_webview()
            
            print("WebView started successfully" if success else "Failed to start WebView")
        """
        if self.config.debug:
            print("Webview: Starting the webview server...")
        start_app(self.config)
        print(f"Webview: Webview server started, you can view it at http://{self.config.host}:{self.config.port}/")
        return True


webview = WebView(
    config=config, 
    html_updater=html_updater, 
    audio_player=audio_player,
    audio_recorder=audio_recorder
)