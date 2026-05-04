"""
巴别塔实验 · 染色画布 — 画布服务器
Babel Experiment: Dye Canvas — Canvas Server

接收来自分布式染坊的心跳信号，在画布上生成随机像素，
实现画布自动成长。画布是L4诺亚世界的物理雏形。

CLI 命令:
  python canvas_server.py                        启动画布服务器
  python canvas_server.py --show-password        显示上帝之手密码
  python canvas_server.py --reset-password       重置上帝之手密码
"""

import sys

# ── CLI 命令（在导入Flask之前执行）──
if __name__ == "__main__" and len(sys.argv) > 1:
    cmd = sys.argv[1]
    if cmd == "--show-password" or cmd == "--reset-password":
        import os, secrets
        
        _env_path = os.path.join(os.path.dirname(__file__), ".env")
        
        if cmd == "--show-password":
            # 尝试从.env读取
            pwd = os.environ.get("GOD_PASSWORD", "")
            if not pwd:
                try:
                    with open(_env_path) as f:
                        for line in f:
                            if line.startswith("GOD_PASSWORD="):
                                pwd = line.strip().split("=", 1)[1]
                                break
                except FileNotFoundError:
                    pass
            if pwd:
                print(f"\n🔑  GOD_PASSWORD={pwd}")
                print(f"📄  {_env_path}")
            else:
                print("\n⚠️  上帝之手未启用 (GOD_PASSWORD 未设置)")
            sys.exit(0)
        
        if cmd == "--reset-password":
            new_pass = secrets.token_hex(16)
            try:
                lines = []
                found = False
                try:
                    with open(_env_path) as f:
                        for line in f:
                            if line.startswith("GOD_PASSWORD="):
                                lines.append(f"GOD_PASSWORD={new_pass}\n")
                                found = True
                            else:
                                lines.append(line)
                except FileNotFoundError:
                    pass
                if not found:
                    lines.append(f"GOD_PASSWORD={new_pass}\n")
                with open(_env_path, "w") as f:
                    f.writelines(lines)
                print(f"✅  上帝之手密码已重置")
                print(f"🔑  GOD_PASSWORD={new_pass}")
                print(f"📄  已写入: {_env_path}")
            except OSError as e:
                print(f"❌  密码写入失败: {e}")
            sys.exit(0)

import os
import json
import time
import random
import atexit
import signal
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "babel-experiment-secret-2026")

# ── 配置 ──────────────────────────────────
CONFIG = {
    "width": int(os.environ.get("CANVAS_WIDTH", "200")),
    "height": int(os.environ.get("CANVAS_HEIGHT", "200")),
    "pixel_size": int(os.environ.get("PIXEL_SIZE", "2")),
    "growth_threshold": float(os.environ.get("GROWTH_THRESHOLD", "0.7")),
    "growth_size": int(os.environ.get("GROWTH_SIZE", "50")),
    "auto_growth": os.environ.get("AUTO_GROWTH", "true").lower() == "true",
    "backup_file": os.environ.get("BACKUP_FILE", "canvas_backup.json"),
    "palette": [
        "#E6194B", "#3CB44B", "#FFE119", "#4363D8", "#F58231", "#911EB4",
        "#42D4F4", "#F032E6", "#BFEF45", "#FABED4", "#469990", "#DCBEFF",
        "#9A6324", "#FFFAC8", "#800000", "#AAFFC3", "#808000", "#FFD8B1",
        "#000075", "#A9A9A9", "#FF6F61", "#00CED1", "#FF4500", "#7B68EE",
        "#00FA9A", "#FF69B4", "#20B2AA", "#DDA0DD", "#87CEEB", "#98FB98",
        "#FFD700", "#FF6347",
    ],
}

# ── 上帝之手密码 ──────────────────────────
_GOD_PASSWORD_ENV = "GOD_PASSWORD"
GOD_PASSWORD = os.environ.get(_GOD_PASSWORD_ENV, "")

if not GOD_PASSWORD:
    # 自动生成：检查.env文件
    _env_path = os.path.join(os.path.dirname(__file__), ".env")
    try:
        with open(_env_path) as f:
            for line in f:
                if line.startswith("GOD_PASSWORD="):
                    GOD_PASSWORD = line.strip().split("=", 1)[1]
                    break
    except FileNotFoundError:
        pass
    
    if not GOD_PASSWORD:
        # 生成新密码
        import secrets
        GOD_PASSWORD = secrets.token_hex(16)  # 32字符, 128位熵
        try:
            with open(_env_path, "a") as f:
                f.write(f"\n# 上帝之手密码 (自动生成)\nGOD_PASSWORD={GOD_PASSWORD}\n")
            print(f"🔑  上帝之手密码已写入 {_env_path}")
        except OSError:
            pass  # .env 不可写, 密码仅本次有效
        print(f"🔑  GOD_PASSWORD={GOD_PASSWORD}")
        print(f"🔑  保存此密码以访问管理面板 /admin")
else:
    print(f"🔑  上帝之手已启用 (GOD_PASSWORD 来自环境变量)")

# ── 画布状态 ──────────────────────────────
canvas = {
    "width": CONFIG["width"],
    "height": CONFIG["height"],
    "pixels": None,
    "total_signals": 0,
    "non_blank_pixels": 0,
    "growth_count": 0,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "is_frozen": False,
    "god_interventions": 0,
    "growth_log": [],
    "ip_cooldowns": {},  # IP -> last signal timestamp
}


def init_canvas():
    """初始化画布（空白）"""
    canvas["pixels"] = [
        ["#FFFFFF" for _ in range(canvas["width"])]
        for _ in range(canvas["height"])
    ]
    canvas["non_blank_pixels"] = 0


def resize_canvas(new_w, new_h):
    """扩展画布尺寸，新增区域为空白"""
    old_h = len(canvas["pixels"])
    old_w = len(canvas["pixels"][0]) if old_h > 0 else 0

    # Expand rows
    for _ in range(new_h - old_h):
        canvas["pixels"].append(["#FFFFFF" for _ in range(max(old_w, new_w))])

    # Expand columns in existing rows
    for y in range(len(canvas["pixels"])):
        while len(canvas["pixels"][y]) < new_w:
            canvas["pixels"][y].append("#FFFFFF")

    # Update dimensions
    canvas["width"] = new_w
    canvas["height"] = new_h

    # Recalculate non-blank count
    count = 0
    for row in canvas["pixels"]:
        for px in row:
            if px != "#FFFFFF":
                count += 1
    canvas["non_blank_pixels"] = count


def check_growth():
    """检查并触发画布成长"""
    if not CONFIG["auto_growth"] or canvas["is_frozen"]:
        return False

    total = canvas["width"] * canvas["height"]
    if total == 0:
        return False

    ratio = canvas["non_blank_pixels"] / total
    if ratio >= CONFIG["growth_threshold"]:
        new_w = canvas["width"] + CONFIG["growth_size"]
        new_h = canvas["height"] + CONFIG["growth_size"]
        resize_canvas(new_w, new_h)
        canvas["growth_count"] += 1
        canvas["growth_log"].append({
            "time": datetime.now(timezone.utc).isoformat(),
            "from_size": f"{canvas['width'] - CONFIG['growth_size']}x{canvas['height'] - CONFIG['growth_size']}",
            "to_size": f"{canvas['width']}x{canvas['height']}",
            "ratio": round(ratio, 4),
        })
        save_backup()
        return True
    return False


def save_backup():
    """保存画布到JSON文件"""
    try:
        data = {
            "width": canvas["width"],
            "height": canvas["height"],
            "pixels": canvas["pixels"],
            "total_signals": canvas["total_signals"],
            "ip_cooldowns": canvas["ip_cooldowns"],
            "non_blank_pixels": canvas["non_blank_pixels"],
            "growth_count": canvas["growth_count"],
            "created_at": canvas["created_at"],
            "is_frozen": canvas["is_frozen"],
            "god_interventions": canvas["god_interventions"],
            "growth_log": canvas["growth_log"],
        }
        with open(CONFIG["backup_file"], "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"[BACKUP ERROR] {e}")


def load_backup():
    """从JSON文件恢复画布"""
    try:
        if os.path.exists(CONFIG["backup_file"]):
            with open(CONFIG["backup_file"], "r") as f:
                data = json.load(f)
            canvas["width"] = data["width"]
            canvas["height"] = data["height"]
            canvas["pixels"] = data["pixels"]
            canvas["total_signals"] = data["total_signals"]
            if "ip_cooldowns" in data:
                canvas["ip_cooldowns"] = data["ip_cooldowns"]
            canvas["non_blank_pixels"] = data["non_blank_pixels"]
            canvas["growth_count"] = data["growth_count"]
            canvas["created_at"] = data["created_at"]
            canvas["is_frozen"] = data.get("is_frozen", False)
            canvas["god_interventions"] = data.get("god_interventions", 0)
            canvas["growth_log"] = data.get("growth_log", [])
            return True
    except Exception as e:
        print(f"[LOAD ERROR] {e}")
    return False


def require_god(f):
    """装饰器：检查上帝权限"""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("X-God-Key", "")
        if auth_header == GOD_PASSWORD:
            return f(*args, **kwargs)
        return jsonify({"error": "unauthorized"}), 403

    return decorated


# ── 启动 ──────────────────────────────────
if not load_backup():
    init_canvas()
    save_backup()


# ── 路由：染坊信号 ───────────────────────

def get_client_ip():
    """Get real client IP (supports Cloudflare CDN)"""
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"

@app.route("/signal", methods=["POST"])
def receive_signal():
    """接收染坊心跳信号，生成一个随机像素"""
    if canvas["is_frozen"]:
        return jsonify({"status": "frozen", "message": "画布已冻结"}), 423

    # IP 24h cooldown (anti-DDoS)
    client_ip = get_client_ip()
    now = time.time()
    last_time = canvas["ip_cooldowns"].get(client_ip, 0)
    if now - last_time < 86400:
        remaining = int(86400 - (now - last_time))
        h = remaining // 3600
        m = (remaining % 3600) // 60
        return jsonify({
            "status": "cooldown",
            "message": f"每IP每24h一次，还剩{h}h{m}m",
            "next_available": int(last_time + 86400),
            "remaining_seconds": remaining,
        }), 429
    canvas["ip_cooldowns"][client_ip] = now
    # Clean stale entries (>48h)
    cutoff = now - 172800
    stale = [ip for ip, ts in canvas["ip_cooldowns"].items() if ts < cutoff]
    for ip in stale:
        del canvas["ip_cooldowns"][ip]

    canvas["total_signals"] += 1

    # 颜色倾向（可选）
    color_preference = request.json.get("color") if request.is_json else None

    # 随机位置
    x = random.randint(0, canvas["width"] - 1)
    y = random.randint(0, canvas["height"] - 1)

    # 确定颜色
    if color_preference and color_preference in CONFIG["palette"]:
        color = color_preference
    else:
        color = random.choice(CONFIG["palette"])

    # 如果该位置原本是空白，增加非空白计数
    if canvas["pixels"][y][x] == "#FFFFFF":
        canvas["non_blank_pixels"] += 1

    canvas["pixels"][y][x] = color

    # 检查成长
    grew = check_growth()

    # 每10次信号备份一次
    if canvas["total_signals"] % 10 == 0:
        save_backup()

    return jsonify({
        "status": "ok",
        "x": x,
        "y": y,
        "color": color,
        "total_signals": canvas["total_signals"],
        "grew": grew,
        "canvas_size": f"{canvas['width']}x{canvas['height']}",
    })


# ── 路由：获取画布数据 ───────────────────
@app.route("/canvas", methods=["GET"])
def get_canvas():
    """返回当前画布数据"""
    total = canvas["width"] * canvas["height"]
    ratio = round(canvas["non_blank_pixels"] / total, 4) if total > 0 else 0
    return jsonify({
        "width": canvas["width"],
        "height": canvas["height"],
        "pixels": canvas["pixels"],
        "total_signals": canvas["total_signals"],
        "non_blank_pixels": canvas["non_blank_pixels"],
        "fill_ratio": ratio,
        "growth_count": canvas["growth_count"],
        "is_frozen": canvas["is_frozen"],
        "god_interventions": canvas["god_interventions"],
        "created_at": canvas["created_at"],
        "growth_log": canvas["growth_log"][-20:],
    })


# ── 路由：统计 ────────────────────────────
@app.route("/stats", methods=["GET"])
def get_stats():
    """返回统计信息"""
    total = canvas["width"] * canvas["height"]
    ratio = round(canvas["non_blank_pixels"] / total, 4) if total > 0 else 0
    uptime = datetime.now(timezone.utc) - datetime.fromisoformat(canvas["created_at"])
    return jsonify({
        "canvas_size": f"{canvas['width']}x{canvas['height']}",
        "total_signals": canvas["total_signals"],
        "non_blank_pixels": canvas["non_blank_pixels"],
        "blank_pixels": total - canvas["non_blank_pixels"],
        "fill_ratio": ratio,
        "growth_count": canvas["growth_count"],
        "growth_threshold": CONFIG["growth_threshold"],
        "is_frozen": canvas["is_frozen"],
        "god_interventions": canvas["god_interventions"],
        "uptime_seconds": int(uptime.total_seconds()),
        "created_at": canvas["created_at"],
    })


# ── 路由：查看页面 ───────────────────────
@app.route("/view")
def view_canvas():
    """画布展示页面"""
    return render_template("view.html",
                           pixel_size=CONFIG["pixel_size"],
                           refresh_interval=2)


# ── 路由：上帝面板 ───────────────────────
@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    """上帝之手管理面板（需设置GOD_PASSWORD环境变量）"""
    if not GOD_PASSWORD:
        return "<h1>上帝之手未启用</h1><p>设置 GOD_PASSWORD 环境变量以启用。</p>", 403
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if pwd == GOD_PASSWORD:
            session["god_mode"] = True
        else:
            return render_template("admin.html", error="密码错误"), 403

    if not session.get("god_mode"):
        return render_template("admin.html", need_login=True)

    return render_template("admin.html",
                           need_login=False,
                           config=CONFIG,
                           canvas=canvas,
                           GOD_PASSWORD=GOD_PASSWORD)


# ── 上帝API ───────────────────────────────
@app.route("/api/reset", methods=["POST"])
@require_god
def api_reset():
    """重置画布"""
    init_canvas()
    canvas["total_signals"] = 0
    canvas["growth_count"] = 0
    canvas["growth_log"] = []
    canvas["god_interventions"] += 1
    save_backup()
    return jsonify({"status": "ok", "message": "画布已重置"})


@app.route("/api/freeze", methods=["POST"])
@require_god
def api_freeze():
    """冻结/解冻画布"""
    canvas["is_frozen"] = not canvas["is_frozen"]
    canvas["god_interventions"] += 1
    save_backup()
    return jsonify({
        "status": "ok",
        "is_frozen": canvas["is_frozen"],
        "message": "画布已冻结" if canvas["is_frozen"] else "画布已恢复",
    })


@app.route("/api/splash", methods=["POST"])
@require_god
def api_splash():
    """随机泼色"""
    if canvas["is_frozen"]:
        return jsonify({"error": "画布已冻结，无法泼色"}), 423

    count = request.json.get("count", 100) if request.is_json else 100
    count = min(count, 1000)

    splashed = 0
    for _ in range(count):
        x = random.randint(0, canvas["width"] - 1)
        y = random.randint(0, canvas["height"] - 1)
        if canvas["pixels"][y][x] == "#FFFFFF":
            canvas["non_blank_pixels"] += 1
        canvas["pixels"][y][x] = random.choice(CONFIG["palette"])
        splashed += 1

    canvas["god_interventions"] += 1
    check_growth()
    save_backup()

    return jsonify({"status": "ok", "splashed": splashed})


@app.route("/api/config", methods=["POST"])
@require_god
def api_config():
    """修改配置"""
    data = request.json if request.is_json else {}
    if "growth_threshold" in data:
        val = float(data["growth_threshold"])
        if 0.1 <= val <= 1.0:
            CONFIG["growth_threshold"] = val
    if "growth_size" in data:
        val = int(data["growth_size"])
        if 10 <= val <= 500:
            CONFIG["growth_size"] = val
    if "pixel_size" in data:
        val = int(data["pixel_size"])
        if 1 <= val <= 20:
            CONFIG["pixel_size"] = val
    if "auto_growth" in data:
        CONFIG["auto_growth"] = bool(data["auto_growth"])
    return jsonify({"status": "ok", "config": {
        "growth_threshold": CONFIG["growth_threshold"],
        "growth_size": CONFIG["growth_size"],
        "pixel_size": CONFIG["pixel_size"],
        "auto_growth": CONFIG["auto_growth"],
    }})


# ── 退出时备份 ────────────────────────────
atexit.register(save_backup)


# ── 优雅关闭 ──────────────────────────────
def shutdown_handler(signum, frame):
    save_backup()
    print("\n画布服务器关闭，数据已保存。")
    exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == "__main__":
    # ── 启动画布服务器 ──
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"🖼️  巴别塔实验 · 画布服务器启动")
    print(f"   尺寸: {canvas['width']}x{canvas['height']}")
    print(f"   信号数: {canvas['total_signals']}")
    print(f"   成长次数: {canvas['growth_count']}")
    print(f"   冻结: {'是' if canvas['is_frozen'] else '否'}")
    print(f"   端口: {port}")
    print(f"   查看: http://localhost:{port}/view")
    print(f"   管理: http://localhost:{port}/admin")
    app.run(host="0.0.0.0", port=port, debug=debug)
