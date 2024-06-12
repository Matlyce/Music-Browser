import sys, requests, tempfile, os, json
from PyQt5 import QtGui
from PyQt5.QtCore import Qt  # Import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTabBar, QWidget, QGridLayout, QMenu, QAction, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSplashScreen, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QEvent, QRect, QSettings, QTimer, QPropertyAnimation
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import qInstallMessageHandler, qDebug, qWarning, qCritical
from PyQt5.QtWinExtras import QtWin
# import QCloseEvent
import webbrowser

# Custom message handler to suppress web engine logs
def customMessageHandler(type, context, message):
    pass  # Suppress all messages

# Install the custom message handler
qInstallMessageHandler(customMessageHandler)

DONATE_URL = "https://www.buymeacoffee.com/matlyce"

BASEDIR = os.path.abspath(os.path.dirname(__file__))
ICON_PATH = os.path.join(BASEDIR, "PP9.ico")


def open_donate_url():
    webbrowser.open(DONATE_URL)


def get_favicon_url(url):
    # Extract the base URL
    base_url = QUrl(url).toString(QUrl.RemovePath | QUrl.RemoveQuery | QUrl.RemoveFragment)

    # Check for common favicon locations
    favicon_urls = [f"{base_url}/favicon.ico", f"{base_url}/favicon.png"]
    for favicon_url in favicon_urls:
        response = requests.head(favicon_url)
        if response.status_code == 200:
            return favicon_url
    return None


def get_favicon(favicon_url):
    response = requests.get(favicon_url)
    if response.status_code == 200:
        # Create a temporary file to save the favicon
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    return None


def open_about_dialog(parent):
    # Create an about dialog
    about = QMessageBox(parent)

    # set the size to 500x500
    about.setFixedSize(500, 500)

    # set the style for the about dialog
    about.setStyleSheet("""
        QMessageBox {
            background-color: #282828;
            border: none;
            color: white;
            /* set the font to roboto */
            font-family: Roboto;
            font-weight: bold;
        }
        QMessageBox QLabel {
            color: white;
        }
        QMessageBox QPushButton {
            background-color: #080908;
            color: white;
            border: none;
            padding: 5px 20px;
        }
        QMessageBox QPushButton:hover {
            background-color: #282828;
        }
    """)
    # set the icon for the about dialog from this website: "https://matlyce.fr/"
    icon = get_favicon_url("https://matlyce.fr/")
    icon = QIcon(get_favicon(icon))
    about.setWindowIcon(icon)

    # set the title of the about dialog
    about.setWindowTitle("About")

    # set icon
    about.setWindowIcon(QIcon(ICON_PATH))

    # set the text of the about dialog
    about.setText("Music Browser\t\t\tVersion: 1.0\n\nAuthor: Matlyce")

    # add an ok button to the about dialog
    about.addButton(QMessageBox.Close)
    # set the text of the ok button
    about.button(QMessageBox.Close).setText("Close")
    # connect the ok button to close the about dialog
    about.button(QMessageBox.Close).clicked.connect(about.close)

    # add a donate button to the about dialog
    about.addButton(QMessageBox.Yes)
    # set the text of the donate button
    about.button(QMessageBox.Yes).setText("Donate")
    # connect the donate button to open the donate url in the user browser (using webbroser module)
    about.button(QMessageBox.Yes).clicked.connect(open_donate_url)

    # add a linkedin button to the about dialog
    about.addButton(QMessageBox.No)
    # connect the linkedin button to open the linkedin url in the user browser (using webbroser module)
    about.button(QMessageBox.No).clicked.connect(lambda: webbrowser.open("https://www.linkedin.com/in/mathis-emaille/"))
    # set the text of the linkedin button
    about.button(QMessageBox.No).setText("LinkedIn")

    # add a github button to the about dialog
    about.addButton(QMessageBox.Ok)
    # set the text of the github button
    about.button(QMessageBox.Ok).setText("GitHub")
    # connect the github button to open the github url in the user browser (using webbroser module)
    about.button(QMessageBox.Ok).clicked.connect(lambda: webbrowser.open("https://www.github.com/matlyce/"))


    # set the donate button to be the default button
    about.setDefaultButton(QMessageBox.Yes)

    # show the about dialog
    about.exec_()



class CustomQWebEngineView(QWebEngineView):
    def __init__(self):
        super().__init__()

        # set style for the web view
        self.setStyleSheet("""
            background-color: #282828;
        """)

        # Set a dark background color for the main window
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))  # Dark gray background
        self.setPalette(palette)

        self.setWindowIcon(QIcon(ICON_PATH))
        # set name of the window
        self.setWindowTitle("Music Browser")
        # rename the C++ Developement Framework (defautl name) to Music Browser
        self.setObjectName("Music Browser")

        # set the default icon
        self.setWindowIcon(QIcon(ICON_PATH))


    def contextMenuEvent(self, event):
        # Create a custom context menu for the web view
        self.context_menu = QMenu(self)
        # donate action that will open in the user browser the donate url
        donate_action = QAction("Donate", self)
        donate_action.triggered.connect(open_donate_url)
        # about action that will open the about dialog
        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: open_about_dialog(self))
        # add the actions to the context menu
        self.context_menu.addAction(donate_action)
        self.context_menu.addAction(about_action)

        # set style for the context menu
        self.context_menu.setStyleSheet("""
            QMenu {
                background-color: #282828;
                border: none;
                color: white;
                /* set the font to roboto */
                font-family: Roboto;
                font-weight: bold;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #080908;
            }
        """)

        self.context_menu.popup(event.globalPos())


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the default icon
        self.setWindowIcon(QIcon(ICON_PATH))
        # set name of the window
        self.setWindowTitle("Music Browser")
        # rename the C++ Developement Framework (defautl name) to Music Browser
        self.setObjectName("Music Browser")


        # set style for the main window
        self.setStyleSheet("background-color: #000000;") 

        # Set a dark background color for the main window
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))  # Dark gray background
        self.setPalette(palette)

        # Create a QSettings instance to manage settings
        self.settings = QSettings("Matlyce", "MusicBrowser")

        # Load tab configuration or create a default one
        self.tab_config = self.load_tab_config()

        if self.tab_config:
            print("[CONFIG] loaded: " + str(self.tab_config))

        self.setGeometry(100, 100, 1280, 720)

        # create three tabs for the tabbed browser
        # these tabs must take the full space of the window (width) and be placed at the top
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBar().setObjectName("tabs")
        self.tabs.setTabsClosable(False)
        # disable tab scrolling
        self.tabs.setMovable(False)
        # connect the tabCloseRequested signal to the close_tab method
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Create a context menu for the tabs
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)

        # Connect the iconChanged signal to update the app's window icon
        # self.tabs.currentChanged.connect(self.update_window_icon)

        # set the width of the tabs to fit the window
        self.tabs.tabBar().setExpanding(True)

        self.tabs.setStyleSheet("""
            background-color: #282828;
        """)

        # create the first tab
        self.add_tab(QUrl("https://music.youtube.com/"), "YouTube Music")
        # check if key exists in dict
        if "youtube_music" in self.tab_config:
            if self.tab_config["youtube_music"] == False:
                # disable
                self.tabs.setTabEnabled(0, False)
                # hide
                self.tabs.setTabVisible(0, False)

        # create the second tab
        self.add_tab(QUrl("https://www.deezer.com/fr/"), "Deezer")
        if "deezer" in self.tab_config:
            if self.tab_config["deezer"] == False:
                # disable
                self.tabs.setTabEnabled(1, False)
                # hide
                self.tabs.setTabVisible(1, False)

        # create the third tab
        self.add_tab(QUrl("https://open.spotify.com/"), "Spotify")
        if "spotify" in self.tab_config:
            if self.tab_config["spotify"] == False:
                # disable
                self.tabs.setTabEnabled(2, False)
                # hide
                self.tabs.setTabVisible(2, False)

        # set the selected tab to first enabled tab
        for i in range(self.tabs.count()):
            if self.tabs.isTabEnabled(i):
                self.tabs.setCurrentIndex(i)
                break
                

        self.tab_height = 40

        # set the height of the tabs
        self.tabs.tabBar().setFixedHeight(self.tab_height)

        # Set the style of the tabs like following rules:
        # - the height of the tabs is 50px
        # - the color theme must be a dark mode theme (like youtube dark mode)
        # - the tabs must be placed at the top of the window
        # - the text of the tabs must be white and bigger than the default size
        
        self.setStyleSheet("""
            QTabBar#tabs::tab {
                height: """ + str(self.tab_height) + """px;
                background-color: #282828;
            }
            /* move the icon tabs closer to the label text */
            QTabBar::tab:only-icon {
                padding-right: 5px;
                padding-left: 20px;
            }
            
            #tabs::tab-bar {
                height: """ + str(self.tab_height) + """px;
                background-color: #282828;
            }
            #tabs::tab {
                color: white;
                font-size: 16px;
                background-color: #282828;
            }
            #tabs::tab:selected {
                background-color: #080908;
            }
            /* remove the border of the tab bar */
            QTabWidget::pane {
                border: none;
                background-color: #282828;
            }
            /* remove the border of the tab bar */
            QTabBar::tab {
                border: none;
                background-color: #282828;
                /* set the font to roboto */
                font-family: Roboto;
                font-weight: bold;
            }
            /* set the entiere windows background to dark */
            QMainWindow {
                background-color: #282828;
            }
            /* set the background color of the tabs to dark */
            QTabWidget::pane {
                background-color: #282828;
            }
            /* set the background color of the tabs to dark */
            QTabBar::tab {
                background-color: #282828;
            }
        """)

        # set the default icon
        self.setWindowIcon(QIcon(ICON_PATH))
        print("INIT DONE")

        # Creating the splash screen
        rounded_img = QPixmap(ICON_PATH)
        rounded_img = rounded_img.copy(rounded_img.rect())
        rounded_img.setMask(rounded_img.createHeuristicMask())
        self.splash = QSplashScreen(rounded_img)
        self.splash.show()

        # minimize the window while the splash screen is shown
        self.setWindowState(Qt.WindowMinimized)

        # add the tabs to the window -> This gonna start the app "loading process"
        self.setCentralWidget(self.tabs)

        # Close the splash screen after a delay
        # QTimer.singleShot(200, self.close_splash)
        self.close_splash()
        print("SPLASH REQUESTED")


    def close_splash(self):
        self.splash.finish(self)
        # Restore the window
        self.setWindowState(Qt.WindowActive)


    def load_tab_config(self):
        default_tab_config = {
            "youtube_music": True,
            "deezer": True,
            "spotify": True
        }
        tab_config = self.settings.value("tab_config", defaultValue=default_tab_config)
        return tab_config

    def save_tab_config(self):
        self.settings.setValue("tab_config", self.tab_config)
        print("[CONFIG] Saved: " + str(self.tab_config))



    def close_tab(self, index):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(index)


    def add_tab(self, url, label):
        # Create a new web view for the tab
        web_view = CustomQWebEngineView()
        web_view.setUrl(url)

        # Add the web view to the tabs
        self.tabs.addTab(web_view, label)

        # Retrieve and set the website's favicon as the tab's icon
        favicon_url = get_favicon_url(url.toString())
        if favicon_url:
            icon = QIcon(get_favicon(favicon_url))
            self.tabs.setTabIcon(self.tabs.count() - 1, icon)


    def show_tab_context_menu(self, position):
        tab_bar = self.tabs.tabBar()
        context_menu = QMenu(self)

        for index in range(tab_bar.count()):
            tab_text = tab_bar.tabText(index)
            toggle_action = QAction(f"Toggle '{tab_text}'", self)
            toggle_action.setCheckable(True)
            toggle_action.setChecked(self.tabs.isTabEnabled(index))
            toggle_action.triggered.connect(lambda checked, index=index: self.toggle_tab(checked, index))
            context_menu.addAction(toggle_action)

        # set the style for the context menu
        context_menu.setStyleSheet("""
            QMenu {
                background-color: #282828;
                border: none;
                color: white;
                /* set the font to roboto */
                font-family: Roboto;
                font-weight: bold;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #080908;
            }
        """)

        context_menu.exec_(tab_bar.mapToGlobal(position))


    def toggle_tab(self, checked: bool, index: int):
        if checked:
            # DISABLING PART

            # need to update the tab config
            item_name = self.tabs.tabText(index).lower().replace(" ", "_")
            print("item_name: " + item_name)
            self.tab_config[str(item_name)] = checked

            # now set the state of the tab
            self.tabs.setTabEnabled(index, checked)
        else:
            # ENABLING PART

            # Check if at least one other tab is enabled
            at_least_one_enabled = any(self.tabs.isTabEnabled(i) for i in range(self.tabs.count()) if i != index)

            if at_least_one_enabled:
                # need to update the tab config
                item_name = self.tabs.tabText(index).lower().replace(" ", "_")
                print("item_name: " + item_name)
                self.tab_config[str(item_name)] = checked

                self.tabs.setTabEnabled(index, checked)
            else:
                QMessageBox.warning(self, "Warning", "At least one tab must be active.")
                self.tabs.setTabEnabled(index, True)

        # Hide disabled tabs
        for i in range(self.tabs.count()):
            self.tabs.setTabVisible(i, self.tabs.isTabEnabled(i))


    def update_window_icon(self, index):
        # Update the app's window icon with the favicon of the selected tab
        tab = self.tabs.widget(index)
        if tab:
            icon = tab.page().icon()
            if not icon.isNull():
                self.set_window_icon_with_tab_icon(icon)

    def set_window_icon_with_tab_icon(self, icon):
        pixmap = icon.pixmap(16, 16)  # Adjust the size of the icon as needed
        self.setWindowIcon(QIcon(pixmap))


    def contextMenuEvent(self, event):
        print("contextMenuEvent")
        pass


    def closeEvent(self, event) -> None:
        self.save_tab_config()
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    try:
        from ctypes import windll  # Only exists on Windows.
        appid = 'matlyce.music.browser.1'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    except ImportError:
        app.setApplicationName("music.browser")
        pass

    app.setApplicationDisplayName("Music Browser")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("matlyce")
    app.setOrganizationDomain("tech")
    app.setWindowIcon(QIcon(ICON_PATH))
    app.setQuitOnLastWindowClosed(True)
    app.setObjectName("Music Browser")
    app.setDesktopFileName("Music Browser")

    browser = WebBrowser()

    # then show the window
    browser.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
