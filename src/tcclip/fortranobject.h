#ifndef Py_FORTRANOBJECT_H
#define Py_FORTRANOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

#include "Python.h"
#define PY_ARRAY_UNIQUE_SYMBOL PyArray_API
#include "Numeric/arrayobject.h"

/* Fortran object interface */

/*
123456789-123456789-123456789-123456789-123456789-123456789-123456789-12

PyFortranObject represents various Fortran objects:
Fortran (module) routines, COMMON blocks, module data. 

Author: Pearu Peterson <pearu@ioc.ee>
*/

#define F2PY_MAX_DIMS 40
typedef struct {
  char *name;                /* attribute (array||routine) name */
  int rank;                  /* array rank, 0 for scalar, max is F2PY_MAX_DIMS,
				|| rank=-1 for Fortran routine */
  struct {int d[F2PY_MAX_DIMS];} dims;  /* dimensions of the array, || not used */
  int type;                  /* PyArray_<type> || not used */
  char *data;                /* pointer to array || Fortran routine */
  void (*func)();            /* initialization function for
				allocatable arrays:
				func(&rank,dims,set_ptr_func,name,len(name))
				|| C/API wrapper for Fortran routine */
  char *doc;                 /* documentation string; only recommended
				for routines. */
} FortranDataDef;

typedef struct {
  PyObject_HEAD
  int len;                   /* Number of attributes */
  FortranDataDef *defs;      /* An array of FortranDataDef's */ 
  PyObject       *dict;      /* Fortran object attribute dictionary */
} PyFortranObject;

extern DL_IMPORT(PyTypeObject) PyFortran_Type;

#define PyFortran_Check(op) ((op)->ob_type == &PyFortran_Type)
  
extern DL_IMPORT(PyObject *) PyFortranObject_New(FortranDataDef* defs, void (*init)());
extern DL_IMPORT(PyObject *) PyFortranObject_NewAsAttr(FortranDataDef* defs);

typedef void *(*f2pycfunc)();
  
#ifdef __cplusplus
}
#endif
#endif /* !Py_FORTRANOBJECT_H */
