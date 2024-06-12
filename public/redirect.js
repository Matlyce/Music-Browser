function initLinks() {
    // retrieve all elements with class 'redirect-element'
    const redirectElements = document.querySelectorAll('.redirect-element');
    if (!redirectElements)
        return;

    // add click event listener to each element
    redirectElements.forEach(element => {
        element.addEventListener('click', () => {
            console.log('redirect element clicked');
            // retrieve the 'data-redirect-url' attribute
            const url = element.getAttribute('data-redirect-url');
            if (!url)
                return;

            // send the 'open-url' event to the main process
            window.api.openUrl(url);
        });
    });
}

initLinks();