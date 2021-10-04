"""
File for constant values to be used throughout the projet
"""

PAGE_TITLES = {
            'feed': "Page d'accueil - Flux",
            'posts': "Mes posts",
            'ticket_creation': 'Créer un ticket',
            'ticket_modification': 'Modifier un ticket',
            'ticket_delete': 'Supprimer un ticket',
            'review_creation_no_ticket': 'Créer une critique',
            'review_ticket_reply': 'Répondre à un ticket',
            'review_modification': 'Modifier une critique',
            'review_delete': 'Supprimer une critique',
        }

RATINGS = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
}


ticket_created = "Le ticket a bien été créé"
ticket_already_replied = 'Action Impossible: ce ticket a déja une réponse'
ticket_modified = "Le ticket a bien été modifié"
ticket_deleted = "Le ticket a bien été supprimé"
review_created = "La critique a bien été créée"
review_modified ="La critique a bien été modifiée"
review_deleted = "La critique a bien été supprimée"
form_error = "Veuillez renseigner à nouveau le formulaire"
registration_success = "Votre inscripiton a bien été prise en compte"
login_success = "Connexion réussie"
