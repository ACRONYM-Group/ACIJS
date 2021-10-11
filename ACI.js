runningInNode = false;
if (typeof window === 'undefined') {
    runningInNode = true;
} else {
    runningInNode = false;
}
if (runningInNode) {
    console.log("Running in Node")
    var WebSocket = require('isomorphic-ws');
}

class connection {
    constructor(ip, port, connectedCallBack, messageCallback) {
        this.ip = ip;
        this.port = port;
        this.connected = false;
        this.connectedCallBack = connectedCallBack;
        this.messageCallback = messageCallback;
        this.user_id = "";
    }

    start() {

        console.log("Starting");
        this.websocket = new WebSocket('ws://' + this.ip + ':' + this.port);
        this.websocket.connectionReference = this;

        this.websocket.onopen = this.onOpenHandler

        this.websocket.onmessage = this.onMessageHandler
        this.websocket.onerror = this.onConnectionErrorHandler
    }

    onOpenHandler(event) {
        console.log('connected to ' + event.target.connectionReference.ip);
        event.target.connectionReference.connected = true;
        event.target.connectionReference.connectedCallBack();
    }

    onConnectionErrorHandler(event) {
        console.log("Error connecting to ACI.");
    }

    onMessageHandler(event) {
        var msg = JSON.parse(event.data);

        event.target.connectionReference.messageCallback(msg);
    }

    getRequest(key, db_key) {
        var data = JSON.stringify({"cmd":"get_value", "key":key, "db_key":db_key})
        this.websocket.send(data);
    }

    printIP() {
        console.log(this.ip);
    }

    setRequest(key, db_key, val, conn) {
        this.websocket.send(JSON.stringify({"cmd":"set_value", "key":key, "db_key":db_key, "val":val}));
    }

    get_index_request(key, db_key, index) {
        this.websocket.send(JSON.stringify({"cmd":"get_index", "key":key, "db_key":db_key, "index":index}));
    }

    set_index_request(key, db_key, index, value) {
        this.websocket.send(JSON.stringify({"cmd":"set_index", "key":key, "db_key":db_key, "index":index, "value":value}));
    }

    append_list_request(key, db_key, value) {
        this.websocket.send(JSON.stringify({"cmd":"append_list", "key":key, "db_key":db_key, "value":value}));
    }

    get_list_length_request(key, db_key) {
        this.websocket.send(JSON.stringify({"cmd":"get_list_length", "key":key, "db_key":db_key}));
    }

    get_recent_request(key, db_key, num) {
        this.websocket.send(JSON.stringify({"cmd":"get_recent", "key":key, "db_key":db_key, "num":num}));
    }

    authenticate(id_token) {
        this.user_id = id;
        this.websocket.send(JSON.stringify({"cmd":"g_auth", "id_token":id_token}));
    }

    a_authenticate(id, token) {
        this.user_id = id;
        this.websocket.send(JSON.stringify({"cmd":"a_auth", "id":id, "token":token}));
    }

    send_event(destination, id, data) { //Send ACI Event
        this.websocket.send(JSON.stringify({"cmd":"event", "destination":destination, "origin":this.user_id, "event_id":id, "data":data}));
    }
}

if (runningInNode) {
    exports.connection = connection;
}

console.log("ACI Loaded");
