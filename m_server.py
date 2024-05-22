from http.server import HTTPServer, CGIHTTPRequestHandler, SimpleHTTPRequestHandler
import urllib, json, time, curses
import RPi.GPIO as GPIO

sHandler = ''

class MotorRequestHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        #self.send_response(200)
        #self.send_header('content-type','text/html')
        #self.end_headers()
        #if self.path == '/':
        #    self.path = '/web/'
        return SimpleHTTPRequestHandler.do_GET(self)
        #self.wfile.write('Python HTTP Webserver Tutorial'.encode())
    
    def do_POST(self):
        print(self.headers)
        length = int(self.headers['Content-Length'])
        d = self.rfile.read(length).decode('utf-8')
        print('d:')
        print(d)
        #post_data = urllib.parse.parse_qs(d)
        #print(post_data)
        handlePostData(d)
        self.send_response(200, "ok")
        self.end_headers()
        
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")        
        self.end_headers()
    
def setDuty(d):
    global sHandler
    #print('Setting duty: %s' %d)
    sHandler.ChangeDutyCycle(d)
    #time.sleep(2)
    
def handleCommand(cmd, sleep):
    #print('Handling command: %s' %cmd)
    if cmd == 'dn':
        setDuty(9)
    elif cmd == 'up':
        setDuty(5)
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
    while pwm < 25:
        setDuty(pwm)
        pwm = pwm + 1;
    
def handlePostData(post_data):
    global sHandler
    print('pd:')
    #post_data = '\"' + post_data +'\"'
    print(post_data)
    jx = json.loads(post_data)
    for key in jx.keys():
        if key == 'cmd':
            handleCommand(jx[key], float(jx['dur']))

    #data = post_data["payload"]
    #print('d:')
    #print(data)
    #for x in post_data:
    #    jx = json.loads(x)
    #    for key in jx.keys():
    #        if key == 'cmd':
    #            handleCommand(jx[key], float(jx['dur']))
        

def keyListen(stdscr):
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:
            
            if c == 259:
                handleCommand('up', 0.08)
                stdscr.addstr('up   ')
            elif c == 258:
                handleCommand('dn', 0.08)
                stdscr.addstr('down ')
            else:
                # print numeric value
                stdscr.addstr(str(c) + ' ')
                
            stdscr.refresh()
            # return curser to start position
            stdscr.move(0, 0)

def main():
    
    setupMotors()
    
    #curses.wrapper(keyListen)
    
    PRT = 8110
    serv = HTTPServer(('',PRT), MotorRequestHandler)
    serv.allow_reuse_address = True
    print('Motor server started on port %s' %PRT)
    serv.serve_forever()
    
if __name__ == '__main__':
    #print('Starting')
    main()
