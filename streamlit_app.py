import json

import httpx
import streamlit as st

from components.version import select_versions
from models import KnownGoodVersions
from utils import get_version_object

st.title("Chrome 便携版")


@st.cache_data(ttl=600)
def fetch_known_good_versions():
    url = "https://raw.githubusercontent.com/GoogleChromeLabs/chrome-for-testing/main/data/known-good-versions.json"
    response = httpx.get(url)
    response.raise_for_status()
    return KnownGoodVersions.model_validate_json(response.text)


@st.cache_data(ttl=600)
def fetch_chromium_history_version() -> dict[str, str]:
    url = "https://raw.githubusercontent.com/vikyd/chromium-history-version-position/master/json/ver-pos-os/version-position-Win_x64.json"
    response = httpx.get(url)
    response.raise_for_status()
    return json.loads(response.text)


tabs_chromium_history_version, tabs_chrome_for_testing = st.tabs(
    [
        "Chromium History Versions Download (Chrome 52 ~ 121)",
        "Chrome for Testing (Chrome 113 +)",
    ]
)

with tabs_chromium_history_version:
    st.markdown("https://vikyd.github.io/download-chromium-history-version/")
    selected_version = select_versions(
        label_major="选择 Chrome 主版本",
        label_version="选择 Chrome 版本",
        versions=fetch_chromium_history_version(),
    )
    if selected_version:
        position = fetch_chromium_history_version()[selected_version]
        version_object = get_version_object(selected_version)
        assert version_object, f"Bad version {selected_version}"
        milestone = version_object.milestone
        st.markdown(
            f"""
### 获取启动器
下载 [Google Chrome Portable](https://portableapps.com/apps/internet/google_chrome_portable)
或者 [GoogleChromePortableLauncher](https://sourceforge.net/projects/portableapps/files/Source/Google%20Chrome/Launcher/), 用 7-Zip 打开

`GoogleChromePortable.exe` 就是我们需要的启动器。

### 获取Chrome主程序
下载离线安装包 [mini_installer.exe](https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2F{position}%2Fmini_installer.exe?alt=media)

离线安装包下载好后, 不要运行, 我们同样用7-Zip打开这个压缩包, 会发现里面有一个chrome.7z文件, 我们把他提取出来。


### 制作便携版
1. 新建一个文件夹，用来存放便携版，比如 `{milestone}` 文件夹。
2. 复制 `GoogleChromePortable.exe` 到这个文件夹，可以改名成自己想要的名称，比如 `Chrome{milestone}.exe`。
3. 新建 `App` 文件夹，把 `chrome.7z` 解压到这个目录内，注意只要 `Chrome-bin` 文件夹，完成后的目录结构应该是 `{milestone}/App/Chrome-bin` 。
4. 双击 `GoogleChromePortable.exe (Chrome{milestone}.exe)` 就能启动这个Chrome了。
"""
        )

with tabs_chrome_for_testing:
    st.markdown("https://developer.chrome.com/blog/chrome-for-testing")
    version_options: list[str] = [i.version for i in fetch_known_good_versions().versions]
    selected_version = selected_version = select_versions(
        label_major="选择 Chrome 主版本",
        label_version="选择 Chrome 版本",
        versions=version_options,
    )
    if selected_version:
        st.markdown(f"""
```
npx @puppeteer/browsers install chrome@{selected_version}
```""")
