const ACI = require("./ACI.js");

function connectedCallBack() {
    conn.setRequest("val", "db1", "Hi World!");
    conn.getRequest("val", "db1");
}

function messageCallback(data) {
    if ( data["cmdType"] == "getResp") {
        console.log(data["db_key"] + "[" + data["key"] + "]" + " = " + data["val"]);
    }
}

const conn = new ACI.connection("127.0.0.1", 8765, connectedCallBack, messageCallback);