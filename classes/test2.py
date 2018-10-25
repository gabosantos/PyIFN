import tkinter as tk
import tkinter as ttk

'''
目的： 在startPage上添加一个输入框，然后把输入的值在传递到pageOne打印出来

步骤: 1.在startPage上添加一个Entry widget作为输入
     2.在myFrame添加get_page函数来获取页面
     3.最后在pageOne获取页面，从而获得value并打印出来
'''

class myFrame1(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)  #
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (startPage, pageOne):
            frame = F(container, self)  #startPage继承了container
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.show_frame(startPage)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_name):
        for page in self.frames.values():
            if str(page.__class__.__name__) == page_name:
                return page
        return None     


class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.make_widget(controller)

        label = tk.Label(self, text = "StartPage")
        label.pack(pady = 10, padx = 10)

        # 在__init__下面，可以写self.controller或者controller，它们是一样的
        # 但是在上面的show_frame（不在__init__下），那么就需要self.frames，要不然找不到frames
        b1 = tk.Button(self, text = "Page One", command = lambda: controller.show_frame(pageOne))
        b1.pack()


    def make_widget(self, controller):
        some_input = "test input widget"
        self.some_entry = tk.Entry(self, textvariable=some_input, width=8)
        self.some_entry.pack()
        button1 = tk.Button(self, text='Confirm and go to next page', command=lambda: controller.show_frame(pageOne))
        button1.pack()

class pageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text = "Page one")
        label.pack(pady = 10, padx = 10)

        b1 = tk.Button(self, text = "go home", command = lambda: self.controller.show_frame(startPage))
        b1.pack()

        b2 = tk.Button(self, text = "print", command = lambda: self.print_it())
        b2.pack()

    def print_it(self):
        startpage = self.controller.get_page("startPage")
        value = startpage.some_entry.get()
        print (value)



app1 = myFrame1()
app1.mainloop()