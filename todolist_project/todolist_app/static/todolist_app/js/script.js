document.addEventListener("DOMContentLoaded", function() {
    if (window.location.search.indexOf('search') !== -1) {
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});