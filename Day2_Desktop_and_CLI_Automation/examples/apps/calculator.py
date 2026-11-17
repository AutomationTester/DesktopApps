# encoding: utf-8

from pywinauto_recorder.recorder import Recorder
from pywinauto_recorder.player import UIPath, click, move, playback


with UIPath(u"||List"):
	click(u"")

with UIPath(u"Taskbar||Pane"):
	with UIPath(u"||Pane->||Pane"):
		click(u"Start||Button")

with UIPath(u"||List"):
	click(u"")
	click(u"")

with UIPath(u"Calculator||Window"):
	with UIPath(u"Calculator||Window"):
		click(u"||Custom")
	with UIPath(u"Calculator||Window->||Custom->||Group->Number pad||Group"):
		click(u"Nine||Button")
		click(u"Nine||Button")
		click(u"Nine||Button")
		click(u"Nine||Button")
