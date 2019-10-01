#define PY_SSIZE_T_CLEAN	/* Make "s#" use Py_ssize_t rather than int. */
#include <Python.h>

static PyObject *
GuiCanvasWxBackendFast_drawPatches(PyObject *self, PyObject *args)
{
	Py_RETURN_NONE;
}

static PyMethodDef
GuiCanvasWxBackendFast_methods[] = {
	{"drawPatches", GuiCanvasWxBackendFast_drawPatches, METH_VARARGS, "XXX"},
	{NULL, NULL, 0, NULL},
};

static struct PyModuleDef
GuiCanvasWxBackendFastmodule = {
	PyModuleDef_HEAD_INIT, "GuiCanvasWxBackendFast", NULL, -1, GuiCanvasWxBackendFast_methods,
};

PyMODINIT_FUNC
PyInit_GuiCanvasWxBackendFast(void)
{
	return PyModule_Create(&GuiCanvasWxBackendFastmodule);
}