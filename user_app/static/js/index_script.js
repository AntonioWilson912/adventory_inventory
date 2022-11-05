$(document).ready(function() {
    // console.log("JS loaded.");
    $("#register-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "register",
            data: {
                first_name: $("input[name=first_name]").val(),
                last_name: $("input[name=last_name]").val(),
                email: $("input[name=email]").val(),
                password: $("input[name=password]").val(),
                confirm_password: $("input[name=confirm_password]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("Register was successful");
                    window.location = "/dashboard";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#register-errors").html("");
                    $("#login-errors").html("");
                    for (var msg in data) {
                        $("#register-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
                $("#register-form")[0].reset();
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
    $("#login-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "login",
            data: {
                email: $("#login-email").val(),
                password: $("#login-password").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("Login was successful");
                    window.location = "/dashboard";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#register-errors").html(""); // why does this not work???
                    $("#login-errors").html("");
                    for (var msg in data) {
                        $("#login-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
                $("#login-form")[0].reset();
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
});