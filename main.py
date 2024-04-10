import argparse
import re
import copy
from itertools import product
from dataclasses import dataclass
from absl import app
from absl.flags import argparse_flags
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm


@dataclass
class Person:
    name: str
    CPF: str
    status: str

    def __init__(self, name, cpf, status):
        self.name = name
        self.CPF = cpf
        self.status = status


def extract_single_person_pattern_match(match):
    name = match.group('name').strip()
    cpf = match.group('cpf')
    status = match.group('status').strip()
    person = Person(name, cpf, status)
    return person


def extract_person_info(text):
    # Define regex patterns to extract name, CPF, and status
    name_pattern = r'(?P<name>[A-Z\s]+)\n'
    cpf_pattern = r'CPF (?P<cpf>\*{3}\.\d{3}\.\d{3}-\*\*)\n'
    status_pattern = r'(?P<status>.+?)(?=\n[A-Z]|$)'
    pattern = name_pattern + cpf_pattern + status_pattern
    matches = re.finditer(pattern, text)
    person_info_list = [extract_single_person_pattern_match(match)
                        for match in matches]
    return person_info_list


def is_valid_cpf(cpf):
    cpf = [int(char) for char in cpf if char.isdigit()]

    if len(cpf) != 11:
        return False

    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


def extract_cpf_parts(cpf):
    # Regular expression pattern to extract CPF parts
    pattern = r'(\*\*\*).(\d{3}).(\d{3})-(\*\*)'
    match = re.match(pattern, cpf)
    if match:
        first_part = match.group(1)
        second_part = match.group(2)
        third_part = match.group(3)
        last_part = match.group(4)
        return first_part, second_part, third_part, last_part
    else:
        return None


def get_combinations():
    triplets = [''.join(map(str, c)) for c in product(range(10), repeat=3)]
    tuples = [''.join(map(str, c)) for c in product(range(10), repeat=2)]
    combinations = product(triplets, tuples)
    return combinations


def get_all_cpfs_by_bruteforce(second_part, third_part):
    all_combinations = get_combinations()
    all_cpfs = []
    for first_part, validation_digit in all_combinations:
        parts = (first_part, second_part, third_part, validation_digit)
        generated_cpf = "".join(parts)
        all_cpfs.append(generated_cpf)
    return all_cpfs


def get_all_valid_cpfs(second_part, third_part):
    all_cpfs = get_all_cpfs_by_bruteforce(second_part, third_part)
    valid_cpfs = [c for c in all_cpfs if is_valid_cpf(c)]
    return valid_cpfs


class CPFFinder:
    url = "https://portaldatransparencia.gov.br/pessoa-fisica/busca/lista?"

    def __init__(self, name: str, keyword: str):
        self.name = name
        self.keyword = keyword
        self.url = CPFFinder.url
        self._start_crawler()

    def _start_crawler(self):
        header = Headers(browser="chrome", os="win", headers=False)
        customUserAgent = header.generate()['User-Agent']

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--enable-javascript")
        options.add_argument(f"user-agent={customUserAgent}")
        self.driver = webdriver.Chrome(options=options)

    def _get_remote_info(self, keyword: str, wait_seconds: int = 5):
        driver = copy.copy(self.driver)
        driver.get(self.url)
        input_field = driver.find_element(By.ID, "termo")
        button = driver.find_element(By.ID, "btnBuscar")
        input_field.send_keys(f"\"{keyword}\"")
        input_field.send_keys(Keys.ENTER)
        button.click()
        try:
            wait = WebDriverWait(driver, wait_seconds)
            dynamic_content = wait.until(
                EC.visibility_of_element_located((By.ID, "resultados")))
            results = extract_person_info(dynamic_content.text)
            return results
        except TimeoutException:
            return self._get_remote_info(keyword, wait_seconds + 10)

    def _try_single_cpf(self, cpf):
        results = self._get_remote_info(cpf)
        if len(results) == 1:
            found_person = Person(results[0].name, cpf, results[0].status)
            print(f"{found_person} exists in DB.")
            if self.name.lower() == found_person.name.lower():
                return found_person
        return None

    def _try_cpfs_by_bruteforce(self, incomplete_cpf):
        _, second_part, third_part, _ = extract_cpf_parts(incomplete_cpf)
        valid_cpfs = get_all_valid_cpfs(second_part, third_part)
        for cpf in (pbar := tqdm(valid_cpfs)):
            pbar.set_description(f"Trying CPF {cpf}")
            result = self._try_single_cpf(cpf)
            if result:
                return result
        return None

    def run(self):
        if self.keyword is None:
            results = self._get_remote_info(self.name)
            if len(results) != 1:
                msg = "Many results with this pattern."
                msg += "Try a more specific one."
                print(msg)
            else:
                incomplete_cpf = results[0].CPF
        else:
            incomplete_cpf = self.keyword
        print(f"Parcial CPF: {incomplete_cpf}")
        matched_person = self._try_cpfs_by_bruteforce(incomplete_cpf)
        if matched_person:
            print(f"Found -> {matched_person}")


def parse_args(argv):
    parser = argparse_flags.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--name',
        type=str,
        help='Nome completo da pessoa que se deseja descobrir o CPF',
    )
    parser.add_argument(
        '--keyword',
        type=str,
        help='CPF parcial da pessoa',
        default=None
    )
    return parser.parse_args(argv[1:])


def main(args):
    CPFFinder(args.name, args.keyword).run()


if __name__ == "__main__":
    app.run(main, flags_parser=parse_args)
