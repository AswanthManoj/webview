html_updater_script = """
class HtmlUpdater {
    constructor(wsUrl) {
        this.socket = new WebSocket(wsUrl);
        this.socket.onopen = this.onOpen.bind(this);
        this.socket.onmessage = this.onMessage.bind(this);
        this.socket.onclose = this.onClose.bind(this);
        this.socket.onerror = this.onError.bind(this);
    }

    onOpen(event) {
        console.log('WebSocket connection opened for html updater');
    }

    onMessage(event) {
        document.getElementById("main_update_content").innerHTML = event.data;
    }
    
    onClose(event) {
        console.log('WebSocket connection closed for html updater');
    }
    
    onError(error) {
        console.error('Html updater websocket error:', error);
    }
}
"""