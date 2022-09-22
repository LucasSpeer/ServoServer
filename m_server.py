from http.server import HTTPServer, CGIHTTPRequestHandler
import urllib, json, time
import RPi.GPIO as GPIO

sHandler = ''

class MotorRequestHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write('Python HTTP Webserver Tutorial'.encode())
    
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        #print(post_data)
        handlePostData(post_data)
        self.send_response(200)
        self.end_headers()
    
def setDuty(d):
    global sHandler
    #print('Setting duty: %s' %d)
    sHandler.ChangeDutyCycle(d)
    #time.sleep(2)
    
def handleCommand(cmd, sleep):
    #print('Handling command: %s' %cmd)
    if cmd == 'dn':
        setDuty(17)
    elif cmd == 'up':
        setDuty(2)
    time.sleep(sleep)
    setDuty(0)
        
def setupMotors():
    global sHandler
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.OUT)
    sHandler = GPIO.PWM(12, 50)
    sHandler.start(0)
    #time.sleep(1)
    #testLoop()
    
def testLoop():
    global sHandler
    pwm = 0;
    while pwm < 40:
        setDuty(pwm)
        pwm = pwm + 2;
    
def handlePostData(post_data):
    global sHandler
    data = post_data["payload"]
    print(data)
    for x in data:
        jx = json.loads(x)
        for key in jx.keys():
            if key == 'cmd':
                handleCommand(jx[key], float(jx['dur']))
            

def main():
    setupMotors()
    
    PRT = 8110
    serv = HTTPServer(('',PRT), MotorRequestHandler)
    print('Motor server started on port %s' %PRT)
    serv.serve_forever()
    
if __name__ == '__main__':
    print('Starting')
    main()
