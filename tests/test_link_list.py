"""parseLinkList 的逐分支测试——拖入 .txt 链接清单时使用。

Seam: app.platform.filesystem.parseLinkList。
"""
from __future__ import annotations

from app.platform.filesystem import LinkListEntry, parseLinkList


class TestParseLinkList:

    def test_parses_name_and_url(self):
        entries = parseLinkList("影片一,https://example.com/a.mp4")
        assert entries == [LinkListEntry("影片一", "https://example.com/a.mp4")]

    def test_parses_name_url_and_key(self):
        entries = parseLinkList("影片,https://example.com/a.m3u8,secret")
        assert entries == [LinkListEntry("影片", "https://example.com/a.m3u8", "secret")]

    def test_skips_lines_without_comma_url(self):
        entries = parseLinkList("https://example.com/a.mp4\njust text\n")
        assert entries == []

    def test_skips_blank_lines(self):
        entries = parseLinkList("\n\n影片,https://example.com/a.mp4\n\n")
        assert len(entries) == 1

    def test_parses_multiple_lines(self):
        text = "一,https://example.com/1\n二,https://example.com/2\n"
        entries = parseLinkList(text)
        assert [e.name for e in entries] == ["一", "二"]
        assert [e.url for e in entries] == ["https://example.com/1", "https://example.com/2"]

    def test_strips_whitespace_around_name(self):
        entries = parseLinkList("  影片 ,https://example.com/a.mp4")
        assert entries == [LinkListEntry("影片", "https://example.com/a.mp4")]
