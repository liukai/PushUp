<%inherit file="/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
$(document).ready(function() {
        $("#nicknameInput").focus();
    });
</script>
</%def>

<h1>Chat room: Powered by Speedo</h1>
<form action="/room/chat" method="POST">
    <fieldset> 
        <label for="nick">Polled By: </label>
        <select id="methodInput" name="polledBy">
            <option value="multithread">Multitheading Long Polling</option>
            <option value="client">Client Poll</option>
        </select>
        <label for="nick">Nick Name: </label>
        <input id="nicknameInput" class="text" type="text" name="nickname" value="Mr. Speedo">
        <input id="joinButton" class="button" type="submit" name="" value="Join">
    </fieldset>
</form>

