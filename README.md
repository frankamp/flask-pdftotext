```docker run -p 5000:5000 frankamp/flask-pdftotext``` 

to extract text:

curl -X PUT --data-binary @pdf-sample.pdf http://host_ip:5000/extract_stream

build!
