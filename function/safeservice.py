try:
    from __main__ import app
except ImportError:
    from main import app
import json
import settings.repositories as repositories

from time import time as epoch
from flask import abort, request
from settings.database import get_db
from settings.response import json_rsp


# =====================GameServer请求处理=====================#
# 玩家登入
@app.route("/bat/game/gameLoginNotify", methods=["POST"])
@app.route("/inner/bat/game/gameLoginNotify", methods=["POST"])
# @ip_whitelist(['192.168.1.8'])
def player_login():
    cursor = get_db().cursor()
    player_info = json.loads(request.data.decode())
    uid = player_info["uid"]
    account_type = player_info["account_type"]
    account = player_info["account"]
    platform = player_info["platform"]
    region = player_info["region"]
    biz_game = player_info["biz_game"]
    cursor.execute(
        "INSERT INTO `t_accounts_events` (`uid`, `method`, `account_type`, `account_id`, `platform`, `region`, `biz_game`, `epoch_created`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (uid, "LOGIN", account_type, account, platform, region, biz_game, int(epoch())),
    )
    return json_rsp(repositories.RES_SUCCESS, {})


# 玩家登出
@app.route("/bat/game/gameLogoutNotify", methods=["POST"])
@app.route("/inner/bat/game/gameLogoutNotify", methods=["POST"])
def player_logout():
    cursor = get_db().cursor()
    player_info = json.loads(request.data.decode())
    uid = player_info["uid"]
    account_type = player_info["account_type"]
    account = player_info["account"]
    platform = player_info["platform"]
    region = player_info["region"]
    biz_game = player_info["biz_game"]
    cursor.execute(
        "INSERT INTO `t_accounts_events` (`uid`, `method`, `account_type`, `account_id`, `platform`, `region`, `biz_game`, `epoch_created`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            uid,
            "LOGOUT",
            account_type,
            account,
            platform,
            region,
            biz_game,
            int(epoch()),
        ),
    )
    return json_rsp(repositories.RES_SUCCESS, {})


# 心跳包
@app.route("/bat/game/gameHeartBeatNotify", methods=["POST"])
@app.route("/inner/bat/game/gameHeartBeatNotify", methods=["POST"])
def player_heartbeat():
    print(request.data)
    try:
        return json_rsp(repositories.RES_SUCCESS, {})
    except Exception as err:
        print(f"处理心跳包时出现意外错误{err=}, {type(err)=}")
        abort(500)


# 配置验证
@app.route("/config/verify", methods=["GET"])
@app.route("/perf/config/verify", methods=["GET"])
def config_verify():
    return json_rsp(repositories.RES_SUCCESS, {"code": 0})


# Data上传
@app.route("/dataUpload", methods=["POST"])
@app.route("/perf/dataUpload", methods=["POST"])
def data_upload():
    return json_rsp(repositories.RES_SUCCESS, {"code": 0})
