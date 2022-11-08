$(document).ready(function() {
    $("#info-tab").click(function() {
        if (!$("#info-tab").hasClass("active")) {
            $("#info-tab").addClass("active");
            $("#info").addClass("show").addClass("active");
            $("#vendor-tab").removeClass("active").removeClass("bg-indigo");
            $("#vendors").removeClass("show").removeClass("active");
        }
    });
    $("#vendor-tab").click(function() {
        if (!$("#vendor-tab").hasClass("active")) {
            $("#info-tab").removeClass("active");
            $("#vendor-tab").addClass("active").addClass("bg-indigo");
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
    loadProducts("", "all", "all");
    $("#search-product-form").on("submit", function(e) {
        e.preventDefault();
        var searchTerm = $("#search_term").val();
        var searchCategory = $("#search_category").val();
        var searchVendor = $("#search_vendor").val();
        // console.log("Searching for products with the name " + $("#search_term").val() + " and category " + $("#search_category").val() + " and vendor " + $("#search_vendor").val());
        loadProducts(searchTerm, searchCategory, searchVendor);
    });
});

function loadProducts(searchTerm, searchCategory, searchVendor) {
    $.ajax( {
        type: "POST",
        url: "/products/search_products",
        data: {
            search_term: searchTerm,
            search_category: searchCategory,
            search_vendor: searchVendor,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            dataType: "json"
        },
        success: function(data) {
            // console.log("Successfully retrieved products from the server.");
            // console.log(data.all_products);
            $("#all-products").html("")
            if (data.all_products.length > 0) {
                for (var index = 0; index < data.all_products.length; index++) {
                    // console.log(data.all_products[index]);
                    var productRow = document.createElement("tr");
    
                    var barcode = document.createElement("td");
                    barcode.innerHTML = data.all_products[index].barcode;
    
                    var sku = document.createElement("td");
                    sku.innerHTML = data.all_products[index].sku;
    
                    var category = document.createElement("td");
                    category.innerHTML = data.all_products[index].category;
    
                    var product = document.createElement("td");
                    product.innerHTML = data.all_products[index].name;
    
                    var price = document.createElement("td");
                    price.innerHTML = "$" + data.all_products[index].price;
    
                    var actions = document.createElement("td");
                    actions.innerHTML = `<a href="/products/${data.all_products[index].id}">View</a>`;
                    if ($("#is_admin").val() == 1) {
                        actions.innerHTML += `
                        | <a href="/products/${data.all_products[index].id}/edit">Edit</a>
                        | <a href="/products/${data.all_products[index].id}/delete">Delete</a>
                        `;
                    }
    
                    productRow.append(barcode, sku, category, product, price, actions);
                    $("#all-products").append(productRow);
                }
            }
            else {
                var emptyProducts = document.createElement("tr");
                var emptyProductMessage = document.createElement("td");
                emptyProductMessage.colSpan = "6";
                emptyProductMessage.classList.add("text-center")
                emptyProductMessage.innerText = "There were no products found with that search term.";

                emptyProducts.append(emptyProductMessage);
                $("#all-products").html(emptyProducts);
            }
        },
        error: function(errorMessage) {
            console.log(errorMessage);
        }
    })
}