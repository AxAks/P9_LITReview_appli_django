reviewRating: {
    let possible_ratings = [0, 1, 2, 3, 4, 5]
    let rating_classes = ['One', 'Two', 'Three', 'Four', 'Five']
    let review_rating = post.rating;
    for (rating of possible_ratings) { 
        while (rating <= review_rating) {
            $rating_classes.parent().removeClass('One Two Three Four Five').addClass(rating_classes.index(review_rating));
        };
    };
};

// Launch functions when DOM is ready
document.addEventListener('DOMContentLoaded', async() => {
        reviewRating();
    })
    /*
        // Site-wide forms events
        o.forms = {
            init: function() {
                // Forms with this behaviour are 'locked' once they are submitted to
                // prevent multiple submissions
                $('form[data-behaviours~="lock"]').submit(o.forms.submitIfNotLocked);

                // Disable buttons when they are clicked and show a "loading" message taken from the
                // data-loading-text attribute (http://getbootstrap.com/2.3.2/javascript.html#buttons).
                // Do not disable if button is inside a form with invalid fields.
                // This uses a delegated event so that it keeps working for forms that are reloaded
                // via AJAX: https://api.jquery.com/on/#direct-and-delegated-events
                $(document.body).on('click', '[data-loading-text]', function(){
                    var form = $(this).parents("form");
                    if (!form || $(":invalid", form).length == 0)
                        $(this).button('loading');
                });
                // stuff for star rating on review page
                // show clickable stars instead of a select dropdown for product rating
                ratings = $('.reviewrating');
                if(ratings.length){
                    ratings.find('.star-rating i').on('click',o.forms.reviewRatingClick);
                }
            },
            submitIfNotLocked: function(event) {
                var $form = $(this);
                if ($form.data('locked')) {
                    return false;
                }
                $form.data('locked', true);
            },
            reviewRatingClick: function(event){
                var ratings = ['One','Two','Three','Four','Five']; //possible classes for display state
                $(this).parent().removeClass('One Two Three Four Five').addClass(ratings[$(this).index()]);
                $(this).closest('.controls').find('select').val($(this).index() + 1); //select is hidden, set value
            }
        };
        */