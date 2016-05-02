from selenium import webdriver

service_args = [
    '--proxy=127.0.0.1:1080',
    '--proxy-type=socks5',
]

driver = webdriver.PhantomJS(service_args=service_args)

driver.get('https://www.google.com')

driver.save_screenshot('1.png')
