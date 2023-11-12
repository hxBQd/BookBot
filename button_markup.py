import telebot

class ListUpdater:

    books_per_page = 6

    def split_by_page(self, data):
        splitted = []
        start_i, end_i = 0, self.books_per_page
        while end_i < len(data):
            splitted += [[el[0] for el in data[start_i:end_i]]]
            start_i, end_i = end_i, end_i + 6
        # print(start_i, end_i)
        splitted += [[el[0] for el in data[start_i:]]]
        return splitted

    def __init__(self, db_getter): # , titles=None
        self.markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.cur_page = 0
        self.titles = self.split_by_page(db_getter.getAllRows(poles='title'))
        self.last_page = len(self.titles) - 1
        self.markups = [None] * len(self.titles)
        # print(self.titles)
        # self.titles = titles
        self.create_markup()
    

    def create_markup(self, action=None):
        if action is None:
            cur_len_page = len(self.titles[self.cur_page])
            for i in range(1, cur_len_page, 2):
                self.markup.row(self.titles[self.cur_page][i - 1], self.titles[self.cur_page][i])
            
            if cur_len_page < self.books_per_page:
                if cur_len_page % 2:
                    self.markup.row(self.titles[self.cur_page][cur_len_page - 1])
            else:
                self.markup.row(telebot.types.KeyboardButton('➡️'))

            self.markups[self.cur_page] = self.markup
        else:
            if action == '➡️':
                self.cur_page += 1
            else:
                self.cur_page -= 1
            
            if self.markups[self.cur_page] is not None:
                self.markup = self.markups[self.cur_page]
                return
            
            markup = telebot.types.ReplyKeyboardMarkup(True, True)
            cur_len_page = len(self.titles[self.cur_page])
            for i in range(1, cur_len_page, 2):
                markup.row(self.titles[self.cur_page][i - 1], self.titles[self.cur_page][i])
            if self.cur_page == self.last_page:
                if cur_len_page % 2:
                    markup.row(self.titles[self.cur_page][cur_len_page - 1])
                markup.row(telebot.types.KeyboardButton('⬅️'))
            else:
                markup.row(telebot.types.KeyboardButton('⬅️'), telebot.types.KeyboardButton('➡️'))
            
            self.markup = markup
            self.markups[self.cur_page] = markup

        # if cur_len_page < self.books_per_page and cur_len_page % 2:
        #     if cur_len_page % 2:
        #         self.markup.row(self.titles[self.cur_page][cur_len_page - 1])
        #     self.markup.row(telebot.types.KeyboardButton('⬅️'))
        # elif self.cur_page == 0:
        #     self.markup.row(telebot.types.KeyboardButton('➡️'))
        # else:
        #     self.markup.row(telebot.types.KeyboardButton('⬅️'), telebot.types.KeyboardButton('➡️'))

    # def change_markup(self, action: str):
    #     if action == '➡️':
    #         self.cur_page += 1
    #     else:
    #         self.cur_page -= 1
        

        


# a = ListUpdater(None, [['Дикая собака Динго, или Повесть о первой любви', '#любовь, или Невыдуманная  история', 'Большая волна в гавани', 'На качелях между холмами', 'Класс коррекции', 'Паренёк в пузыре'], ['Виноваты звёзды']])
# print(a.markup)
# print(dir(a.markup.keyboard), type(a.markup.keyboard))
# for el in a.markup.keyboard:
#     print(el)
# telebot.types.ReplyKeyboardMarkup().keyboard - list, like
# [[{'text': 'Дикая собака Динго, или Повесть о первой любви'}, {'text': '#любовь, или Невыдуманная  история'}],
# [{'text': 'Большая волна в гавани'}, {'text': 'На качелях между холмами'}],
# [{'text': 'Класс коррекции'}, {'text': 'Паренёк в пузыре'}],
# [{'text': '➡️'}]]