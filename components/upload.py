# -*- coding: utf-8 -*-
# @Author   : caov
# @Time     : 2024/3/8 5:06 PM
# @File     : upload.py
# @Project  : xpt-viewer
import feffery_antd_components as fac
from dash import html

xpt_upload = html.Div(
    [
        fac.AntdAlert(
            message="；".join(
                [
                    "可上传单个或多个xpt文件",
                    "服务器资源有限，为了能同时给更多人使用，xpt-viewer限制单个文件大小为200MB，大于200MB的文件还是建议大家在sas导出查看",
                    "在上传时需要根据实际情况选择正确的文件编码，否则会上传失败（目前支持的编码为utf-8、gbk、latin-1）",
                ]
            ),
            description="",
            showIcon=True,
            messageRenderMode="marquee",
        ),
        fac.AntdForm(
            [
                fac.AntdFormItem(
                    fac.AntdRadioGroup(
                        id="xpt-encoding-select",
                        options=[
                            {
                                "label": "中文",
                                "value": "GBK",
                            },
                            {
                                "label": "英文",
                                "value": "ISO-8859-1",
                            },
                            {
                                "label": "utf-8",
                                "value": "utf-8",
                            },
                        ],
                        optionType="button",
                        defaultValue="utf-8",
                    ),
                    label="选择文件编码",
                    style={"paddingTop": "30px"},
                ),
                fac.AntdFormItem(
                    [
                        fac.AntdDraggerUpload(
                            id="xpt-uploader",
                            apiUrl="/upload/",
                            # fileMaxSize=2 * 1024,
                            fileMaxSize=200,
                            text="上传.xpt，单个文件限制为200MB",
                            hint="点击或拖拽文件至此处进行上传",
                            fileTypes=["xpt"],
                            multiple=True,
                            showPercent=True,
                            style={"paddingTop": "10px"},
                        ),
                    ]
                ),
            ]
        ),
    ],
    style={
        "width": "100%",
        "display": "flex",
        "flexDirection": "column",
    },
)
