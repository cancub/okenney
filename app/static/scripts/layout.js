$( function () {
    var $glisseurs = $('.glisser');
    var $loupe = $('#Loupe');
    var $entreeRecherche = $('#BarreDeRecherche input');
    var $faireRechercher = $('#FaireRechercher');
    var $supprimerText = $('#SupprimerText');

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

    $('#Contenu').add($loupe).click(function(event) {
        if ($(this).attr('id') != 'Contenu' || $(this).hasClass('ouvert')) {
            $glisseurs.add($loupe).toggleClass('ouvert ferme');
            event.stopPropagation();
        }
    })

    let resizeTimer;
    window.addEventListener("resize", () => {
        document.body.classList.add("resize-animation-stopper");
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            document.body.classList.remove("resize-animation-stopper");
        }, 100);
    });

    /* Menu */
    var dateObj = new Date();
    $('#NumeroDuJour').text(dateObj.getDate());
});
