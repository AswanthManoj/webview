import browsers as br
from .config import Config
from typing import Optional
from threading import Thread
from .utils import ensure_event_loop
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request
from playwright.async_api import async_playwright
from webview.scripts.html_updater import html_updater_script
from webview.scripts.audio_player import audio_player_script
from webview.scripts.audio_recorder import audio_recorder_script
from .page_view import html_updater, audio_player, audio_recorder


config: Optional[Config] = None
page, browser, playwright = None, None, None


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await shutdown


app = FastAPI(lifespan=lifespan)
AUDIO_PLAYER_ENDPOINT = "ws-audio-player"
HTML_UPDATER_ENDPOINT = "ws-html-updater"
AUDIO_RECORDER_ENDPOINT = "ws-audio_recorder"


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    global config
    """
    Serve the main HTML page.
    
    Returns:
        HTMLResponse: The rendered HTML template.
    """
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>[=[title]=]</title>
        <style>
            html, body, #main_update_content {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
            }
        </style>
    </head>
    <body>
        <div id="main_update_content"></div>
        <script>
            [=[html_updater_script]=]   // has the class definition HtmlUpdater
            [=[audio_player_script]=]   // has the class definition AudioPlayer
            [=[audio_recorder_script]=] // has the class definition AudioRecorder
            
            // Initialize the AudioPlayer and AudioRecorder when the page loads
            window.onload = () => {
                new HtmlUpdater(`ws://[=[host]=]:[=[port]=]/[=[html_updater_endpoint]=]`);
                new AudioPlayer('ws://[=[host]=]:[=[port]=]/[=[audio_player_endpoint]=]');
                new AudioRecorder("ws://[=[host]=]:[=[port]=]/[=[audio_recorder_endpoint]=]");
            };
        </script>
    </body>
    </html>"""
    html = html.replace("[=[html_updater_script]=]", html_updater_script)
    html = html.replace("[=[audio_player_script]=]", audio_player_script)
    html = html.replace("[=[audio_recorder_script]=]", audio_recorder_script)
    html = html.replace("[=[host]=]", config.host)
    html = html.replace("[=[title]=]", config.title)
    html = html.replace("[=[port]=]", str(config.port))
    html = html.replace("[=[html_updater_endpoint]=]", HTML_UPDATER_ENDPOINT)
    html = html.replace("[=[audio_player_endpoint]=]", AUDIO_PLAYER_ENDPOINT)
    html = html.replace("[=[audio_recorder_endpoint]=]", AUDIO_RECORDER_ENDPOINT)
    return HTMLResponse(html)

@app.websocket(f"/{HTML_UPDATER_ENDPOINT}")
async def html_updater_socket(websocket: WebSocket):
    global config
    try:
        await html_updater.connect(websocket)
    except Exception as e:
        if config.debug:
            print(f"Client browser disconnected from html updater socket: {str(e)}")
        
@app.websocket(f"/{AUDIO_PLAYER_ENDPOINT}")
async def audio_playback_socket(websocket: WebSocket):
    global config
    try:
        await audio_player.connect(websocket)
    except Exception as e:
        if config.debug:
            print(f"Client browser disconnected from audio playback socket: {str(e)}")

@app.websocket(f"/{AUDIO_RECORDER_ENDPOINT}")
async def audio_recorder_socket(websocket: WebSocket):
    global config
    try:
        await audio_recorder.connect(websocket)
    except Exception as e:
        if config.debug:
            print(f"Client browser disconnected from audio recorder socket: {str(e)}")


async def start_browser():
    global browser, page, playwright, config
    url = f"http://{config.host}:{config.port}/"
    if config.custom_browser:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=False, 
            args=[
                '--fullscreen',
                '--no-first-run', 
                '--start-maximized',
                '--disable-infobars', 
                '--no-default-browser-check',
                '--autoplay-policy=no-user-gesture-required'
            ],
            ignore_default_args=['--enable-automation']
        )
        context = await browser.new_context(
            viewport=None,
            no_viewport=True,  
            color_scheme='dark'
        )
        page = await context.new_page()
        await page.goto(url, wait_until='domcontentloaded')
        await page.evaluate('''document.body.style.overflow='hidden';''')
    elif browsers := list(br.browsers()):
        br.launch(browsers[0].get("browser_type"), url=url)
        
async def shutdown():
    global browser, playwright
    if playwright and browser:
        await browser.close()
        await playwright.stop()

def run_app():
    global config
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level)

def start_app(server_config: Config) -> bool:
    """
    Start the FastAPI application in a separate thread.

    This function creates a new thread to run the FastAPI application,
    allowing the main thread to continue execution.

    Example:
        >>> from webview import start_app
        >>> start_app()
        >>> # The app is now running in the background
    """
    global config
    config = server_config
    
    thread = Thread(target=run_app, daemon=True)
    thread.start()
    
    loop = ensure_event_loop()
    loop.run_until_complete(start_browser())
    
    return True