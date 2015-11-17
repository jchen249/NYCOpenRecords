"""
    public_records_portal.upload_helpers
    ~~~~~~~~~~~~~~~~

    Implements functions to upload files

"""

import os
import socket
from datetime import datetime
from werkzeug.utils import secure_filename

from public_records_portal import app
import sys
import datetime
import traceback
def should_upload():
    if app.config['ENVIRONMENT'] != 'LOCAL':
        return True
    elif 'UPLOAD_DOCS' in app.config:
        return True
    return False


# These are the extensions that can be uploaded:
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'rtf', 'odt', 'odp', 'ods', 'odg',
                      'odf',
                      'ppt', 'pps', 'xls', 'docx', 'pptx', 'ppsx', 'xlsx']
HOST=socket.gethostbyname(socket.gethostname())
SERVICE = app.config['SERVICE']
PORT = int(app.config['PORT'])


def get_download_url(doc_id, record_id=None):
    if not should_upload():
        return None


# @timeout(seconds=20)
def upload_file(document, request_id):
    """
    Takes an uploaded file, scans it using an ICAP Scanner, and stores the
    file if the scan passed
    :param document: File
    :type document:
    :param request_id: Current request
    :type request_id:
    :return:
    :rtype:
    """
    app.logger.info("\n\nLocal upload file")
    if not should_upload():
        app.logger.info("\n\nshoud not upload file")
        return '1', None  # Don't need to do real uploads locally
<<<<<<< HEAD
    if app.config["SHOULD_SCAN_FILES"]:
        if allowed_file(document.filename):
            app.logger.info("\n\nbegin file upload")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                print "Unable to bind socket and create connection to ICAP server."

            try:
                sock.connect((SERVICE, PORT))
            except socket.error, msg:
                print("[ERROR] %s\n" % msg[1])
                print("Unable to verify file for malware. Please try again.")
            print "----- RESPMOD -----"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                sys.stderr.write("[ERROR] %s\n" % msg[1])
                sys.exit(1)
            try:
                sock.connect((SERVICE, PORT))
            except socket.error, msg:
                sys.stderr.write("[ERROR] %s\n" % msg[1])
                sys.exit(2)
            today = datetime.date.today()
            cDate = today.strftime("%a, %d %b %Y")
            time = datetime.datetime.now()
            cTime = time.strftime("%H:%M:%S")
            sock.send( "RESPMOD %s ICAP/1.0\r\n" % ( SERVICE ) )
            sock.send( "Host: %s\r\n" % ( HOST ) )
            sock.send( "Encapsulated: req-hdr=0, res-hdr=137, res-body=296\r\n" )
            sock.send( "\r\n" )
            sock.send( "GET /origin-resource HTTP/1.1\r\n" )
            sock.send( "Host: www.origin-server.com\r\n" )
            sock.send( "Accept: text/html, text/plain, image/gif\r\n" )
            sock.send( "Accept-Encoding: gzip, compress\r\n" )
            sock.send( "\r\n" )
            sock.send( "HTTP/1.1 200 OK\r\n" )
            sock.send( "Date: "+cDate +" "+cTime+" GMT\r\n" )
            sock.send( "Server: Apache/1.3.6 (Unix)\r\n" )
            sock.send( 'ETag: "63840-1ab7-378d415b"\r\n' )
            sock.send( "Content-Type: text/html\r\n" )
            sock.send( "Content-Length: "+ str(len(document.read()))+"\r\n" )
            sock.send( "\r\n" )
            sock.send( "33\r\n" )
            sock.send(document.read()+"\r\n")
            sock.send( "0\r\n" )
            sock.send( "\r\n" )
            document.seek(0)
            try:
                data = sock.recv(1024)
                string = data
                print data
            except:
                print traceback.format_exc()
            if "200 OK"in string:
                app.logger.info("\n\n%s is allowed: %s" % (document.filename, string))
                filename = secure_filename(document.filename)
                upload_path = upload_file_locally(document, filename, request_id)
                return upload_path, filename
            else:
                app.logger.error("Malware detected. Upload failed")
                sock.close()
                return None, None
        return None, None
    sock.close()
    return "1", None
=======
    if allowed_file(document.filename):
        app.logger.info("\n\nbegin file upload")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print "Unable to bind socket and create connection to ICAP server."

        try:
            sock.connect((SERVICE, PORT))
        except socket.error, msg:
            print("[ERROR] %s\n" % msg[1])
            print("Unable to verify file for malware. Please try again.")
        print "----- RESPMOD -----"
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)
        try:
            sock.connect((SERVICE, PORT))
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(2)
        today = datetime.date.today()
        cDate = today.strftime("%a, %d %b %Y")
        time = datetime.datetime.now()
        cTime = time.strftime("%H:%M:%S")
        sock.send( "RESPMOD %s ICAP/1.0\r\n" % ( SERVICE ) )
        sock.send( "Host: %s\r\n" % ( HOST ) )
        sock.send( "Encapsulated: req-hdr=0, res-hdr=137, res-body=296\r\n" )
        sock.send( "\r\n" )
        sock.send( "GET /origin-resource HTTP/1.1\r\n" )
        sock.send( "Host: www.origin-server.com\r\n" )
        sock.send( "Accept: text/html, text/plain, image/gif\r\n" )
        sock.send( "Accept-Encoding: gzip, compress\r\n" )
        sock.send( "\r\n" )
        sock.send( "HTTP/1.1 200 OK\r\n" )
        sock.send( "Date: "+cDate +" "+cTime+" GMT\r\n" )
        sock.send( "Server: Apache/1.3.6 (Unix)\r\n" )
        sock.send( 'ETag: "63840-1ab7-378d415b"\r\n' )
        sock.send( "Content-Type: text/html\r\n" )
        sock.send( "Content-Length: "+ str(len(document.read()))+"\r\n" )
        sock.send( "\r\n" )
        sock.send( "33\r\n" )
        sock.send(document.read()+"\r\n")
        sock.send( "0\r\n" )
        sock.send( "\r\n" )
        document.seek(0)
        try:
            data = sock.recv(1024)
            string = data
            print data
        except:
            print traceback.format_exc()
        if "200 OK"in string:
            app.logger.info("\n\n%s is allowed: %s" % (document.filename, string))
            filename = secure_filename(document.filename)
            upload_path = upload_file_locally(document, filename, request_id)
            return upload_path, filename
        else:
            app.logger.error("Malware detected. Upload failed")
            return None, None
    return None, None
>>>>>>> 35317c20527fc790b148fe7b36bccfe0fac48c82


def upload_file_locally(document, filename, request_id):
    app.logger.info("\n\nuploading file locally")
    app.logger.info("\n\n%s" % (document))

    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    app.logger.info("\n\nupload path: %s" % (upload_path))

    document.save(upload_path)

    app.logger.info("\n\nfile uploaded to local successfully")

    return upload_path


### @export "allowed_file"
def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1]
    return ext in ALLOWED_EXTENSIONS
