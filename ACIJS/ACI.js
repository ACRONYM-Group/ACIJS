runningInNode = false;
if (typeof window === 'undefined') {
    runningInNode = true;
} else {
    runningInNode = false;
}

if (runningInNode) {
    const WebSocket = require('isomorphic-ws')
}

class connection {
    constructor(ip, port, connectedCallBack, messageCallback) {
        this.ip = ip;
        this.port = port;
        this.connected = false;
        this.connectedCallBack = connectedCallBack;
        this.messageCallback = messageCallback;
    }

    start() {
        console.log("Starting");
        this.websocket = new WebSocket('ws://' + this.ip + ':' + this.port);
        this.websocket.connectionReference = this;

        this.websocket.onopen = this.onOpenHandler

        this.websocket.onmessage = this.onMessageHandler
    }

    onOpenHandler(event) {
        console.log('connected to ' + event.target.connectionReference.ip);
        event.target.connectionReference.connected = true;
        event.target.connectionReference.connectedCallBack();
    }

    onMessageHandler(event) {
        var msg = JSON.parse(event.data);

        event.target.connectionReference.messageCallback(msg);
    }

    getRequest(key, db_key) {
        var data = JSON.stringify({"cmdType":"get_val", "key":key, "db_key":db_key})
        this.websocket.send(data);
    }

    printIP() {
        console.log(this.ip);
    }

    setRequest(key, db_key, val, conn) {
        this.websocket.send(JSON.stringify({"cmdType":"set_val", "key":key, "db_key":db_key, "val":val}));
    }
}

if (runningInNode) {
    exports.connection = connection;
}

console.log("ACI Loaded");
