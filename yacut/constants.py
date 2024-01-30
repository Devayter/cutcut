import string

ALLOWED_SYMBOLS = string.ascii_letters + string.digits
CUSTOM_LENGHT = 16
LENGTH = 6


CUSTOM_ID_LABLE = 'Введите сокращенный вариант'
CUSTOM_ID_VALIDATOR_LENGTH = 'Длина превышает 16 символов'
NO_DATA = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
ORIGINAL_LINK_LABLE = 'Введите оригинальную ссылку'
ORIGINAL_LINK_VALIDATOR_DATA = 'Обязательное поле'
UNCORRECT_ID = 'Указанный id не найден'
UNCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'
URL_FOR_API = 'http://localhost/{short}'
URL_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
URL_SUCCESS_CREATED = 'Ваша новая ссылка готова: http://localhost/{short}'

MODEL_API_FIELDS = ['url', 'custom_id']
