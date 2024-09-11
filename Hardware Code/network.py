import socket
import ServeMachine as serve
import time

HOST = ''  
PORT = 12345 # Same port as used by the laptop

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind to the port
    s.bind((HOST, PORT))
    
    s.listen()
    
    # Accept a connection
    conn, addr = s.accept()
    
    with conn:
        print('Connected by', addr)
        
        while True:
            # Receive data from the laptop
            data = conn.recv(1024)
            message = data.decode().strip() 
            
            print('Received:', message)
            
            while len(message) > 0:
                currentMessage = message[:5]
                message = message[5:]
            
                print(currentMessage)
            # Check if the received message is 'stop'
                #if currentMessage == 'stop-':
                    #print("Stopping...")
                    #break  
                
                if currentMessage == 'Freq+':
                    serve.IncFrequency()
                if currentMessage == 'Freq-':
                    serve.DecFrequency()
                    
                if currentMessage == 'Osci+':
                    serve.IncOscillation()
                if currentMessage == 'Osci-':
                    serve.DecOscillation()
                    
                if currentMessage == 'Tops+':
                    serve.IncTopspin()
                if currentMessage == 'Tops-':
                    serve.DecTopspin()
                    
                if currentMessage == 'Back+':
                    serve.IncBackspin()
                if currentMessage == 'Back-':
                    serve.DecBackspin()
                time.sleep(0.15)
            
