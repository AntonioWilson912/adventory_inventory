$(document).ready(function() {
    $("#info-tab").click(function() {
        if (!$("#info-tab").hasClass("active")) {
            $("#info-tab").addClass("active");
            $("#info").addClass("show").addClass("active");
            $("#vendor-tab").removeClass("active");
            $("#vendors").removeClass("show").removeClass("active");
        }
    });
    $("#vendor-tab").click(function() {
        if (!$("#vendor-tab").hasClass("active")) {
            $("#info-tab").removeClass("active");
            $("#vendor-tab").addClass("active");
            $("#info").removeClass("show").removeClass("active");
            $("#vendors").addClass("show").addClass("active");
        }
    });
    $("#new-product-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "/products/add_product_to_db",
            data: {
                name: $("input[name=name]").val(),
                barcode: $("input[name=barcode]").val(),
                category_id: $("#category_id").val(),
                vendor_id: $("#vendor_id").val(),
                sku: $("input[name=sku]").val(),
                description: $("#description").val(),
                cost: $("input[name=cost]").val(),
                price: $("input[name=price]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("Product creation was successful");
                    window.location = "/products";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#new-product-errors").html("");
                    for (var msg in data) {
                        $("#new-product-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
    $("#edit-product-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "/products/" + $("input[name=product_id]").val() + "/update",
            data: {
                name: $("input[name=name]").val(),
                barcode: $("input[name=barcode]").val(),
                category_id: $("#category_id").val(),
                description: $("#description").val(),
                qty_available: $("input[name=qty_available]").val(),
                price: $("input[name=price]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.message) {
                    // console.log("Product update was successful");
                    window.location = "/products";
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#edit-product-errors").html("");
                    for (var msg in data) {
                        $("#edit-product-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
    $("#new-product-vendor-form").on("submit", function(e) {
        e.preventDefault();
        // console.log("Form submitted.");
        $.ajax( {
            type: "POST",
            url: "/products/" + $("input[name=product_id]").val() + "/add_vendor",
            data: {
                vendor_id: $("#vendor_id").val(),
                sku: $("input[name=sku]").val(),
                cost: $("input[name=cost]").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
    
            success: function(data) {
                if (data.product) {
                    // console.log("Product vendor creation was successful");
                    window.location = "/products/" + data.product;
                }
                else {
                    // console.log("There were errors.");
                    // console.log(data);
                    $("#new-product-vendor-errors").html("");
                    for (var msg in data) {
                        $("#new-product-vendor-errors").append("<li class='text-danger'>" + data[msg] + "</li>");
                    }
                }
            },
    
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        });
    });
    $(":radio").on("change", function(e) {
        console.log(e.currentTarget);
        console.log($(e.currentTarget).val(), "shall be the new primary vendor.");
        $.ajax( {
            type: "POST",
            url: "/products/" + $("#product_id").val() + "/update_primary_vendor",
            data: {
                vendor_id: $(e.currentTarget).val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                dataType: "json"
            },
            success: function(data) {
                // console.log(data);
            },
            error: function(errorMessage) {
                console.log(errorMessage);
            }
        })
    });
    $("#delete-product").click(function(e) {
        var result = confirm("Are you sure you want to delete " + $("#product_name").val());
        if (result) {
            $.ajax( {
                type: 'POST',
                url: '/products/' + $("#product_id").val() + "/delete",
                data: {
                    product_id: $("#product_id").val(),
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    dataType: "json"
                },
                success: function(data) {
                    // console.log("Product deleted.");
                    window.location = "/products";
                },
                error: function(errorMessage) {
                    console.log(errorMessage);
                }
            })
        }
    });
    $("#search-product-form").on("submit", function(e) {
        e.preventDefault();
        console.log("Searching for products with the name " + $("#search_term").val() + " and category " + $("#search_category").val() + " and vendor " + $("#search_vendor").val());
        loadProducts();
    });
});

function loadProducts() {

}