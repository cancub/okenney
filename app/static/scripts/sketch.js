$(function() {
    var filename = 'pmr-carte.jpg';
    var sketchpadWidth, sketchpadHeight;

    $.ajax({
        url: "/api/image/" + filename,
        success: function(resp) {
            sketchpadWidth = resp.width;
            sketchpadHeight = resp.height;
            var sketchpad = Raphael.sketchpad("editor", {
                width: sketchpadWidth,
                height: sketchpadHeight,
                editing: true
            });
            sketchpad.paper().image('/images/' + filename, 0, 0, sketchpadWidth, sketchpadHeight)
        
            $('#editor image').on('dragstart', false);
        
            // When the sketchpad changes, update the input field.
            sketchpad.change(function() {
                console.log(sketchpad.json());
            });
        },
    });

});