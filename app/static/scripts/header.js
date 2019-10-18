$( function () {
    var $searchBar = $('#BarDeRecherche');
    var $searchInputText = $('#BarDeRecherche input');
    var $openSearch = $('#OpenSearch');
    var $doSearch = $('#FaireRechercher');
    var $clearSearch = $('#ClearText');
    function toggleSearchButtons(transition) {
        if (transition === undefined) {
            $($doSearch.find('i')).toggleClass('md-inactive');
            $clearSearch.toggle();
        }
        else if (transition == 'hide') {
            $($doSearch.find('i')).addClass('md-inactive');
            $clearSearch.hide();
        }
        else if (transition == 'show'){
            $($doSearch.find('i')).removeClass('md-inactive');
            $clearSearch.show();
        }
    }
    $openSearch.click( function () {
        $(this).hide();
        $searchInputText[0].value = '';
        $searchBar.show();
        $searchInputText.focus();
    });
    $clearSearch.click( function() {
        $searchInputText[0].value = '';
        toggleSearchButtons('hide');
        $searchInputText.focus();
    });
    $(document).mouseup(function(e) {
        if (!$(e.target).hasClass('search-bar') && $searchBar.is(':visible')) {
            $openSearch.show();
            $searchBar.hide();
            $clearSearch.click();
            e.stopPropagation();
        }
    });
    $searchInputText.keyup(function(e) {
        if ($clearSearch.is($searchInputText[0].value == '' ? ':visible' : ':hidden' )) {
            toggleSearchButtons();
        }
    })
});
