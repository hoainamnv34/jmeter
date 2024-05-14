jmeter -Dlog_level.jmeter=DEBUG -JTARGET_HOST=172.17.0.1 -JTARGET_PORT=8081 -H 172.17.0.1 -P 8083  -n -t ./HTTP_Request.jmx -l ./HTTP_Request.jtl -j ./jmeter.log -e -o ./securityreport
jmeter -Dlog_level.jmeter=DEBUG  -n -t /root/tests/test-file/HTTP_Request.jmx -l /root/tests/jmeter-report/HTTP_Request.jtl -j /root/tests/jmeter-report/jmeter.log -e -o /root/tests/jmeter-report/output

python3 pen-test-app.py --target "http://127.0.0.1:8081/" --zap-host "http://127.0.0.1:8083" --zap-host-ssh "http://127.0.0.1:8083"

docker run hoainamnv34/jmeter:0.0.2 --target "http://172.17.0.1:8081" --zap-host "http://172.17.0.1:8083"