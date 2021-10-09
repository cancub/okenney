$(function () {

    $('.progim').each(function () {
        var $frame = $(this);
        var preview = $frame.find('img')[0];

        // Make the replacement image and give it the path for the large
        // version of the original image.
        var img = new Image();
        img.src = preview.src.split('-pt.png')[0] + '-gd.png';

        // Hide the image so that we can fade it into view only after we append
        // it to its container.
        $(img).hide();

        if (img.complete)
            addImg();
        else
            img.onload = addImg;

        // Replace the original image.
        function addImg() {
            $frame.append(img);
            // Make sure to only remove the preview after the high-res
            // replacement has finished fading it. This avoids flashing.
            $(img).fadeIn(400, () => {$(preview).hide()})
        }
    });

});
