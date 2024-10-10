# -*- coding: utf-8 -*-
# @Author   : caov
# @Time     : 2024/3/11 2:30 PM
# @File     : data_meta.py
# @Project  : xpt-viewer
import feffery_antd_components as fac
from dash import html


def generate_dataset_meta(data_meta={}):
    if data_meta:
        return fac.AntdTabs(
            items=[
                {
                    "key": "basic-info",
                    "label": "基本信息",
                    "children": [
                        fac.AntdDescriptions(
                            [
                                fac.AntdDescriptionItem(
                                    data_meta["data_name"], label="数据集名称"
                                ),
                                fac.AntdDescriptionItem(
                                    data_meta["data_label"], label="数据集标签"
                                ),
                                fac.AntdDescriptionItem(
                                    data_meta["ncols"], label="列数"
                                ),
                                fac.AntdDescriptionItem(
                                    data_meta["nrows"], label="行数"
                                ),
                                fac.AntdDescriptionItem(
                                    data_meta["encoding"], label="文件编码"
                                ),
                                fac.AntdDescriptionItem(
                                    data_meta["create_datetime"], label="创建时间"
                                ),
                            ],
                            column=1,
                            bordered=True,
                            labelStyle={"fontWeight": "bold"},
                        )
                    ],
                },
                {
                    "key": "column-info",
                    "label": "列信息",
                    "children": html.Div(
                        [
                            fac.AntdTable(
                                columns=[
                                    {
                                        "title": "列名",
                                        "dataIndex": "name",
                                        "fixed": "left",
                                        "align": "left",
                                    },
                                    {
                                        "title": "列标签",
                                        "dataIndex": "label",
                                        "align": "left",
                                        # "renderOptions": {
                                        #     "renderType": "ellipsis-copyable"
                                        # },
                                    },
                                    {
                                        "title": "类型",
                                        "dataIndex": "type",
                                        "align": "center",
                                        "renderOptions": {"renderType": "tags"},
                                    },
                                    {
                                        "title": "长度",
                                        "dataIndex": "width",
                                        "align": "center",
                                    },
                                ],
                                data=data_meta["column_info"],
                                pagination=False,
                                size="small",
                                bordered=True,
                                # sticky=True,
                                conditionalStyleFuncs={
                                    "name": """
                                    (record, index) => {
                                        return {
                                                style: {
                                                    fontWeight: "bold"
                                                }
                                            }
                                    }
                                    """
                                },
                            )
                        ],
                        style={
                            "maxHeight": "400px",
                            "overflowY": "auto",
                        },
                    ),
                },
            ],
            centered=True,
        )
    else:
        return fac.AntdEmpty()
