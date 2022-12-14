$(document).ready(function() {
    // console.log("JS loaded.");
    $("#new-user-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        var is_admin_value = -1;
        if ($("#is_admin_yes").is(":checked"))
            is_admin_value = 1;
        else if ($("#is_admin_no").is(":checked"))
            is_admin_value = 0;
        $.ajax( {
            type: "POST",
            url: "/users/create_user_in_db",
            data: {
                first_name: $("input[name=first_name]").val(),
                last_name: $("input[name=last_name]").val(),
                email: $("input[name=email]").val(),
                is_admin: is_admin_value,
                password: $("input[name=password]").val(),
                confirm_password: $("input[name=confirm_password]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("User creation was successful");
                    window.location = "/users";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#new-user-errors").html("");
                    for (var msg in data) {
                        $("#new-user-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
                $("#new-user-form")[0].reset();
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
    $("#edit-user-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        var is_admin_value = -1;
        if ($("#is_admin_yes").is(":checked"))
            is_admin_value = 1;
        else if ($("#is_admin_no").is(":checked"))
            is_admin_value = 0;
        $.ajax( {
            type: "POST",
            url: "/users/" + $("input[name=user_id]").val() + "/update_user_in_db",
            data: {
                first_name: $("input[name=first_name]").val(),
                last_name: $("input[name=last_name]").val(),
                email: $("input[name=email]").val(),
                is_admin: is_admin_value,
                password: $("input[name=password]").val(),
                confirm_password: $("input[name=confirm_password]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("User edit was successful");
                    window.location = "/users";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#edit-user-errors").html("");
                    for (var msg in data) {
                        $("#edit-user-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
});