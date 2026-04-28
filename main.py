
import time
from server import connectionHandler, serverLogic
from server import positionBroadcast

def main():

    connect = connectionHandler.ThreadConnection()
    connect.start()

    server_thread_check = False

    while True:
        # menuCall() here
        if connect.game_state.startFlag() and not server_thread_check:
            print("Launching game...")
            positionBroadcast.positionBroadcastThread(connect.clientList, connect.game_state) # Thread for updating positions for all clients
            serverLogic.serverToClientThread(connect.clientList, connect.game_state) # Thread for enabling client to client communication using the server
            server_thread_check = True

           
        time.sleep(0.001) # Reserved for broadcast

if __name__ == '__main__':
    main()
