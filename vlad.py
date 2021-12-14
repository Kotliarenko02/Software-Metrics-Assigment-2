from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest
import pprint
import json

ADDRESS = "https://en.wikipedia.org/wiki/Software_metric"
DRIVER_PATH = "/Users/valikpavlenko/code/geckodriver"
RANGE = 10

class TestResults(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=DRIVER_PATH)
        self.wait = WebDriverWait(self.driver, RANGE)
        self.address = ADDRESS

    def test_open_page(self):
        csv_content_count = {}
        csv_content_duration = {}
        for i in range(RANGE):
            result = self.driver.get(ADDRESS)
            self.assertIn(self.address, self.driver.current_url)
            script = "return window.performance.getEntries();"
            perf = self.driver.execute_script(script)

            for curr in perf:
                if 'https:' not in curr['name']:
                    continue
                if csv_content_count.get(curr['name'], None):
                    csv_content_count[curr['name']] += 1
                else:
                    csv_content_count[curr['name']] = 1
                csv_content_duration[curr['name']] = csv_content_duration.get(curr['name'], 0) + curr['duration']

        dict_for_json = {}
        dict_for_json_id = 0
        for key, value in csv_content_duration.items():
            dict_for_json[f'{dict_for_json_id}'] = {'name': key, 'duration': round(value / csv_content_count[key])}
            dict_for_json_id += 1

        with open('result.json', 'w') as fh:
            json.dump(dict_for_json, fh, indent=1)
        with open('result.json', 'r') as fh:
            result = json.load(fh)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()