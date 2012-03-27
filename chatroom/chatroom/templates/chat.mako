<%inherit file="/base.mako" />

<%def name="head_tags()">
<style type="text/css">
body {
  padding: 20px;
  margin: 0;
  background: #22252a;
  color: #eee;

  font-family: DejaVu Sans Mono, fixed; 
  line-height: 150%;
}

#messages .hidden {
    display: none;
}

#method_text {
    display: block;
    float: left;
    color: #CCC;
    font-size: 10pt;
    clear: both;
    margin: 5px;
}

#leave {
   float:left;
   display: block;
   color: white;
   font-size: 20px;
   text-decoration: none;
   padding: 10px;
}

#leave:hover {
    color: grey;
}

/* Input Box */
#input_box {
    clear: left;
}
#input_box input {
    font-size: 16pt;
    background-color: #33352a;
    padding: 8px;
    border: solid #aaa 1px;
    color: white;
    display: block;
    float: left;
    width: 85%;
}

/* Message Board */
.message {
    clear: left;
    margin-top: 20px;
    display: block;
    float:left;
    width: 90%;
    border-bottom: 1px solid #555;
    padding-bottom: 5px;
}
.message *
{
    float: left;
    display: block;
    margin-left: 8px;
    font-size: 16pt;

}
.message .time
{
    color: #888;
    font-size: 10pt;
    margin-top: 3px;
    float: right;
}
.message .name {
    color: yellow;
}
.message .content {
    color: #EEE;
    white-space:wrap;
    width: 90%;
}
</style>
<script type="text/javascript">
methods = {
    "event": { name: "Event-based Long Polling", 
               call: update_client_poll }, 
    "multithread": { name: "Multithreading Long Polling",
                        call: update_long_polling },
    "client": { name: "Client Polling",
               call: update_client_poll }, 
};

function update() {
    methods["${c.polling}"].call();
}
function update_client_poll() {
    (function poll() {
     setTimeout(function(){
         $.ajax({ url: "/message/update",
                  success: function(data){
                     add_new_message_nodes(data);
                     //Setup the next poll recursively
                     poll();
                  }, 
                  dataType: "json", 
                  type: "POST"});
         }, 1000);
     })();
}

function update_long_polling() {
    (function poll(){
         $.ajax({ url: "/message/update_long_poll",
                 success: add_new_message_nodes, 
                 error: function() { console.log("error occurs"); },
                 dataType: "json", complete: poll, timeout: 50000 });
         })();
}

function add_new_message_nodes(data) {
    if (data == null || data.result == "error")
        return;

    var messages = data.data;
    for (i = 0; i < messages.length; ++i) {
        var message = messages[i];
        add_new_message_node(message);
    }
}
function add_new_message_node(message) {
    var board = $("#messages");
    var node = $("#message_sample").clone();
    node.children(".time").html(message["time"]);
    node.children(".name").html(message["nickname"]);
    node.children(".content").html(message["content"]);
    node.attr("id", "");
    // TODO: Quck and dirty fix of the "UNSEEN" message in
    // in Safari
    board.prepend(node);
    node.fadeIn(300);
}

function add(message) {
    if (message == null || message.length == 0)
        return;
    data = {"content": message}
    $.post("/message/add", data, function(data) {
    });
}

$(document).ready(function () {
    textbox = $("#textbox");
    textbox.keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            add(textbox.val());
            textbox.val("");
        }
    });

    // 
    textbox.focus();

    // title
    document.title = "${c.nickname} - Chat room";
    $("#method_text").html("Polled by: "+ methods["${c.polling}"]["name"]);

    // 
    update();
});
</script>
</%def>

<div id="input_box">
    <input id = "textbox" type="text"></input>
    <a href="/room/leave" id="leave">Leave</a>
</div>
<span id="method_text"></span>
<div id="messages" onload="init()">
    <div id = "message_sample" class="message hidden">
        <span class="time">2010-10-30 1:20</span>
        <span class="name">Name</span>
        <div class="content">Content</div>
    </div>
</div>
