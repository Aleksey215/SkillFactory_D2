from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются

# Теперь каждый раз, когда мы захотим пользоваться нашими фильтрами,
# в шаблоне нужно будет прописывать следующий тег:
# {% load custom_filters %}.


@register.filter(name='multiply')  # регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def multiply(value, arg):  # первый аргумент здесь это то значение, к которому надо применить фильтр,
# второй аргумент — это аргумент фильтра, т. е.
# примерно следующее будет в шаблоне value|multiply:arg
    if isinstance(value, str) and isinstance(arg, int):
        return str(value)*arg  # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')


@register.filter(name='censor')
def censor(value):
    censor_list = ['мат']
    text = value.split()
    for word in text:
        if word.lower() in censor_list:
            value = value.replace(word, '[CENSORED]')
    return value
