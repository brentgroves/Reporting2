#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python
#!/miniconda/bin/python # for docker image
#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
# https://raw.githubusercontent.com/rogalmic/vscode-bash-debug/gif/images/bash-debug-samp-launch-autoconfig.gif
# https://marketplace.visualstudio.com/items?itemName=rogalmic.bash-debug
# https://janakiev.com/blog/python-shell-commands/
# https://www.bogotobogo.com/python/python_subprocess_module.php
import os
import subprocess
# This only prints the return code of the command
# If you save this as a script and run it, you will see the output in the command line. 
# The problem with this approach is in its inflexibility since you can’t even get the resulting output as a variable. 
# You can read more about this function in the documentation.

print(os.system('pwd'))

# https://www.bogotobogo.com/python/python_subprocess_module.php
# os.system('command with args') passes the command and arguments to our system's shell. 
# By using this can actually run multiple commands at once and set up pipes and input/output redirections. :
os.system('echo $HOME > outfile')
f = open('outfile','r')
print(f.read())

# Next, the os.popen() command opens a pipe from or to the command line. This means that we can access the stream within Python. 
# This is useful since you can now get the output as a variable:

# To redirect a standard output of any command to another process, use the > symbol. To redirect a standard input of any command, use the < symbol.
# ls -al . > contents.txt
# tail -n 2 < contents.txt


# In Linux, the pipe command lets you sends the output of one command to another. Piping, as the term suggests, can redirect the standard output, input, or error of one process to another for further processing.
# The syntax for the pipe or unnamed pipe command is the | character between any two commands:
# Command-1 | Command-2 | …| Command-N
# Here, the pipe cannot be accessed via another session; it is created temporarily to accommodate the execution of Command-1 and redirect the standard output. It is deleted after successful execution.


# cat contents.txt | grep py
# Awk is a scripting language used for manipulating data and generating reports. The awk command programming language requires no compiling
# cat contents.txt | grep py | awk '{print $10}'
# cat contents.txt | wc -l'

# A named pipe can last until as long as the system is up and running or until it is deleted. It is a special file that follows the FIFO (first in, first out) mechanism. It can be used just like a normal file; i.e., you can write to it, read from it, and open or close it. To create a named pipe, the command is:
# mkfifo <pipe-name>
# This creates a named pipe file that can be used even over multiple shell sessions.
# Another way to create a FIFO named pipe is to use this command:
# mknod p <pipe-name>

# mkfifo my_named_pipe
# ls -al > my_named_pipe
# cat my_named_pipe

# Here, we have created a named pipe, my-named-pipe, and redirected the output of the ls -al command into the named pipe. 
# We can the open a new shell session and cat the contents of the named pipe, which shows the output of the ls -al command, as previously supplied. Notice the size of the named pipe is zero and it has a designation of "p".

# Pipe is used to pass output to another program or utility. Redirect is used to pass output to either a file or stream
# Next, the os.popen() command opens a pipe from or to the command line. This means that we can access the stream within Python. 
# This is useful since you can now get the output as a variable
stream = os.popen('echo Returned output')
output = stream.read()
print(output)

# When you use the .read() function, you will get the whole output as one string. You can also use the .readlines() function, 
# which splits each line (including a trailing \n). Note, that you can run them only once. It is also possible to write to the stream by using the mode='w' argument. To delve deeper into this function, have a look at the documentation.

# Open a pipe to or from command. The return value is an open file object connected to the pipe, 
# which can be read or written depending on whether mode is 'r' (default) or 'w'. The bufsize argument has the same meaning as 
# the corresponding argument to the built-in open() function. The exit status of the command (encoded in the format specified for wait()) 
# is available as the return value of the close() method of the file object, 
# except that when the exit status is zero (termination without errors), None is returned.

# Don't understand the write mode
# stream = os.popen('echo Returned output',mode='w')
# output = stream.write('test')
# print(output)

# Thank you Abba for the work you have given us to do!

# os.popen() does the same thing as os.system except that it gives us a file-like stream object that we can use to access standard input/output for that process. There are 3 other variants of popen that all handle the i/o slightly differently.
# If we pass everything as a string, then our command is passed to the shell; if we pass them as a list then we don't need to worry about escaping anything.
# However, it's been deprecated since version 2.6: This function is obsolete. Use the subprocess module. docs.python.org

# subprocess.call()
# This is basically just like the Popen class and takes all of the same arguments, but it simply wait until the command completes and 
# gives us the return code.

# subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
# Run the command described by args. Wait for command to complete, then return the returncode attribute.

os.chdir('/home/bgroves@BUSCHE-CNC.COM/src/python-train/how_to/run_shell_commands')
subprocess.call(['ls','-l'])
# The command line arguments are passed as a list of strings, which avoids the need for escaping quotes or other special characters 
# that might be interpreted by the shell.

# $PATH error no such file or directory because no shell expansion
# subprocess.call('echo $PATH')

subprocess.call('echo $PATH', shell=True)
# Setting the shell argument to a true value causes subprocess to spawn an intermediate shell process, and tell it to run the command. 
# In other words, using an intermediate shell means that variables, glob patterns, and other special shell features in the command string 
# are processed before the command is run. Here, in the example, $HOME was processed 
# before the echo command. Actually, this is the case of command with shell expansion while the command ls -l considered as a simple command.
result = subprocess.call('./main.sh', shell=True)
print(f'\nFrom run_shell_command.py -> result={result}')


