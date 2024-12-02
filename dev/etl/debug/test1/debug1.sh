#!/bin/bash
# python debug1.py
# ./debug2.sh

tm=$( TIMEFORMAT='%R'; \
          { 
            time source ./debug2.sh; \
          } 2>&1; 
        );
echo "time=$tm"
