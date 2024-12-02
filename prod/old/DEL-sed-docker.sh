#!/bin/bash
app=$1


printf "\nsed-docker param 1: $1" 
printf "\nsed-docker app: $1" 



# sed '/pattern/s/^#//' -i file


if [[ $1 == "etl" ]]; then
    echo "etl"
    sed '/ENTRYPOINT \["cron", "-f"\]/s/^[ \t]*#[ \t]*//' -i dockerfile
    sed '/EXPOSE 5000/s/^[ \t]*/#&/' -i dockerfile    
    sed '/CMD \["flask", "run", "--host=0.0.0.0", "--port=5000" \]/s/^[ \t]*/#&/' -i dockerfile    
fi 
if [[ $app == "api" ]]; then
    echo "api"
    sed '/EXPOSE 5000/s/^[ \t]*#[ \t]*//' -i dockerfile
    sed '/CMD \["flask", "run", "--host=0.0.0.0", "--port=5000" \]/s/^[ \t]*#[ \t]*//' -i dockerfile
    sed '/ENTRYPOINT \["cron", "-f"\]/s/^[ \t]*/#&/' -i dockerfile

fi


# sed '/ENTRYPOINT ["cron", "-f"]/s/^#//' -i dockerfile

# sed '/EXPOSE 5000/s/^#//' -i dockerfile
# sed '/CMD ["flask", "run", "--host=0.0.0.0", "--port=5000" ]/s/^#//' -i dockerfile

# sed s/%APP%/$app/g \
#  deployment-template.yaml | \
# sed s/%VER%/$ver/g > base/deployment.yaml 
