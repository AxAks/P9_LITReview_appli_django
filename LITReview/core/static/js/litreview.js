// CONSTANTS

const empty_star = '&#x2606;'
const filled_star = '&#x2605;'
const possible_ratings = [0, 1, 2, 3, 4, 5]

// Function to display stars for reviews rating
async function addStarsForRating() {
    let reviews_ratings = Array.from(document.getElementsByClassName("rating")).map(element => parseInt(element.innerHTML));
    let star_ratings = Array.from(document.getElementsByClassName("star-rating"));
    for (review_rating of reviews_ratings) {
        for (star_rating of star_ratings) {
            for (possible_rating of possible_ratings) {
                if (review_rating == 0) {
                    star_rating.innerHTML += 5 * empty_star;
                } else if (possible_rating <= review_rating) {
                    star_rating.innerHTML += filled_star;
                } else {
                    star_rating.innerHTML += empty_star;
                };
            };
        };
    };
};

// Launch functions when DOM is ready
document.addEventListener('DOMContentLoaded', async() => {
    addStarsForRating();
})