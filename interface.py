from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure

window = Tk()

p_frame = Frame(window, height=500, width=500, relief="ridge")
g_frame = Frame(window, height=1000, width=500, relief="ridge")

event1_label = Label(p_frame, text="Событие - поступления задачи в очередь")
m1_label = Label(p_frame, text="Математическое ожидание")
m1_entry = Entry(p_frame, text="1", width=10, bd=3)
d1_label = Label(p_frame, text="Дисперсия")
d1_entry = Entry(p_frame, text="1", width=10, bd=3)
event1_label.grid(row=0, column=0, pady=20)
m1_label.grid(row=1, column=0)
m1_entry.grid(row=1, column=1)
d1_label.grid(row=2, column=0)
d1_entry.grid(row=2, column=1)

event2_label = Label(p_frame, text="Событие - выполнение задачи сервером")
m2_label = Label(p_frame, text="Математическое ожидание")
m2_entry = Entry(p_frame, text="1", width=10, bd=3)
d2_label = Label(p_frame, text="Дисперсия")
d2_entry = Entry(p_frame, text="1", width=10, bd=3)
event2_label.grid(row=3, column=0, pady=20)
m2_label.grid(row=4, column=0)
m2_entry.grid(row=4, column=1)
d2_label.grid(row=5, column=0)
d2_entry.grid(row=5, column=1)

start_btn = Button(window, text="Запуск моделирования")
start_btn.grid(row=1, column=0, padx=20, pady=20)

p_frame.grid(row=0, column=0, padx=20, pady=20)
g_frame.grid(row=0, column=1, padx=20, pady=20)
window.mainloop()
