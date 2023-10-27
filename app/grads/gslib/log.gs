*
*  Write a log of GrADS commands entered from the console.
*
while (1)
  prompt 'ga> '
  pull cmd
  if (cmd='stop'); break; endif;
  cmd
  say result
  rc = write ("grads.log",cmd)
endwhile
