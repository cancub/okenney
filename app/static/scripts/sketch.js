$(function() {
	var sketchpadWidth = $( window ).width();
	var sketchpadHeight = $( window ).height() - $('#sketch-header').height();
	var sketchpad = Raphael.sketchpad("editor", {
        width: sketchpadWidth,
        height: sketchpadHeight,
        editing: true
    });

    var filename = 'pmr-carte.jpg';

    $.ajax({
        url: "/api/image/" + filename,
        success: function(resp) {
            console.log(resp);
        },
    });

    var carte = $('#carte');
    sketchpad.paper().image(carte);
    $('#editor image').on('dragstart', false);

    var filename = 'pmr-carte.jpg';


    // When the sketchpad changes, update the input field.
    sketchpad.change(function() {
        console.log(sketchpad.json());
    });
});
