$(function() {
	var sketchpadWidth = $( window ).width();
	var sketchpadHeight = $( window ).height() - $('#sketch-header').height();
	var sketchpad = Raphael.sketchpad("editor", {
        width: sketchpadWidth,
        height: sketchpadHeight,
        editing: true
    });
    var carte = $('#carte');
    sketchpad.paper().image(carte);
    $('#editor image').on('dragstart', false);

    // When the sketchpad changes, update the input field.
    sketchpad.change(function() {
        console.log(sketchpad.json());
    });
});