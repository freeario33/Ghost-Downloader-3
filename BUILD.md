# Ghost-Downloader-3 源码运行与分支管理说明

本文档记录本仓库在本机（Kali GNU/Linux Rolling）上的**源码运行**方式、依赖安装步骤、代理开关方法，以及本地双分支的同步操作。

> 本项目按需求**不做 Nuitka 编译**，直接以源码方式运行。

---

## 一、仓库与分支

| 项目 | 值 |
|---|---|
| 仓库 | https://github.com/XiaoYouChR/Ghost-Downloader-3 |
| remote | 仅 `upstream`（指向上述官方仓库），**无 fork** |
| 本地分支 | `main`（跟踪上游，只拉更新）、`dev`（二次开发） |
| 当前工作分支 | `dev` |

### 分支职责

- **`main`**：跟踪 `upstream/main`，**不在此分支开发**。仅用于拉取官方更新。
- **`dev`**：所有自己的修改都提交在这里。需要同步上游时，把 `main` 合并进来。

### 日常分支操作

```bash
# 1) 拉取官方更新（不改动本地开发成果）
git checkout main
git pull upstream main

# 2) 把官方更新同步进开发分支
git checkout dev
git merge main          # 或用 git rebase main

# 3) 日常开发（在 dev 上）
git add -A
git commit -m "描述本次改动"
```

---

## 二、环境要求

实测环境：

| 组件 | 版本 |
|---|---|
| 系统 | Kali GNU/Linux Rolling 2026.2（glibc ≥ 2.35 满足） |
| Python | 3.13.12（项目要求 `>=3.13`） |
| pip | 26.2.1（venv 内） |
| Qt | PySide6 6.10.3（随依赖安装） |

---

## 三、一次性依赖安装

项目用 `uv` 管理依赖（`pyproject.toml` / `uv.lock`），但本机环境改用**标准 venv + pip** 安装依赖，效果等价。

```bash
cd /home/kali/deepseekharnes/Ghost-Downloader-3

# 1) 创建虚拟环境（Python 3.13）
python3 -m venv .venv
.venv/bin/pip install --upgrade pip

# 2) 安装运行依赖（对应 pyproject.toml 的 [project].dependencies）
.venv/bin/pip install \
  "aioftp[socks]>=0.27.2" "desktop-notifier>=6.2.0" "libtorrent>=2.0.13" \
  "loguru>=0.7.3" "m3u8>=6.0.0" "mpegdash>=0.4.1" "nuitka>=4.2" \
  "pyside6~=6.10.3" "pyside6-fluent-widgets>=1.11.2" "qrcode[png]>=8.2" \
  "websockets>=14" "wreq>=0.12.0" "uvloop>=0.22.1"
```

实测已装成的关键版本：`PySide6 6.10.3`、`libtorrent 2.1.1`、`wreq 0.12.3`、`pyside6-fluent-widgets 1.11.3`、`uvloop 0.23.0`。

> 说明：**不要**执行 `pip install -e .`。项目是 flat-layout 多包结构（`app` / `features` / `browser_extension`），setuptools 自动发现会拒绝，且本项目本来就不需要把自身安装为包。只装依赖即可。

### 若以后能用 uv（可选）

```bash
uv sync          # 会按 uv.lock 精确还原依赖
```

---

## 四、源码运行

```bash
cd /home/kali/deepseekharnes/Ghost-Downloader-3
.venv/bin/python Ghost-Downloader-3.py
```

入口文件：`Ghost-Downloader-3.py`。

### 无图形环境时的冒烟测试

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/python Ghost-Downloader-3.py
```

---

## 五、代理（按需使用）

**默认直连，不设全局代理。** 仅当网络不通时才针对单条命令挂代理 `192.168.133.1:10808`。

```bash
# 单条命令临时挂代理
export https_proxy=http://192.168.133.1:10808
export http_proxy=http://192.168.133.1:10808

# 用完取消
unset https_proxy http_proxy
```

### git 代理（可选，仅在本仓库生效）

```bash
# 开启
git config --local http.proxy http://192.168.133.1:10808
git config --local https.proxy http://192.168.133.1:10808

# 关闭
git config --local --unset http.proxy
git config --local --unset https.proxy
```

### pip 代理（单次）

```bash
.venv/bin/pip install --proxy http://192.168.133.1:10808 <包名>
```

---

## 六、已知环境限制

- 程序启动时会向 `~/.local/share/GhostDownloader/` 写日志与配置。在受限沙箱中该路径不可写，会以 `OSError: [Errno 30] Read-only file system` 中止。这是**沙箱限制**，不是程序缺陷；在正常桌面环境下可写，程序可正常启动。
- Qt 6.6+ 不再支持缺少 AVX 指令集的 CPU。
- Kali 为滚动发行版，Qt/glibc 版本较新，实测与项目要求（glibc ≥ 2.35）兼容。
