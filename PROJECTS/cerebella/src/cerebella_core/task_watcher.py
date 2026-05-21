"""
🧬 Cerebella Core — 任务书文件监控器
======================================
核心功能：
1. 监控任务发布区的新 .task 文件
2. 解析 YAML 头部元数据
3. 通过 API路由中心 匹配最合适的"脑"
4. 驱动状态机：pending → in_progress → completed → verified
5. 完成归档到看过的/

哲学：聊天是沟通，文件是契约。AI 只认任务书。
"""

import os
import sys
import time
import json
import yaml
import re
import logging
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ======== 配置 ========
TASKS_DIR = os.path.expanduser("~/Cerebella/tasks")
ARCHIVE_DIR = os.path.join(TASKS_DIR, "看过的")
ROUTER_URL = "http://127.0.0.1:18081"
POLL_INTERVAL = 5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Cerebella] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("cerebella")

def cli(msg):
    """输出到stdout（后台可见）"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{ts} [Cerebella] {msg}", flush=True)


# ======== .task 文件解析 ========
YAML_DELIMITER = re.compile(r"^---\s*$", re.MULTILINE)

def parse_task_file(path):
    """解析 .task 文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        cli(f"  ERROR 读取失败 {path}: {e}")
        return None

    parts = YAML_DELIMITER.split(content, 2)
    if len(parts) < 3:
        cli(f"  WARN 格式错误: {path} — 需要 YAML 头")
        return None

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except Exception as e:
        cli(f"  WARN YAML解析失败 {path}: {e}")
        meta = {}

    return {"meta": meta, "body": parts[2].strip()}


def write_task_file(path, meta, body):
    """写回 .task 文件"""
    meta["updated_at"] = datetime.now().isoformat(timespec="seconds")
    content = f"---\n{yaml.dump(meta, allow_unicode=True, sort_keys=False).strip()}\n---\n\n{body}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ======== 路由中心交互 ========
import urllib.request

def route_task(capability):
    """通过API路由中心匹配AI"""
    url = f"{ROUTER_URL}/api/route?capability={capability}"
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        if data.get("selected"):
            return data["selected"]
        cli(f"  WARN 路由未匹配: {data.get('decision')} — {data.get('message')}")
        return None
    except Exception as e:
        cli(f"  ERROR 路由请求失败: {e}")
        return None


# ======== 执行任务 ========
def execute_task(task_path, task_data):
    """执行一个任务"""
    meta = task_data["meta"]
    body = task_data["body"]
    task_id = meta.get("task_id", Path(task_path).stem)
    capability = meta.get("capability", "chat")
    title = meta.get("title", task_id)

    cli(f"▶️  [{task_id}] {title}")
    cli(f"   所需能力: {capability}")

    # Step 1: 路由
    brain = route_task(capability)
    if not brain:
        meta["status"] = "failed"
        meta["fail_reason"] = "无可用AI匹配该能力"
        write_task_file(task_path, meta, body)
        cli(f"  ❌ [{task_id}] 无可用脑")
        return

    cli(f"  🧠 分配: {brain['name']} ({brain['model_name']})")

    # Step 2: 标记进行中
    meta["status"] = "in_progress"
    meta["assigned_to"] = brain["name"]
    meta["assigned_model"] = brain["model_name"]
    write_task_file(task_path, meta, body)
    cli(f"  🔄 [{task_id}] → in_progress")

    # Step 3: 执行（后续可接入 Hermes Agent 实际调用）
    # 目前先完成标记
    meta["status"] = "completed"
    meta["completed_at"] = datetime.now().isoformat(timespec="seconds")
    write_task_file(task_path, meta, body)
    cli(f"  ✅ [{task_id}] → completed")

    # Step 4: 归档
    archive_task(task_path, meta, body)


def archive_task(task_path, meta, body):
    """归档到看过的/"""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    meta["status"] = "verified"
    meta["updated_at"] = datetime.now().isoformat(timespec="seconds")

    archive_name = f"已看_{Path(task_path).name}"
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)
    write_task_file(archive_path, meta, body)

    try:
        os.remove(task_path)
        cli(f"  📦 [{meta.get('task_id', '?')}] 已归档")
    except Exception as e:
        cli(f"  ⚠️  归档失败: {e}")


# ======== 文件监控器 ========
class TaskHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".task"):
            cli(f"📥 新任务书: {Path(event.src_path).name}")
            process_task(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".task"):
            process_task(event.src_path)


def process_task(path):
    """处理单个任务书"""
    data = parse_task_file(path)
    if not data:
        return
    if data["meta"].get("status") != "pending":
        return
    execute_task(path, data)


def scan_existing():
    """启动时扫描已有待办"""
    tasks_dir = Path(TASKS_DIR)
    if not tasks_dir.exists():
        tasks_dir.mkdir(parents=True, exist_ok=True)
        return
    for f in sorted(tasks_dir.glob("*.task")):
        cli(f"📋 发现待处理: {f.name}")
        process_task(str(f))


# ======== 主入口 ========
def main():
    cli("🧬 Cerebella Core — 任务书监控器启动")
    cli(f"   监控目录: {TASKS_DIR}")
    cli(f"   路由中心: {ROUTER_URL}")
    cli(f"   归档目录: {ARCHIVE_DIR}")

    os.makedirs(TASKS_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    scan_existing()

    handler = TaskHandler()
    observer = Observer()
    observer.schedule(handler, TASKS_DIR, recursive=False)
    observer.start()
    cli("👀 监控中... 放入 .task 文件即可触发")

    try:
        while True:
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
        cli("🛑 Cerebella Core 已停止")
    observer.join()


if __name__ == "__main__":
    main()
