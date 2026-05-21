"""
巴别塔实验 · 染色画布 — 染坊客户端
Babel Experiment · Dye Workshop — Workshop Client

安装依赖：pip install requests
使用方法：python workshop.py [--config workshop_config.json]
"""

import json
import time
import random
import argparse
import logging
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("请先安装 requests：pip install requests")
    sys.exit(1)


def load_config(path="workshop_config.json"):
    """加载染坊配置文件"""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("配置文件 %s 不存在，使用默认配置", path)
        return {
            "canvas_server_url": "http://localhost:5000",
            "interval_minutes": 60,
            "color_preference": None,
        }
    except json.JSONDecodeError:
        logging.error("配置文件 %s 格式错误", path)
        sys.exit(1)


def setup_logging():
    """配置日志输出"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def send_signal(url, color=None, timeout=10):
    """向画布服务器发送心跳信号"""
    payload = {}
    if color:
        payload["color"] = color

    try:
        resp = requests.post(
            f"{url.rstrip('/')}/signal",
            json=payload,
            timeout=timeout,
        )
        if resp.status_code == 200:
            data = resp.json()
            logging.info(
                "✅ 信号发送成功 | 像素位置: (%d, %d) | 颜色: %s | 总信号: %d | 画布: %s",
                data.get("x", -1),
                data.get("y", -1),
                data.get("color", "?"),
                data.get("total_signals", 0),
                data.get("canvas_size", "?"),
            )
            if data.get("grew"):
                logging.info("🌟 画布刚刚成长了！")
            return True
        elif resp.status_code == 423:
            logging.warning("⏸ 画布已冻结，信号被拒绝")
            return False
        else:
            logging.warning("⚠️ 服务器返回非预期状态码: %d %s", resp.status_code, resp.text[:100])
            return False
    except requests.ConnectionError:
        logging.error("❌ 连接失败: %s (检查服务器地址和网络)", url)
        return False
    except requests.Timeout:
        logging.error("❌ 请求超时 (%ds)", timeout)
        return False
    except Exception as e:
        logging.error("❌ 发送失败: %s", e)
        return False


def main():
    parser = argparse.ArgumentParser(description="巴别塔实验 · 染坊客户端")
    parser.add_argument("--config", default="workshop_config.json",
                        help="配置文件路径 (默认: workshop_config.json)")
    parser.add_argument("--url", help="画布服务器地址 (覆盖配置文件)")
    parser.add_argument("--interval", type=int,
                        help="发送间隔（分钟）(覆盖配置文件)")
    parser.add_argument("--color", help="颜色倾向 (HEX，如 #FF0000)")
    parser.add_argument("--once", action="store_true",
                        help="仅发送一次信号后退出")
    args = parser.parse_args()

    setup_logging()

    config = load_config(args.config)

    # 命令行参数覆盖配置文件
    url = args.url or config.get("canvas_server_url", "http://localhost:5000")
    interval = args.interval if args.interval is not None else config.get("interval_minutes", 60)
    color = args.color or config.get("color_preference")

    if color and not color.startswith("#"):
        color = "#" + color

    logging.info("=" * 50)
    logging.info("🌐 巴别塔实验 · 染坊客户端启动")
    logging.info("   画布服务器: %s", url)
    logging.info("   发送间隔: %d 分钟", interval)
    logging.info("   颜色倾向: %s", color or "随机")
    logging.info("=" * 50)

    if args.once:
        logging.info("单次发送模式")
        send_signal(url, color)
        return

    cycle_count = 0
    while True:
        cycle_count += 1
        logging.info("--- 第 %d 次心跳 ---", cycle_count)
        success = send_signal(url, color)

        if success:
            # 睡眠到下一个间隔
            logging.info("等待 %d 分钟...", interval)
            time.sleep(interval * 60)
        else:
            # 失败后等待较短时间重试
            retry_wait = min(5, interval)
            logging.info("%d 秒后重试...", retry_wait * 60)
            time.sleep(retry_wait * 60)


if __name__ == "__main__":
    main()
