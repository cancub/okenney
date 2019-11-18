$( function () {
    var $header = $('#HeaderContainer');
    var $loupe = $('#Loupe');
    var $menuHB = $('#MenuBoutonHB');
    var $menuDT = $('#MenuBoutonDT');
    var $searchBar = $('#BarreDeRecherche');
    var $searchInputText = $('#BarreDeRecherche .entry-box');
    var $doSearch = $('#FaireRechercher');
    var $clearSearch = $('#SupprimerText');
    var searchVisible = false;
    var menuVisible = false;
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

    /* Menu */
    $menuHB.click(function () {
        $(this).toggleClass('open');
        toggleMenu();
    });
    $menuDT.click(function() {
        toggleMenu();
    });
    function hideMenu() {
        $menuHB.removeClass('open');
        if (menuVisible) {
            if (amMobile()) {
                $('.menu-slider-right').animate(
                    { left: '-=200px' },
                    {
                        easing: 'swing',
                        duration: mobileSlideSpeed,
                    },
                );
            }
            else {
                $('.menu-slider-right').animate(
                    { left: '-=160px'},
                    {
                        easing: 'swing',
                        duration: desktopSlideSpeed,
                    },
                );
                $('.menu-slider-left').animate(
                    { left: '+=80px'},
                    {
                        easing: 'swing',
                        duration: desktopSlideSpeed,
                    },
                );
            }
        }
        menuVisible = false;
    }
    function toggleMenu() {
        console.log(menuVisible)
        if (menuVisible) {
            console.log('hiding');
            hideMenu();
        }
        else {
            if (amMobile()) {
                $('.menu-slider-right').animate(
                    { left: '+=200px' },
                    {
                        easing: 'swing',
                        duration: mobileSlideSpeed,
                    },
                );
            }
            else {
                $('.menu-slider-right').animate(
                    { left: '+=160px' },
                    {
                        easing: 'swing',
                        duration: desktopSlideSpeed,
                    },
                );
                $('.menu-slider-left').animate(
                    { left: '-=80px' },
                    {
                        easing: 'swing',
                        duration: desktopSlideSpeed,
                    },
                );
            }
            menuVisible = true;
        }
    }

    /* En-tete glisseur */
    /* TODO:
    clean up toggle search to call hide search */
    function toggleSearch() {
        if (amMobile()) {
            var distance = $(window).width() - mobileRemaining;
            $header.animate(
                {'left': (searchVisible ? '-' : '+') + '=' + distance + 'px' },
                mobileSlideSpeed,
            );
        }
        else {
            $header.animate(
                { 'top': (searchVisible ? '+' : '-') + '=' + desktopSlide + 'px' },
                desktopSlideSpeed,
            );
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
                $header.animate(
                    { 'left': '-=' + distance + 'px' },
                    mobileSlideSpeed,
                );
            }
            else {
                $header.animate(
                    { 'top': '+=' + desktopSlide + 'px' },
                    desktopSlideSpeed,
                );
            }
            searchVisible = false;
            $loupe.removeClass('open')
        }
    }
    $loupe.click( toggleSearch );    
    /* Cacher En-tete avec clique sur Corps */
    $(document).mouseup(function(e) {
        $.each(['Contenu', 'ColonneGauche','footer'], function (i, element) {
            if ($(e.target).closest('#' + element).length == 1) {
                hideSearch();
                hideMenu();
                e.stopPropagation();
                return false;
            }
        });
    });
});
