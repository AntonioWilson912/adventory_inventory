$(document).ready(function() {
    // console.log("JS loaded.");
    $("#new-vendor-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "/vendors/add_vendor_to_db",
            data: {
                name: $("input[name=name]").val(),
                description: $("#description").val(),
                address: $("input[name=address]").val(),
                city: $("input[name=city]").val(),
                state: $("input[name=state]").val(),
                zip_code: $("input[name=zip_code]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("Vendor creation was successful");
                    window.location = "/vendors";
                }
                else if (data.last_page) {
                    // console.log("Navigating back to the previous page...");
                    if (data.last_page == "view_product")
                        window.location = "/products/" + data.product_id;
                    else if (data.last_page == "new_product")
                        window.location = "/products/new";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#new-vendor-errors").html("");
                    for (var msg in data) {
                        $("#new-vendor-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
    $("#edit-vendor-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "/vendors/" + $("input[name=vendor_id]").val() + "/update",
            data: {
                name: $("input[name=name]").val(),
                description: $("#description").val(),
                address: $("input[name=address]").val(),
                city: $("input[name=city]").val(),
                state: $("input[name=state]").val(),
                zip_code: $("input[name=zip_code]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("Vendor edit was successful");
                    window.location = "/vendors";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#edit-vendor-errors").html("");
                    for (var msg in data) {
                        $("#edit-vendor-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
    $("#delete-vendor").click(function(e) {
        // console.log("Delete vendor link clicked.");
        var result = confirm("Are you sure you want to delete " + $("#vendor_name").val());
        if (result) {
            $.ajax( {
                type: "POST",
                url: "/vendors/" + $("#vendor_id").val() + "/delete",
                data: {
                    "vendor_id": $("#vendor_id").val(),
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    dataType: "json"
                },
                success: function(data) {
                    // console.log(data);
                    window.location = "/vendors";
                },
                error: function(errorMessage) {
                    console.log(errorMessage);
                }
            })
        }
    })
});