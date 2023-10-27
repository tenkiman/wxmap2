c         
      parameter (im=480, lm=18, lpout=21) 
      parameter (jm= im/2, im2= im/2,  jm2= jm/2) 
      parameter (jtrun= 2*((1+(im-1)/3)/2),  mlmax= (jtrun+1)*jtrun/2)
      parameter (imlm=im*lm,  imjm=im*jm,  idim2= mlmax*2)  
      parameter (mllm= idim2*lm,  lmm1= lm-1,  lmp1= lm+1,  lmm2= lm-2)         
      parameter (zero=0.0,one=1.0,two=2.0,three=3.0,four=4.0,haf= 0.5)
c
      parameter (mlx= (jtrun/2)*((jtrun+1)/2))
      parameter (jump= im+3)
c
      parameter (nshist=lm*8+2)
      parameter (nc3sp= lm+2)
      parameter (ncnosv= 14)
      parameter (nc3grd= 10+ncnosv)
      parameter (numave= 20+21*lm)  
