$(document).ready(function() {
    // console.log("JS loaded.");
    $("#reset-password-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "reset_password_in_db",
            data: {
                email: $("input[name=email]").val(),
                password: $("input[name=password]").val(),
                confirm_password: $("input[name=confirm_password]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("Password reset was successful");
                    window.location = "/";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#reset-password-errors").html("");
                    for (var msg in data) {
                        $("#reset-password-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
                $("#reset-password-form")[0].reset();
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
});