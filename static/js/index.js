showingGameCreation = false;
showing_num = 0;
username = "foo";

/**
 * Sends a request to the server to create a new game
 */
function createNewGame() {
    $.ajax({
        url: "/create_game",
        type: "POST"
    });
}

/**
 * Shows an alert to the user with a "Game created!" message
 */
function showGameCreate() {
    showing_num++;
    if (showing_num > 1) {
        $('#alert_text').html("Game created! (" + showing_num + ")");
    } else {
        $('#alert_text').html("Game created!");
    }

    $('#new_game').fadeIn(1000);
    showingGameCreation = true;
}

/**
 * Shows an alert to the user with the message:
 * "cannot join full game"
 */
function showGameFull() {
    $('#alert_text_2').html("Cannot join full game!");
    $('#join_full').fadeIn(1000);
}

/**
 *
 */
function show_game_done() {
    showing_num = 0;
    showingGameCreation = false;
}

/**
 * Gets the first available game from the server and then
 * joins that game
 */
function quickJoin() {
    $.ajax({
        url: "/quick_join/",
        type: "POST",
        success: function(data){
            data = JSON.parse(data);
            if (data == "error") {
                console.log('error')
            } else {
                window.location.href = data;
            }
        }
    });
}

/**
 * shows the user profile if the user is logged in
 */
function getProfile() {
    $('#homeBtn').removeClass('active');
    $('#profileBtn').addClass("active");
    $('#highScoreBtn').removeClass("active");
    if (username == null) {
        new_page = `
        <h1 style="padding-left: 30px;">
            Currently not logged in.
        </h1>
        `
        document.getElementById('curr_disp').innerHTML = new_page;
    } else {
        // we will not use the default profile display, but
        // rather insert the profile_info.html data into the
        // current web page.

        // we will call a python function using jQuery that
        // will return the correct HTML code
        $.ajax({
            url: "/get_profile/" + username,
            type: "POST",
            success: function(data){
                new_page = data;
                document.getElementById('curr_disp').innerHTML = new_page;
            }
        });
    }
}

/**
 * Changes game list display so that all games are displayed
 */
function showMore() {
    showHome(true);
}

/**
 * Changes game list display so not all games are displayed
 */
function showLess() {
    showHome(false);
}

/**
 * Sends a request to the server for list of games / game infos,
 * and then updates the game list accordingly
 */
function reloadGameList() {
    $.ajax({
        url: "/get_game_list",
        type: "POST",
        success: function(data) {
            gameData = JSON.parse(data);
            showHome();
        }
    });
}