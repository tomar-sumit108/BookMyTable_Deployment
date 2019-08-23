from flask import jsonify
def send_get_response(data,resp,code=200):
    # if len(data)==0:
    #     res=jsonify(resp)
    #     res.status_code=404
    #     return res

    res=jsonify(data)
    res.status_code = code
    res.headers.add('Access-Control-Allow-Origin','*')
    return res
