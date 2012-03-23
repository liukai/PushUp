<%inherit file="/base.mako" />

<%def name="head_tags()">
<script type="text/javascript">
    function update() {
        update_long_polling();
    }
    function update_client_poll() {
        (function poll() {
         setTimeout(function(){
             $.ajax({ url: "/message/update",
                 success: function(data){
                    console.log(data);
                    var messages = data;
                    board = $("#messages")
                    for (i = 0; i < messages.length; ++i) {
                        var message = messages[i];
                        node = $("#message_sample").clone();
                        node.children(".date").html(message["time"])
                        node.children(".name").html(message["id"])
                        node.children(".content").html(message["content"])
                        board.prepend(node);
                    }
                    //Setup the next poll recursively
                    poll();
                 }, dataType: "json", type: "POST"});
             }, 1000);
         })();
    }
    function update_long_polling() {
        (function poll(){
             $.ajax({ url: "/message/update_long_poll",
                     success: function(data){
                        console.log("one call")
                        console.log(data);
                        var messages = data;
                        board = $("#messages")
                        for (i = 0; i < messages.length; ++i) {
                            var message = messages[i];
                            node = $("#message_sample").clone();
                            node.children(".date").html(message["time"])
                            node.children(".name").html(message["id"])
                            node.children(".content").html(message["content"])
                            board.prepend(node);
                        }
                 }, dataType: "json", complete: poll, timeout: 10000 });
             })();
    }

    function add() {
        data = {"content": $("#textbox").val()}
        $.post("/message/add", data, function(data) {
                console.log(data);
            });
    }
 </script>
 </%def>

 <h1>Chat room</h1>
 <div>
     <textarea id="textbox" rows="10" cols="100"></textarea>
     <button type="button" onclick="add()">Send</button> 
 </div>
 <div id="messages">
     <div id = "message_sample" class="message">
         <span class="name">name</span>
         <span class="date">2010-10-30 1:20</span>
         <div class="content">
             holy c
         </div>
     </div>
 </div>
<script type="text/javascript">
    update();
</script>
