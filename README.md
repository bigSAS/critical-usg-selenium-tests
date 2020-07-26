# Critical USG Selenium tests   
## Getting started   

Install pipenv `pip install pipenv`   

Download chromedriver from https://chromedriver.chromium.org/   
Add chromedriver to PATH.   

Run tests with HTML report `pipenv run pytest -v --html=report.html --self-contained-html --log-file=tests.log`   

#### Example configuration (default configuration dir is configurationz/config.yml)
```yaml
browser: chrome
browser_version: 83.0
wd_hub_url: null  # when null -> local webrdriver is being used :)
headless: false
action_framework:
  wait_between_actions_sec: 1
  timeout_find_element_sec: 5
  timeout_wait_for_condition_sec: 15
```
