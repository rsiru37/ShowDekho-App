import asyncore
from smtpd import DebuggingServer

def run_debugging_server():
    server = DebuggingServer(('localhost', 1025), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run_debugging_server()
