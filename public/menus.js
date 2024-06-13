var availableMenus = [];
var hiddenMenus = [];
var activesTabs = 0;

async function saveSettings() {
    // save hiddenMenus to the main process
    window.api.saveSettings(hiddenMenus);
}

async function loadSettings() {
    // retrieve hiddenMenus from the main process
    window.api.retrieveSettings();
    window.api.onRetrieveSettingsReply((hiddenMenusList) => {
        if (!hiddenMenus)
            return;

        console.log("Available Menus count: " + availableMenus.length);
        console.log("Actives Tabs count: " + activesTabs);

        let tmp = JSON.parse(hiddenMenusList);
        if (!tmp)
            return;
        hiddenMenus = tmp;
        hiddenMenus.forEach(hiddenMenu => {
            const tab = document.querySelector(`.tab[data-target-url="${hiddenMenu}"]`);
            if (!tab)
                return;

            tab.classList.add('hidden');
            activesTabs--;
        });

        console.log("[inited] Actives Tabs count: " + activesTabs);
        console.log("[inited] hidden menu list: " + hiddenMenus);

        // retrieve togglers
        const togglerContainer = document.getElementById('toggler_container');
        if (!togglerContainer)
            return;

        const togglers = togglerContainer.querySelectorAll('.toggler');
        if (!togglers)
            return;

        togglers.forEach(toggler => {
            const targetValue = toggler.getAttribute('data-target-url');
            if (hiddenMenus.includes(targetValue)) {
                toggler.classList.add('off');
            }
        });
    });
}

function initSettings() {
    // retrieve 'settings_button'  element
    const settingsButton = document.getElementById('settings_button');
    if (!settingsButton)
        return;

    // on click event listener, retrieve 'panel' element and toggle 'active' class
    settingsButton.addEventListener('click', () => {
        console.log('settings button clicked');
        const panel = document.getElementById('panel');
        if (!panel)
            return;

        panel.classList.toggle('active');
    });

    // fill availableMenus with all 'tab' elements
    const tabs = document.querySelectorAll('.tab');
    if (!tabs)
        return;

    tabs.forEach(tab => {
        availableMenus.push(tab.getAttribute('data-target-url'));
    });
    activesTabs = availableMenus.length;
}

initSettings();

async function initPanelContent() {
    const togglerContainer = document.getElementById('toggler_container');
    if (!togglerContainer)
        return;

    const tabs = document.querySelectorAll('.tab');
    if (!tabs)
        return;

    tabs.forEach(async tab => {
        // create a toggler element for each tab
        const toggler = document.createElement('div');
        toggler.classList.add('toggler');
        toggler.setAttribute('data-target-url', tab.getAttribute('data-target-url'));

        // set the toggler text to the tab text (from the inner span)
        const span = document.createElement('span');
        span.textContent = tab.querySelector('span').textContent;

        const img = document.createElement('img');
        img.src = await retrieveFavicon(tab.getAttribute('data-target-url'));

        toggler.appendChild(span);
        toggler.appendChild(img);

        // add click event listener to the toggler
        toggler.addEventListener('click', () => {
            const targetValue = toggler.getAttribute('data-target-url');
            console.log(`toggler clicked: ${targetValue}`);

            // check if the tab is already hidden
            const index = hiddenMenus.indexOf(targetValue);
            if (index === -1) {
                if (activesTabs <= 1)
                    return;
                // hide the tab
                hiddenMenus.push(targetValue);
                tab.classList.add('hidden');
                activesTabs--;

                toggler.classList.add('off');
            }
            else {
                // show the tab
                hiddenMenus.splice(index, 1);
                tab.classList.remove('hidden');
                activesTabs++;

                toggler.classList.remove('off');
            }

            saveSettings();
        });

        // append the toggler to the toggler container
        togglerContainer.appendChild(toggler);

    });

    setTimeout(() => {
        loadSettings();
    }, 1000);
    }

initPanelContent();
