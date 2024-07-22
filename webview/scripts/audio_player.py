audio_player_script = """
class AudioPlayer {
    constructor(wsUrl) {
        this.socket = new WebSocket(wsUrl);
        this.audioQueue = [];
        this.isPlaying = false;

        this.socket.onopen = this.onOpen.bind(this);
        this.socket.onmessage = this.onMessage.bind(this);
        this.socket.onclose = this.onClose.bind(this);
        this.socket.onerror = this.onError.bind(this);
    }

    onOpen(event) {
        console.log('WebSocket connection opened for audio player');
    }

    onMessage(event) {
        const data = JSON.parse(event.data);
        
        if (data.type === 'audio') {
            this.audioQueue.push(data);
            if (!this.isPlaying) {
                this.playNextAudio();
            }
        }
    }

    onClose(event) {
        console.log('WebSocket connection closed for audio player');
    }

    onError(error) {
        console.error('Audio player websocket error:', error);
    }

    playNextAudio() {
        if (this.audioQueue.length === 0) {
            this.isPlaying = false;
            return;
        }

        this.isPlaying = true;
        const audioData = this.audioQueue.shift();

        this.playAudio(audioData.data, audioData.delay)
            .then(() => {
                this.socket.send(JSON.stringify({ 
                    type: 'playback_complete',
                    id: audioData.id
                }));
                this.playNextAudio();
            })
            .catch((error) => {
                console.error('Error playing audio:', error);
                this.playNextAudio();
            });
    }

    async playAudio(base64Audio, delay) {
        return new Promise((resolve, reject) => {
            const audio = new Audio(base64Audio);
            audio.onended = resolve;
            audio.onerror = reject;
            
            const playWithDelay = () => {
                audio.play().catch(reject);
            };
            
            if (delay && delay > 0) {
                setTimeout(playWithDelay, delay * 1000);
            } else {
                playWithDelay();
            }
        });
    }
}
"""