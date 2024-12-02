#!/bin/bash
# The set -e option instructs bash to immediately exit if any command [1] has a non-zero exit status.
# set -e
# set +e
# Affects variables. When set, a reference to any variable you haven't previously defined - with the exceptions of @ - is an error, and causes the program to immediately exit.
# set -u
# This setting prevents errors in a pipeline from being masked. If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline. By default, the pipeline's return code is that of the last command even if it succeeds.
# set -o pipefail
# set +o pipefail
# Enables a mode of the shell where all executed commands are printed to the terminal.
# set -x
# The IFS variable - which stands for Internal Field Separator - controls what Bash calls word splitting.
# IFS=$' '
# IFS=$'\n'
export MESSAGE="hello"
. ./b.sh
echo "[A] The message is: $MESSAGE"
# echo "A - The python message is: $PYMESSAGE"
# https://stackoverflow.com/questions/9772036/pass-all-variables-from-one-shell-script-to-another
