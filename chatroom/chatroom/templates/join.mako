<%inherit file="/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
function init() {
    $("#nicknameInput").focus();
}
</script>
</%def>

<%def name="body_attr()">onload="init()"</%def>

<h1>Chat room: Powered by Speedo</h1>
<form action="/room/chat" method="POST">
    <fieldset> 
        <label for="nick">Nick Name:</label>
        <input id="nicknameInput" class="text" type="text" name="nickname" value="Mr. Speedo">
        <input id="joinButton" class="button" type="submit" name="" value="Join">
    </fieldset>
</form>

