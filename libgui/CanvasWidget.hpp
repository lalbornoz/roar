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

#ifndef _CANVAS_WIDGET_HPP_
#define _CANVAS_WIDGET_HPP_

#include <wchar.h>

#include <functional>
#include <map>
#include <vector>

#include <QtWidgets/QOpenGLWidget>
#include <QtGui/QOpenGLFunctions>

#include "../librtl/rtldef.hpp"
#include "../libcanvas/Canvas.hpp"

/*
 * Public types
 */

class CanvasWidget : public QOpenGLWidget, protected QOpenGLFunctions {
	Q_OBJECT

public:
	typedef std::vector<std::vector<Canvas::COLOUR>>
				CHAR_MAP_ITEM;
	typedef std::map<wchar_t, CHAR_MAP_ITEM>
				CHAR_MAP;
	typedef enum event_type_e {
		ETYPE_NONE		= 0,
		ETYPE_KEYBOARD_PRESS	= 1,
		ETYPE_KEYBOARD_RELEASE	= 2,
		ETYPE_MOUSE_MOVE	= 3,
		ETYPE_MOUSE_PRESS	= 4,
		ETYPE_MOUSE_RELEASE	= 5,
		ETYPE_MOUSE_WHEEL	= 6,
	}			EVENT_TYPE;
	typedef std::function<bool(QKeyEvent *, QMouseEvent *, QWheelEvent *, EVENT_TYPE)>
				EVENT_DISPATCHER;
	typedef struct rect_either_s {
		Rtl::Either<bool, Canvas::POINT>
				p0;
		Canvas::POINT	p1;
	}			RECT_EITHER;

	CanvasWidget(QWidget *parent=nullptr, Canvas::SIZE cellSize={7, 13}, Canvas::SIZE sizeDefault={100, 35});
	bool focusNextPrevChild(bool next);
	bool import(Rtl::STATUS& pstatus, const std::wstring& data, Canvas::DATA_TYPE type);
	bool import(Rtl::STATUS& pstatus, Canvas::CELL_MAP& cells, Canvas::SIZE size);
	void keyPressEvent(QKeyEvent *event);
	void keyReleaseEvent(QKeyEvent *event);
	QSize minimumSizeHint() const override;
	void mouseMoveEvent(QMouseEvent *event);
	void mousePressEvent(QMouseEvent *event);
	void mouseReleaseEvent(QMouseEvent *event);
	Rtl::Either<bool, Canvas::RECT> renderCells(bool isCursor, const Canvas::CELL_LIST& cells);
	void setEventDispatcher(EVENT_DISPATCHER eventDispacher);
	QSize sizeHint() const override;
	void wheelEvent(QWheelEvent *event);

	Canvas			canvas;
	Canvas::SIZE		cellSize;
	CHAR_MAP		charMap;
	EVENT_DISPATCHER	eventDispatcher;
	QFont			font;
	QImage			image;
	QSize			imageSize;
	QWidget	*		parent;
	Canvas::SIZE		sizeDefault;

private:
	Canvas::CELL cellFetch(const Canvas::CELL& cell, bool fromCanvas);

protected:
	void initializeGL();
};

#endif /* _CANVAS_WIDGET_HPP_ */
