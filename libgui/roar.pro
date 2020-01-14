debug {
	DEFINES		+= DEBUG
}
FORMS			= roar.ui roar_about.ui
HEADERS			= CanvasWidget.hpp CanvasEditorWindow.hpp						\
			../libcanvas/Canvas.hpp									\
			../librtl/rtldef.hpp									\
			../libtools/ToolCircle.hpp ../libtools/ToolCursor.hpp ../libtools/ToolErase.hpp		\
			../libtools/ToolFill.hpp ../libtools/ToolLine.hpp ../libtools/ToolObject.hpp		\
			../libtools/ToolPickColour.hpp ../libtools/ToolRect.hpp ../libtools/ToolText.hpp
linux {
	QMAKE_CXXFLAGS	+= -std=c++14
}
win32 {
	QMAKE_CXXFLAGS	+= /FC /MP /std:c++17
}
QT			+= widgets
SOURCES			= roar.cpp CanvasWidget.cpp CanvasEditorWindow.cpp					\
			../libcanvas/Canvas.cpp ../libcanvas/subr_export.cpp ../libcanvas/subr_import.cpp	\
			../librtl/subr_rtl.cpp									\
			../libtools/ToolCircle.cpp ../libtools/ToolCursor.cpp ../libtools/ToolErase.cpp		\
			../libtools/ToolFill.cpp ../libtools/ToolLine.cpp ../libtools/ToolObject.cpp		\
			../libtools/ToolPickColour.cpp ../libtools/ToolRect.cpp ../libtools/ToolText.cpp
