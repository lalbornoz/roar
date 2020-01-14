/*
 * GuiCanvasWxBackendFast.cpp
 * Copyright (c) 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
 */

#ifdef _MSC_VER
#pragma warning(disable : 4514)
#pragma warning(disable : 4530)
#pragma warning(disable : 4577)
#pragma warning(disable : 4706)
#pragma warning(disable : 4710)
#pragma warning(disable : 4711)
#pragma warning(disable : 4820)
#pragma warning(disable : 5045)
#endif /* _MSC_VER_ */

#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>

#include <chrono>
#include <cmath>
#include <map>
#include <vector>

#define PY_SSIZE_T_CLEAN	/* Make "s#" use Py_ssize_t rather than int. */
#include <Python.h>

/*
 * Private types
 */

typedef uint32_t		COLOUR;
#define COLOUR_ALPHA(colour)	(((colour) >> 24) & 0xff)

typedef uint64_t		COORD;

typedef struct point_s {
	COORD			x, y;
} POINT;
#define POINT_EMPTY		{0ULL, 0ULL}

typedef enum cell_attrs_e {
	CATTR_NONE		= 0x00,
	CATTR_BOLD		= 0x01,
	CATTR_UNDERLINE		= 0x02,
} CELL_ATTRS;

typedef struct cell_s {
	CELL_ATTRS		attrs;
	COLOUR			bg, fg;
	POINT			p;
	wchar_t			txt[8];
} CELL;
#define CELL_EMPTY		{CATTR_NONE, 0UL, 0UL, POINT_EMPTY, {L'\0',}}

typedef struct rect_s {
	POINT			p0, p1;
} RECT;
#define RECT_EMPTY		{POINT_EMPTY, POINT_EMPTY}
#define RECT_HEIGHT(r)		((r).p1.y - (r).p0.y)
#define RECT_WIDTH(r)		((r).p1.x - (r).p0.x)

typedef struct size_s {
	uint64_t		h, w;
} SIZE;
#define SIZE_EMPTY		{0ULL, 0ULL}

typedef std::vector<std::vector<uint8_t>>	COLOUR_LIST;
typedef std::vector<std::vector<COLOUR>>	CHAR_MAP_ITEM;
typedef std::map<wchar_t, CHAR_MAP_ITEM>	CHAR_MAP;

/*
 * Private constants and variables
 */

#define BITMAP_BPS		24
#define BITMAP_BPS_BYTES	3
#define BLEND_ALPHA_COEFFICIENT	0.8

static PyObject *s_bitmap = NULL, *s_dc = NULL, *s_dc_tmp = NULL, *s_font = NULL, *s_wx = NULL, *s_wx_NullBitmap = NULL;
static uint8_t *s_bitmap_buffer = NULL;
static size_t s_bitmap_buffer_size = 0;
static SIZE s_bitmap_size = SIZE_EMPTY, s_cell_size = SIZE_EMPTY;
static CHAR_MAP s_char_map;
static PyObject *s_colour_black = NULL, *s_colour_white = NULL;
static PyObject *s_error = NULL;

static COLOUR_LIST s_colours = {
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

static COLOUR_LIST s_colours_bold = {
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
 * Private preprocessor macros
 */

#define MAX(a,b)		(((a) > (b)) ? (a) : (b))
#define MIN(a,b)		(((a) < (b)) ? (a) : (b))

#define PYTHON_TRY(expr, msg)									\
	[&](){bool rc = (bool)(expr); if (!rc) { PyErr_SetString(s_error, msg); }; return rc;}()
#define PYTHON_TRY_NOMEMORY(expr, msg)								\
	[&](){bool rc = (bool)(expr); if (!rc) { PyErr_SetString(PyExc_MemoryError, msg); }; return rc;}()

/*
 * N.B.	required due to absence of Python_CallMethodV()
 */
#define COMMA	,
#define PYTHON_WRAP_METHOD(fn, fmt, args1, args2)						\
	static bool										\
	python_##fn(PyObject *obj, const char *default_error, PyObject **presult, args1)	\
	{											\
		bool rc = true;									\
		PyObject *result;								\
												\
		if ((result = PyObject_CallMethod(obj, #fn, fmt, args2))) {			\
			if (!presult) {								\
				Py_XDECREF(result);						\
			} else {								\
				*presult = result;						\
			}									\
		} else {									\
			rc = false;								\
			setErrorFromLast(default_error ? default_error				\
						       : "Failed to call " # fn "()");		\
		}										\
		return rc;									\
	}
#define PYTHON_WRAP_METHOD0(fn)									\
	static bool										\
	python_##fn(PyObject *obj, const char *default_error, PyObject **presult)		\
	{											\
		bool rc = true;									\
		PyObject *result;								\
												\
		if ((result = PyObject_CallMethod(obj, #fn, ""))) {				\
			if (!presult) {								\
				Py_XDECREF(result);						\
			} else {								\
				*presult = result;						\
			}									\
		} else {									\
			rc = false;								\
			setErrorFromLast(default_error ? default_error				\
						       : "Failed to call " # fn "()");		\
		}										\
		return rc;									\
	}

/*
 * Static private subroutine prototypes
 */

static COLOUR blendColours(COLOUR bg, COLOUR fg);
static void cellDraw(size_t bitmap_bps_bytes, uint8_t *bitmap_buffer, SIZE bitmap_size, CELL cell, SIZE cell_size, RECT *prect);
static bool cellDrawPixel(size_t bitmap_bps_bytes, uint8_t *bitmap_buffer, SIZE bitmap_size, CELL cell, SIZE cell_size, COLOUR colour, RECT *prect, COORD rx, COORD ry);
static bool cellDrawText(size_t bitmap_bps_bytes, uint8_t *bitmap_buffer, SIZE bitmap_size, CELL cell, SIZE cell_size, CHAR_MAP& char_map, RECT *prect);
static bool cellFetch(const COLOUR_LIST& colours, const COLOUR_LIST& colours_bold, PyObject *object, bool fromCanvas, POINT canvasPoint, CELL *pcell);
static void setErrorFromLast(const char *default_fmt, ...);
#ifdef TIMING
static std::chrono::system_clock::time_point timeBegin();
static double timeDelta(std::chrono::system_clock::time_point t0);
#endif /* TIMING */
static bool updateCharMap(SIZE cell_size, CHAR_MAP& char_map, wchar_t wch);

PYTHON_WRAP_METHOD(Bitmap, "lll", unsigned long long width COMMA unsigned long long height COMMA unsigned long long bits, width COMMA height COMMA bits);
PYTHON_WRAP_METHOD(Blit, "OllllOll", PyObject *self COMMA unsigned long long xdest COMMA unsigned long long ydest COMMA unsigned long long width COMMA unsigned long long height COMMA PyObject *source COMMA unsigned long long xsrc COMMA unsigned long long ysrc, self COMMA xdest COMMA ydest COMMA width COMMA height COMMA source COMMA xsrc COMMA ysrc);
PYTHON_WRAP_METHOD(Colour, "lll", unsigned long long red COMMA unsigned long long green COMMA unsigned long long blue, red COMMA green COMMA blue);
PYTHON_WRAP_METHOD(CopyFromBuffer, "Ol", PyObject *data COMMA unsigned long long format, data COMMA format);
PYTHON_WRAP_METHOD(CopyToBuffer, "Ol", PyObject *data COMMA unsigned long long format, data COMMA format);
PYTHON_WRAP_METHOD(DrawText, "u#ll", wchar_t *text COMMA size_t text_size COMMA unsigned long long x COMMA unsigned long long y, text COMMA text_size COMMA x COMMA y);
PYTHON_WRAP_METHOD0(MemoryDC);
PYTHON_WRAP_METHOD(SelectObject, "O", PyObject *bitmap, bitmap);
PYTHON_WRAP_METHOD(SetFont, "O", PyObject *font, font);
PYTHON_WRAP_METHOD(SetTextBackground, "O", PyObject *colour, colour);
PYTHON_WRAP_METHOD(SetTextForeground, "O", PyObject *colour, colour);

/*
 * Static private subroutines
 */

static COLOUR
blendColours(COLOUR bg, COLOUR fg)
{
	return (COLOUR)
		(std::llround(((fg & 0xff) * BLEND_ALPHA_COEFFICIENT) + ((bg & 0xff) * (1.0 - BLEND_ALPHA_COEFFICIENT))) |
		(std::llround((((fg >> 8) & 0xff) * BLEND_ALPHA_COEFFICIENT) + (((bg >> 8) & 0xff) * (1.0 - BLEND_ALPHA_COEFFICIENT))) << 8) |
		(std::llround((((fg >> 16) & 0xff) * BLEND_ALPHA_COEFFICIENT) + (((bg >> 16) & 0xff) * (1.0 - BLEND_ALPHA_COEFFICIENT))) << 16));
}

static void
cellDraw(size_t bitmap_bps_bytes, uint8_t *bitmap_buffer, SIZE bitmap_size, CELL cell, SIZE cell_size, RECT *prect)
{
	for (COORD ry = 0; ry < cell_size.h; ry++) {
		for (COORD rx = 0; rx < cell_size.w; rx++)
			cellDrawPixel(bitmap_bps_bytes, bitmap_buffer, bitmap_size, cell, cell_size, cell.bg, prect, rx, ry);
	}
	if (cell.attrs & CATTR_UNDERLINE) {
		for (COORD rx = 0, ry = (cell_size.h - 1); rx < cell_size.w; rx++)
			cellDrawPixel(bitmap_bps_bytes, bitmap_buffer, bitmap_size, cell, cell_size, cell.fg, prect, rx, ry);
	}
}

static bool
cellDrawPixel(size_t bitmap_bps_bytes, uint8_t *bitmap_buffer, SIZE bitmap_size, CELL cell, SIZE cell_size, COLOUR colour, RECT *prect, COORD rx, COORD ry)
{
	COORD offset, x_, y_;
	bool rc = false;
	
	x_ = (cell.p.x * cell_size.w) + rx, y_ = (cell.p.y * cell_size.h) + ry;
	offset = ((y_ * bitmap_size.w) + x_) * bitmap_bps_bytes;
	if ((x_ < bitmap_size.w) && (y_ < bitmap_size.h)) {
		prect->p0.x = MIN(prect->p0.x > 0 ? prect->p0.x : x_, x_);
		prect->p0.y = MIN(prect->p0.y > 0 ? prect->p0.y : y_, y_);
		prect->p1.x = MAX(prect->p1.x, x_+ 1); prect->p1.y = MAX(prect->p1.y, y_+ 1);
		bitmap_buffer[offset] = colour & 0xff;
		bitmap_buffer[offset + 1] = (colour >> 8) & 0xff;
		bitmap_buffer[offset + 2] = (colour >> 16) & 0xff;
		rc = true;
	}
	return rc;
}

static bool
cellDrawText(size_t bitmap_bps_bytes, uint8_t *bitmap_buffer, SIZE bitmap_size, CELL cell, SIZE cell_size, CHAR_MAP& char_map, RECT *prect)
{
	CHAR_MAP::iterator char_map_item;
	COLOUR colour;
	bool rc = true;

	for (size_t nch = 0; (nch < (sizeof(cell.txt) / sizeof(cell.txt[0]))) && (cell.txt[nch]); nch++) {
		if ((char_map_item = char_map.find(cell.txt[nch])) == char_map.end()) {
			if (updateCharMap(cell_size, char_map, cell.txt[nch]))
				char_map_item = char_map.find(cell.txt[nch]);
			else {
				rc = false; break;
			}
		}
		for (COORD ry = 0; ry < cell_size.h; ry++) {
			for (COORD rx = 0; rx < cell_size.w; rx++) {
				if ((char_map_item != char_map.end())
				&&  (char_map_item->second[ry][rx] != (COLOUR)0x0L))
					colour = cell.fg;
				else
					colour = cell.bg;
				cellDrawPixel(bitmap_bps_bytes, bitmap_buffer, bitmap_size, cell, cell_size, colour, prect, rx, ry);
			}
		}
	}
	if (cell.attrs & CATTR_UNDERLINE) {
		for (COORD rx = 0, ry = (cell_size.h - 1); rx < cell_size.w; rx++)
			cellDrawPixel(bitmap_bps_bytes, bitmap_buffer, bitmap_size, cell, cell_size, cell.fg, prect, rx, ry);
	}
	return rc;
}

static bool
cellFetch(const COLOUR_LIST& colours, const COLOUR_LIST& colours_bold, PyObject *object, bool fromCanvas, POINT canvasPoint, CELL *pcell)
{
	long bg, fg;
	PyObject *canvasMapRow, *cellObject = NULL, *txt;
	Py_ssize_t offset, txt_len;
	const COLOUR_LIST *pcolours;
	bool rc = false;

	if (fromCanvas) {
		offset = -2;
		if ((canvasMapRow = PyList_GetItem(object, (Py_ssize_t)canvasPoint.y)))
			cellObject = PyList_GetItem(canvasMapRow, (Py_ssize_t)canvasPoint.x);
	} else
		cellObject = object, offset = 0;
	if (cellObject && PyList_Check(cellObject) && (PyList_Size(cellObject) == 6 + offset)) {
		if (!fromCanvas) {
			pcell->p.x = PyLong_AsUnsignedLongLong(PyList_GetItem(cellObject, 0));
			pcell->p.y = PyLong_AsUnsignedLongLong(PyList_GetItem(cellObject, 1));
		}
		fg = PyLong_AsLong(PyList_GetItem(cellObject, 2 + offset));
		bg = PyLong_AsLong(PyList_GetItem(cellObject, 3 + offset));
		pcell->attrs = (CELL_ATTRS)PyLong_AsUnsignedLong(PyList_GetItem(cellObject, 4 + offset));
		if (pcell->attrs & CATTR_BOLD)
			pcolours = &colours_bold;
		else
			pcolours = &colours;
		pcell->bg = (bg == -1) ? 0xff000000 : (COLOUR)((colours[(uint8_t)bg][0]) | ((colours[(uint8_t)bg][1] << 8) & 0xff00) | ((colours[(uint8_t)bg][2] << 16) & 0xff0000));
		pcell->fg = (fg == -1) ? pcell->bg : (COLOUR)(((*pcolours)[(uint8_t)fg][0]) | (((*pcolours)[(uint8_t)fg][1] << 8) & 0xff00) | (((*pcolours)[(uint8_t)fg][2] << 16) & 0xff0000));
		txt = PyList_GetItem(cellObject, 5 + offset);
		if ((txt_len = PyUnicode_AsWideChar(txt, pcell->txt, sizeof(pcell->txt) / sizeof(pcell->txt[0]))) > 0) {
			if (txt_len < (sizeof(pcell->txt) / sizeof(pcell->txt[0])))
				pcell->txt[txt_len] = L'\0';
			rc = true;
		}
	}
	return rc;
}

static void
setErrorFromLast(const char *default_fmt, ...)
{
	va_list ap;
	static char default_buf[1024];
	PyObject *exc_traceback, *exc_type, *exc_value = NULL;

	PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
	if (exc_value)
		PyErr_SetObject(s_error, exc_value);
	else {
		va_start(ap, default_fmt);
		vsnprintf_s(default_buf, sizeof(default_buf), default_fmt, ap);
		va_end(ap);
		PyErr_SetString(s_error, default_buf);
	}
}

#ifdef TIMING
static std::chrono::system_clock::time_point
timeBegin()
{
	return std::chrono::system_clock::now();
}

static double
timeDelta(std::chrono::system_clock::time_point t0)
{
	return ((std::chrono::duration<double>)(std::chrono::system_clock::now() - t0)).count();
}
#endif /* TIMING */

static bool
updateCharMap(SIZE cell_size, CHAR_MAP& char_map, wchar_t wch)
{
	PyObject *bitmap, *mv = NULL;
	Py_buffer buffer;
	uint8_t *char_buffer = NULL;
	size_t char_buffer_size;
	bool rc = false;

	PyBuffer_FillInfo(&buffer, 0, NULL, 0, false, PyBUF_WRITABLE);
	char_buffer_size = s_cell_size.w * s_cell_size.h * BITMAP_BPS_BYTES;
	if (python_Bitmap(s_wx, NULL, &bitmap, s_cell_size.w, s_cell_size.h, BITMAP_BPS)
	&&  python_SelectObject(s_dc_tmp, NULL, NULL, bitmap)
	&&  python_SetFont(s_dc_tmp, NULL, NULL, s_font)
	&&  python_SetTextBackground(s_dc_tmp, NULL, NULL, s_colour_black)
	&&  python_SetTextForeground(s_dc_tmp, NULL, NULL, s_colour_white)
	&&  python_DrawText(s_dc_tmp, NULL, NULL, &wch, 1, 0, 0)
	&&  PYTHON_TRY_NOMEMORY((char_buffer = (uint8_t *)malloc(char_buffer_size)), "Failed to allocate character bitmap buffer")
	&&  PYTHON_TRY(PyBuffer_FillInfo(&buffer, 0, char_buffer, (Py_ssize_t)char_buffer_size, false, PyBUF_WRITABLE) == 0, "Failed to create Py_buffer")
	&&  PYTHON_TRY((mv = PyMemoryView_FromBuffer(&buffer)), "Failed to create Py_buffer memory view")
	&&  python_CopyToBuffer(bitmap, NULL, NULL, mv, 0)) {
		char_map[wch] = CHAR_MAP_ITEM(cell_size.h);
		for (COORD ry = 0; ry < cell_size.h; ry++) {
			for (COORD rx = 0; rx < cell_size.w; rx++)
				char_map[wch][ry].push_back(
					(((COLOUR)char_buffer[(((ry * cell_size.w) + rx) * BITMAP_BPS_BYTES)]) & 0xff) |
					(((COLOUR)char_buffer[(((ry * cell_size.w) + rx) * BITMAP_BPS_BYTES) + 1] << 8) & 0xff00) |
					(((COLOUR)char_buffer[(((ry * cell_size.w) + rx) * BITMAP_BPS_BYTES) + 2] << 16) & 0xff0000));
		}
		rc = true;
	}
	if (s_dc_tmp)
		python_SelectObject(s_dc_tmp, NULL, NULL, s_wx_NullBitmap);
	Py_XDECREF(bitmap);
	if (char_buffer) {
		free(char_buffer);
	}
	Py_XDECREF(mv); PyBuffer_Release(&buffer);
	return rc;
}

/*
 * Private Python module subroutine prototypes
 */

static PyObject *GuiCanvasWxBackendFast_drawPatches(PyObject *self, PyObject *args);
static PyObject *GuiCanvasWxBackendFast_init(PyObject *self, PyObject *args);
static PyObject *GuiCanvasWxBackendFast_resize(PyObject *self, PyObject *args);

/*
 * Private Python module subroutines
 */

static PyObject *
GuiCanvasWxBackendFast_drawPatches(PyObject *self, PyObject *args)
{
	PyObject *bitmap, *canvas_map, *canvas_size_obj, *eventDc, *patches;
	Py_buffer buffer;
	SIZE canvas_size;
	CELL cell, cell_canvas;
	bool isCursor, skip, status = true;
	PyObject *iter, *iter_cur, *mv = NULL, *rc = NULL;
	RECT rect = RECT_EMPTY;

	(void)self;
	PyBuffer_FillInfo(&buffer, 0, NULL, 0, false, PyBUF_WRITABLE);
#ifdef TIMING
	auto t0 = timeBegin();
#endif /* TIMING */
	if (PYTHON_TRY(PyArg_ParseTuple(args, "OOOOpO", &bitmap, &canvas_map, &canvas_size_obj, &eventDc, &isCursor, &patches), "Invalid arguments")
	&&  PYTHON_TRY((iter = PyObject_GetIter(patches)), "Failed to get patches iterator object")) {
		canvas_size.w = PyLong_AsUnsignedLong(PyList_GetItem(canvas_size_obj, 0));
		canvas_size.h = PyLong_AsUnsignedLong(PyList_GetItem(canvas_size_obj, 1));
		while (iter_cur = PyIter_Next(iter)) {
			skip = false, status = true;
			if (PYTHON_TRY(cellFetch(s_colours, s_colours_bold, iter_cur, false, POINT_EMPTY, &cell), "Failed to get patch cell")) {
				if (isCursor) {
					if (!(skip = !cellFetch(s_colours, s_colours_bold, canvas_map, true, cell.p, &cell_canvas))) {
						cell.attrs = cell_canvas.attrs;
						if (COLOUR_ALPHA(cell.bg) != 0xff) {
							cell.fg = blendColours(cell_canvas.fg, cell.bg); cell.bg = blendColours(cell_canvas.bg, cell.bg);
							if ((cell_canvas.txt[0] == L' ') && (COLOUR_ALPHA(cell_canvas.bg) == 0xff))
								cell.txt[0] = L'\u2591', cell.txt[1] = L'\0';
							else
								memcpy(cell.txt, cell_canvas.txt, sizeof(cell.txt));
						} else if (COLOUR_ALPHA(cell_canvas.bg) == 0xff) {
							cell.fg = cell_canvas.fg, cell.bg = cell_canvas.bg;
							if (cell_canvas.txt[0] == L' ')
								cell.txt[0] = L'\u2591', cell.txt[1] = L'\0';
							else
								memcpy(cell.txt, cell_canvas.txt, sizeof(cell.txt));
						} else {
							cell.fg = cell_canvas.fg, cell.bg = cell_canvas.bg;
							memcpy(cell.txt, cell_canvas.txt, sizeof(cell.txt));
						}
					}
				} else if ((cell.txt[0] == L' ') && (COLOUR_ALPHA(cell.bg) == 0xff))
					cell.bg = 0x00000000, cell.txt[0] = L'\u2591', cell.txt[1] = L'\0';
				if (status && !skip) {
					if (cell.txt[0] != L' ')
						status = cellDrawText(BITMAP_BPS_BYTES, s_bitmap_buffer, s_bitmap_size, cell, s_cell_size, s_char_map, &rect);
					else
						cellDraw(BITMAP_BPS_BYTES, s_bitmap_buffer, s_bitmap_size, cell, s_cell_size, &rect);
				}
			}
			Py_XDECREF(iter_cur);
		}
		Py_XDECREF(iter);
		if (status
		&&  PYTHON_TRY(PyBuffer_FillInfo(&buffer, 0, s_bitmap_buffer, (Py_ssize_t)s_bitmap_buffer_size, false, PyBUF_WRITABLE) == 0, "Failed to create Py_buffer")
		&&  PYTHON_TRY((mv = PyMemoryView_FromBuffer(&buffer)), "Failed to create Py_buffer memory view")
		&&  python_CopyFromBuffer(s_bitmap, NULL, NULL, mv, 0)
		&&  python_Blit((PyObject *)eventDc->ob_type, NULL, NULL, eventDc, rect.p0.x, rect.p0.y, RECT_WIDTH(rect), RECT_HEIGHT(rect), s_dc, rect.p0.x, rect.p0.y)) {
			Py_INCREF(Py_True), rc = Py_True;
		}
	}
#ifdef TIMING
	printf("drawing took %.2f ms\n", timeDelta(t0) * 1000);
#endif /* TIMING */
	Py_XDECREF(mv); PyBuffer_Release(&buffer);
	return rc;
}

static PyObject *
GuiCanvasWxBackendFast_init(PyObject *self, PyObject *args)
{
	PyObject *colour_black = NULL, *colour_white = NULL, *dc = NULL, *dc_tmp = NULL, *wx = NULL, *wx_NullBitmap = NULL;
	PyObject *rc = NULL, *wx_dict;

	(void)self;
	if (PYTHON_TRY(PyArg_ParseTuple(args, "O", &wx), "Invalid arguments")
	&&  PYTHON_TRY((wx_dict = PyModule_GetDict(wx)), "Failed to get wx module dictionary")
	&&  python_Colour(wx, NULL, &colour_black, 0, 0, 0)
	&&  python_Colour(wx, NULL, &colour_white, 255, 255, 255)
	&&  python_MemoryDC(wx, NULL, &dc)
	&&  python_MemoryDC(wx, NULL, &dc_tmp)
	&&  PYTHON_TRY((wx_NullBitmap = PyObject_GetAttrString(wx, "NullBitmap")), "Failed to get wx.NullBitmap attribute")) {
		s_colour_black = colour_black, s_colour_white = colour_white, s_dc = dc, s_dc_tmp = dc_tmp;
		s_wx = wx; Py_INCREF(wx_NullBitmap), s_wx_NullBitmap = wx_NullBitmap;
		Py_INCREF(Py_True), rc = Py_True;
	}
	if (!rc) {
		Py_XDECREF(colour_black); Py_XDECREF(colour_white); Py_XDECREF(dc); Py_XDECREF(dc_tmp); Py_XDECREF(wx_NullBitmap);
	}
	return rc;
}

static PyObject *
GuiCanvasWxBackendFast_resize(PyObject *self, PyObject *args)
{
	uint8_t *bitmap_buffer_new = NULL;
	size_t bitmap_buffer_size_new;
	PyObject *bitmap_new = NULL;
	SIZE bitmap_size_new, cell_size_new;
	PyObject *cellSize, *cellSizeHeightObj, *cellSizeWidthObj, *font, *winSize, *winSizeHeightObj, *winSizeWidthObj, *rc = NULL;

	(void)self;
	if (PYTHON_TRY(PyArg_ParseTuple(args, "OOO", &cellSize, &font, &winSize) && PyTuple_Check(cellSize) && PyTuple_Check(winSize), "Invalid arguments")) {
		cellSizeWidthObj = PyTuple_GetItem(cellSize, 0); cellSizeHeightObj = PyTuple_GetItem(cellSize, 1);
		cell_size_new.w = PyLong_AsUnsignedLong(cellSizeWidthObj); cell_size_new.h = PyLong_AsUnsignedLong(cellSizeHeightObj);
		winSizeWidthObj = PyTuple_GetItem(winSize, 0); bitmap_size_new.w = PyLong_AsUnsignedLong(winSizeWidthObj);
		winSizeHeightObj = PyTuple_GetItem(winSize, 1); bitmap_size_new.h = PyLong_AsUnsignedLong(winSizeHeightObj);
		bitmap_buffer_size_new = bitmap_size_new.h * bitmap_size_new.w * BITMAP_BPS_BYTES;
		if (python_Bitmap(s_wx, NULL, &bitmap_new, bitmap_size_new.w, bitmap_size_new.h, BITMAP_BPS)
		&&  (s_bitmap ? python_SelectObject(s_dc, NULL, NULL, s_wx_NullBitmap) : true)
		&&  python_SelectObject(s_dc, NULL, NULL, bitmap_new)
		&&  PYTHON_TRY_NOMEMORY((bitmap_buffer_new = (uint8_t *)malloc(bitmap_buffer_size_new)), "Failed to allocate bitmap buffer")) {
			if (s_bitmap_buffer)
				free(s_bitmap_buffer);
			s_bitmap_buffer = bitmap_buffer_new;
			Py_XDECREF(s_bitmap); s_bitmap = bitmap_new;
			s_bitmap_buffer_size = bitmap_buffer_size_new, s_bitmap_size = bitmap_size_new;
			if ((cell_size_new.h != s_cell_size.h) || (cell_size_new.w != s_cell_size.w))
				s_char_map.clear();
			s_cell_size = cell_size_new; Py_INCREF(font), s_font = font; Py_INCREF(Py_True), rc = Py_True;
		}
	}
	if (!rc) {
		if (bitmap_buffer_new)
			free(bitmap_buffer_new);
		Py_XDECREF(bitmap_new); Py_XDECREF(font);
	}
	return rc;
}

/*
 * Python C/C++ extension footer
 */

static PyMethodDef
GuiCanvasWxBackendFast_methods[] = {
	{"drawPatches", GuiCanvasWxBackendFast_drawPatches, METH_VARARGS, "drawPatches"},
	{"init", GuiCanvasWxBackendFast_init, METH_VARARGS, "init"},
	{"resize", GuiCanvasWxBackendFast_resize, METH_VARARGS, "resize"},
	{NULL, NULL, 0, NULL},
};

static struct PyModuleDef
GuiCanvasWxBackendFastmodule = {
	PyModuleDef_HEAD_INIT, "GuiCanvasWxBackendFast", NULL, -1, GuiCanvasWxBackendFast_methods,
};

PyMODINIT_FUNC
PyInit_GuiCanvasWxBackendFast(void)
{
	PyObject *m = NULL;

	m = PyModule_Create(&GuiCanvasWxBackendFastmodule);
	s_error = PyErr_NewException("GuiCanvasWxBackendFast.error", NULL, NULL);
	Py_XINCREF(s_error);
	if (PyModule_AddObject(m, "error", s_error) < 0) {
		Py_XDECREF(s_error); Py_CLEAR(s_error); Py_DECREF(m); m = NULL;
	}
	return m;
}
