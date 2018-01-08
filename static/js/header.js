
/**
 * Uses form data to send a login request to the server
 */
function login() {
    val1 = document.getElementById("username").value;
    val2 = document.getElementById("password").value;
    logindata = {
        username: val1,
        password: val2
    };
    $.ajax({
        type: "POST",
        url: "/login",
        data: JSON.stringify(logindata),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    });
}

/**
 * Uses form data to send a register request to the server
 */
function register() {
    val1 = document.getElementById("username").value;
    val2 = document.getElementById("password").value;
    registerdata = {
        username: val1,
        password: val2
    };
    $.ajax({
        type: "POST",
        url: "/register",
        data: JSON.stringify(registerdata),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    });
}