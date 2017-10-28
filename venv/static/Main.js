var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
const COL_WIDTH = 30;
const ROW_WIDTH = 30;
var loadedImages = 0;
var bluepico;
var redpico;
var item;
var map;
getImages();

function getImages() {
    /* Load guy 1 */
    bluepico = new Image();
    bluepico.onload = function() {
        loadedImages++;
        if (loadedImages == 2) {
            startGame();
        }
    };

    bluepico.src = "/static/picoblue.png";

    redpico = new Image();
    redpico.onload = function() {
        loadedImages++;
        if (loadedImages == 2) {
            startGame();
        }
    };

    redpico.src = "/static/picored.png";

    item = new Image();
    item.onload = function() {
        loadedImages++;
        if (loadedImages == 2) {
            startGame();
        }
    };

    item.src = "/static/item.png"
}

function startGame() {
    getData();
}

interval = setInterval(function() {
    getScore();
    a = getData();
}, 450);

function getData() {
    $.ajax({
        url: "/get_map",
        type: "POST",
        success: function(data){
            if ( data == "poop" ) {
                clearInterval(interval);
                return -1
            } else {
                map = eval(data);
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                drawMap(map);
            }
        }
    });
    return 0;
}

function getScore() {
    $.ajax({
        url: "/get_score",
        type: "POST",
        success: function(data){
            console.log(data);
            if (data == -2) {

            } else if (data == -1) {
                document.getElementById("timer").innerHTML = 0 + " s";
                if (data[2] == data[0]) {
                    document.getElementById("score1").innerHTML = "TIE";
                    document.getElementById("score2").innerHTML = "TIE";
                } else if (data[2] < data[0]) {
                    document.getElementById("score1").innerHTML = "WINNER";
                    document.getElementById("score2").innerHTML = "LOSER";
                } else {
                    document.getElementById("score1").innerHTML = "LOSER";
                    document.getElementById("score2").innerHTML = "WINNER";
                }
            } else {
                data = eval(data);
                document.getElementById("timer").innerHTML = data[1] + " s";
                document.getElementById("score1").innerHTML = data[2] + " points";
                document.getElementById("score2").innerHTML = data[0] + " points";
            }
        }
    });
    return 0;
}

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
            } else if(currSquare[1] == "Item()") {
                ctx.drawImage(item, xpos, ypos);
            } else if(currSquare[1] == "Picobot(1)") {
                ctx.drawImage(bluepico, xpos, ypos);
            } else if(currSquare[1] == "Picobot(2)") {
                ctx.drawImage(redpico, xpos, ypos);
            }
        }
    }
}

function submit() {
    playerNum = document.getElementById('player_num').getAttribute('val');
    inst = document.getElementById('pico_instructions').value.split('\n');
    $.ajax({
        url: "/update_instructions",
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(playerNum + inst) ,
        success: function(data){
            document.getElementById("pico_errors").innerHTML = data;
        }
    });
}
sampleMap = [];

