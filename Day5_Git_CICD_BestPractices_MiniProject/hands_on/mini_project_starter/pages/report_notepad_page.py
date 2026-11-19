"""
STARTER - ReportNotepadPage: NotepadPage plus the methods the mini project needs.

We EXTEND the existing page object instead of editing the shared framework file.
Available from NotepadPage (do not re-implement):
    open_file(path)  type_text(text)  text  save()  saved_content()  close_tab()  is_modified()
    self.file_path   self.log
Safety rules you inherit: work only on your own temp file, close only your own tab (Ctrl+W),
never close the whole Notepad window.
"""
from pages.notepad_page import NotepadPage


class ReportNotepadPage(NotepadPage):
    def write_lines(self, lines):
        """Type several lines joined with '\\n' and return the text typed."""
        # TODO: build the text, log how many lines, call self.type_text(...)
        raise NotImplementedError

    def append_line(self, line):
        """Add one line at the end of the current content (newline first if not empty)."""
        # TODO: hint - self.text gives the current editor content
        raise NotImplementedError

    def saved_text_normalised(self):
        """File content FROM DISK, BOM removed ('utf-8-sig'), line endings normalised to '\\n'."""
        # TODO
        raise NotImplementedError
