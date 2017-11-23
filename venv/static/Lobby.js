showingGameCreation = false;
showing_num = 0;

/**
 * Sends a request to the server to create a new game
 */
function createNewGame() {
    $.ajax({
        url: "/create_game",
        type: "POST"
    });
}
function showGameCreate() {
    showing_num++;
    if (showing_num > 1) {
        $('#alert_text').html("Game created! (" + showing_num +")");
    } else {
        $('#alert_text').html("Game created!");
    }

    $('#new_game').fadeIn(1000);
    showingGameCreation = true;

}

function showGameFull() {
    $('#alert_text_2').html("Cannot join full game!");
    $('#join_full').fadeIn(1000);
    console.log('hello')
}

function show_game_done() {
    showing_num = 0;
    showingGameCreation = false;
}

function quickJoin() {
    // TODO - get the first game available and join it

}