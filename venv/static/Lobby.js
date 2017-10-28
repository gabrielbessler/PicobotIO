function createNewGame() {
    $.ajax({
        url: "/create_game",
        type: "POST",
        success: function(data){

        }
    });
}