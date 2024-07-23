ui_event_listener_script = """
class UIEventHandler {
    static instance;

    constructor(websocketUrl) {
        if (UIEventHandler.instance) {
            return UIEventHandler.instance;
        }
        this.socket = new WebSocket(websocketUrl);
        this.socket.onopen = () => {
            console.log('WebSocket connection opened for UI event listening');
        };
        this.socket.onclose = () => {
            console.log('WebSocket connection closed for UI event listening');
            // Attempt to reconnect after a delay
            setTimeout(() => new UIEventHandler(websocketUrl), 5000);
        };
        UIEventHandler.instance = this;
    }

    sendEvent(elementId, eventType) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                elementId: elementId,
                eventType: eventType
            }));
        } else {
            console.error('WebSocket is not connected to UI event listening. Attempting to reconnect...');
            new UIEventHandler(this.socket.url);
        }
    }
}
"""