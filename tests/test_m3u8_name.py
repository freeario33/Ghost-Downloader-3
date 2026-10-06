"""m3u8 任务名解析优先级测试。

Seam: features.m3u8_pack.pack.resolveName — 用户显式标题优先于服务器提示。
"""
from app.models.task import PageTaskOptions, ResourceTaskOptions, TaskOptions
from features.m3u8_pack.pack import resolveName

URL = "https://cdn.example.com/path/a.m3u8"


class TestResolveName:

    def test_resource_name_wins(self):
        options = ResourceTaskOptions(url=URL, name="我的剧集")
        assert resolveName(options, {}, URL, "mp4") == "我的剧集.mp4"

    def test_resource_name_beats_content_disposition(self):
        options = ResourceTaskOptions(url=URL, name="用户标题")
        headers = {"content-disposition": 'attachment; filename="server.mp4"'}
        assert resolveName(options, headers, URL, "mp4") == "用户标题.mp4"

    def test_page_title_still_wins(self):
        options = PageTaskOptions(url=URL, pageTitle="页面标题")
        assert resolveName(options, {}, URL, "mp4") == "页面标题.mp4"

    def test_falls_back_to_url_path_when_no_name(self):
        options = ResourceTaskOptions(url=URL)
        assert resolveName(options, {}, URL, "mp4") == "a.mp4"

    def test_falls_back_to_content_disposition(self):
        options = ResourceTaskOptions(url=URL)
        headers = {"content-disposition": 'attachment; filename="server.mp4"'}
        assert resolveName(options, headers, URL, "mp4") == "server.mp4"

    def test_plain_options_fall_back_to_url_path(self):
        assert resolveName(TaskOptions(url=URL), {}, URL, "mp4") == "a.mp4"

    def test_stream_fallback_when_nothing_available(self):
        assert resolveName(TaskOptions(url="https://x.com/"), {}, "https://x.com/", "mp4") == "stream.mp4"
