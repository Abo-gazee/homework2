import socket
import threading

# قائمة الحسابات البنكية المحددة مسبقًا
bank_accounts = [
    {"name": "Ali", "password": "123", "balance": 5000},
    {"name": "Alaa", "password": "1234", "balance": 1000},
    {"name": "Isaa", "password": "12345", "balance": 7500}
]


# تابع للعثور على حساب حسب الاسم وكلمة المرور
def find_account(name, password):
    for account in bank_accounts:
        if account["name"] == name and account["password"] == password:
            return account
    return None


# تابع للتعامل مع كل عميل
def handle_client(client_socket, client_address):
    print(f"عميل جديد متصل من {client_address}")

    authenticated = False
    account = None

    # حلقة التحقق من الهوية
    while not authenticated:
        client_socket.send("أدخل اسم الحساب وكلمة المرور (مفصولين بمسافة): ".encode())
        credentials = client_socket.recv(1024).decode().strip().split()

        if len(credentials) == 2:
            name, password = credentials
            account = find_account(name, password)
            if account:
                authenticated = True
                client_socket.send("تم التحقق بنجاح.\n".encode())
            else:
                client_socket.send("اسم الحساب أو كلمة المرور غير صحيحة. حاول مرة أخرى.\n".encode())
        else:
            client_socket.send("الإدخال غير صحيح. حاول مرة أخرى.\n".encode())

    # حلقة العمليات
    while True:
        client_socket.send("اختر خيارًا (1: فحص الرصيد، 2: إيداع، 3: سحب، 4: إنهاء): ".encode())
        option = client_socket.recv(1024).decode().strip()

        if option == "1":
            balance = account["balance"]
            client_socket.send(f"رصيدك هو: {balance:.2f}\n".encode())
        elif option == "2":
            client_socket.send("أدخل المبلغ للإيداع: ".encode())
            amount = float(client_socket.recv(1024).decode().strip())
            account["balance"] += amount
            client_socket.send(f"تم الإيداع بنجاح. الرصيد الجديد هو: {account['balance']:.2f}\n".encode())
        elif option == "3":
            client_socket.send("أدخل المبلغ للسحب: ".encode())
            amount = float(client_socket.recv(1024).decode().strip())
            if amount > account["balance"]:
                client_socket.send("لا توجد أموال كافية.\n".encode())
            else:
                account["balance"] -= amount
                client_socket.send(f"تم السحب بنجاح. الرصيد الجديد هو: {account['balance']:.2f}\n".encode())
        elif option == "4":
            client_socket.send(f"الرصيد النهائي هو: {account['balance']:.2f}\nوداعًا!\n".encode())
            break
        else:
            client_socket.send("الخيار غير صحيح. حاول مرة أخرى.\n".encode())

    client_socket.close()
    print(f"العميل من {client_address} تم قطع الاتصال.")

# إنشاء وتشغيل الخادم
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 5555))
server_socket.listen()

print("الخادم بدأ. في انتظار اتصالات العملاء...")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()