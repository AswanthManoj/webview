audio_recorder_script = """
class AudioRecorder {
    constructor(websocketUrl) {
        this.websocketUrl = websocketUrl;
        this.socket = null;
        this.audioContext = null;
        this.mediaStreamSource = null;
        this.processor = null;
        this.stream = null;
        this.isRecording = false;

        this.connect();
    }

    connect() {
        this.socket = new WebSocket(this.websocketUrl);
        this.socket.onmessage = this.handleServerMessage.bind(this);
        this.socket.onopen = () => console.log("WebSocket connection opened for audio recorder");
        this.socket.onclose = () => console.log("WebSocket disconnected for audio recorder");
    }

    handleServerMessage(event) {
        const message = JSON.parse(event.data);
        if (message.command === "start_recording") {
            this.startRecording();
        } else if (message.command === "stop_recording") {
            this.stopRecording();
        }
    }

    async startRecording() {
        if (this.isRecording) return;

        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.mediaStreamSource = this.audioContext.createMediaStreamSource(this.stream);
            this.processor = this.audioContext.createScriptProcessor(8192, 1, 1);

            this.processor.onaudioprocess = (event) => {
                const inputData = event.inputBuffer.getChannelData(0);
                const buffer = new Float32Array(inputData);
                this.socket.send(JSON.stringify({
                    type: "audio_data",
                    data: Array.from(buffer)
                }));
            };

            this.mediaStreamSource.connect(this.processor);
            this.processor.connect(this.audioContext.destination);
            this.isRecording = true;
            console.log("Recording started");
        } catch (error) {
            console.error("Audio recorder recording error:", error);
        }
    }

    stopRecording() {
        if (!this.isRecording) return;

        if (this.processor) {
            this.processor.disconnect();
            this.mediaStreamSource.disconnect();
        }
        if (this.audioContext) {
            this.audioContext.close();
        }
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        this.isRecording = false;
        console.log("Recording stopped");
    }
}
"""