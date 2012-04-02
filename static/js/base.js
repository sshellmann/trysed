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
                    else {
                        clear_error();
                        $(".main_panel:first textarea").val(data["result"]);
                        if (data["dialog"]) {
                            $("#dialog").html(data["dialog"]);
                        }
                    }
                }
            });
        }
    });

    $("#reset_step").click(function() {
        $.ajax({
            url: "/reset_step",
            type: "POST",
        });
    });

    $("#get_step").click(function() {
        $.ajax({
            url: "/get_step",
            type: "POST",
            success: function(data){
                console.debug(data);
            }
        });
    });
});

function handle_error(error) {
    if (!error)
        error = "An error has occurred."
    $("#input_error p").html(error);
    $("#input_error").css("visibility", "visible").delay(4000).queue(function() {
        $("#input_error").fadeOut(1000, function() {
            $(this).show().css({visibility: "hidden"});
        });
        $(this).dequeue();
    });
}

function clear_error() {
    $("#input_error").css("visibility", "hidden");
}
