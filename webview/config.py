from typing import Optional

class Config:
    """
    Configuration class for the WebView application.

    This class manages the configuration settings for the WebView application,
    including server settings, debug mode, and browser options.

    Attributes:
        title (str): The title to be shown on the browser tab.
        host (str): The host address for the server. Defaults to "127.0.0.1".
        port (int): The port number for the server. Defaults to 8080.
        debug (bool): Whether debug mode is enabled. Defaults to False.
        log_level (str): The logging verbosity for the fastapi server. Defaults to "warning".
        custom_browser (bool): Whether to use a custom browser implementation. Defaults to False.

    Example:
        >>> from webview import config
        >>> config.set(title="my server", host="localhost", port=5000, debug=True, custom_browser=True)
        >>> print(config.title, config.host, config.port, config.debug, config.custom_browser)
        my server localhost 5000 True True
    """
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8080
        self.debug = False
        self.log_level = "warning"
        self.title = "Webview Server"
        self.custom_browser = False
        
    def set(self, title: Optional[str] = None, host: Optional[str] = None, 
            port: Optional[int] = None, debug: Optional[bool] = None, 
            log_level: Optional[str] = None, custom_browser: Optional[bool] = None):
        """
        Set the configuration parameters for the WebView application.

        Args:
            title (str, optional): The title to be shown on the browser tab.
            host (str, optional): The host address for the server.
            port (int, optional): The port number for the server.
            debug (bool, optional): Whether to enable debug mode.
            log_level (str, optional): The logging verbosity for the fastapi server.
            custom_browser (bool, optional): Whether to use a custom browser implementation.
            
        Example:
            >>> from webview import config
            >>> config.set(title="my-webview", host="0.0.0.0", port=3000, debug=True, custom_browser=True)
        """
        if title is not None:
            self.title = title
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if debug is not None:
            self.debug = debug
        if log_level is not None:
            self.log_level = log_level
        if custom_browser is not None:
            self.custom_browser = custom_browser

config = Config()