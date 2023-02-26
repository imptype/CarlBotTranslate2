"""
Creates selenium chrome driver with all the settings.
Lots of attempts at optimizing Selenium to work faster.
"""

import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ChromeDriver(selenium.webdriver.Chrome):
  def __init__(self, width, height):
    options = Options()
    options.add_argument('no-sandbox')
    options.add_argument('headless')
    #options.headless = True
    options.add_argument('window-size={},{}'.format(width, height))
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-browser-side-navigation')
    options.add_argument('disable-infobars')
    options.add_argument('enable-automation')
    options.add_argument('incognito')
    options.add_argument('hide-scrollbars')
    #options.add_argument('ignore-certificate-errors')
    #options.add_argument('make-default-browser')
    #options.add_argument('make-chrome-default')
    #options.add_argument('force-enable-night-mode')
    #options.add_argument('no-startup-window')
    #options.add_argument('no-service-autorun')
    #options.add_argument('no-proxy-server')
    #options.add_argument('no-pings')
    #options.add_argument('no-first-run')
    #options.add_argument('no-experiments')
    #options.add_argument('no-default-browser-check')
    #options.add_argument('disable-logging-redirect')
    #options.add_argument('disable-extensions')
    #options.add_argument('disable-popup-blocking')
    #options.add_argument('disable-windows10-custom-titlebar')
    #options.add_argument('disable-login-screen-apps')
    #options.add_argument('disable-zero-browsers-open-for-tests')
    #options.add_argument('disable-stack-profiler')
    #options.add_argument('disable-prompt-on-repost')
    #options.add_argument('disable-print-preview')
    #options.add_argument('disable-domain-reliability')
    #options.add_argument('disable-extensions-file-access-check')
    #options.add_argument('disable-default-apps')
    #options.add_argument('disable-component-extensions-with-background-pages')
    #options.add_argument('disable-component-update')
    #options.add_argument('disable-background-networking')
    # https://www.selenium.dev/documentation/webdriver/capabilities/shared/
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'eager'
    super().__init__(options = options, desired_capabilities = caps)