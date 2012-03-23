<%inherit file="/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
    function join() {
        // TODO: need to check the validity of nickname
        nickname = $("#nicknameInput").val()
        
        // TODO need to froze the input/button
        $.get("/users/join", {"nickname": nickname}, 
            function(response) {
                if (response == null || response.result == "error") {
                    // TODO: simple error reporting
                    alert("Error occurs");
                    return
                }
                console.log("ready to redirect...")
                window.location.replace("/room/chat");
            });

    }
function init() {
    $("#nicknameInput").focus();
}
</script>
</%def>

<%def name="body_attr()">onload="init()"</%def>

<h1>the Chat room: Powered by Speedo</h1>
<form action="/users/join" method="POST">
    <fieldset> 
        <label for="nick">Nick Name:</label>
        <input id="nicknameInput" class="text" type="text" name="nickname" value="Mr. Speedo">
        <input id="joinButton" class="button" type="submit" name="" value="Join">
    </fieldset>
</form>
