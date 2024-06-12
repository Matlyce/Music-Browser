async function retrieveFavicon(url) {
    const domain = new URL(url).hostname;
    const faviconUrl = `https://s2.googleusercontent.com/s2/favicons?domain=${domain}`;
    return faviconUrl;
}

async function retrieveDomainName(url) {
    return new URL(url).hostname;
}

async function initTabs() {
    const tabs = document.querySelector('.tabs');
    const tabsElements = tabs.querySelectorAll('.tab');

    for (const tab of tabsElements) {
        const targetUrl = tab.getAttribute('data-target-url');
        if (!targetUrl) {
            continue;
        }

        const img = tab.querySelector('img');
        const faviconUrl = await retrieveFavicon(targetUrl);
        img.src = faviconUrl;

        // add click event listener to the tab element
        tab.addEventListener('click', async () => {
            const domainName = await retrieveDomainName(targetUrl);
            const id = `${domainName}-webview`;
            const webview = document.getElementById(id);

            const container = document.getElementById('container');
            if (!container)
                return;

            const tabs = document.querySelectorAll('.tab');
            for (const t of tabs) {
                t.classList.remove('active');
            }
            tab.classList.add('active');

            // if the element does not exist, create it
            if (!webview) {
                const webview = document.createElement('webview');
                webview.id = `${domainName}-webview`;
                webview.src = targetUrl;
                webview.classList.add('webview');
                container.appendChild(webview);
            }

            const webviews = document.querySelectorAll('webview');
            for (const webv of webviews) {
                if (webv.id !== id) {
                    webv.style.display = 'none';
                } else {
                    webv.style.display = 'flex';
                }
            }
        });
    }

    // simulate click on the first tab (memory improvement)
    tabsElements[0].click();
}

initTabs();