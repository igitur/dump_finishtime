from abc import ABC, abstractmethod
import re

import requests
from bs4 import BeautifulSoup
from loguru import logger

PARSER = "html5lib"


class Scraper(ABC):
    @abstractmethod
    def get_results(self, detailed: bool) -> list:
        pass


def get(url: str) -> BeautifulSoup:
    logger.debug(f"Downloading {url}")
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, PARSER)
        return soup

    logger.error(f"Failed to download the URL. Status code: {response.status_code}")
    return None


def get_json(url: str):
    logger.debug(f"Downloading {url}")
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        return response.json()

    logger.error(f"Error: {response.status_code}")
    return None


def post_json(url: str, data: dict):
    logger.debug(f"Downloading {url}")
    response = requests.post(url, json=data, timeout=30)

    if response.status_code == 200:
        return response.json()

    logger.error(f"Error: {response.status_code}")
    return None


def cp437_to_utf8(s: str) -> str:
    try:
        return s.encode("cp437").decode("utf-8")
    except Exception:
        return s


def deduce_first_and_last_name_Jan_VAN_DER_MERWE(s) -> tuple[str, str]:
    # use regex to split the string into first and last name where lastname is capital letters only:
    match = re.match(r"(.+?) ([A-Z][A-Z\ -]*$)", s)
    if match is None:
        return (s, "")

    if len(match.groups()) >= 2:
        return match.groups()[-2:]

    return (match.group(1), "")


def deduce_first_and_last_name_Van_der_merwe_Jan(s) -> tuple[str, str]:
    # use regex to split the string into first and last name where lastname is capital letters only:
    match = re.match(
        r"((?:Le +\w+)|(?:D[eou] +\w+)|(?:(?:Janse +)?V[ao]n +(?:Der +)?\w+)|(?:\w+)) +((?:\w+ )*\w+)",
        s,
    )
    if match is None:
        return (s, "")

    if len(match.groups()) >= 2:
        return match.groups()[-2:]

    return (match.group(1), "")
