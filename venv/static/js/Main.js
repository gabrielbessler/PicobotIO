var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
const COL_WIDTH = 30;
const ROW_WIDTH = 30;
var loadedImages = 0;
var sampleMap = [];
var gameNumber;
var bluepico;
var redpico;
var score1;
var score2;
var item;
var map;

// FOR TESTING
var manualControl = false;

getImages();
$(document).keypress(function(event){
    keyCode = String.fromCharCode(event.which).toLowerCase();

    if (keyCode == "a") {
        console.log("got A");
    }
    else if(keyCode == "s") {

    }
    else if(keyCode == "d") {

    }
    else if(keyCode == "w") {

    }
    else if(keyCode == "m") {
        manualControl = !manualControl;
    }

});


function getGameNum() {
    gameNumber = document.getElementById('game_num').getAttribute('val');
}

/**
 * Loads all of the images that will be used for the game
 */
function getImages() {
    imageURLS = ["/static/imgs/item.png", "/static/imgs/picoblue.png", "/static/imgs/picored.png"]
    loadedImages = 0;
    images = [0, 0, 0];
    for (i = 0; i < imageURLS.length; i++) {
        pic = new Image();
        pic.src = imageURLS[i];
        images[i] = pic;

        pic.onload = function() {
            loadedImages++;
            if (loadedImages == 3) {
                bluepico = images[1];
                redpico = images[2];
                item = images[0];

                interval = setInterval(function() {
                    getScore();
                }, 450);
            }
        }
    }
}

/**
 * Sends a post request to the server and updates the score being displayed
 * using a callback function.
 */
function getScore() {
    getGameNum();
    $.ajax({
        url: "/get_score/" + gameNumber,
        type: "POST",
        success: function(data){
            if (data == -1) {
                clearInterval(interval);
                document.getElementById("timer").innerHTML = 0 + " s";
                if (score1 == score2) {
                    document.getElementById("score1").innerHTML = "TIE";
                    document.getElementById("score2").innerHTML = "TIE";
                } else if (score2 < score1) {
                    document.getElementById("score1").innerHTML = "WINNER";
                    document.getElementById("score2").innerHTML = "LOSER";
                } else {
                    document.getElementById("score1").innerHTML = "LOSER";
                    document.getElementById("score2").innerHTML = "WINNER";
                }
            } else if (data != -2) {
                data = eval(data);
                map = eval(data[3]);
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                drawMap(map);
                document.getElementById("timer").innerHTML = Math.round(data[1]) + " s";
                document.getElementById("score1").innerHTML = data[2] + " points";
                score1 = data[2];
                document.getElementById("score2").innerHTML = data[0] + " points";
                score2 = data[0];
            }
        }
    });
    return 0;
}

/**
 * Takes a 2D array representing the picobot map and draws it on the HTML5
 * canvas
 * @param {Array} map
 */
function drawMap(map) {
    /* Takes a map as a javascript array and draws the map on the screen */
    ctx.strokeStyle = "rgba(0, 0, 0, .7)";
    for (var row = 0; row < map.length; row++) {
        for (var col = 0; col < map[row].length; col++) {
            currSquare = map[row][col];
            var xpos = col * COL_WIDTH;
            var ypos = row * ROW_WIDTH;
            ctx.strokeRect(xpos, ypos, COL_WIDTH, ROW_WIDTH);
            /* First, we pick the color to set the squares */
            if (currSquare[0] == 0) {
                // WHITE WITH BLACK BORDER
                ctx.fillStyle = "rgba(255, 255, 255, 1)"
            }
            else if (currSquare[0] == 1) {
                // BLUE
                ctx.fillStyle = "rgba(66, 134, 244, .5)";
                ctx.fillRect(xpos, ypos, COL_WIDTH, ROW_WIDTH);
            }
            else if (currSquare[0] == 2) {
                // RED
                ctx.fillStyle = "rgba(247, 63, 22, .5)";
                ctx.fillRect(xpos, ypos, COL_WIDTH, ROW_WIDTH);
            }

            /* Draw the objects */
            if (currSquare[1] == "Wall()") {
                ctx.fillStyle = "rgba(50, 50, 50, .9)";
                ctx.fillRect(xpos, ypos, COL_WIDTH, ROW_WIDTH);
            } else if(currSquare[1] == "Item(1)") {
                ctx.drawImage(item, xpos, ypos);
            } else if(currSquare[1] == "Picobot(1)") {
                ctx.drawImage(bluepico, xpos, ypos);
            } else if(currSquare[1] == "Picobot(2)") {
                ctx.drawImage(redpico, xpos, ypos);
            }
        }
    }
}

/**
 * Sets the picobot instructions to a preset of instructions that work
 */
function preset2() {
    document.getElementById('pico_instructions').value = "[0, '_***', 'N', 0]\n[0, 'x***', 'W', 1]\n[1, '***_', 'W', 1]\n[1, '***x', 'S', 2]\n[2, '*_**', 'S', 2]\n[2, '*x**', 'E', 3]\n[3, '**_*', 'E', 3]\n[3, '**x*', 'N', 0]";
}

/**
 * Sets the picobot instructions to a preset of instructions that work
 */
function preset1() {
    document.getElementById('pico_instructions').value = "[0, '****', 'S', 1]\n[1, '****', 'S', 2]\n[2, '****', 'E', 3]\n[3, '**x*', 'S', 3]\n[3, '**_*', 'E', 4]\n[4, 'x***', 'E', 4]\n[4, '_***','N', 5]\n[5, '***x', 'N', 5]\n[5, '***_', 'W', 6]\n[6, '*x**', 'W', 6]\n[6, '*_**', 'S', 3]";
}

/**
 * Submit inscructions to the server for the picobot of your given your color
 */
function submit() {
    playerNum = document.getElementById('player_num').getAttribute('val');
    inst = document.getElementById('pico_instructions').value.split('\n');
    getGameNum();
    $.ajax({
        url: "/update_instructions/" + gameNumber,
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(playerNum + inst) ,
        success: function(data){
            document.getElementById("pico_errors").innerHTML = data;
        }
    });
}

function reloadGameList() {
    console.log("feature currently in progress.");
}
