<!-- https://janakiev.com/blog/python-shell-commands/ -->

Python is a wonderful language for scripting and automating workflows and it is packed with useful tools out of the box with the Python Standard Library. A common thing to do, especially for a sysadmin, is to execute shell commands. But what usually will end up in a bash or batch file, can be also done in Python. You’ll learn here how to do just that with the os and subprocess modules.

Using the os Module
The first and the most straight forward approach to run a shell command is by using os.system():

import os
os.system('ls -l')

If you save this as a script and run it, you will see the output in the command line. The problem with this approach is in its inflexibility since you can’t even get the resulting output as a variable. You can read more about this function in the documentation.

Note, that if you run this function in Jupyter notebook, you won’t have an output inline. Instead you the inline output will be the return code of the executed programm (0 for successful and -1 for unsuccessful). You will find the output in the command line where you have started Jupyter notebook.

Next, the os.popen() command opens a pipe from or to the command line. This means that we can access the stream within Python. This is useful since you can now get the output as a variable:

import os
stream = os.popen('echo Returned output')
output = stream.read()
output