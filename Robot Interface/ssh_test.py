from fabric import Connection

def run_remote_command(host, username, password, command):
    # Establish the SSH connection
    connection = Connection(host=host, user=username, connect_kwargs={"password": password})
    
    # Run the command and stream the output line by line
    result = connection.run(command, hide=False, pty=True)
    
    # Loop through the output in real-time
    for line in result.stdout:
        print(line, end="")  # Print each line as it is received
    
    connection.close()


# Example usage
host = 'raspberrypi.local'
port = 22
username = 'liam'
password = 'F@g_Proj'
command = 'python3 /home/liam/Documents/Python\ Scripts/hx711py/example.py'

run_remote_command(host, username, password, command)