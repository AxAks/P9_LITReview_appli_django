// CONSTANTS

const empty_star = '&#x2606;'
const filled_star = '&#x2605;'


// Function to display stars for reviews rating
function addStarsForRating() {
    let review_stars = document.querySelectorAll('.stars');

    for (stars of review_stars) {
        let i = 0;
        for (star of stars.children){
            if (i < stars.parentElement.getAttribute('value')) {
                star.innerHTML = '&#x2605;';
                i++;
            }
        }
    }
}

window.onload = () => {
    addStarsForRating();
};