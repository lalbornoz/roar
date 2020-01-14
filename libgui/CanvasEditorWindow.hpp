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

#ifndef _CANVASEDITORWINDOW_HPP_
#define _CANVASEDITORWINDOW_HPP_

#include <memory>
#include <string>

#include <QtWidgets/QAction>
#include <QtWidgets/QtWidgets>

#include "../libcanvas/Canvas.hpp"
#include "../librtl/rtldef.hpp"
#include "../libtools/Tool.hpp"
#include "CanvasWidget.hpp"
#include "ui_roar.h"
#include "ui_roar_about.h"

/*
 * Public types
 */

class CanvasEditorWindow : public QMainWindow {
	Q_OBJECT

public:
	explicit CanvasEditorWindow(Canvas::BRUSH brush={{-1, 3}, {1, 1}}, QWidget *parent=nullptr);
	~CanvasEditorWindow();

private:
	typedef struct mouse_state_e {
		Tool::DRAG_STATE	dragState;
		Tool::MOUSE_BUTTON	button;
		Canvas::POINT		lastPos;
	}				MOUSE_STATE;
	#define MOUSE_STATE_EMPTY	DRAG_STATE_EMPTY, Tool::MBUTTON_NONE, {0, 0}

	Canvas::BRUSH			brush;
	Canvas::POINT			brushPos;
	CanvasWidget *			canvasWidget;
	QAction *			currentColourAction, *currentColourBgAction, *currentOperatorAction, *currentToolAction;
	std::unique_ptr<Tool>		currentTool;
	Canvas::CELL_LIST		cursorCells;
	bool				dirty;
	std::wstring			fileName;
	QIcon				icon;
	CanvasWidget::EVENT_TYPE	lastEvent;
	MOUSE_STATE			mouseState;
	QLabel *			statusLabel;
	Ui::canvas			ui;
	Ui::Dialog			uiAbout;

	void applyLastTool();
	Tool::TOOL_CELLS applyTool(Tool::TOOL_CELLS rc);
	void cursorHide();
	void cursorShow(const Canvas::CELL_LIST& cells);
	bool exportMiRCtoFile(Rtl::STATUS& pstatus, const std::wstring& fileName, bool printError, bool setTitle);
	bool importMiRCfromFile(Rtl::STATUS& pstatus, const std::wstring& fileName, bool printError, bool setTitle);
	bool importNew(Rtl::STATUS& pstatus, bool printError, bool setTitle);
	void on_actionBrushSize_triggered(bool checked);
	void on_actionCanvasSize_triggered(bool checked);
	void on_actionColour_triggered(bool checked);
	void on_actionColourBg_triggered(bool checked);
	void on_actionFlipColours_triggered(bool checked);
	void on_actionOperator_triggered(bool checked);
	void on_actionReUndo_triggered(bool checked);
	void on_actionTool_triggered(bool checked);
	bool promptSaveChanges();
	bool saveAsMiRC(const QString& fileName, bool printError, bool promptName);
	bool setRandomAppIcon(Rtl::STATUS& pstatus);
	Canvas::POINT translateMousePointQt(QPoint pointQt);
	void updateStatusBar();
	bool updateToolState(QKeyEvent *, QMouseEvent *, QWheelEvent *, CanvasWidget::EVENT_TYPE);

private slots:
	void on_actionAboutRoar_triggered(bool checked);
	void on_actionExit_triggered(bool checked);
	void on_actionExportAsANSI_triggered(bool checked);
	void on_actionExportAsPNG_triggered(bool checked);
	void on_actionExportToClipboard_triggered(bool checked);
	void on_actionExportToImgur_triggered(bool checked);
	void on_actionExportToPastebin_triggered(bool checked);
	void on_actionImportANSI_triggered(bool checked);
	void on_actionImportFromClipboard_triggered(bool checked);
	void on_actionImportSAUCE_triggered(bool checked);
	void on_actionNew_triggered(bool checked);
	void on_actionOpen_triggered(bool checked);
	void on_actionSave_triggered(bool checked);
	void on_actionSaveAs_triggered(bool checked);
};

#endif /* _CANVASEDITORWINDOW_HPP_ */
