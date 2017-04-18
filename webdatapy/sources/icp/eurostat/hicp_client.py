import urllib
import gzip

"""
Source: http://ec.europa.eu/eurostat/web/hicp/data/database
Download source: http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing
"""


def download_hicp_index(path):
    """
    Download tsv file from Eurostat's page to provided folder
    :param path: str path to folder to save downloaded file
    :return: str path to file (path + file name)
    """
    if not path:
        raise ValueError("Missing path to download folder")

    tmp_file_path = path + "/prc_hicp_midx.tsv.gz"

    if path.endswith('/'):
        tmp_file_path = path + "prc_hicp_midx.tsv.gz"

    url = "http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2Fprc_hicp_midx.tsv.gz"

    downloader = urllib.URLopener()
    downloader.retrieve(url, tmp_file_path)

    return tmp_file_path


class DefaultHicpImportFilter:
    def is_row_valid(self, index, classification, country):
        return True

    def is_entry_valid(self, index, classification, country, year, month, value):
        return True


def load_hicp_tsv_file_to_memory(file_path, data_filter = DefaultHicpImportFilter()):
    """
    Load data from tsv file to memory
    :param data_filter: filter rows and entries from imported data
    :param file_path: str path to data source tsv file
    :return: list[dict] list of entries from file
    """
    with gzip.open(file_path, 'rb') as tsv:
        header = tsv.readline()
        headers = header.strip().split("\t")

        first_year = int(headers[1].split("M")[0])
        first_month = int(headers[1].split("M")[1])

        result = []

        for row in tsv:
            columns = row.strip().split("\t")

            row_header = columns[0]

            index = row_header.split(",")[0].strip()
            classification = row_header.split(",")[1].strip()
            country = row_header.split(",")[2].strip()

            if not data_filter.is_row_valid(index, classification, country):
                continue

            entry = {"index": index, "classification": classification, "country": country, "data": []}
            result.append(entry)

            year = first_year
            month = first_month

            for column in columns[1:]:

                value = column.strip()
                if not data_filter.is_entry_valid(index, classification, country, year, month, value):
                    continue

                entry["data"].append({"year": year, "month": month, "value": value})

                month -= 1
                if month == 0:
                    month = 12
                    year -= 1

        return result
