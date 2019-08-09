$(function() {
    var $titleBar = $('#title-bar');
    var $alf = $('#title-text .first-name');
    var $okenney = $('#title-text .last-name');
    var minTitleHeight = 40;
    var maxTitleHeight = 200;
    var titleHeightRange = maxTitleHeight - minTitleHeight;
    var atMinHeight = false;
    var minAlfSize = 5;
    var maxAlfSize = 40;
    var alfSizeRange = maxAlfSize - minAlfSize;
    var minOkenneySize = 20;
    var maxOkenneySize = 70;
    var okenneySizeRange = maxOkenneySize - minOkenneySize;
    var maxShadow = getComputedStyle(document.body,null).getPropertyValue('--max-shadow');
    function resizeTitle(percent){
        if (percent == 0){
            $titleBar.height(minTitleHeight);
            $alf.html('&nbsp');
            $alf.css({'font-size': minAlfSize});
            $okenney.css({'font-size': minOkenneySize});
            document.body.style.setProperty('--cur-shadow', maxShadow);
        }
        else {
            $alf.html('Alf');
            if (percent == 1) {
                $titleBar.height(maxTitleHeight);
                $alf.css({'font-size': maxAlfSize});
                $okenney.css({'font-size': maxOkenneySize});
                document.body.style.setProperty('--cur-shadow', 0);
            }
            else {
                $titleBar.height( percent * titleHeightRange + minTitleHeight);
                $alf.css({'font-size': percent * alfSizeRange + minAlfSize});
                $okenney.css({'font-size': percent * okenneySizeRange + minOkenneySize});
                document.body.style.setProperty('--cur-shadow', (1-percent)*maxShadow);
            }
        }
    }
    $(document).scroll(function() {
        var top = $(this).scrollTop();
        if ( top < titleHeightRange ){
            atMinHeight = false;
            resizeTitle( Math.min( Math.max( ( titleHeightRange - top ) , 0 ) / titleHeightRange, 1));
        }
        else if (atMinHeight == false){
            atMinHeight = true;
            resizeTitle(0);
        }
    });
});
