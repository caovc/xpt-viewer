# -*- coding: utf-8 -*-
# @Author   : caov
# @Time     : 2024/3/8 6:00 PM
# @File     : data_list.py
# @Project  : xpt-viewer
import feffery_antd_components as fac
from dash import html


def generate_data_list(files=[]):
    if files:
        return html.Div(
            [
                fac.AntdTree(
                    id="dataset-list",
                    treeData=[
                        {
                            "title": "文件列表",
                            "key": "root",
                            "selectable": False,
                            "children": [
                                {
                                    "title": f"{file}",
                                    "key": f"{file}",
                                    # "contextMenu": [
                                    #     {
                                    #         "key": f"{file}",
                                    #         "label": "数据集基本信息",
                                    #         "icon": "antd-info-circle",
                                    #     }
                                    # ],
                                }
                                for file in files
                            ],
                        }
                    ],
                    height=500,
                    defaultExpandAll=True,
                )
            ]
        )
    else:
        return html.Div(
            [fac.AntdEmpty()],
            style={"paddingTop": "10px"},
        )
