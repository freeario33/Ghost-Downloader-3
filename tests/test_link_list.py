"""parseLinkList 的逐分支测试——拖入 .txt 链接清单时使用。

Seam: app.platform.filesystem.parseLinkList。
"""
from __future__ import annotations

from app.platform.filesystem import LinkListEntry, parseLinkList, toSafeSubfolder


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

    def test_parses_key_and_folder(self):
        entries = parseLinkList("影片,https://example.com/a.m3u8,secret,S01")
        assert entries == [LinkListEntry("影片", "https://example.com/a.m3u8", "secret", "S01")]

    def test_parses_empty_key_with_folder(self):
        entries = parseLinkList("影片,https://example.com/a.mp4,,2024")
        assert entries == [LinkListEntry("影片", "https://example.com/a.mp4", "", "2024")]

    def test_parses_key_with_empty_folder(self):
        entries = parseLinkList("影片,https://example.com/a.m3u8,secret,")
        assert entries == [LinkListEntry("影片", "https://example.com/a.m3u8", "secret", "")]

    def test_empty_key_and_folder_equals_two_segments(self):
        entries = parseLinkList("影片,https://example.com/a.mp4,,")
        assert entries == [LinkListEntry("影片", "https://example.com/a.mp4")]

    def test_three_segments_third_is_key_not_folder(self):
        entries = parseLinkList("影片,https://example.com/a.mp4,电影")
        assert entries == [LinkListEntry("影片", "https://example.com/a.mp4", "电影", "")]

    def test_skips_five_segments(self):
        entries = parseLinkList("影片,https://example.com/a.mp4,k,f,extra")
        assert entries == []

    def test_skips_invalid_url(self):
        entries = parseLinkList("影片,not-a-url")
        assert entries == []

    def test_comma_in_url_is_dropped_with_warning(self):
        entries = parseLinkList("影片,https://example.com/a.mp4?x=1,y=2,key,dir")
        assert entries == []

    def test_encoded_comma_in_url_is_kept(self):
        entries = parseLinkList("影片,https://example.com/a.mp4?x=1%2Cy=2")
        assert entries == [LinkListEntry("影片", "https://example.com/a.mp4?x=1%2Cy=2")]


class TestToSafeSubfolder:

    def test_strips_parent_segments(self):
        assert toSafeSubfolder("../../etc") == "etc"

    def test_drops_absolute_prefix(self):
        assert toSafeSubfolder("/abs/path") == "abs/path"

    def test_collapses_inner_parent_segments(self):
        assert toSafeSubfolder("a/../../b") == "a/b"

    def test_strips_drive_letter(self):
        assert toSafeSubfolder("C:\\x") == "C_/x"

    def test_pure_parent_is_empty(self):
        assert toSafeSubfolder("..") == ""

    def test_normal_subfolder_unchanged(self):
        assert toSafeSubfolder("normal/sub") == "normal/sub"

    def test_empty_is_empty(self):
        assert toSafeSubfolder("") == ""

    def test_collapses_duplicate_separators(self):
        assert toSafeSubfolder("a//b") == "a/b"
