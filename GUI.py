# -*- coding: utf-8 -*-

__author__ = 'Ricky Chen'

from Recorder import Recorder
from Tkinter import *
import tkMessageBox
import ttk


class GUI(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        parent.title("HappenedOrNotRecorder")
        self.pack(fill=BOTH, expand=1)

        self.recoder = Recorder()
        self.__create_widgets()
        self.update_content()

    def __create_widgets(self):
        # 選擇事件
        self.section = ttk.Combobox(self, state='readonly', )
        self.section.place(x=3, y=3)
        self.section.bind('<<ComboboxSelected>>', self.section_handler)
        self.__update_sections()

        # 發生與否的記錄按鈕
        button = Button(self)
        button["text"] = "Y"
        button["width"] = 5
        button["height"] = 2
        button.place(x=180, y=30)
        button["command"] = self.do_happened
        button = Button(self)
        button["text"] = "N"
        button["width"] = 5
        button["height"] = 2
        button.place(x=180, y=80)
        button["command"] = self.do_not_happened

        # Total, Happened, Ratio Lable
        label = Label(self)
        label["text"] = "Total :"
        label.place(x=15, y=35)
        label = Label(self)
        label["text"] = "Happened :"
        label.place(x=15, y=65)
        label = Label(self)
        label["text"] = "Ratio :"
        label.place(x=15, y=95)

        # 總次數, 發生次數, 比例
        self.total = Label(self)
        self.total.place(x=95, y=35)
        self.happened = Label(self)
        self.happened.place(x=95, y=65)
        self.ratio = Label(self)
        self.ratio.place(x=95, y=95)

        # 發生與否的記錄按鈕
        button = Button(self)
        button["text"] = "增加新事件"
        button["width"] = 10
        button.place(x=27, y=140)
        button["command"] = self.do_add_new_section
        button = Button(self)
        button["text"] = "刪除此事件"
        button["width"] = 10
        button.place(x=125, y=140)
        button["command"] = self.do_remove_section


    def __update_sections(self):
        content = []
        for e in self.recoder.get_sections():
            content.append(e.decode('utf-8'))
        self.section['values'] = content
        self.section.set(self.recoder.current_section)

    def section_handler(self, event):
        self.update_content()

    def do_happened(self):
        self.recoder.record_happened()
        self.update_context()

    def do_not_happened(self):
        self.recoder.record_not_happened()
        self.update_context()

    def do_add_new_section(self):
        popup = PopupEntry(self.master)
        self.wait_window(popup.top_window)

        self.recoder.add_section(popup.get_input_in_utf8())
        self.__update_sections()
        self.update_content()

    def do_remove_section(self):
        is_sure = tkMessageBox.askyesno("Remove Event", "Do you want to remove this event ?")
        if is_sure:
            self.recoder.remove_section(self.get_section_in_utf8())
            self.__update_sections()
            self.update_content()

    def update_content(self):
        self.recoder.change_section(self.get_section_in_utf8())
        self.update_context()

    def update_context(self):
        self.total['text'] = self.recoder.current_total
        self.happened['text'] = self.recoder.current_happened
        try:
            ratio = '%.2f%%' % (float(self.recoder.current_happened) / self.recoder.current_total * 100)
        except:
            ratio = 'N/A'
        self.ratio['text'] = ratio

    def get_section_in_utf8(self):
        return self.section.get().encode('utf-8')


class PopupEntry(object):
    def __init__(self, master):
        top = self.top_window = Toplevel(master)
        self.input = ''
        label = Label(top, text=u"請輸入事件名稱")
        label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.entry.focus_force()
        button = Button(top, text='OK', command=self.cleanup)
        button.pack()

    def cleanup(self):
        self.input = self.entry.get()
        self.top_window.destroy()

    def get_input_in_utf8(self):
        return self.input.encode('utf-8')


if __name__ == "__main__":
    root = Tk()
    root.geometry("235x175+540+360")
    app = GUI(parent=root)
    app.mainloop()
