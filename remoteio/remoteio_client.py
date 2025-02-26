import socket

class RemoteServer:
    def __init__(self, server_ip, server_port):
        """        Initialize the client with the server IP and port.

        Args:
            server_ip (str): The IP address of the server.
            server_port (int): The port number of the server.


        Raises:
            OSError: If the connection to the server fails.
        """

        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

    def pin(self, pin_number, numbering='b'):
        """        Return a RemotePin object for the specified pin number and numbering scheme.

        This method returns a RemotePin object that represents the specified pin number and numbering scheme.

        Args:
            pin_number (int): The pin number to be accessed.
            numbering (str): The numbering scheme for the pin. Default is 'b'.

        Returns:
            RemotePin: An object representing the specified pin number and numbering scheme.
        """

        return RemotePin(self.client_socket, pin_number, numbering)

    def close(self):
        """        Closes the client socket connection.

        This method closes the client socket connection.
        """

        self.client_socket.close()

class RemotePin:
    
    def __init__(self, client_socket, pin_number, numbering):
        """        Initialize the object with client socket, pin number, and numbering.

        Args:
            client_socket (socket): The client socket object.
            pin_number (int): The pin number for the object.
            numbering (int): The numbering for the object.
        """

        self.client_socket = client_socket
        self.pin_number = pin_number
        self.numbering = numbering
        self.time_ms = 0

    def __create_command(self, command:str, time_ms:int=0):
        """        Create a command with an optional time delay.

        This function creates a command string by combining the given command with an optional time delay in milliseconds.

        Args:
            command (str): The base command to be executed.
            time_ms (int?): The time delay in milliseconds. Defaults to 0.

        Returns:
            str: The constructed command string.
        """

        cmd = f"{command} {time_ms}"
        return cmd
    
    def __send_command(self, command):
        """        Send a command to the client socket.

        This method constructs a command using the instance's numbering and pin_number attributes,
        and then sends the command to the client socket.

        Args:
            command (str): The command to be sent to the client socket.
        """

        command = f"{self.numbering} {self.pin_number} {command}"
        self.client_socket.sendall(command.encode())
    
    def on(self, time_ms:int=0):
        """        Turn on the device for a specified duration.

        This method sends a command to turn on the device for a specified duration in milliseconds.

        Args:
            time_ms (int?): The duration in milliseconds for which the device should be turned on. Defaults to 0.

        Returns:
            self: The current instance of the device.
        """

        cmd = self.__create_command("on", time_ms)
        self.__send_command(cmd)
        return self
    
    def blink(self):
        """        Execute the blink command.

        This method creates a command to execute the blink action and sends the command to the device.

        Returns:
            self: The instance of the class.
        """

        cmd = self.__create_command("blink")
        self.__send_command(cmd)
        return self
    
    def pulse(self):
        """        Send a pulse command to the device.

        This method creates a pulse command using the private method __create_command,
        sends the command using the private method __send_command, and returns the instance of the object.

        Returns:
            object: The instance of the object.
        """

        cmd = self.__create_command("pulse")
        self.__send_command(cmd)
        return self

    def off(self):
        """        Turn off the device.

        This method creates a command to turn off the device and sends the command to the device.

        Returns:
            self: The current instance of the device.
        """

        cmd = self.__create_command("off")
        self.__send_command(cmd)
        return self




# Example usage:
if __name__ == "__main__":
    server_ip = "192.168.0.90"
    server_port = 8509

    remote_server = RemoteServer(server_ip, server_port)
    remote_pin = remote_server.pin(8, 'b')
    remote_pin.on(time_ms=2000) # Time in ms until switch off
    remote_pin.blink()
    remote_pin.on()  # Turn on the pin with the applied settings
    remote_pin.off()  # Turn off the pin
    remote_server.close()
 
