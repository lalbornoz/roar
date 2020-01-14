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

#include <algorithm>
#include <execution>

#include <QtGui/QFontDatabase>
#include <QtGui/QPainter>
#include <QtGui/QPaintEvent>

#include "CanvasWidget.hpp"

/*
 * Private constants and variables
 */

#define BLEND_ALPHA_COEFFICIENT	0.8

static const Canvas::COLOUR_LIST s_colours = {
	{255, 255, 255},	// Bright White
	{0,   0,   0},		// Black
	{0,   0,   187},	// Light Blue
	{0,   187, 0},		// Green
	{255, 85,  85},		// Red
	{187, 0,   0},		// Light Red
	{187, 0,   187},	// Pink
	{187, 187, 0},		// Yellow
	{255, 255, 85},		// Light Yellow
	{85,  255, 85},		// Light Green
	{0,   187, 187},	// Cyan
	{85,  255, 255},	// Light Cyan
	{85,  85,  255},	// Blue
	{255, 85,  255},	// Light Pink
	{85,  85,  85},		// Grey
	{187, 187, 187},	// Light Grey
};

static const Canvas::COLOUR_LIST s_colours_bold = {
	{255, 255, 255},	// Bright White
	{85, 85, 85},		// Black
	{85, 85, 255},		// Light Blue
	{85, 255, 85},		// Green
	{255, 85, 85},		// Red
	{255, 85, 85},		// Light Red
	{255, 85, 255},		// Pink
	{255, 255, 85},		// Yellow
	{255, 255, 85},		// Light Yellow
	{85, 255, 85},		// Light Green
	{85, 255, 255},		// Cyan
	{85, 255, 255},		// Light Cyan
	{85, 85, 255},		// Blue
	{255, 85, 255},		// Light Pink
	{85, 85, 85},		// Grey
	{255, 255, 255},	// Light Grey
};

/*
 * Public class functions
 */

CanvasWidget::CanvasWidget(
	QWidget *	parent,
	Canvas::SIZE	cellSize,
	Canvas::SIZE	sizeDefault
)
: QOpenGLWidget(parent), canvas(sizeDefault), cellSize(cellSize), charMap(), eventDispatcher(), parent(parent), sizeDefault(sizeDefault)
{
	this->font = QFont("DejaVu Sans Mono", 8); // XXX
	this->font.setStyleStrategy(QFont::PreferAntialias);
	this->imageSize = QSize(this->canvas.size.w * this->cellSize.w, this->canvas.size.h * this->cellSize.h);
	this->image = QImage(this->imageSize.width(), this->imageSize.height(), QImage::Format_RGB32);
	this->setAutoFillBackground(false);
}

Rtl::Either<bool, Canvas::RECT>
CanvasWidget::renderCells(
	bool				isCursor,
	const Canvas::CELL_LIST&	cells
)
{
	Canvas::CELL			cell_, cell_canvas;
	Rtl::Either<bool, Canvas::RECT>	rc(true, Canvas::RECT());
	CanvasWidget::RECT_EITHER	rectEither{Rtl::Either<bool, Canvas::POINT>(false, Canvas::POINT()), Canvas::POINT()};

#ifdef TIMING
	auto t0 = Rtl::timeBegin();
#endif /* TIMING */
	for (auto& cell : cells) {
		cell_ = this->cellFetch(cell, false);
		if ((cell_.p.x >= this->canvas.size.w) || (cell_.p.y >= this->canvas.size.h))
			continue;
		else if (isCursor) {
			cell_canvas = this->cellFetch(cell, true); cell_.attrs = cell_canvas.attrs;
			if (COLOUR_ALPHA(cell_.bg) != 0xff) {
//				cell_.fg = this->blendColours(cell_canvas.fg, cell_.bg, BLEND_ALPHA_COEFFICIENT);
//				cell_.bg = this->blendColours(cell_canvas.bg, cell_.bg, BLEND_ALPHA_COEFFICIENT);
				if ((cell_canvas.txt[0] == L' ') && (COLOUR_ALPHA(cell_canvas.bg) == 0xff))
					cell_.txt[0] = L'\u2591', cell_.txt[1] = L'\0';
				else
					memcpy(cell_.txt, cell_canvas.txt, sizeof(cell_.txt));
			} else if (COLOUR_ALPHA(cell_canvas.bg) == 0xff) {
				cell_.fg = cell_canvas.fg, cell_.bg = cell_canvas.bg;
				if (cell_canvas.txt[0] == L' ')
					cell_.txt[0] = L'\u2591', cell_.txt[1] = L'\0';
				else
					memcpy(cell_.txt, cell_canvas.txt, sizeof(cell_.txt));
			} else {
				cell_.fg = cell_canvas.fg, cell_.bg = cell_canvas.bg;
				memcpy(cell_.txt, cell_canvas.txt, sizeof(cell_.txt));
			}
		} else if ((cell_.txt[0] == L' ') && (COLOUR_ALPHA(cell_.bg) == 0xff))
			cell_.bg = 0x00000000, cell_.txt[0] = L'\u2591', cell_.txt[1] = L'\0';
#if 0
		if ((cell_.txt[0] != L' ') && (cell_.txt[0] != L'_'))
			this->cellDrawText(cell_, rectEither);
		else
			this->cellDraw(cell_, rectEither);
		if (cell.attrs & Canvas::CATTR_UNDERLINE)
			this->cellDrawLine(cell_, rectEither);
#endif
	}
	if (rc)
		rc.right.p0 = rectEither.p0.right, rc.right.p1 = rectEither.p1;
	return rc;
}

bool
CanvasWidget::focusNextPrevChild(
	bool	next
)
{
	(void)next;
	return false;
}

bool
CanvasWidget::import(
	Rtl::STATUS&		pstatus,
	const std::wstring&	data,
	Canvas::DATA_TYPE	type
)
{
	if (this->canvas.import(pstatus, data, type)) {
		this->imageSize = QSize(this->canvas.size.w * this->cellSize.w, this->canvas.size.h * this->cellSize.h);
		this->image = QImage(this->imageSize.width(), this->imageSize.height(), QImage::Format_RGB32);
		this->resize(this->imageSize);
		for (auto row : this->canvas.cells)
			this->renderCells(false, row);
		this->update();
	}
	return (bool)pstatus;
}

bool
CanvasWidget::import(
	Rtl::STATUS&		pstatus,
	Canvas::CELL_MAP&	cells,
	Canvas::SIZE		size
)
{
	if (this->canvas.import(pstatus, cells, size)) {
		this->imageSize = QSize(this->canvas.size.w * this->cellSize.w, this->canvas.size.h * this->cellSize.h);
		this->image = QImage(this->imageSize.width(), this->imageSize.height(), QImage::Format_RGB32);
		this->resize(this->imageSize);
		for (auto row : this->canvas.cells)
			this->renderCells(false, row);
		this->update();
	}
	return (bool)pstatus;
}

void
CanvasWidget::keyPressEvent(
	QKeyEvent * event
)
{
	if (this->eventDispatcher)
		this->eventDispatcher(event, nullptr, nullptr, CanvasWidget::ETYPE_KEYBOARD_PRESS);
}

void
CanvasWidget::keyReleaseEvent(
	QKeyEvent * event
)
{
	if (this->eventDispatcher)
		this->eventDispatcher(event, nullptr, nullptr, CanvasWidget::ETYPE_KEYBOARD_RELEASE);
}

QSize
CanvasWidget::minimumSizeHint(
) const
{
	return this->imageSize;
}

void
CanvasWidget::mouseMoveEvent(
	QMouseEvent * event
)
{
	if (this->eventDispatcher)
		this->eventDispatcher(nullptr, event, nullptr, CanvasWidget::ETYPE_MOUSE_MOVE);
}

void
CanvasWidget::mousePressEvent(
	QMouseEvent * event
)
{
	if (this->eventDispatcher)
		this->eventDispatcher(nullptr, event, nullptr, CanvasWidget::ETYPE_MOUSE_PRESS);
}

void
CanvasWidget::mouseReleaseEvent(
	QMouseEvent *	event
)
{
	if (this->eventDispatcher)
		this->eventDispatcher(nullptr, event, nullptr, CanvasWidget::ETYPE_MOUSE_RELEASE);
}

void
CanvasWidget::setEventDispatcher(
	EVENT_DISPATCHER	eventDispatcher
)
{
	this->eventDispatcher = eventDispatcher;
}

QSize
CanvasWidget::sizeHint(
) const
{
	return this->imageSize;
}

void
CanvasWidget::wheelEvent(
	QWheelEvent *	event
)
{
	if (this->eventDispatcher)
		this->eventDispatcher(nullptr, nullptr, event, CanvasWidget::ETYPE_MOUSE_WHEEL);
}

/*
 * Private class methods
 */

Canvas::CELL
CanvasWidget::cellFetch(
	const Canvas::CELL&	cell,
	bool			fromCanvas
)
{
	Canvas::CELL			cell_;
	const Canvas::COLOUR_LIST *	pcolours;

	if (!fromCanvas)
		cell_ = Canvas::CELL(cell);
	else
		cell_ = this->canvas.cells[cell.p.y][cell.p.x];
	if (cell_.attrs & Canvas::CATTR_BOLD)
		pcolours = &s_colours_bold;
	else
		pcolours = &s_colours;
	if ((cell_.txt[0] == L'_') && (cell_.txt[1] == L'\0'))
		cell_.attrs = (Canvas::CELL_ATTRS)(cell_.attrs | Canvas::CATTR_UNDERLINE);
	cell_.bg = (cell_.bg == -1) ? 0xff000000 : (Canvas::COLOUR)(((s_colours[(uint8_t)cell_.bg][0] & 0xff) << 16) | ((s_colours[(uint8_t)cell_.bg][1] & 0xff) << 8) | ((s_colours[(uint8_t)cell_.bg][2] & 0xff)));
	cell_.fg = (cell_.fg == -1) ? cell_.bg : (Canvas::COLOUR)((((*pcolours)[(uint8_t)cell_.fg][0] & 0xff) << 16) | (((*pcolours)[(uint8_t)cell_.fg][1] & 0xff) << 8) | (((*pcolours)[(uint8_t)cell_.fg][2] & 0xff)));
	return cell_;
}

/*
 * Protected class methods
 */

#if 0
static const char *vertexShaderSource =
    "attribute highp vec4 posAttr;\n"
    "attribute lowp vec4 colAttr;\n"
    "varying lowp vec4 col;\n"
    "uniform highp mat4 matrix;\n"
    "void main() {\n"
    "   col = colAttr;\n"
    "   gl_Position = matrix * posAttr;\n"
    "}\n";

static const char *fragmentShaderSource =
    "varying lowp vec4 col;\n"
    "void main() {\n"
    "   gl_FragColor = col;\n"
    "}\n";
#endif

void
CanvasWidget::initializeGL(
)
{
	this->initializeOpenGLFunctions();
#if 0
	glClearColor(0, 0, 0, m_transparent ? 0 : 1);

	m_program = new QOpenGLShaderProgram;
	m_program->addShaderFromSourceCode(QOpenGLShader::Vertex, m_core ? vertexShaderSourceCore : vertexShaderSource);
	m_program->addShaderFromSourceCode(QOpenGLShader::Fragment, m_core ? fragmentShaderSourceCore : fragmentShaderSource);
	m_program->bindAttributeLocation("vertex", 0);
	m_program->bindAttributeLocation("normal", 1);
	m_program->link();

	m_program->bind();
	m_projMatrixLoc = m_program->uniformLocation("projMatrix");
	m_mvMatrixLoc = m_program->uniformLocation("mvMatrix");
	m_normalMatrixLoc = m_program->uniformLocation("normalMatrix");
	m_lightPosLoc = m_program->uniformLocation("lightPos");

	// Create a vertex array object. In OpenGL ES 2.0 and OpenGL 2.x
	// implementations this is optional and support may not be present
	// at all. Nonetheless the below code works in all cases and makes
	// sure there is a VAO when one is needed.
	m_vao.create();
	QOpenGLVertexArrayObject::Binder vaoBinder(&m_vao);

	// Setup our vertex buffer object.
	m_logoVbo.create();
	m_logoVbo.bind();
	m_logoVbo.allocate(m_logo.constData(), m_logo.count() * sizeof(GLfloat));

	// Store the vertex attribute bindings for the program.
	setupVertexAttribs();

	// Our camera never changes in this example.
	m_camera.setToIdentity();
	m_camera.translate(0, 0, -1);

	// Light position is fixed.
	m_program->setUniformValue(m_lightPosLoc, QVector3D(0, 0, 70));

	m_program->release();
#endif
}