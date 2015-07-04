import os
from flask import Flask, request, redirect, url_for, Response, stream_with_context
import subprocess
import uuid
import logging    
UPLOAD_FOLDER = '/tmp'
app = Flask(__name__)
app.logger.setLevel(logging.INFO)



def get_temp_file():
    return UPLOAD_FOLDER + "/myfile_%s" % (uuid.uuid4())

@app.route('/extract_full', methods=['PUT'])
def extract_full():
    file_path = get_temp_file()
    with open(file_path, 'wb') as f:
        f.write(request.get_data())
    with os.popen('/usr/bin/pdftotext %s -' % file_path) as p:
        output = p.read()
    os.remove(file_path)
    return output


@app.route('/extract_stream', methods=['PUT', 'GET'])
def extract_stream():
    file_path = get_temp_file()
    with open(file_path, 'wb') as f:
        f.write(request.get_data())
    def generate():
        p = subprocess.Popen(['/usr/bin/pdftotext', file_path, "-"], stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, ''):
            yield line
        os.remove(file_path)
    return Response(generate(), mimetype="text/plain")

# # This is my attempt at streaming both the input and output at the same time
# # it fails with this error. Apparently the executable can't do it, confirmed by trying
# # it on the command line like: pdftotext - < pdf-sample.pdf
# # Command Line Error: You have to provide an output filename when reading form stdin.
# import threading
# class WriterThread(threading.Thread):
#     def __init__(self, stream, target):
#         threading.Thread.__init__(self)
#         self.target = target
#         self.stream = stream
#     def get_chunk(self):
#         return self.stream.read(1024 * 10)
#     def run(self):
#         for chunk in iter(self.get_chunk, ''):
#             app.logger.info("writing chunk")
#             self.target.write(chunk)
#         self.target.close()

# @app.route('/extract_stream_both', methods=['PUT', 'GET'])
# def extract_stream_both():
#     app.logger.info("running both thing!")
#     def generate():
#         app.logger.info("generating...")
#         p = subprocess.Popen(['/usr/bin/pdftotext', "-"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#         writer_thread = WriterThread(request.stream, p.stdin)
#         writer_thread.start()
#         app.logger.info("reading line...")
#         for line in iter(p.stdout.readline, ''):
#             app.logger.info("reading line")
#             yield line

#     return Response(stream_with_context(generate()), mimetype="text/plain")

app.run(host="0.0.0.0", debug=True)