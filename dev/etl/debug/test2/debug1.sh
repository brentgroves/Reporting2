#!/bin/bash
# python debug1.py
# ./debug2.sh

# sends err to file and time to $var
exec 3>error-msg 4>dbg-msg 5>error-num 6>tm-msg 7>final

out=$( 

  tm=$( cd ./subfolder1; TIMEFORMAT='%R'; \
      { 
        time source ./debug2.sh 2>&3 1>&4 ; \
      } 2>&1; 
    );
  echo "time=$tm" 1>&6; 
);
# read -r tm <&6       # read the first 3 characters from fd 5.
# # read -n 3 tm <&6       # read the first 3 characters from fd 5.
# echo "time=$tm" 

exec 3>&- 4>&- 5>&- 6>&- 7>&-
exec 3<error-msg 4<dbg-msg 5<error-num 6<tm-msg 7<final
read -r tm <&6       # read the first 3 characters from fd 5.
echo "time=$tm" 

while IFS= read -r emline
do
  em="${em}"$'\n'"${emline}"  
  #  p="${var1}"$'\n'"${var2}"
  # echo "$line"
done <&3
echo "em = $em"

while IFS= read -r line
do
  dm="${dm}"$'\n'"${line}"  
  #  p="${var1}"$'\n'"${var2}"
  # echo "$line"
done <&4
echo "dm = $dm"
read -r error <&5       # read the first 3 characters from fd 5.
# read -n 3 tm <&6       # read the first 3 characters from fd 5.
echo "error=$error"

exec 3<&- 4<&- 5<&- 6>&- 7<&-

# tm=$( TIMEFORMAT='%R'; \
#           { 
#             time source ./debug2.sh; \
#           } 2>&1; 
#         );
# echo "time=$tm"