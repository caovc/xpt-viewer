# -*- coding: utf-8 -*-
import os

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html, dcc, Input, Output, State
from flask import request

from components.data_list import generate_data_list
from components.data_meta import generate_dataset_meta
from components.guides import get_app_guides
from components.upload import xpt_upload
from config import CACHE_PATH
from layouts import layout
from utils.xpt import get_xpt_info, get_xpt_data, rm_xpt_cache

# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    suppress_callback_exceptions=True,
    serve_locally=True,
    compress=True,
    update_title="",
)
app.title = "XPT Viewer"
server = app.server

# ------------------------------------------------ App UI Section --------------------------------------------------

app.layout = html.Div(
    [
        dcc.Store(id="file-path", storage_type="session"),
        dcc.Store(id="file-encoding", storage_type="session"),
        layout,
        # 用于清理缓存xpt文件
        fuc.FefferyListenUnload(id="unload-listener"),
        # 应用指引dom容器
        html.Div(id="app-guide"),
        fac.AntdModal(id="app-modal", width=700, renderFooter=True),
    ]
)


# ------------------------------------------------ Server Callback Section --------------------------------------------
# 上传文件弹窗
@app.callback(
    Output("app-modal", "visible"),
    Output("app-modal", "title"),
    Output("app-modal", "children"),
    Input("upload-button", "nClicks"),
    prevent_initial_call=True,
)
def upload_modal(nclick):
    if nclick:
        return True, "上传.xpt文件", xpt_upload
    else:
        return dash.no_update


# 上传文件
@app.callback(
    Output("file-path", "data"),
    Output("file-encoding", "data"),
    Input("app-modal", "okCounts"),
    State("xpt-uploader", "lastUploadTaskRecord"),
    State("xpt-encoding-select", "value"),
    State("file-path", "data"),
    prevent_initial_call=True,
)
def upload_xpt(confirmed, file_path, file_encoding, old_tasks):
    if confirmed and file_path:
        if old_tasks:
            rm_xpt_cache(old_tasks)
        return [f for f in file_path if f["taskStatus"] == "success"], file_encoding
    else:
        return dash.no_update


@app.callback(
    Output("file-path", "data", allow_duplicate=True),
    Output("file-encoding", "data", allow_duplicate=True),
    Input("unload-listener", "unloaded"),
    State("file-path", "data"),
    prevent_initial_call=True,
)
def clear_cache(unload, files_info):
    if unload:
        rm_xpt_cache(files_info)
        return [], []


# 生成数据列表
@app.callback(
    Output("dataset-list-container", "children"),
    Output("datatable-header-type", "disabled"),
    Input("app-modal", "okCounts"),
    State("xpt-uploader", "lastUploadTaskRecord"),
    prevent_initial_call=True,
)
def get_data_list(confirmed, file_path):
    if confirmed and file_path:
        return (
            generate_data_list(
                files=[f["fileName"] for f in file_path if f["taskStatus"] == "success"]
            ),
            False,
        )
    else:
        return dash.no_update


# 根据选择数据更改页头副标签
@app.callback(
    Output("app-page-header", "subTitle"),
    Input("dataset-list", "selectedKeys"),
    State("file-path", "data"),
    prevent_initial_call=True,
)
def change_page_header(selected_data, files_info):
    if selected_data:
        meta = [
            f["uploadResponse"]
            for f in files_info
            if f["fileName"] == selected_data[0] and f["taskStatus"] == "success"
        ]
        return fac.AntdPopover(
            fac.AntdSpace(
                [
                    fac.AntdText(f"{selected_data[0]}"),
                    fac.AntdIcon(icon="antd-info-circle"),
                ]
            ),
            placement="bottom",
            title=[],
            content=generate_dataset_meta(data_meta=meta[0]),
        )
    else:
        return ""


# 展示XPT里的数据
@app.callback(
    Output("app-datatable", "columnDefs"),
    Output("app-datatable", "rowData"),
    Input("dataset-list", "selectedKeys"),
    Input("datatable-header-type", "value"),
    State("file-path", "data"),
    prevent_initial_call=True,
)
def show_xpt_data(selected_data, header_type, files_info):
    if selected_data:
        meta = [
            f["uploadResponse"]
            for f in files_info
            if f["fileName"] == selected_data[0] and f["taskStatus"] == "success"
        ]
        return get_xpt_data(
            file_path=meta[0]["file_path"],
            header_type=header_type,
            file_encoding=meta[0]["encoding"],
        )
    else:
        return [], []


# 点击帮助按钮展示应用使用指引
@app.callback(Output("app-guide", "children"), Input("app-help-button", "nClicks"))
def start_app_guide(show):
    if show:
        return get_app_guides()


# ------------------------------------------------ Client Callback Section --------------------------------------------

# 把encoding传入到上传组件
app.clientside_callback(
    """
    function(encoding){
        return {encoding: encoding};
    };
    """,
    Output("xpt-uploader", "apiUrlExtraParams"),
    Input("xpt-encoding-select", "value"),
)

# 清理应用指引的localStorage键，保证每次都能触发应用指引
app.clientside_callback(
    """
    function(n){
        Object.keys(localStorage).forEach(function(key){
            if (key.includes("xpt-viewer-guide")){
                localStorage.removeItem(key)
            }
        });
        return {};
    }
    """,
    Output("dataset-list-container", "style"),
    Input("app-help-button", "nClicks"),
)
# ------------------------------------------------ Upload Function Section --------------------------------------------


# 这里的app即为Dash实例
@app.server.route("/upload/", methods=["POST"])
def upload():
    """
    构建文件上传服务
    :return:
    """

    # 获取上传id参数，用于指向保存路径
    uploadId = request.values.get("uploadId")

    # 获取上传的文件名称
    filename = request.files["file"].filename

    # 获取上传的文件编码
    encoding = request.values.get("encoding")
    # print(f"File Encoding: {encoding}")

    # 基于上传id，若本地不存在则会自动创建目录
    try:
        os.mkdir(os.path.join(CACHE_PATH, uploadId))
    except FileExistsError:
        pass

    full_path = os.path.join(CACHE_PATH, uploadId, filename)

    # 流式写出文件到指定目录
    with open(os.path.join(full_path), "wb") as f:
        # 流式写出大型文件，这里的10代表10MB
        for chunk in iter(lambda: request.files["file"].read(1024 * 1024 * 10), b""):
            f.write(chunk)

    # if re.search(r"\.zip$", filename, re.I):
    #     with zipfile.ZipFile(full_path) as f:
    #         f.extractall(os.path.join(CACHE_PATH, uploadId))
    #     # os.remove(full_path)

    try:
        data_meta = get_xpt_info(full_path, file_encoding=encoding)
        return data_meta
    except Exception as e:
        print(f"{filename}上传失败，原因：{e}")
        # 清理文件
        os.remove(full_path)
        raise e


if __name__ == "__main__":
    is_debug = os.getenv("DEBUG", "True")
    app.run_server(debug=eval(is_debug), port=4000)
