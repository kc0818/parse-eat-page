import csv
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup
import requests


@dataclass
class ClinicInfo:
    area: str
    name: str
    address: str
    tel: str
    site: str
    hours: str
    day: str
    reserve_limitation: str
    disease_limitation: str


def safe_find_text(soup_obj, tag, class_name=None):
    """
    指定したタグとクラス名で.find()を実行し、見つからなかった場合は空文字を返す
    """

    element = soup_obj.find(tag, class_=class_name)
    if element is None:
        return ""
    return element.text.strip()


def choose_clinic_info(clinic):
    area = clinic.find_previous("h3").text

    return ClinicInfo(
        area=area,
        name=safe_find_text(clinic, "dt"),
        address=safe_find_text(clinic, "li", "list_add"),
        tel=safe_find_text(clinic, "li", "list_tel"),
        site=safe_find_text(clinic, "li", "list_site"),
        hours=safe_find_text(clinic, "li", "hours"),
        day=safe_find_text(clinic, "li", "day"),
        reserve_limitation=safe_find_text(clinic, "li", "list_reservation"),
        disease_limitation=safe_find_text(clinic, "li", "list_limit"),
    )


def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        # ファイルの内容をBeautiful Soupで解析
        soup = BeautifulSoup(file, "html.parser")

    return soup


def write_csv(clinic_info_list):
    fieldnames = ['area', 'name', 'address', 'tel', 'site', 'hours', 'day', 'reserve_limitation', 'disease_limitation']

    with open("output.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # ヘッダー書き込み
        writer.writeheader()
        # データを書き込む
        for clinic in clinic_info_list:
            writer.writerow(asdict(clinic))  # データクラスを辞書に変換して書き込む

def parse_html(soup_obj):
    # HTMLをパース
    clinic_list = soup_obj.find_all("dl")

    clinic_info_list = []
    for clinic in clinic_list:
        clinic_info = choose_clinic_info(clinic)
        clinic_info_list.append(clinic_info)

    return clinic_info_list


def fetch_html(url):
    response = requests.get(url)
    return response


def main():
    url_list = [
        "https://jfir.jp/eat-facilities/",
        "https://jfir.jp/eat-facilities-2/",
        "https://jfir.jp/eat-facilities-3/",
        "https://jfir.jp/eat-facilities-4/",
    ]

    clinic_info_list = []
    for url in url_list:
        response = fetch_html(url)
        soup = BeautifulSoup(response.content, "html.parser")

        clinic_info = parse_html(soup)
        clinic_info_list.extend(clinic_info)

    # csv書き出し
    write_csv(clinic_info_list)


if __name__ == '__main__':
    main()
