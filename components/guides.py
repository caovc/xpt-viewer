# -*- coding: utf-8 -*-
# @Author   : caov
# @Time     : 2024/3/12 2:18 PM
# @File     : guides.py
# @Project  : xpt-viewer
import uuid

import feffery_utils_components as fuc


def get_app_guides():
    return fuc.FefferyGuide(
        id="xpt-viewer-guide" + str(uuid.uuid4()),
        steps=[
            {
                "selector": "#app-help-button",
                "title": "这是帮助按钮",
                "content": "点击这里开始使用指引。",
                "placement": "right",
            },
            {
                "selector": "#upload-button",
                "title": "这是上传按钮",
                "content": "点击上传xpt文件。",
                "placement": "right",
            },
            {
                "selector": "#dataset-guide-container",
                "title": "这是文件列表",
                "content": "上传文件成功后，会在此处显示文件列表，没有文件显示为空。",
                "placement": "right",
            },
            {
                "selector": "#app-page-header-container",
                "title": "数据集基本信息区域",
                "content": "在左侧文件列表点击选中某个文件后，会在此处显示其文件名，鼠标悬停到其上方的图标上，会出现该数据的一些元信息。",
                "placement": "bottom",
            },
            {
                "selector": ".ag-root-wrapper",
                "title": "数据集数据区域",
                "content": "在左侧文件列表点击选中某个文件后，会在此处以表格形式显示该文件的数据内容。",
                "placement": "top",
                "offset": {"x": 0, "y": 150},
            },
            {
                "selector": "#datatable-header-type",
                "title": "切换数据表表头内容",
                "content": "点击切换数据表表头内容，可选的有显示数据集变量名和显示数据集变量标签。没有上传xpt文件前此按钮禁用。",
                "placement": "right",
            },
        ],
        localKey="xpt-viewer-guide" + str(uuid.uuid4()),
        closable=True,
    )
