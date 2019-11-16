$( function () {
    var $header = $('#HeaderContainer');
    var $loupe = $('#Loupe');
    var $menuHB = $('#MenuHB');
    var $searchBar = $('#BarreDeRecherche');
    var $searchInputText = $('#BarreDeRecherche .entry-box');
    var $doSearch = $('#FaireRechercher');
    var $clearSearch = $('#SupprimerText');
    var searchVisible = false;
    var mobileSlideSpeed = 500;
    var desktopSlideSpeed = 400;
    var mobileRemaining = 60;
    var desktopSlide = 60;


    function amMobile() {
        return $(window).width() <= 640;
    }

    /* Controle de Boutons de Barre de Recherche */
    function showSearchButtons() {
        $($doSearch.find('i')).removeClass('md-inactive');
        $clearSearch.show();
    }
    function hideSearchButtons() {
        $($doSearch.find('i')).addClass('md-inactive');
        $clearSearch.hide();
    }
    function toggleSearchButtons() {
        $($doSearch.find('i')).toggleClass('md-inactive');
        $clearSearch.toggle();
    }
    $clearSearch.click( function() {
        $searchInputText[0].value = '';
        hideSearchButtons();
        $searchInputText.focus();
    });
    $searchInputText.keyup(function(e) {
        if ($clearSearch.is($searchInputText[0].value == '' ? ':visible' : ':hidden' )) {
            toggleSearchButtons();
        }
    })

    $menuHB.click(function () {
        $(this).toggleClass('open');
    });
    function hideMenu() {
        $menuHB.removeClass('open');
    }

    /* En-tete glisseur */
    function toggleSearch() {
        if (amMobile()) {
            var distance = $(window).width() - mobileRemaining;
            $header.animate({ 'left': (searchVisible ? '-' : '+') + '=' + distance + 'px' }, mobileSlideSpeed);
        }
        else {
            $header.animate({ 'top': (searchVisible ? '+' : '-') + '=' + desktopSlide + 'px' }, desktopSlideSpeed);
            $loupe.toggleClass('open');
        }
        searchVisible = !searchVisible;
        if (searchVisible)
            $searchInputText.focus();
    }
    function hideSearch() {
        if (searchVisible){
            if (amMobile()) {
                var distance = $(window).width() - mobileRemaining;
                $header.animate({ 'left': '-=' + distance + 'px' }, mobileSlideSpeed);
            }
            else
                $header.animate({ 'top': '+=' + desktopSlide + 'px' }, desktopSlideSpeed);
            searchVisible = false;
            $loupe.removeClass('open')
        }
    }
    $loupe.click( toggleSearch );    
    /* Cacher En-tete avec clique sur Corps */
    $(document).mouseup(function(e) {
        if ($(e.target).closest('#Corps').length == 1) {
            hideSearch();
            hideMenu();
            e.stopPropagation();
        }
    });
});
