"""
ReportNotepadPage - NotepadPage plus the extra methods the mini project needs.

We EXTEND the existing page object (inheritance) instead of editing it, so the shared
framework file stays untouched and all its safety rules are inherited:
  * works only on a file the test created itself (open_file)
  * closes only its own tab with Ctrl+W (close_tab) - never the whole Notepad window
"""
from pages.notepad_page import NotepadPage


class ReportNotepadPage(NotepadPage):
    def write_lines(self, lines):
        """Type several lines (joined with newlines). type_text() waits until the text is visible."""
        text = "\n".join(lines)
        self.log.info("Writing %d report lines", len(lines))
        self.type_text(text)
        return text

    def append_line(self, line):
        """Add one line at the end of the current content."""
        prefix = "\n" if self.text else ""
        self.type_text(prefix + line)

    def saved_text_normalised(self):
        """File content from DISK with a possible BOM removed and line endings normalised to '\\n'."""
        raw = self.file_path.read_text(encoding="utf-8-sig")
        return raw.replace("\r\n", "\n").replace("\r", "\n")
