How to ensure previous Trial Balance script completes before executing the next one?
Father if you are willing please help me to answer this question :-)
Don't execute the script from the Reporting API. Instead insert it into the Report.report_queue table.
Have one process that checks the table and uses the wait command to run the report script.
Create another k8s deployment script in the Reporting reposistory called run-reports. 