# Reserved for options of what type of client to be, and starting the actual client thread

from client import host

def main():
    print("Executing host client")
    host_client = host.Host([0,0])
    host_client.execute()
if __name__ == '__main__':
    main()


