/*
 * roar -- mIRC art editor for Windows & Linux
 * Copyright (C) 2018, 2019  Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <errno.h>
#include <fcntl.h>
#if defined(_WIN32)
#include <io.h>
#elif defined(__linux__)
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#else
#error Unknown platform
#endif /* defined(_WIN32), defined(__linux__) */

#include <iomanip>
#include <sstream>

#include "../libtools/ToolCircle.hpp"
#include "../libtools/ToolCursor.hpp"
#include "../libtools/ToolErase.hpp"
#include "../libtools/ToolFill.hpp"
#include "../libtools/ToolLine.hpp"
#include "../libtools/ToolObject.hpp"
#include "../libtools/ToolPickColour.hpp"
#include "../libtools/ToolRect.hpp"
#include "../libtools/ToolText.hpp"
#include "CanvasEditorWindow.hpp"

/*
 * Private variables
 */

std::map<Canvas::COLOUR, const std::wstring> s_colour_names = {
	{-1, L"Transparent colour"},
	{ 0, L"Bright White"},
	{ 1, L"Black"},
	{ 2, L"Light Blue"},
	{ 3, L"Green"},
	{ 4, L"Red"},
	{ 5, L"Light Red"},
	{ 6, L"Pink"},
	{ 7, L"Yellow"},
	{ 8, L"Light Yellow"},
	{ 9, L"Light Green"},
	{10, L"Cyan"},
	{11, L"Light Cyan"},
	{12, L"Blue"},
	{13, L"Light Pink"},
	{14, L"Grey"},
	{15, L"Light Grey"},
};

/*
 * Private subroutines
 */

static Qt::MouseButton translateMouseButton(Tool::MOUSE_BUTTON button);
static Tool::MOUSE_BUTTON translateMouseButtonQt(Qt::MouseButton buttonQt);
static Tool::MOUSE_BUTTON translateMouseButtonsQt(Qt::MouseButtons buttonsQt);

static Qt::MouseButton
translateMouseButton(
	Tool::MOUSE_BUTTON	button
)
{
	switch (button) {
	case Tool::MBUTTON_LEFT:
		return Qt::MouseButton::LeftButton;
	case Tool::MBUTTON_MIDDLE:
		return Qt::MouseButton::MiddleButton;
	case Tool::MBUTTON_RIGHT:
		return Qt::MouseButton::RightButton;
	default:
		return Qt::NoButton;
	}
}

static Tool::MOUSE_BUTTON
translateMouseButtonQt(
	Qt::MouseButton	buttonQt
)
{
	switch (buttonQt) {
	case Qt::MouseButton::LeftButton:
		return Tool::MBUTTON_LEFT;
	case Qt::MouseButton::MiddleButton:
		return Tool::MBUTTON_MIDDLE;
	case Qt::MouseButton::RightButton:
		return Tool::MBUTTON_RIGHT;
	default:
		return Tool::MBUTTON_NONE;
	}
}

static Tool::MOUSE_BUTTON
translateMouseButtonsQt(
	Qt::MouseButtons	buttonsQt
)
{
	switch (buttonsQt) {
	case Qt::MouseButton::LeftButton:
		return Tool::MBUTTON_LEFT;
	case Qt::MouseButton::MiddleButton:
		return Tool::MBUTTON_MIDDLE;
	case Qt::MouseButton::RightButton:
		return Tool::MBUTTON_RIGHT;
	default:
		return Tool::MBUTTON_NONE;
	}
}

/*
 * Public class methods
 */

CanvasEditorWindow::CanvasEditorWindow(
	Canvas::BRUSH	brush,
	QWidget *	parent
)
: QMainWindow(parent),
  brush(brush), brushPos{0, 0},
  currentColourAction(nullptr), currentColourBgAction(nullptr), currentOperatorAction(nullptr), currentToolAction(nullptr),
  currentTool(nullptr), cursorCells(), dirty(false), fileName(L""), lastEvent(CanvasWidget::ETYPE_NONE), mouseState{MOUSE_STATE_EMPTY},
  statusLabel(nullptr)
{
	QStringList		arguments;
	auto			mainLayout = new QHBoxLayout();
	auto			scrollArea = new QScrollArea();
	Rtl::STATUS		status;

	this->canvasWidget = new CanvasWidget();
	this->canvasWidget->setEventDispatcher((CanvasWidget::EVENT_DISPATCHER)[&](QKeyEvent *k, QMouseEvent *m, QWheelEvent *w, CanvasWidget::EVENT_TYPE t) {return this->updateToolState(k, m, w, t); });
	this->canvasWidget->setFocusPolicy(Qt::FocusPolicy::ClickFocus);
	this->canvasWidget->setFocus(Qt::FocusReason::ActiveWindowFocusReason);
	this->canvasWidget->setMouseTracking(true);
	scrollArea->setWidget(this->canvasWidget);

	ui.setupUi(this);
	for (const auto& action : {
			this->ui.actionDecreaseBrushHeight, this->ui.actionDecreaseBrushSize, this->ui.actionDecreaseBrushWidth,
			this->ui.actionIncreaseBrushHeight, this->ui.actionIncreaseBrushSize, this->ui.actionIncreaseBrushWidth})
		(void)this->connect(action, &QAction::triggered, this, &CanvasEditorWindow::on_actionBrushSize_triggered);
	for (const auto& action : {
			this->ui.actionDecreaseCanvasHeight, this->ui.actionDecreaseCanvasSize, this->ui.actionDecreaseCanvasWidth,
			this->ui.actionIncreaseCanvasHeight, this->ui.actionIncreaseCanvasSize, this->ui.actionIncreaseCanvasWidth})
		(void)this->connect(action, &QAction::triggered, this, &CanvasEditorWindow::on_actionCanvasSize_triggered);
	for (const auto& action : {
			this->ui.actionColour00, this->ui.actionColour01, this->ui.actionColour02, this->ui.actionColour03, this->ui.actionColour04,
			this->ui.actionColour05, this->ui.actionColour06, this->ui.actionColour07, this->ui.actionColour08, this->ui.actionColour09,
			this->ui.actionColour10, this->ui.actionColour11, this->ui.actionColour12, this->ui.actionColour13, this->ui.actionColour14,
			this->ui.actionColour15, this->ui.actionColourTransparent})
		(void)this->connect(action, &QAction::triggered, this, &CanvasEditorWindow::on_actionColour_triggered);
	for (const auto& action : {
			this->ui.actionColourBg00, this->ui.actionColourBg01, this->ui.actionColourBg02, this->ui.actionColourBg03, this->ui.actionColourBg04,
			this->ui.actionColourBg05, this->ui.actionColourBg06, this->ui.actionColourBg07, this->ui.actionColourBg08, this->ui.actionColourBg09,
			this->ui.actionColourBg10, this->ui.actionColourBg11, this->ui.actionColourBg12, this->ui.actionColourBg13, this->ui.actionColourBg14,
			this->ui.actionColourBg15, this->ui.actionColourBgTransparent})
		(void)this->connect(action, &QAction::triggered, this, &CanvasEditorWindow::on_actionColourBg_triggered);
	(void)this->connect(this->ui.actionFlipColours, &QAction::triggered, this, &CanvasEditorWindow::on_actionFlipColours_triggered);
	for (auto &action : {
			this->ui.actionFlip, this->ui.actionFlipHorizontally, this->ui.actionInvertColours, this->ui.actionRotate, this->ui.actionTile})
		(void)this->connect(action, &QAction::triggered, this, &CanvasEditorWindow::on_actionOperator_triggered);
	(void)this->connect(this->ui.actionRedo, &QAction::triggered, this, &CanvasEditorWindow::on_actionReUndo_triggered);
	(void)this->connect(this->ui.actionUndo, &QAction::triggered, this, &CanvasEditorWindow::on_actionReUndo_triggered);
	for (auto& action : {
			this->ui.actionCursor, this->ui.actionRectangle, this->ui.actionCircle, this->ui.actionFill,
			this->ui.actionLine, this->ui.actionText, this->ui.actionObject, this->ui.actionErase, this->ui.actionPickColour})
		(void)this->connect(action, &QAction::triggered, this, &CanvasEditorWindow::on_actionTool_triggered);

	mainLayout->addWidget(scrollArea);
	this->setRandomAppIcon(status);
	this->statusLabel = new QLabel(this);
	this->ui.statusbar->addPermanentWidget(this->statusLabel, 1);
	this->ui.centralwidget->setLayout(mainLayout);
	arguments = QCoreApplication::arguments();
	if (arguments.size() > 1)
		this->importMiRCfromFile(status, arguments[1].toStdWString(), true, true);
	else
		this->importNew(status, true, true);
	emit this->ui.actionCursor->triggered();
	emit this->ui.actionColour03->triggered();
	emit this->ui.actionColourBgTransparent->triggered();
	this->updateStatusBar();
}

CanvasEditorWindow::~CanvasEditorWindow(
)
{
	/* XXX */
}

/*
 * Private class methods
 */

void
CanvasEditorWindow::applyLastTool(
)
{
	Tool::TOOL_CELLS	rc(false, Tool::TOOL_CELLS_PAIR(Canvas::CELL_LIST(), Canvas::CELL_LIST()));

	if (this->currentTool) {
		if (this->mouseState.dragState.status >= Tool::DSTATUS_BEGIN)
			rc = this->currentTool->drag(this->brush, this->brushPos, this->canvasWidget->canvas, this->mouseState.dragState, this->brushPos);
		else
			rc = this->currentTool->cursor(this->brush, this->brushPos, this->canvasWidget->canvas, this->brushPos);
	}
	if (rc) {
		(void)this->applyTool(rc); this->updateStatusBar();
	}
}

Tool::TOOL_CELLS
CanvasEditorWindow::applyTool(
	Tool::TOOL_CELLS	rc
)
{
	bool				commitfl = false;
	Rtl::Either<bool, Canvas::RECT>	rc_(false, Canvas::RECT());

	if (rc.right.first.size()) {
		this->dirty = commitfl = this->canvasWidget->canvas.commit(rc.right.first, false);
		if (commitfl && (this->canvasWidget->canvas.cellsUndo.size > 0))
			this->ui.actionUndo->setEnabled(true);
		else
			this->ui.actionUndo->setEnabled(false);
		if ((rc_ = this->canvasWidget->renderCells(false, rc.right.first)))
			this->canvasWidget->update(QRect(rc_.right.p0.x, rc_.right.p0.y, rc_.right.p1.x, rc_.right.p1.y));
	}
	if (rc.right.second.size()) {
		this->cursorHide(); this->cursorShow(rc.right.second);
	}
	return rc;
}

void
CanvasEditorWindow::cursorHide(
)
{
	Canvas::CELL_LIST		cells;
	Rtl::Either<bool, Canvas::RECT>	rc(false, Canvas::RECT());

	for (auto& cell : this->cursorCells) {
		if ((cell.p.x < this->canvasWidget->canvas.size.w)
		&&  (cell.p.y < this->canvasWidget->canvas.size.h))
			cells.push_back(this->canvasWidget->canvas.cells[cell.p.y][cell.p.x]);
	}
	if (cells.size() && (rc = this->canvasWidget->renderCells(false, cells)))
		this->canvasWidget->update(QRect(rc.right.p0.x, rc.right.p0.y, rc.right.p1.x, rc.right.p1.y));
}

void
CanvasEditorWindow::cursorShow(
	const Canvas::CELL_LIST&	cells
)
{
	Rtl::Either<bool, Canvas::RECT>	rc(false, Canvas::RECT());
	
	if ((rc = this->canvasWidget->renderCells(true, cells))) {
		this->cursorCells = cells;
		this->canvasWidget->update(QRect(rc.right.p0.x, rc.right.p0.y, rc.right.p1.x, rc.right.p1.y));
	}
}

bool
CanvasEditorWindow::exportMiRCtoFile(
	Rtl::STATUS&		pstatus,
	const std::wstring&	fileName,
	bool			printError,
	bool			setTitle
)
{
	int		fd = -1;
	std::string	fileData;
	std::wstring	fileDataW;
#if defined(__linux__)
	std::string	fileName_;
#endif /* defined(__linux__) */
#if defined(_WIN32)
	int		nwritten = -2;
#elif defined(__linux__)
	ssize_t		nwritten = -2;
#endif /* defined(_WIN32), defined(__linux__) */
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	try {
#if defined(_WIN32)
		if (STATUS_BIND_LIBC(status, fd = _wopen(fileName.c_str(), _O_BINARY | _O_CREAT | _O_WRONLY, 0600))
#elif defined(__linux__)
		if (Rtl::convert_wstring(&status, fileName, fileName_)
		&&  STATUS_BIND_LIBC(status, fd = ::open(fileName_.c_str(), O_CREAT | O_WRONLY, 0600))
#endif /* defined(_WIN32), defined(__linux__) */
		&&  this->canvasWidget->canvas.export_(status, fileDataW, Canvas::DTYPE_MIRC)
		&&  Rtl::convert_wstring(&status, fileDataW, fileData)
#if defined(_WIN32)
		&&  STATUS_BIND_LIBC(status, nwritten = _write(fd, &fileData[0], (unsigned int)fileData.length()))
#elif defined(__linux__)
		&&  STATUS_BIND_LIBC(status, nwritten = ::write(fd, &fileData[0], (size_t)fileData.length()))
#endif /* defined(_WIN32), defined(__linux__) */
		&&  STATUS_BIND_ROAR(status, "short write", ((size_t)nwritten == fileData.length()))) {
			this->dirty = false, this->fileName = fileName;
			if (setTitle)
				this->setWindowTitle(QString("%1 - roar").arg(QString().fromUtf16((const ushort *)this->fileName.c_str())));
		}
	}
	catch (std::bad_alloc) {
		status = Rtl::STATUS_POSIX(ENOMEM);
	}
	if (fd != -1)
#if defined(_WIN32)
		_close(fd);
#elif defined(__linux__)
		::close(fd);
#endif /* defined(_WIN32), defined(__linux__) */
	printf("fileData.length()=%zu fileDataW.length()=%zu nwritten=%d\n", fileData.length(), fileDataW.length(), nwritten);
	if (!status && printError)
		QMessageBox::critical(this, "File error",
			QString("Failed to open %1: %2").arg(QString().fromUtf16((const ushort *)fileName.c_str())).arg(QString().fromUtf16((const ushort *)Rtl::perror(status).c_str())));
	return (bool)(pstatus = status);
}

bool
CanvasEditorWindow::importMiRCfromFile(
	Rtl::STATUS&		pstatus,
	const std::wstring&	fileName,
	bool			printError,
	bool			setTitle
)
{
	int		fd = -1;
	std::string	fileData;
	std::wstring	fileDataW;
#if defined(__linux__)
	std::string	fileName_;
#endif /* defined(__linux__) */
	int64_t		fileSize = 0;
#if defined(_WIN32)
	int		nread;
#elif defined(__linux__)
	ssize_t		nread;
#endif /* defined(_WIN32), defined(__linux__) */
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	try {
#if defined(_WIN32)
		if (STATUS_BIND_LIBC(status, fd = _wopen(fileName.c_str(), _O_BINARY | _O_RDONLY))
		&&  STATUS_BIND_LIBC(status, _lseeki64(fd, 0, SEEK_END))
		&&  STATUS_BIND_LIBC(status, fileSize = _telli64(fd))
#elif defined(__linux__)
		if (Rtl::convert_wstring(&status, fileName, fileName_)
		&&  STATUS_BIND_LIBC(status, fd = ::open(fileName_.c_str(), O_RDONLY))
		&&  STATUS_BIND_LIBC(status, lseek(fd, 0, SEEK_END))
		&&  STATUS_BIND_LIBC(status, fileSize = lseek(fd, 0, SEEK_CUR))
#endif /* defined(_WIN32), defined(__linux__) */
		&&  STATUS_BIND_TRUE(fileData.resize(fileSize))
#if defined(_WIN32)
		&&  STATUS_BIND_LIBC(status, _lseeki64(fd, 0, SEEK_SET))
		&&  STATUS_BIND_LIBC(status, nread = _read(fd, &fileData[0], fileSize))
#elif defined(__linux__)
		&&  STATUS_BIND_LIBC(status, lseek(fd, 0, SEEK_CUR))
		&&  STATUS_BIND_LIBC(status, nread = ::read(fd, &fileData[0], fileSize))
#endif /* defined(_WIN32), defined(__linux__) */
		&&  STATUS_BIND_ROAR(status, "short read", (size_t)nread == (size_t)fileSize)
		&&  Rtl::convert_cstring(&status, fileData, fileDataW)
		&&  this->canvasWidget->import(status, fileDataW, Canvas::DTYPE_MIRC)) {
			this->dirty = false, this->fileName = fileName;
			this->ui.actionRedo->setEnabled(false), this->ui.actionUndo->setEnabled(false);
			if (setTitle)
				this->setWindowTitle(QString("%1 - roar").arg(QString().fromUtf16((const ushort *)this->fileName.c_str())));
		}
	}
	catch (std::bad_alloc) {
		status = Rtl::STATUS_POSIX(ENOMEM);
	}
	if (fd != -1)
#if defined(_WIN32)
		_close(fd);
#elif defined(__linux__)
		::close(fd);
#endif /* defined(_WIN32), defined(__linux__) */
	if (!status && printError)
		QMessageBox::critical(this, "File error",
			QString("Failed to open %1: %2").arg(QString().fromUtf16((const ushort *)fileName.c_str())).arg(QString().fromUtf16((const ushort *)Rtl::perror(status).c_str())));
	return (bool)(pstatus = status);
}

bool
CanvasEditorWindow::importNew(
	Rtl::STATUS&	pstatus,
	bool		printError,
	bool		setTitle
)
{
	Canvas::CELL_MAP	cell_map;
	Rtl::STATUS		status = Rtl::STATUS_NONE_SUCCESS;

	try {
		cell_map = Canvas::CELL_MAP(this->canvasWidget->sizeDefault.h, Canvas::CELL_LIST(this->canvasWidget->sizeDefault.w));
		for (uint64_t y = 0; y < cell_map.size(); y++) {
			for (uint64_t x = 0; x < cell_map[y].size(); x++)
				cell_map[y][x] = Canvas::CELL{Canvas::CATTR_NONE, this->brush.colours.bg, this->brush.colours.fg, {x, y}, L" "};
		}
		if (this->canvasWidget->import(status, cell_map, this->canvasWidget->sizeDefault)) {
			this->dirty = false, this->fileName = L"";
			this->ui.actionRedo->setEnabled(false), this->ui.actionUndo->setEnabled(false);
			if (setTitle)
				this->setWindowTitle(QString("(Untitled) - roar"));
		}
	}
	catch (std::bad_alloc) {
		status = Rtl::STATUS_POSIX(ENOMEM);
	}
	if (!status && printError)
		QMessageBox::critical(this, "Canvas error", QString("%1").arg(QString().fromUtf16((const ushort *)Rtl::perror(status).c_str())));
	return (bool)(pstatus = status);
}

void
CanvasEditorWindow::on_actionBrushSize_triggered(
	bool	checked
)
{
	QAction *	object = (QAction *)sender();
	bool		updatefl = false;

	(void)checked;
	if (object == this->ui.actionDecreaseBrushHeight) {
		if (this->brush.size.h > 0)
			this->brush.size.h--, updatefl = true;
	} else if (object == this->ui.actionDecreaseBrushSize) {
		if (this->brush.size.h > 0)
			this->brush.size.h--, updatefl = true;
		if (this->brush.size.w > 0)
			this->brush.size.w--, updatefl = true;
	} else if (object == this->ui.actionDecreaseBrushWidth) {
		if (this->brush.size.w > 0)
			this->brush.size.w--, updatefl = true;
	} else if (object == this->ui.actionIncreaseBrushHeight) {
		this->brush.size.h++, updatefl = true;
	} else if (object == this->ui.actionIncreaseBrushSize) {
		this->brush.size.h++, this->brush.size.w++, updatefl = true;
	} else if (object == this->ui.actionIncreaseBrushWidth) {
		this->brush.size.w++, updatefl = true;
	}
	if (updatefl)
		this->applyLastTool();
}

void
CanvasEditorWindow::on_actionCanvasSize_triggered(
	bool	checked
)
{
	QAction *	object = (QAction *)sender();

	(void)checked;
	if (object == this->ui.actionDecreaseCanvasHeight) {
	} else if (object == this->ui.actionDecreaseCanvasSize) {
	} else if (object == this->ui.actionDecreaseCanvasWidth) {
	} else if (object == this->ui.actionIncreaseCanvasHeight) {
	} else if (object == this->ui.actionIncreaseCanvasSize) {
	} else if (object == this->ui.actionIncreaseCanvasWidth) {
	}
}

void
CanvasEditorWindow::on_actionColour_triggered(
	bool	checked
)
{
	QAction *	object = (QAction *)sender();
	bool		updatefl = false;

	(void)checked;
	if (this->currentColourAction)
		this->currentColourAction->setChecked(false);
	this->currentColourAction = object; this->currentColourAction->setChecked(true);
	if (object == this->ui.actionColour00)
		this->brush.colours.fg = 0, updatefl = true;
	else if (object == this->ui.actionColour01)
		this->brush.colours.fg = 1, updatefl = true;
	else if (object == this->ui.actionColour02)
		this->brush.colours.fg = 2, updatefl = true;
	else if (object == this->ui.actionColour03)
		this->brush.colours.fg = 3, updatefl = true;
	else if (object == this->ui.actionColour04)
		this->brush.colours.fg = 4, updatefl = true;
	else if (object == this->ui.actionColour05)
		this->brush.colours.fg = 5, updatefl = true;
	else if (object == this->ui.actionColour06)
		this->brush.colours.fg = 6, updatefl = true;
	else if (object == this->ui.actionColour07)
		this->brush.colours.fg = 7, updatefl = true;
	else if (object == this->ui.actionColour08)
		this->brush.colours.fg = 8, updatefl = true;
	else if (object == this->ui.actionColour09)
		this->brush.colours.fg = 9, updatefl = true;
	else if (object == this->ui.actionColour10)
		this->brush.colours.fg = 10, updatefl = true;
	else if (object == this->ui.actionColour11)
		this->brush.colours.fg = 11, updatefl = true;
	else if (object == this->ui.actionColour12)
		this->brush.colours.fg = 12, updatefl = true;
	else if (object == this->ui.actionColour13)
		this->brush.colours.fg = 13, updatefl = true;
	else if (object == this->ui.actionColour14)
		this->brush.colours.fg = 14, updatefl = true;
	else if (object == this->ui.actionColour15)
		this->brush.colours.fg = 15, updatefl = true;
	else if (object == this->ui.actionColourTransparent)
		this->brush.colours.fg = -1, updatefl = true;
	if (updatefl)
		this->applyLastTool();
}

void
CanvasEditorWindow::on_actionColourBg_triggered(
	bool	checked
)
{
	QAction *	object = (QAction *)sender();
	bool		updatefl = false;

	(void)checked;
	if (this->currentColourBgAction)
		this->currentColourBgAction->setChecked(false);
	this->currentColourBgAction = object; this->currentColourBgAction->setChecked(true);
	if (object == this->ui.actionColourBg00)
		this->brush.colours.bg = 0, updatefl = true;
	else if (object == this->ui.actionColourBg01)
		this->brush.colours.bg = 1, updatefl = true;
	else if (object == this->ui.actionColourBg02)
		this->brush.colours.bg = 2, updatefl = true;
	else if (object == this->ui.actionColourBg03)
		this->brush.colours.bg = 3, updatefl = true;
	else if (object == this->ui.actionColourBg04)
		this->brush.colours.bg = 4, updatefl = true;
	else if (object == this->ui.actionColourBg05)
		this->brush.colours.bg = 5, updatefl = true;
	else if (object == this->ui.actionColourBg06)
		this->brush.colours.bg = 6, updatefl = true;
	else if (object == this->ui.actionColourBg07)
		this->brush.colours.bg = 7, updatefl = true;
	else if (object == this->ui.actionColourBg08)
		this->brush.colours.bg = 8, updatefl = true;
	else if (object == this->ui.actionColourBg09)
		this->brush.colours.bg = 9, updatefl = true;
	else if (object == this->ui.actionColourBg10)
		this->brush.colours.bg = 10, updatefl = true;
	else if (object == this->ui.actionColourBg11)
		this->brush.colours.bg = 11, updatefl = true;
	else if (object == this->ui.actionColourBg12)
		this->brush.colours.bg = 12, updatefl = true;
	else if (object == this->ui.actionColourBg13)
		this->brush.colours.bg = 13, updatefl = true;
	else if (object == this->ui.actionColourBg14)
		this->brush.colours.bg = 14, updatefl = true;
	else if (object == this->ui.actionColourBg15)
		this->brush.colours.bg = 15, updatefl = true;
	else if (object == this->ui.actionColourBgTransparent)
		this->brush.colours.bg = -1, updatefl = true;
	if (updatefl)
		this->applyLastTool();
}

void
CanvasEditorWindow::on_actionFlipColours_triggered(
	bool	checked
)
{
	(void)checked;
	std::swap(this->brush.colours.bg, this->brush.colours.fg);
	this->applyLastTool();
}

void
CanvasEditorWindow::on_actionOperator_triggered(
	bool	checked
)
{
	QAction *	object = (QAction *)sender();

	(void)checked;
	if (this->currentOperatorAction)
		this->currentOperatorAction->setChecked(false);
	this->currentOperatorAction = object; this->currentOperatorAction->setChecked(true);
	if (object == this->ui.actionFlip) {
	} else if (object == this->ui.actionFlipHorizontally) {
	} else if (object == this->ui.actionInvertColours) {
	} else if (object == this->ui.actionRotate) {
	} else if (object == this->ui.actionTile) {
	}
}

void
CanvasEditorWindow::on_actionReUndo_triggered(
	bool checked
)
{
	const Canvas::CELL_LIST *	cells = nullptr;
	QAction *			object = (QAction *)sender();
	Rtl::Either<bool, Canvas::RECT>	rc(false, Canvas::RECT());

	(void)checked;
	if (object == this->ui.actionRedo) {
		cells = this->canvasWidget->canvas.redo();
	} else if (object == this->ui.actionUndo) {
		cells = this->canvasWidget->canvas.undo();
	}
	if (this->canvasWidget->canvas.cellsUndo.index > 0)
		this->ui.actionRedo->setEnabled(true);
	else
		this->ui.actionRedo->setEnabled(false);
	if (this->canvasWidget->canvas.cellsUndo.index < this->canvasWidget->canvas.cellsUndo.size)
		this->ui.actionUndo->setEnabled(true);
	else
		this->ui.actionUndo->setEnabled(false);
	if (cells && (rc = this->canvasWidget->renderCells(false, *cells)))
		this->canvasWidget->update(QRect(rc.right.p0.x, rc.right.p0.y, rc.right.p1.x, rc.right.p1.y));
}

void
CanvasEditorWindow::on_actionTool_triggered(
	bool	checked
)
{
	QAction *	object = (QAction *)sender();

	(void)checked;
	if (this->currentToolAction)
		this->currentToolAction->setChecked(false);
	this->currentToolAction = object; this->currentToolAction->setChecked(true);
	if (object == this->ui.actionCircle)
		this->currentTool = std::make_unique<ToolCircle>();
	else if (object == this->ui.actionCursor)
		this->currentTool = std::make_unique<ToolCursor>();
	else if (object == this->ui.actionObject)
		this->currentTool = std::make_unique<ToolObject>();
	else if (object == this->ui.actionRectangle)
		this->currentTool = std::make_unique<ToolRect>();
	else if (object == this->ui.actionLine)
		this->currentTool = std::make_unique<ToolLine>();
	else if (object == this->ui.actionText)
		this->currentTool = std::make_unique<ToolText>();
	else if (object == this->ui.actionPickColour)
		this->currentTool = std::make_unique<ToolPickColour>();
	else if (object == this->ui.actionErase)
		this->currentTool = std::make_unique<ToolErase>();
	else if (object == this->ui.actionFill)
		this->currentTool = std::make_unique<ToolFill>();
	this->updateStatusBar();
}

bool
CanvasEditorWindow::promptSaveChanges(
)
{
	std::wstring	fileName;
	bool		rc;

	fileName = (this->fileName == L"") ? L"(Untitled)" : this->fileName;
	switch (QMessageBox::question(
			this, "roar", QString("Do you want to save changes to %1?").arg(QString().fromUtf16((const ushort *)fileName.c_str())),
			QMessageBox::Cancel | QMessageBox::Discard | QMessageBox::Save, QMessageBox::Save)) {
	case QMessageBox::Cancel:
		rc = false; break;
	case QMessageBox::Discard:
		rc = true; break;
	case QMessageBox::Save:
		rc = this->saveAsMiRC("", true, false); break;
	default:
		rc = false;
	}
	return rc;
}

bool
CanvasEditorWindow::saveAsMiRC(
	const QString&	fileName,
	bool		printError,
	bool		promptName
)
{
	QString		fileName_;
	std::wstring	fileName_W;
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	if (fileName == "") {
		if (promptName || (this->fileName == L"")) {
			if ((fileName_ = QFileDialog::getSaveFileName(this, tr("Save..."), QString(""), tr("mIRC art files (*.txt);;All Files (*.*)"))) != "") {
				if (Rtl::convert_cstring(&status, fileName_.toStdString(), fileName_W))
					this->fileName = fileName_W;
			} else
				return false;
		}
	} else
		Rtl::convert_cstring(&status, fileName.toStdString(), fileName_W);
	if (status)
		this->exportMiRCtoFile(status, this->fileName, true, true);
	else if (printError)
		QMessageBox::critical(this, "Save...", QString("%1").arg(QString().fromUtf16((const ushort *)Rtl::perror(status).c_str())));
	return (bool)status;
}

bool
CanvasEditorWindow::setRandomAppIcon(
	Rtl::STATUS&	pstatus
)
{
	struct _wfinddata_t		fileinfo;
	intptr_t			findHandle;
	QIcon				icon;
	std::vector<std::wstring>	iconNames;
	QPixmap				pixmap;
	QString				pixmapFileName;
	int				rc;
	Rtl::STATUS			status = Rtl::STATUS_NONE_SUCCESS;

	if (STATUS_BIND_LIBC(status, findHandle = _wfindfirst(L"assets\\images\\logo*.bmp", &fileinfo))) {
		while (STATUS_BIND_LIBC(status, (rc = _wfindnext(findHandle, &fileinfo))))
			iconNames.push_back(L"assets\\images\\" + std::wstring(fileinfo.name));
		if (!status && (status.cond == ENOENT))
			status = Rtl::STATUS_NONE_SUCCESS;
		_findclose(findHandle);
	}
	pixmapFileName = QString().fromUtf16((const ushort *)iconNames[rand() % iconNames.size()].c_str());
	pixmap = QPixmap(pixmapFileName);
	icon = QIcon(pixmap);
	this->setWindowIcon(icon);
	return (bool)(pstatus = status);
}

Canvas::POINT
CanvasEditorWindow::translateMousePointQt(
	QPoint	pointQt
)
{
	Canvas::POINT	point = {0, 0};
	if (pointQt.x() > 0)
		point.x = pointQt.x() / this->canvasWidget->cellSize.w;
	if (pointQt.y() > 0)
		point.y = pointQt.y() / this->canvasWidget->cellSize.h;
	return point;
}

void
CanvasEditorWindow::updateStatusBar(
)
{
	std::wstring		statusText;
	std::wstringstream	statusText_stream;

	statusText_stream
		<< L"X: " << setfillw(L'0', 3) << this->brushPos.x << L" "
		<< L"Y: " << setfillw(L'0', 3) << this->brushPos.y
		<< L" | "
		<< L"W: " << setfillw(L'0', 3) << this->canvasWidget->canvas.size.w << L" "
		<< L"H: " << setfillw(L'0', 3) << this->canvasWidget->canvas.size.h
		<< L" | "
		<< L"B: " << setfillw(L'0', 2) << this->brush.size.w << L"x" << setfillw(L'0', 2) << this->brush.size.h
		<< L" | "
		<< L"FG " << setfillw(L'0', 2) << this->brush.colours.fg << L" (" << s_colour_names[this->brush.colours.fg] << L"), "
		<< L"BG " << setfillw(L'0', 2) << this->brush.colours.bg << L" (" << s_colour_names[this->brush.colours.bg];
	if (this->currentTool)
		statusText_stream << L" | T: " << this->currentTool->name;
	if (this->dirty)
		statusText_stream << " | *";
	statusText = statusText_stream.str();
	this->statusLabel->setText(QString().fromUtf16((const ushort *)statusText.c_str()));
}

bool
CanvasEditorWindow::updateToolState(
	QKeyEvent *			keyEvent,
	QMouseEvent *			mouseEvent,
	QWheelEvent *			wheelEvent,
	CanvasWidget::EVENT_TYPE	type
)
{
	QPoint			angleDelta;
	Tool::MOUSE_BUTTON	button = Tool::MBUTTON_NONE;
	Qt::MouseButtons	buttonsQt;
	Canvas::POINT		canvasPos{0, 0};
	Qt::KeyboardModifiers	modifiers;
	Tool::TOOL_CELLS	rc(false, Tool::TOOL_CELLS_PAIR(Canvas::CELL_LIST(), Canvas::CELL_LIST()));
	bool			updatefl = false;

	(void)keyEvent;
	if (!this->currentTool)
		return false;
	switch (type) {
	case CanvasWidget::ETYPE_KEYBOARD_PRESS:
	case CanvasWidget::ETYPE_KEYBOARD_RELEASE:
		break;
	case CanvasWidget::ETYPE_MOUSE_MOVE:
	case CanvasWidget::ETYPE_MOUSE_PRESS:
	case CanvasWidget::ETYPE_MOUSE_RELEASE:
		button = translateMouseButtonQt(mouseEvent->button()), canvasPos = translateMousePointQt(mouseEvent->localPos().toPoint());
		modifiers = mouseEvent->modifiers();
		break;
	case CanvasWidget::ETYPE_MOUSE_WHEEL:
		angleDelta = wheelEvent->angleDelta(), modifiers = wheelEvent->modifiers();
		break;
	default:
		break;
	}
	switch (type) {
	case CanvasWidget::ETYPE_MOUSE_MOVE:
		if (!this->canvasWidget->hasFocus())
			this->canvasWidget->setFocus(Qt::FocusReason::ActiveWindowFocusReason);
		buttonsQt = mouseEvent->buttons();
		switch (this->mouseState.dragState.status) {
		case Tool::DSTATUS_NONE:
			if (this->mouseState.lastPos != canvasPos) {
				if (buttonsQt == Qt::NoButton) {
					rc = this->currentTool->cursor(this->brush, this->brushPos, this->canvasWidget->canvas, canvasPos);
					this->mouseState.lastPos = canvasPos;
				} else if ((button = translateMouseButtonsQt(buttonsQt)) != Tool::MBUTTON_NONE) {
					rc = this->currentTool->click(this->brush, this->brushPos, button, this->canvasWidget->canvas, canvasPos);
					this->mouseState.lastPos = canvasPos;
				}
			}
			break;
		case Tool::DSTATUS_BEGIN:
			if (this->mouseState.dragState.begin != canvasPos) {
				if (buttonsQt == translateMouseButton(this->mouseState.dragState.button)) {
					this->mouseState.dragState.status = Tool::DSTATUS_MOVE;
					rc = this->currentTool->drag(this->brush, this->brushPos, this->canvasWidget->canvas, this->mouseState.dragState, canvasPos);
					this->mouseState.lastPos = canvasPos;
				}
			}
			break;
		case Tool::DSTATUS_MOVE:
			if (this->mouseState.lastPos != canvasPos) {
				rc = this->currentTool->drag(this->brush, this->brushPos, this->canvasWidget->canvas, this->mouseState.dragState, canvasPos);
				this->mouseState.lastPos = canvasPos;
			}
			break;
		default:
			break;
		}
		mouseEvent->accept();
		break;
	case CanvasWidget::ETYPE_MOUSE_PRESS:
		switch (this->mouseState.dragState.status) {
		case Tool::DSTATUS_NONE:
			if (modifiers == Qt::ControlModifier) {
				this->mouseState.dragState.begin = canvasPos;
				this->mouseState.dragState.button = button;
				this->mouseState.dragState.status = Tool::DSTATUS_BEGIN;
				this->mouseState.lastPos = canvasPos;
			}
			break;
		default:
			break;
		}
		mouseEvent->accept();
		break;
	case CanvasWidget::ETYPE_MOUSE_RELEASE:
		switch (this->mouseState.dragState.status) {
		case Tool::DSTATUS_BEGIN:
			this->mouseState.dragState = Tool::DRAG_STATE{DRAG_STATE_EMPTY};
		case Tool::DSTATUS_NONE:
			this->mouseState.lastPos = canvasPos;
			rc = this->currentTool->click(this->brush, this->brushPos, button, this->canvasWidget->canvas, canvasPos);
			break;
		case Tool::DSTATUS_MOVE:
			if (button == this->mouseState.dragState.button) {
				this->mouseState.dragState.set = canvasPos;
				this->mouseState.dragState.status = Tool::DSTATUS_SET;
				rc = this->currentTool->drag(this->brush, this->brushPos, this->canvasWidget->canvas, this->mouseState.dragState, canvasPos);
				this->mouseState.dragState = Tool::DRAG_STATE{DRAG_STATE_EMPTY};
				this->mouseState.lastPos = canvasPos;
			}
			break;
		default:
			break;
		}
		mouseEvent->accept();
		break;
	case CanvasWidget::ETYPE_MOUSE_WHEEL:
		if (modifiers == Qt::ControlModifier) {
			if (angleDelta.y() > 0)
				this->brush.size.h++, this->brush.size.w++, updatefl = true;
			else {
				if (this->brush.size.h > 0)
					this->brush.size.h--, updatefl = true;
				if (this->brush.size.w > 0)
					this->brush.size.w--, updatefl = true;
			}
			if (updatefl)
				this->applyLastTool();
			wheelEvent->accept();
		} else
			wheelEvent->ignore();
		break;
	default:
		break;
	}
	if (rc) {
		rc = this->applyTool(rc); this->updateStatusBar();
	}
	return rc;
}

/*
 * Private Qt class slot functions
 */

void
CanvasEditorWindow::on_actionAboutRoar_triggered(
	bool	checked
)
{
	QDialog *	about = new QDialog(0, Qt::WindowCloseButtonHint | Qt::WindowTitleHint);

	(void)checked;
	this->uiAbout.setupUi(about);
	about->setFixedSize(about->size());
	about->show();
}

void
CanvasEditorWindow::on_actionExit_triggered(
	bool	checked
)
{
	(void)checked;
	if (!this->dirty || (this->dirty && this->promptSaveChanges()))
		this->close();
}

void
CanvasEditorWindow::on_actionExportAsANSI_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionExportAsPNG_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionExportToClipboard_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionExportToImgur_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionExportToPastebin_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionImportANSI_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionImportFromClipboard_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionImportSAUCE_triggered(
	bool	checked
)
{
	(void)checked;
}

void
CanvasEditorWindow::on_actionNew_triggered(
	bool	checked
)
{
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	(void)checked;
	if (!this->dirty || (this->dirty && this->promptSaveChanges()))
		this->importNew(status, true, true);
}

void
CanvasEditorWindow::on_actionOpen_triggered(
	bool	checked
)
{
	QString		fileName;
	std::wstring	fileNameW;
	Rtl::STATUS	status = Rtl::STATUS_NONE_SUCCESS;

	(void)checked;
	if (((fileName = QFileDialog::getOpenFileName(this, tr("Open..."), QString(""), tr("mIRC art files (*.txt);;All Files (*.*)"))) != "")
	&&  (!this->dirty || (this->dirty && this->promptSaveChanges()))) {
		QApplication::setOverrideCursor(Qt::WaitCursor); QApplication::processEvents();
		if (Rtl::convert_cstring(&status, fileName.toStdString(), fileNameW))
			this->importMiRCfromFile(status, fileNameW, true, true);
		QApplication::restoreOverrideCursor(); QApplication::processEvents();
	}
	if (!status)
		QMessageBox::critical(this, "Open...", QString("Failed to open %1: %2").arg(fileName, QString().fromUtf16((const ushort *)Rtl::perror(status).c_str())));
}

void
CanvasEditorWindow::on_actionSave_triggered(
	bool	checked
)
{
	(void)checked;
	this->saveAsMiRC("", true, false);
}

void
CanvasEditorWindow::on_actionSaveAs_triggered(
	bool	checked
)
{
	Rtl::STATUS	status;

	(void)checked;
	this->saveAsMiRC("", true, true);
}
