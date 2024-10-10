# -*- coding: utf-8 -*-
# @Author   : caov
# @Time     : 2024/3/11 12:47 PM
# @File     : xpt.py
# @Project  : xpt-viewer
import os
import shutil
from functools import lru_cache

import pyreadstat

from config import CACHE_PATH


def get_xpt_info(file_path, file_encoding="utf-8"):
    meta = pyreadstat.read_xport(file_path, encoding=file_encoding)[1]
    column_info = [
        {
            "name": info[0],
            "label": info[1],
            "type": {
                "tag": "文本" if info[2] == "string" else "数字",
                "color": "red" if info[2] == "string" else "blue",
            },
            "width": info[3],
        }
        for info in zip(
            meta.column_names,
            meta.column_labels,
            [_type for _type in meta.readstat_variable_types.values()],
            [_width for _width in meta.variable_storage_width.values()],
        )
    ]
    return dict(
        file_path=file_path,
        data_name=meta.table_name,
        data_label=meta.file_label,
        encoding=file_encoding,
        column_info=column_info,
        nrows=meta.number_rows,
        ncols=meta.number_columns,
        create_datetime=meta.creation_time.strftime(format="%Y-%m-%dT%H:%M:%S"),
    )


@lru_cache(maxsize=10)
def get_xpt_data(file_path, header_type="name", file_encoding="utf-8"):
    try:
        data, meta = pyreadstat.read_xport(file_path, encoding=file_encoding)
        data["id"] = range(1, len(data) + 1)
        row_data = data.to_dict(orient="records")
        column_defs = [
            {
                "field": "id",
                "headerName": "No.",
                "width": 80,
            },
        ] + [
            {
                "field": key,
                "headerName": value if header_type == "label" else key,
                "filter": True,
            }
            for key, value in meta.column_names_to_labels.items()
        ]
        return column_defs, row_data
    except Exception as e:
        print(f"读取文件 {file_path} 失败: {e}")
        raise e


def rm_xpt_cache(files_info):
    folders = set([os.path.join(CACHE_PATH, f["taskId"]) for f in files_info])
    for _folder in folders:
        try:
            shutil.rmtree(_folder)
        except FileNotFoundError:
            pass
