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
});

