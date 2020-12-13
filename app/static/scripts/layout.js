var largeurMobileMax = 700;
var largeurTabletteMax = 1001;
var vitesseMobile = 350;
var vitesseBureau = 300;
var resteMobile = 60;
var mobile;
var bureau;
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
    var $glisseGauche = $('.glisseur-gauche');
    var $glisseDroite = $('.glisseur-droite');
    var $colonneGauche = $('#ColonneGauche');
    var $entreeRecherche = $('#BarreDeRecherche input');
    var $faireRechercher = $('#FaireRechercher');
    var $supprimerText = $('#SupprimerText');
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
    $entreeRecherche.on('keyup change paste cut', function(e) {
        if ($supprimerText.is($entreeRecherche[0].value == '' ? ':visible' : ':hidden' )) {
            basculerBoutonsRecherches();
        }
    });

    /* Menu */
    $loupe.click(function() {
        basculerMenu(!menuVisible);
    });
    $('.ferme').click(function() {
        if (!mobile)
            basculerMenu(!menuVisible);
    });
    function basculerMenu(ouvrir) {
        if ((ouvrir == true && menuVisible) || (ouvrir == false && !menuVisible))
            return;
        menuVisible = ouvrir == true || ( ouvrir === undefined && !menuVisible );

        var movement_tete;
        if (mobile){
            $loupe.toggleClass('open');
            movement_tete = {
                left: menuVisible ? '+=' + glisse.enTete.droite : '0px'
            };
        }
        else {
            $colonneGauche.toggleClass('ferme');
            $enTete.toggleClass('ferme');
            movement_tete = {
                top: menuVisible ? '-=' + glisse.enTete.haut : '0px'
            };
        }

        $enTete.animate(
            movement_tete,
            {easing: 'swing',
                duration: glisse.duree,
            }
        );

        $glisseDroite.animate(
            { left: menuVisible ? '+=' + glisse.corps.contenu : '0px' },
            {
                easing: 'swing',
                duration: glisse.duree,
            },
            );
        if (bureau) {
            $glisseGauche.animate(
                { left: menuVisible ? '-=' + glisse.corps.gauche : '0px' },
                {
                    easing: 'swing',
                    duration: glisse.duree,
                },
            );
        }
    }

    function resetTout() {
        $enTete.css({top:'0px', left:'0px'});
        $glisseGauche.css('left', '0px');
        $glisseDroite.css('left', '0px');
        rechercheVisible = menuVisible = false;
        $loupe.removeClass('open');
        $colonneGauche.addClass('ferme');
        $enTete.addClass('ferme');
    }

    function calculerVariables() {
        var largeur = $(window).width();
        glisse.duree = largeur <= largeurMobileMax ? vitesseMobile : vitesseBureau;
        if (largeur <= largeurMobileMax){
            // mobile
            if (!mobile)
                resetTout()
            mobile = true;
            bureau = false;
            glisse.corps.contenu = '200px';
            glisse.enTete.droite = $(window).width() - resteMobile;
        }
        else if (largeur <= largeurTabletteMax){
            // tablette
            if (mobile || bureau)
                resetTout();
            mobile = false;
            bureau = false;
            glisse.corps.contenu = '200px';
        }
        else {
            // bureau
            if (!bureau)
                resetTout();
            mobile = false;
            bureau = true;
            glisse.corps.gauche = '80px';
            glisse.corps.contenu = '120px';
        }
    }
    $(window).resize(calculerVariables);

    /* Cacher En-tete avec clique sur Corps */
    $(document).mouseup(function(e) {
        if ($(e.target).closest('#Contenu').length == 1) {
            basculerMenu(false);
            e.stopPropagation();
            return false;
        }
    });
    reglerJour();
    calculerVariables();
});
