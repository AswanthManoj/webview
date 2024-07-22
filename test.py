import asyncio
import threading, time
from webview import webview
from webview.utils import read_and_encode_mp3

async def async_updater():
    i=0
    while True:
        await webview.async_update_view(f"""<h2>
            <button>click me</button>
            This is update number {i}
            </h2>""")
        await asyncio.sleep(1)
        i+=1

def updater():
    i=0
    while True:
        webview.update_view(f"""<h2>
            <button>click me</button>
            This is update number {i}
        </h2>""")
        time.sleep(1)
        i+=1


async def async_main():
    task = asyncio.create_task(async_updater())
    
    # Plays a sample audio in the browser
    audio_1 = read_and_encode_mp3("sample/sample_audio1.mp3")
    audio_id = await webview.async_play_audio(audio_1)
    print("Audio with id", audio_id, "is playing")
    
    # Plays a second sample audio after a 3 second delay
    audio_2 = read_and_encode_mp3("sample/sample_audio2.mp3")
    audio_id = await webview.async_play_audio(audio_2, delay=3) 
    print("Audio with id", audio_id, "is playing")
    
    # await asyncio.gather(task)
   
   

def main():
    thread = threading.Thread(target=updater, daemon=True)
    thread.start()
    
    # Plays a sample audio in the browser
    audio_1 = read_and_encode_mp3("sample/sample_audio1.mp3")
    audio_id = webview.play_audio(audio_1)
    print("Audio with id", audio_id, "is playing")
    
    # Plays a second sample audio after a 3 second delay
    audio_2 = read_and_encode_mp3("sample/sample_audio2.mp3")
    audio_id = webview.play_audio(audio_2, delay=3)
    print("Audio with id", audio_id, "is playing")  

    thread.join()

    
    
if __name__=='__main__':  
    webview.configure(log_level="critical", custom_browser=True)
    webview.start_webview() 
    
    main()
    
    # asyncio.run(async_main())
    