from datetime import datetime
from run import app
from flask import render_template, Flask, request, Response
import requests


TARGET_BASE_URL = 'http://www.carton622.cn'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy(path):
    # 构造目标URL
    target_url = f"{TARGET_BASE_URL}/{path}"
    
    # 获取请求中的查询参数
    query_params = request.args

    # 获取原始请求的方法、数据和头部
    method = request.method
    data = request.get_data()
    headers = {key: value for (key, value) in request.headers}

    # 发送请求到目标服务
    response = requests.request(
        method=method,
        url=target_url,
        headers=headers,
        data=data,
        params=query_params,
        allow_redirects=False,
        stream=True
    )

    # 创建响应对象
    resp = Response(
        response.iter_content(),
        status=response.status_code,
        headers=response.headers.items()
    )

    # 返回响应给客户端
    return resp


