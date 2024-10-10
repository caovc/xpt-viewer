# -*- coding: utf-8 -*-
# @Author   : caov
# @Time     : 2024/3/8 2:59 PM
# @File     : layout.py
# @Project  : xpt-viewer
import dash_ag_grid as dag
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html, dcc

layout = html.Div(
    id="app-container",
    children=[
        fac.AntdLayout(
            children=[
                fac.AntdHeader(
                    children=[
                        fac.AntdSpace(
                            [
                                fac.AntdTitle(
                                    "XPT Viewer",
                                    level=3,
                                    style={"color": "white", "margin": "0"},
                                ),
                                fac.AntdButton(
                                    id="app-help-button",
                                    children=[fac.AntdIcon(icon="antd-question")],
                                    shape="circle",
                                    size="small",
                                    style={"color": "black"},
                                ),
                            ]
                        )
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "left",
                        "alignItems": "center",
                        "padding": "20px",
                    },
                ),
                fac.AntdLayout(
                    [
                        fuc.FefferyResizable(
                            id="app-sider",
                            children=[
                                fac.AntdButton(
                                    "上传.xpt文件",
                                    id="upload-button",
                                    type="dashed",
                                    icon=fac.AntdIcon(icon="antd-cloud-upload"),
                                    danger=True,
                                    style={"overflow": "hidden"},
                                ),
                                html.Div(
                                    id="dataset-guide-container",
                                    children=[
                                        dcc.Loading(
                                            id="dataset-list-container",
                                            children=[fac.AntdEmpty()],
                                        ),
                                    ],
                                    style={"paddingTop": "10px"},
                                ),
                            ],
                            defaultSize={
                                "width": 200,
                                "height": "calc(100vh - 64px - 10px)",
                            },
                            minWidth="1vw",
                            maxWidth="40vw",
                            direction=["right"],
                            handleClassNames={"right": "right-resize-handle"},
                            bounds="parent",
                        ),
                        fac.AntdLayout(
                            [
                                fac.AntdContent(
                                    html.Div(
                                        children=[
                                            fac.AntdSpace(
                                                [
                                                    html.Div(
                                                        [
                                                            fac.AntdPageHeader(
                                                                id="app-page-header",
                                                                title="数据浏览",
                                                                subTitle="",
                                                                showBackIcon=False,
                                                                children=[],
                                                            ),
                                                        ],
                                                        id="app-page-header-container",
                                                    ),
                                                    fac.AntdSegmented(
                                                        id="datatable-header-type",
                                                        options=[
                                                            {
                                                                "label": "显示列名",
                                                                "value": "name",
                                                            },
                                                            {
                                                                "label": "显示列标签",
                                                                "value": "label",
                                                            },
                                                        ],
                                                        value="label",
                                                        disabled=True,
                                                    ),
                                                ]
                                            ),
                                            dcc.Loading(
                                                children=[
                                                    dag.AgGrid(
                                                        id="app-datatable",
                                                        className="ag-theme-quartz",
                                                        enableEnterpriseModules=True,
                                                        licenseKey="test",
                                                        columnSize="autoSize",
                                                        defaultColDef={
                                                            "resizable": True,
                                                            "sortable": True,
                                                            "filter": True,
                                                        },
                                                        dashGridOptions={
                                                            "sideBar": {
                                                                # "toolPanels": [
                                                                #     "columns",
                                                                #     "filters",
                                                                # ],
                                                                # "defaultToolPanel": None,
                                                            },
                                                            "columnMenu": "new",
                                                            "rowDragManaged": True,
                                                            "pagination": True,
                                                        },
                                                        columnDefs=[],
                                                        rowData=[],
                                                        style={"height": "85vh"},
                                                    )
                                                ],
                                            ),
                                        ],
                                        style={
                                            "height": "100%",
                                            "padding": "10px",
                                        },
                                    ),
                                    style={"backgroundColor": "white"},
                                ),
                            ]
                        ),
                    ],
                    style={"flexDirection": "row"},
                ),
            ],
            style={"height": "100vh"},
        )
    ],
)
