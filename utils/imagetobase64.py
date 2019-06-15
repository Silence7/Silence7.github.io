import sys
import base64

def main(argv):
    if len(argv) < 1:
        print "imagetobase64.py filepath"
    print argv[0]
    f=open(argv[0],'rb')
    code =base64.b64encode(f.read())
    f.close()
    print code

if __name__ == "__main__":
    main(sys.argv[1:])

