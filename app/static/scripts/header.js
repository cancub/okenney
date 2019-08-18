var isMobile;
function updateDevice() {
    var width = $(window).width();
    if ( width > 640 && isMobile) {
        isMobile = false;
    }
    else if (width <= 640 && !isMobile){
        isMobile = true;
    }
}
$(function() {
    isMobile = $(window).width() <= 640;
    $(window).resize(function () {
        updateDevice();
    });
    updateDevice();
});
    