var largeurPetiteMax = 800;
var largeurGrandeMin = 1001;
var vitesseMobile = 350;
var vitesseBureau = 300;
var resteMobile = 60;
var mobile;
var bureauGrand;
var glisse = {
    duree: undefined,
    corps: {
        gauche: undefined,
        contenu: undefined,
    },
    enTete: {
        haut: '60px',
        droite: undefined,
    }
}

$( function () {
    var bodyStyles = window.getComputedStyle(document.body);
    var $enTete = $('#EnTete .glisseur');
    var $loupe = $('#Loupe');
    var $menuHamburger = $('#BoutonsMenus div[name="hamburger"]');
    var $menuBureau = $('#BoutonsMenus div[name="bureau"]');
    var $glisseGauche = $('.glisseur-gauche');
    var $glisseDroite = $('.glisseur-droite');
    var $searchBar = $('#BarreDeRecherche');
    var $entreeRecherche = $('#BarreDeRecherche input');
    var $faireRechercher = $('#FaireRechercher');
    var $supprimerText = $('#SupprimerText');
    var rechercheVisible = false;
    var menuVisible = false;

    function reglerJour() {
        var dateObj = new Date();
        $('#NumeroDuJour').text(dateObj.getDate());
    }

    /* Controle de Boutons de Barre de Recherche */
    function montrerBoutonsRecherches() {
        $($faireRechercher.find('i')).removeClass('md-inactive');
        $supprimerText.show();
    }
    function cacherBoutonsRecherches() {
        $($faireRechercher.find('i')).addClass('md-inactive');
        $supprimerText.hide();
    }
    function basculerBoutonsRecherches() {
        $($faireRechercher.find('i')).toggleClass('md-inactive');
        $supprimerText.toggle();
    }
    $supprimerText.click( function() {
        $entreeRecherche[0].value = '';
        cacherBoutonsRecherches();
        $entreeRecherche.focus();
    });
    $entreeRecherche.keyup(function(e) {
        if ($supprimerText.is($entreeRecherche[0].value == '' ? ':visible' : ':hidden' )) {
            basculerBoutonsRecherches();
        }
    })

    /* Menu */
    $menuHamburger.click(function () {
        basculerMenu(!menuVisible);
    });
    $menuBureau.click(function() {
        basculerMenu(!menuVisible);
    });
    function basculerMenu(ouvrir) {
        if ((ouvrir == true && menuVisible) || (ouvrir == false && !menuVisible))
            return;
        menuVisible = ouvrir == true || ( ouvrir === undefined && !menuVisible );

        if (mobile){
            if (menuVisible)
                $menuHamburger.addClass('open');
            else
                $menuHamburger.removeClass('open');
        }

        $glisseDroite.animate(
            { left: menuVisible ? '+=' + glisse.corps.contenu : '0px' },
            {
                easing: 'swing',
                duration: glisse.duree,
            },
            );
        if (bureauGrand) {
            $glisseGauche.animate(
                { left: menuVisible ? '-=' + glisse.corps.gauche : '0px' },
                {
                    easing: 'swing',
                    duration: glisse.duree,
                },
            );
        }
    }
    
    /* En-tete glisseur */
    $loupe.click(function(e) {
        basculerRecherche(!rechercheVisible);
    });
    function basculerRecherche(ouvrir) {
        if ((ouvrir == true && rechercheVisible) || (ouvrir == false && !rechercheVisible))
            return;
        rechercheVisible = ouvrir == true || (ouvrir === undefined && !rechercheVisible);

        if (rechercheVisible)
            $entreeRecherche.focus();
        
        if (mobile) {
            $enTete.animate(
                { left: rechercheVisible ? '+=' + glisse.enTete.droite : '0px' },
                {
                    easing: 'swing',
                    duration: glisse.duree,
                }
            );
        }
        else {
            $enTete.animate(
                { top: rechercheVisible ? '-=' + glisse.enTete.haut : '0px' },
                {
                    easing: 'swing',
                    duration: glisse.duree,
                }
            );
            $loupe.toggleClass('open');
        }
    }

    function cacherTout(){
        basculerRecherche(false);
        basculerMenu(false);
    }

    function resetTout() {
        $enTete.css({top:'0px', left:'0px'});
        $glisseGauche.css('left', '0px');
        $glisseDroite.css('left', '0px');
        rechercheVisible = menuVisible = false;
        $loupe.removeClass('open');
        $menuHamburger.removeClass('open');
    }

    function calculerVariables() {
        var largeur = $(window).width();
        glisse.duree = largeur <= largeurPetiteMax ? vitesseMobile : vitesseBureau;
        if (largeur <= largeurPetiteMax){
            // mobile
            if (!mobile)
                resetTout()
            mobile = true;
            bureauGrand = false;
            glisse.corps.contenu = '200px';
            glisse.enTete.droite = $(window).width() - resteMobile;
        }
        else if (largeur >= largeurGrandeMin) {
            // bureau grand
            if (!bureauGrand)
                resetTout();
            mobile = false;
            bureauGrand = true;
            glisse.corps.gauche = '80px';
            glisse.corps.contenu = '120px';
        }
        else {
            // bureau petit
            if (mobile || bureauGrand)
                resetTout();
            mobile = false;
            bureauGrand = false;
            glisse.corps.contenu = '200px';
        }
    }
    $(window).resize(calculerVariables);

    /* Cacher En-tete avec clique sur Corps */
    $(document).mouseup(function(e) {
        $.each(['Contenu', 'ColonneGauche','footer'], function (i, element) {
            if ($(e.target).closest('#' + element).length == 1) {
                cacherTout();
                e.stopPropagation();
                return false;
            }
        });
    });
    reglerJour();
    calculerVariables();
});
