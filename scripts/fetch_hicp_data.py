from webdatapy.sources.icp.eurostat.hicp_client import download_hicp_index
from webdatapy.sources.icp.eurostat.hicp_client import load_hicp_tsv_file_to_memory
from webdatapy.sources.icp.codes import classification_code, geo_code, index_code
import gzip
import json

# file_path=download_hicp_index("/home/dev/Documents/python_sandbox/currencies_project/web-data")

file_path = "/home/dev/Documents/python_sandbox/currencies_project/web-data/prc_hicp_midx.tsv.gz"

result = load_hicp_tsv_file_to_memory(file_path)

print(len(result))
print(len(result[0:3]))
print(result[25119])
