```docker run -p 5000:5000 frankamp/flask-pdftotext``` 

to extract text:

curl -X PUT --data-binary @pdf-sample.pdf http://host_ip:5000/extract_stream

build!

really basic load testing...

while true; do curl -X PUT --data-binary @pdf-sample.pdf http://192.168.99.100:5000/extract_stream > /dev/null; done