import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2

# создадим пустой список для хранения записей
notes = []

# создаем приложение aiohttp
app = web.Application()

# Настраиваем Jinja2
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# обработчик для главной страницы
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {'notes': notes}  # Передаем список записок в шаблон

# обработчик для добавления новой записи
async def add_note(request):
    data = await request.post()  # Получаем данные из POST-запроса формы
    note = data.get('note')  # Извлекаем поле "note" из данных формы
    if note:
        notes.append(note)  # Добавляем запись в список notes
        return web.HTTPFound('/')  # Перенаправляем пользователя обратно на главную страницу
    return web.json_response({"error": "Ошибка! Пустая записка"}, status=400)

# обработчик для получения всех записей
async def get_notes(request):
    return web.json_response(notes)


# Настройка Jinja2 с указанием папки для шаблонов
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Добавляем маршруты
app.add_routes([
    web.get('/', index),         # GET-запрос для главной страницы с формой
    web.post('/notes', add_note),  # POST-запрос для добавления новой записи
    web.get('/notes', get_notes)  # GET-запрос для получения всех записей 
])

# Запускаем веб сервер
if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8000)