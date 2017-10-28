var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
const COL_WIDTH = 30;
const ROW_WIDTH = 30;
var loadedImages = 0;
var bluepico;
var redpico;
var item;
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
    drawMap(sampleMap);
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
            } else if(currSquare[1] == "Player(1)") {
                ctx.drawImage(bluepico, xpos, ypos);
            } else if(currSquare[1] == "Player(2)") {
                ctx.drawImage(redpico, xpos, ypos);
            }
        }
    }
}

function submit() {
    inst = document.getElementById('pico_instructions').value.split('\n');
    console.log(inst);
    $.ajax({
        url: "/update_instructions",
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify("hello world"),
        success: function(data){
            console.log("N/A");
        }
    });
}
sampleMap = [[[1,"Wall()"],[0,"Player(1)"],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0]], [[0,0],[2,0],[0,"Item()"]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,"Player(2)"],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]], [[2,0],[1,0],[0,0]]];

