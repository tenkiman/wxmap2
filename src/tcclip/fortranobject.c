#include "fortranobject.h"

/*
  Implementation of FortranObject.
  
  Author: Pearu Peterson <pearu@ioc.ee>
  $Revision: 1.5 $
  $Date: 2000/09/18 12:21:58 $
*/

/*     Here starts Travis Oliphant's contribution  (from f2py)   */
#define INCREMENT(ret_ind, nd, max_ind) \
{ \
  int k; \
  k = (nd) - 1; \
  if (k<0) (ret_ind)[0] = (max_ind)[0]; else \
  if (++(ret_ind)[k] >= (max_ind)[k]) { \
    while (k >= 0 && ((ret_ind)[k] >= (max_ind)[k]-1)) \
      (ret_ind)[k--] = 0; \
    if (k >= 0) (ret_ind)[k]++; \
    else (ret_ind)[0] = (max_ind)[0]; \
  }  \
}
#define CALCINDEX(indx, nd_index, strides, ndim) \
{ \
  int i; \
  indx = 0; \
  for (i=0; i < (ndim); i++)  \
    indx += nd_index[i]*strides[i]; \
} 
static int copy_ND_array(PyArrayObject *in, PyArrayObject *out)
{

  /* This routine copies an N-D array in to an N-D array out where both
     can be discontiguous.  An appropriate (raw) cast is made on the data.
  */

  /* It works by using an N-1 length vector to hold the N-1 first indices 
     into the array.  This counter is looped through copying (and casting) 
     the entire last dimension at a time.
  */

  int *nd_index, indx1;
  int indx2, last_dim;
  int instep, outstep;

  if (0 == in->nd) {
    in->descr->cast[out->descr->type_num]((void *)in->data,1,(void *)out->data,1,1);
    return 0;
  }
  nd_index = (int *)calloc(in->nd-1,sizeof(int));
  last_dim = in->nd - 1;
  instep = in->strides[last_dim] / in->descr->elsize;
  outstep = out->strides[last_dim] / out->descr->elsize;
  if (NULL == nd_index ) {
     fprintf(stderr,"Could not allocate memory for index array.\n");
     return -1;
  }
  while(nd_index[0] != in->dimensions[0]) {
    CALCINDEX(indx1,nd_index,in->strides,in->nd-1);
    CALCINDEX(indx2,nd_index,out->strides,out->nd-1);
    /* Copy (with an appropriate cast) the last dimension of the array */
    (in->descr->cast[out->descr->type_num])((void *)(in->data+indx1),instep,(void *)(out->data+indx2),outstep,in->dimensions[last_dim]); 
    INCREMENT(nd_index,in->nd-1,in->dimensions);
  }
  free(nd_index);
  return 0;
} 
/* EOF T.O.'s contib */

static PyArrayObject *arr_from_pyobj(int type,int *dims,int rank,PyObject *obj) {
  PyArrayObject *self = NULL;
  PyArrayObject *self_cp = NULL;
  int i;
  if (obj == Py_None)
    self = (PyArrayObject *)PyArray_FromDims(rank,dims,type);
  else 
    self = (PyArrayObject *)PyArray_ContiguousFromObject(obj,type,0,0);
  if ((self == NULL) && PyArray_Check(obj)) { /* if could not cast safely in above */
    int loc_rank = ((PyArrayObject *)obj)->nd;
    int *loc_dims = ((PyArrayObject *)obj)->dimensions;
    self = (PyArrayObject *)PyArray_FromDims(loc_rank,loc_dims,type);
  }
  if (self==NULL)
    goto fail;
  self_cp = self;
  if (!(rank==self->nd)) {
    int u_dim = -1, dims_s = 1, self_s = (self->nd)?PyArray_Size((PyObject *)self):1;
    for(i=0;i<rank;i++)
      if (dims[i]<1)
        if (u_dim<0) u_dim = i;
        else dims[i] = 1;
      else dims_s *= dims[i];
    if (u_dim >= 0) {
      dims[u_dim] = self_s/dims_s;
      dims_s *= dims[u_dim];
    }
    if (self_s != dims_s) {
      fprintf(stderr,"arr_from_pyobj: expected rank-%d array but got rank-%d array with different size.\n",rank,self->nd);
    goto fail;
    }
    self = (PyArrayObject *)PyArray_FromDimsAndDataAndDescr(rank, dims,self_cp->descr,self_cp->data);
    if (self == NULL)
      goto fail;
    Py_INCREF(self_cp);
    self->base = (PyObject *)self_cp;
  }
  for (i=0;i<rank;i++)
    if (dims[i]>self->dimensions[i]) {
      fprintf(stderr,"arr_from_pyobj: %d-th dimension must be at least %d but got %d.\n",i+1,dims[i],self->dimensions[i]);
      goto fail;
    }
  if (((PyObject *)self_cp != obj) && PyArray_Check(obj)) {
    if (copy_ND_array((PyArrayObject *)obj,self_cp)) {
      fprintf(stderr,"arr_from_pyobj: failed to copy object to rank-%d array with shape (",self_cp->nd);
      for(i=0;i<self_cp->nd;i++) fprintf(stderr,"%d,",self_cp->dimensions[i]);
      fprintf(stderr,")\n");
      goto fail;
    }
  }
  if (self != NULL)
    return self;
 fail:
  PyErr_SetString(PyExc_TypeError,"getting array from Python object");
  Py_XDECREF(self);
  return NULL;
}

typedef PyObject *(*fortranfunc)(PyObject *,PyObject *,PyObject *,void *);

PyObject *
PyFortranObject_New(FortranDataDef* defs,void (*init)()) {
  int i;
  PyFortranObject *fp = NULL;
  PyObject *v = NULL;
  if (init!=NULL)                           /* Initialize F90 module objects */
    (*(init))();
  if ((fp = PyObject_NEW(PyFortranObject, &PyFortran_Type))==NULL) return NULL;
  if ((fp->dict = PyDict_New())==NULL) return NULL;
  fp->len = 0;
  while (defs[fp->len].name != NULL) fp->len++;
  if (fp->len == 0) goto fail;
  fp->defs = defs;
  for (i=0;i<fp->len;i++)
    if (fp->defs[i].rank == -1) {                      /* Is Fortran routine */
      v = PyFortranObject_NewAsAttr(&(fp->defs[i]));
      if (v==NULL) return NULL;
      PyDict_SetItemString(fp->dict,fp->defs[i].name,v);
    } else
      if ((fp->defs[i].data)!=NULL) { /* Is Fortran variable or array (not allocatable) */
	v = PyArray_FromDimsAndData(fp->defs[i].rank,
				    fp->defs[i].dims.d,
				    fp->defs[i].type,
				    fp->defs[i].data);
	if (v==NULL) return NULL;
	PyDict_SetItemString(fp->dict,fp->defs[i].name,v);
      }
  Py_XDECREF(v);
  return (PyObject *)fp;
 fail:
  Py_XDECREF(v);
  return NULL;
}

PyObject *
PyFortranObject_NewAsAttr(FortranDataDef* defs) { /* used for calling F90 module routines */
  PyFortranObject *fp;
  fp = PyObject_NEW(PyFortranObject, &PyFortran_Type);
  if (fp == NULL) return NULL;
  if ((fp->dict = PyDict_New())==NULL) return NULL;
  fp->len = 1;
  fp->defs = defs;
  return (PyObject *)fp;
}

/* Fortran methods */

static void
fortran_dealloc(PyFortranObject *fp) {
  Py_XDECREF(fp->dict);
  PyMem_DEL(fp);
}


static PyMethodDef fortran_methods[] = {
	{NULL,		NULL}		/* sentinel */
};



static PyObject *
fortran_doc (FortranDataDef def) {
  char *p;
  PyObject *s;
  int i,size=100;
  if (def.doc!=NULL)
    size += strlen(def.doc);
  p = malloc (size);
  if (sprintf(p,"%s - ",def.name)==0) goto fail;;    
  if (def.rank==-1) {
    if (def.doc==NULL) {
      if (sprintf(p,"%sno docs available",p)==0)
	goto fail;
    } else {
      if (sprintf(p,"%s%s",p,def.doc)==0)
	goto fail;
    }
  } else {
    PyArray_Descr *d = PyArray_DescrFromType(def.type);
    if (sprintf(p,"%s'%c'-",p,d->type)==0) goto fail;
    if (def.data==NULL) {
      if (sprintf(p,"%sarray(not allocated)",p)==0) goto fail;
    } else {
      if (def.rank>0) {
	if (sprintf(p,"%sarray(%d",p,def.dims.d[0])==0) goto fail;
	for(i=1;i<def.rank;i++)
	  if (sprintf(p,"%s,%d",p,def.dims.d[i])==0) goto fail;
	if (sprintf(p,"%s)",p)==0) goto fail;
      } else {
	if (sprintf(p,"%sscalar",p)==0) goto fail;
      }
    }
  }
  if (sprintf(p,"%s\n",p)==0) goto fail;
  if (strlen(p)>size) {
    fprintf(stderr,"fortranobject.c:fortran_doc:len(p)=%d>%d(size): too long doc string required, increase size\n",strlen(p),size);
    goto fail;
  }
  if ((s = PyString_FromString(p))==NULL) return NULL;
  free(p);
  Py_INCREF(s);
  return s;
 fail:
  free(p);
  return NULL;
}

static FortranDataDef *save_def; /* save pointer of an allocatable array */
static void set_data(char *d,int *f) {  /* callback from Fortran */
  if (*f)                               /* In fortran f=allocated(d) */
    save_def->data = d;
  else
    save_def->data = NULL;
  /* printf("set_data: d=%p,f=%d\n",d,*f); */
}

static PyObject *
fortran_getattr(PyFortranObject *fp, char *name) {
  int i,j,k;
  if (fp->dict != NULL) {
    PyObject *v = PyDict_GetItemString(fp->dict, name);
    if (v != NULL) {
      Py_INCREF(v);
      return v;
    }
  }
  for (i=0,j=1;i<fp->len && (j=strcmp(name,fp->defs[i].name));i++);
  if (j==0)
    if (fp->defs[i].rank!=-1) {                   /* F90 allocatable array */ 
      if (fp->defs[i].func==NULL) return NULL;
      for(k=0;k<fp->defs[i].rank;k++) fp->defs[i].dims.d[k]=-1;
      save_def = &fp->defs[i];
      (*(fp->defs[i].func))(&fp->defs[i].rank,fp->defs[i].dims.d,set_data);
      if (fp->defs[i].data !=NULL) {              /* array is allocated */
	PyObject *v = PyArray_FromDimsAndData(fp->defs[i].rank,
					      fp->defs[i].dims.d,
					      fp->defs[i].type,
					      fp->defs[i].data
					      );
	if (v==NULL) return NULL; 
	Py_INCREF(v);
	return v;
      } else {                                    /* array is not allocated */
	Py_INCREF(Py_None);
	return Py_None;
      }
    }
  if (strcmp(name,"__dict__")==0) {
    Py_INCREF(fp->dict);
    return fp->dict;
  }
  if (strcmp(name,"__doc__")==0) {
    PyObject *s = PyString_FromString("");
    for (i=0;i<fp->len;i++)
      PyString_ConcatAndDel(&s,fortran_doc(fp->defs[i]));
    Py_INCREF(s);
    return s;
  }
  return Py_FindMethod(fortran_methods, (PyObject *)fp, name);
 fail:
  return NULL;
}

static int
fortran_setattr(PyFortranObject *fp, char *name, PyObject *v) {
  int i,j;
  PyArrayObject *arr;
  for (i=0,j=1;i<fp->len && (j=strcmp(name,fp->defs[i].name));i++);
  if (j==0) {
    if (fp->defs[i].rank==-1) {
      PyErr_SetString(PyExc_AttributeError,"over-writing fortran routine");
      return -1;
    }
    if (fp->defs[i].func!=NULL) { /* is allocatable array */
      int dims[F2PY_MAX_DIMS],k;
      save_def = &fp->defs[i];
      if (v!=Py_None) {     /* set new value (reallocate if needed --
			       see f2py generated code for more
			       details ) */
	for(k=0;k<fp->defs[i].rank;k++) dims[k]=-1;
	if ((arr = arr_from_pyobj(fp->defs[i].type,dims,fp->defs[i].rank,v))==NULL)
	  return -1;
	(*(fp->defs[i].func))(&fp->defs[i].rank,arr->dimensions,set_data);
      } else {             /* deallocate */
	for(k=0;k<fp->defs[i].rank;k++) dims[k]=0;
	(*(fp->defs[i].func))(&fp->defs[i].rank,dims,set_data);
	for(k=0;k<fp->defs[i].rank;k++) dims[k]=-1;
      }
      memcpy(fp->defs[i].dims.d,dims,fp->defs[i].rank*sizeof(int));
    } else {                     /* not allocatable array */
      if ((arr = arr_from_pyobj(fp->defs[i].type,fp->defs[i].dims.d,fp->defs[i].rank,v))==NULL)
	return -1;      
    }
    if (fp->defs[i].data!=NULL) { /* copy Python object to Fortran array */
      int s = _PyArray_multiply_list(fp->defs[i].dims.d,arr->nd);
      if (s==-1)
	s = _PyArray_multiply_list(arr->dimensions,arr->nd);
      if (s<0) return -1;
      if ((memcpy(fp->defs[i].data,arr->data,s*arr->descr->elsize))==NULL) return -1;
    } else return (fp->defs[i].func==NULL?-1:0);
    return 0; /* succesful */
  }
  if (fp->dict == NULL) {
    fp->dict = PyDict_New();
    if (fp->dict == NULL)
      return -1;
  }
  if (v == NULL) {
    int rv = PyDict_DelItemString(fp->dict, name);
    if (rv < 0)
      PyErr_SetString(PyExc_AttributeError,"delete non-existing fortran attribute");
    return rv;
  }
  else
    return PyDict_SetItemString(fp->dict, name, v);
}

static PyObject*
fortran_call(PyFortranObject *fp, PyObject *arg, PyObject *kw) {
  int i = 0;
  /*  printf("fortran call
      name=%s,func=%p,data=%p,%p\n",fp->defs[i].name,
      fp->defs[i].func,fp->defs[i].data,&fp->defs[i].data); */
  if (fp->defs[i].rank==-1) /* is Fortran routine */
    if ((fp->defs[i].func==NULL) || (fp->defs[i].data==NULL))
      return NULL;
    else
      return (*((fortranfunc)(fp->defs[i].func)))((PyObject *)fp,arg,kw,
						  (void *)fp->defs[i].data);
  PyErr_Format(PyExc_TypeError, "this fortran object is not callable");
  return NULL;
}


PyTypeObject PyFortran_Type = {
  PyObject_HEAD_INIT(&PyType_Type)
  0,			/*ob_size*/
  "fortran",			/*tp_name*/
  sizeof(PyFortranObject),	/*tp_basicsize*/
  0,			/*tp_itemsize*/
  /* methods */
  (destructor)fortran_dealloc, /*tp_dealloc*/
  0,			/*tp_print*/
  (getattrfunc)fortran_getattr, /*tp_getattr*/
  (setattrfunc)fortran_setattr, /*tp_setattr*/
  0,			/*tp_compare*/
  0,			/*tp_repr*/
  0,			/*tp_as_number*/
  0,			/*tp_as_sequence*/
  0,			/*tp_as_mapping*/
  0,			/*tp_hash*/
  (ternaryfunc)fortran_call,                    /*tp_call*/
};
