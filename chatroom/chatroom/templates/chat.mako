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
    overflow: hidden;
    width: 90%;
}
</style>
<script type="text/javascript">
function update() {
    update_long_polling();
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
                 dataType: "json", complete: poll, timeout: 10000 });
         })();
}


function add_new_message_nodes(messages) {
    if (messages == null)
        return;
    board = $("#messages")
    for (i = 0; i < messages.length; ++i) {
        var message = messages[i];
        add_new_message_node(message);
    }
}
function add_new_message_node(message) {
    node = $("#message_sample").clone();
    node.children(".date").html(message["time"]);
    node.children(".name").html(message["nickname"]);
    node.children(".content").html(message["content"]);
    // node.fadeIn(500);
    node.removeClass("hidden");
    board.prepend(node);
}

function add(message) {
    data = {"content": message}
    $.post("/message/add", data, function(data) {
    });
}
function init() {
    textbox = $("#textbox");
    textbox.keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            add(textbox.val());
            textbox.val("");
        }
    });

    update();
}
</script>
</%def>
<%def name="body_attr()">onload="init()"</%def>

<div id="input_box">
    <input id = "textbox" type="text"></input>
    <a href="/room/leave" id="leave">Leave</a>
</div>
<div id="messages" onload="init()">
    <div id = "message_sample" class="message hidden">
        <span class="time">2010-10-30 1:20</span>
        <span class="name">name</span>
        <div class="content">Content</div>
    </div>
</div>
