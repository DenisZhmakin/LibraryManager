from bs4 import Tag


def get_book_type(tag: Tag):
    for elem in ['Цикл', 'Роман', 'Роман-эпопея', 'Повесть', 'Рассказ']:
        book_type = tag.find(lambda t: elem in t.text)

        if not book_type:
            continue

        return elem
    else:
        return False