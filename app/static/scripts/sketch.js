$(function() {
    var filename = 'pmr-carte.jpg';
    var sketchpadWidth, sketchpadHeight;

    function toggle(event){
        // was the toggle flipped? if so, flip
        if ($(event.currentTarget).hasClass('toggle-button-unselected')){
            $('#panDrawToggle div').toggleClass('toggle-button-unselected toggle-button-selected');
        }
        event.stopPropagation();
    }

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

    $.each($('#panDrawToggle div'), function(i, element) {
        $(element).click(element, toggle);
    });

});
