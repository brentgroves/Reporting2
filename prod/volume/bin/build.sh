#!/bin/bash
rm JdbcAllTests.jar
rm -rf mobex
javac -verbose -d . ../src/mobex/test/*.java  
jar cvfm JdbcAllTests.jar manifest.txt mobex/test/*.class
