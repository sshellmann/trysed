$(document).ready(function() {
    $("#user_input").keypress(function(event) {
        //If keypress was enter
        if (event.keyCode == 13) {
            entry = $(this).val();
            $.ajax({
                url: "/submit",
                dataType: "json",
                type: "POST",
                data: {
                    "input": $("#user_input").val(),
                },
                error: function(){
                    handle_error();
                },
                success: function(data){
                    if (!data["success"])
                        handle_error(data["error"]);
                }
            });
        }
    });
});

function handle_error(error) {
    if (!error)
        error = "An error has occurred."
    $("#input_error p").html(error);
    $("#input_error").css("visibility", "visible").delay(2000).queue(function() {
        $("#input_error").fadeOut(1000, function() {
            $(this).show().css({visibility: "hidden"});
        });
        $(this).dequeue();
    });
}
