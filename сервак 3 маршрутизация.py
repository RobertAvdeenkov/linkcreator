from http.server import HTTPServer, BaseHTTPRequestHandler
import os
 
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open('index.html','rb') as file:
            content=file.read()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        # Получаем размер данных из заголовка
        content_length = int(self.headers["Content-Length"])
         
        # Читаем сами данные
        post_data = self.rfile.read(content_length)
         
        # Декодируем и выводим в консоль сервера
        print(f"Получен POST запрос: {post_data.decode("utf-8")}")
 
        # Отправляем ответ клиенту
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"POST request received!")
 
 
# Настройки запуска
hostName = "localhost"
serverPort = 8000
 
# Инициализация сервера
webServer = HTTPServer((hostName, serverPort), MyHandler)
print(f"Сервер запущен: http://{hostName}:{serverPort}")
 
# Бесконечный цикл прослушивания порта
try: webServer.serve_forever()
except KeyboardInterrupt: pass
 
webServer.server_close()
print("Сервер остановлен...")