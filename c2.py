import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))

try:
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(message, end="")

        if "أدخل اسم الحساب وكلمة المرور" in message or "أدخل المبلغ" in message or "اختر خيارًا" in message:
            user_input = input()
            client_socket.send(user_input.encode())

finally:
    client_socket.close()