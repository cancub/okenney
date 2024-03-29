$( function () {
    var $glisseurs = $('.glisser');
    var $loupe = $('.en-tete-loupe');
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

    function glisserRecipient(event) {
        $glisseurs.add($loupe).toggleClass('ouvert ferme');
        event.stopPropagation();
    }

    $loupe.click(glisserRecipient);

    $('#RecipContenu').click(function(event) {
        if ($(this).hasClass('ouvert'))
            glisserRecipient(event);
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
