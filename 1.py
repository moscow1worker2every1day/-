import random
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation


class Container:
    def __init__(self, length, width, height, maxwe):
        self.length = length
        self.width = width
        self.height = height
        self.max_weight = maxwe

class Cargo:
    def __init__(self, length, width, height, weight):
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight

    def get_dimensions(self):
        return self.length, self.width, self.height, self.weight

def split_container(space):
    i = 0
    while i < len(space):
        pc_x, pc_y, pc_z, pc_length, pc_width, pc_height = space[i]
        j = 0
        while j < len(space):
            if i != j:
                oc_x, oc_y, oc_z, oc_length, oc_width, oc_height = space[j]
                if (pc_x >= oc_x and pc_y >= oc_y and pc_z >= oc_z and
                        pc_length <= oc_length and
                        pc_width <= oc_width and
                        pc_height <= oc_height):
                    space.pop(i)
                    i -= 1
                    break
            j += 1
        i += 1




def optimize_loading(cargos, container):
    cargos.sort(key=lambda c: c.length * c.width, reverse=True)  # Сортировка грузов по убыванию объема
    cargos_positions = []
    for key in range(1, 4):
        per = 0
        cargos_pos = []
        cargos_no_pos = []
        coord = []
        avaliable_space = [(0, 0, 0, container.length, container.width, container.height)]
        for cargo in cargos:
            best_fit_index = None
            if key == 1:
                avaliable_space = sorted(avaliable_space, key=lambda p: (p[0], p[1], p[2]))
            if key == 2:
                avaliable_space = sorted(avaliable_space, key=lambda p: (p[1], p[2], p[0]))
            if key == 3:
                avaliable_space = sorted(avaliable_space, key=lambda p: (p[2], p[1], p[0]))

            for i, potential_container in enumerate(avaliable_space):
                pc_x, pc_y, pc_z, pc_length, pc_width, pc_height = potential_container
                if (pc_x + cargo.length <= pc_length and pc_y + cargo.width <= pc_width and pc_z + cargo.height <= pc_height):
                    best_fit_index = i
                    break

            if best_fit_index is not None:
                cargos_pos.append(cargo)
                pc_x, pc_y, pc_z, pc_length, pc_width, pc_height = avaliable_space[best_fit_index]
                coord.append((pc_x, pc_y, pc_z))
                per += (cargo.length*cargo.height*cargo.width*100)/(container.length*container.height*container.width)
                avaliable_space.pop(best_fit_index)
                if pc_x + cargo.length < pc_length:
                    avaliable_space.append((pc_x + cargo.length, pc_y, pc_z, pc_length, pc_width, pc_height))
                if pc_y + cargo.width < pc_width:
                    avaliable_space.append((pc_x, pc_y + cargo.width, pc_z, pc_length, pc_width, pc_height))
                if pc_z + cargo.height < pc_height:
                    avaliable_space.append((pc_x, pc_y, pc_z + cargo.height, pc_length, pc_width, pc_height))
                # Проверяем вложенные области
                split_container(avaliable_space)
            else:
                cargos_no_pos.append(cargo)

        cargos_positions.append((cargos_pos, cargos_no_pos, coord, per))
    return cargos_positions


class WINDOW():
    def __init__(self, root):
        self.root = root
        self.cargos = []
        self.container = None
        self.window()

    def window(self):
        for widget in frame.winfo_children():
            widget.destroy()

        self.button1 = Button(frame, text="Добавить груз", font=35, command=self.addcargo, width=12)
        self.button1.grid(row=8, column=0)
        self.button2 = Button(frame, text="Далее", font=35, command=self.newwindow, width=12)
        self.button2.grid(row=8, column=3)
        self.button3 = Button(frame, text="Удалить груз", font=35, command=self.deletecargo, width=12)
        self.button3.grid(row=8, column=1, columnspan=2)
        self.text1 = Label(frame, text="     Введите габариты грузов", font=35).grid(row=0, column=0, columnspan=3)
        self.text2 = Label(frame, text="Добавленные грузы: ", font=35).grid(row=2, column=3)

        scbar = Scrollbar(frame)
        scbar.grid(row=3, column=4, rowspan=5, stick='ns')
        scbar2 = Scrollbar(frame, orient='horizontal')
        scbar2.grid(row=8, column=3, stick='new')
        self.text3 = Listbox(frame, yscrollcommand=scbar.set, xscrollcommand=scbar2.set, font=30, width=23)
        self.text3.grid(row=3, column=3, rowspan=7, stick='nw')

        k = 0
        for cargo in self.cargos:
            k += 1
            self.text3.insert(END, f"Груз {k}: {cargo.length} м, {cargo.width} м, {cargo.height} м, {cargo.weight} кг\n")

        scbar.config(command=self.text3.yview)
        scbar2.config(command=self.text3.xview)

        self.length_label = Label(frame, text=" Длина: ", font=30).grid(row=3, column=0)
        self.llabel = Label(frame, text="м", font=30).grid(row=3, column=2, stick='w')

        self.width_label = Label(frame, text=" Ширина: ", font=30).grid(row=4, column=0)
        self.wlabel = Label(frame, text="м", font=30).grid(row=4, column=2, stick='w')

        self.height_label = Label(frame, text=" Высота: ", font=30).grid(row=5, column=0)
        self.hlabel = Label(frame, text="м", font=30).grid(row=5, column=2, stick='w')

        self.weight_label = Label(frame, text=" Вес: ", font=30).grid(row=6, column=0)
        self.welabel = Label(frame, text="кг", font=30).grid(row=6, column=2, stick='w')

        self.num_label = Label(frame, text="Количество: ", font=30).grid(row=7, column=0)
        self.nlabel = Label(frame, text="шт", font=30).grid(row=7, column=2, stick='w')

        self.lenght_cargo = Entry(frame)
        self.lenght_cargo.grid(row=3, column=1, stick='w')
        self.width_cargo = Entry(frame)
        self.width_cargo.grid(row=4, column=1, stick='w')
        self.height_cargo = Entry(frame)
        self.height_cargo.grid(row=5, column=1, stick='w')
        self.weight_cargo = Entry(frame)
        self.weight_cargo.grid(row=6, column=1, stick='w')
        self.num_cargo = Entry(frame)
        self.num_cargo.grid(row=7, column=1, stick='w')

        frame.grid_columnconfigure(0, minsize=200)
        frame.grid_rowconfigure(0, minsize=50)
        frame.grid_columnconfigure(1, minsize=20)
        frame.grid_rowconfigure(1, minsize=100)
        frame.grid_columnconfigure(2, minsize=60)
        frame.grid_rowconfigure(2, minsize=50)
        frame.grid_columnconfigure(3, minsize=200)
        frame.grid_rowconfigure(3, minsize=50)
        frame.grid_rowconfigure(4, minsize=50)
        frame.grid_rowconfigure(5, minsize=50)
        frame.grid_rowconfigure(6, minsize=50)
        frame.grid_rowconfigure(7, minsize=40)
        frame.grid_rowconfigure(8, minsize=420)

    def addcargo(self):
        t = []
        l = self.lenght_cargo.get()
        w = self.width_cargo.get()
        h = self.height_cargo.get()
        we = self.weight_cargo.get()
        n = self.num_cargo.get()
        try:
            l = float(l)
        except ValueError:
            t.append('длины')
        try:
            w = float(w)
        except ValueError:
            t.append('ширины')
        try:
            h = float(h)
        except ValueError:
            t.append('высоты')
        try:
            we = float(we)
        except ValueError:
            t.append('веса')
        try:
            n = int(n)
        except ValueError:
            t.append('количества')

        if len(t) != 0:
            root2 = Tk()
            root2.title("Предупреждение!")
            if len(t) == 1:
                ttx = 'Пожалуста введите корректное значение ' + t[0] + ' и добавьте груз!'
            else:
                ttx = 'Пожалуста введите корректное значение '
                for i in range(len(t)):
                    ttx += t[i]
                    if i != len(t) - 1:
                        ttx += ', '
                ttx += ' и добавьте груз!'
            TTX = Label(root2, text=ttx, font=5)
            TTX.grid()
            root2.mainloop()
        else:
            if l <= 0 and 'длины' not in t:
                t.append('длины')
            if w <= 0 and 'ширины' not in t:
                t.append('ширины')
            if h <= 0 and 'высоты' not in t:
                t.append('высоты')
            if we <= 0 and 'веса' not in t:
                t.append('веса')
            if n <= 0 and 'количества' not in t:
                t.append('количества')
            if len(t) != 0:
                root2 = Tk()
                root2.title("Предупреждение!")
                if len(t) == 1:
                    ttx = 'Значение ' + t[0] + ' должно быть больше 0!'
                else:
                    ttx = 'Значение '
                    for i in range(len(t)):
                        ttx += t[i]
                        if i != len(t) - 1:
                            ttx += ', '
                    ttx += ' должно быть больше 0!'
                TTX = Label(root2, text=ttx, font=5)
                TTX.grid()
                root2.mainloop()
            else:
                if l==int(l):
                    l = int(l)
                if w==int(w):
                    w = int(w)
                if h==int(h):
                    h = int(h)
                if we==int(we):
                    we = int(we)
                for i in range(n):
                    self.cargos.append(Cargo(l, w, h, we))
                    self.text3.insert(END, f"Груз {len(self.cargos)}: {l} м, {w} м, {h} м, {we} кг\n")

    def deletecargo(self):
        if self.cargos:
            self.cargos.pop()
            self.text3.delete(0, END)
            k = 0
            for cargo in self.cargos:
                k += 1
                self.text3.insert(END, f"Груз {k}: {cargo.length} м, {cargo.width} м, {cargo.height} м, {cargo.weight} кг\n")
        else:
            al = Tk()
            al.title("Предупреждение!")
            Textal = Label(al, text="Пожалуйста добавьте грузы перед удалением!", font=5)
            Textal.grid()
            al.mainloop()

    def newwindow(self):
        if len(self.cargos) > 0:
            for widget in frame.winfo_children():
                widget.destroy()
            self.text1 = Label(frame, text="     Выберете размер контейнера", font=35).grid(row=0, column=0, columnspan=3)
            self.text2 = Label(frame, text="Длина 12,192 м (40 футов)\nШирина 2,438 м (8 футов)\nВысота 2,438 м (8 футов)\nМаксимальный вес 30480 кг", font=35).grid(row=1, column=2, stick='e', columnspan=3)
            self.text3 = Label(frame, text="Длина 6,058 м (19 ф. 10,5 д.)\nШирина 2,438 м (8 футов)\nВысота 2,438 м (8 футов)\nМаксимальный вес 20320 кг", font=35).grid(row=2, column=2, stick='e', columnspan=3)

            self.lenght_c = Entry(frame)
            self.lenght_c.grid(row=3, column=3, stick='w')
            self.width_c = Entry(frame)
            self.width_c.grid(row=4, column=3, stick='w')
            self.height_c = Entry(frame)
            self.height_c.grid(row=5, column=3, stick='w')
            self.weight_c = Entry(frame)
            self.weight_c.grid(row=6, column=3, stick='w')

            self.button1 = Button(frame, text="Рассчитать положение", font=35, command=self.optimize)
            self.button1.grid(row=7, column=3, columnspan=2, stick='e')

            self.button2 = Button(frame, text="Назад", font=35, command=self.window, width=12)
            self.button2.grid(row=7, column=0, columnspan=2, stick='e')

            self.container_value = IntVar()

            self.btn1 = Radiobutton(frame, variable=self.container_value, value=1)
            self.btn1.grid(row=1, column=0)
            self.btn2 = Radiobutton(frame, variable=self.container_value, value=2)
            self.btn2.grid(row=2, column=0)
            self.btn3 = Radiobutton(frame, variable=self.container_value, value=3)
            self.btn3.grid(row=3, column=0, rowspan=4)

            self.length_label = Label(frame, text="Длина: ", font=30).grid(row=3, column=2)
            self.llabel = Label(frame, text="м", font=30).grid(row=3, column=4, stick='e')

            self.width_label = Label(frame, text="Ширина: ", font=30).grid(row=4, column=2)
            self.wlabel = Label(frame, text="м", font=30).grid(row=4, column=4, stick='e')

            self.height_label = Label(frame, text="Высота: ", font=30).grid(row=5, column=2)
            self.hlabel = Label(frame, text="м", font=30).grid(row=5, column=4, stick='e')

            self.weight_label = Label(frame, text=" Макс. вес: ", font=30).grid(row=6, column=2)
            self.welabel = Label(frame, text="кг", font=30).grid(row=6, column=4, stick='e')

            frame.grid_columnconfigure(0, minsize=100)
            frame.grid_rowconfigure(0, minsize=50)
            frame.grid_columnconfigure(1, minsize=100)
            frame.grid_rowconfigure(1, minsize=150)
            frame.grid_columnconfigure(2, minsize=100)
            frame.grid_rowconfigure(2, minsize=200)
            frame.grid_columnconfigure(3, minsize=100)
            frame.grid_rowconfigure(3, minsize=20)
            frame.grid_rowconfigure(4, minsize=20)
            frame.grid_rowconfigure(5, minsize=20)
            frame.grid_rowconfigure(6, minsize=20)
            frame.grid_rowconfigure(7, minsize=260)
        else:
            root2 = Tk()
            root2.title("Предупреждение!")
            root2.maxsize(750, 50)
            TTX = Label(root2, text="Пожалуйста добавьте грузы!", font=5)
            TTX.grid()
            root2.mainloop()

    def optimize(self):
        self.container = None
        if self.container_value.get() == 0:
            al = Tk()
            al.title("Предупреждение!")
            al.maxsize(750, 50)
            Textal = Label(al, text="Выберете габариты контейнера!", font=5)
            Textal.grid()
            al.mainloop()
        if self.container_value.get() == 3:
            l = self.lenght_c.get()
            w = self.width_c.get()
            h = self.height_c.get()
            we = self.weight_c.get()
            t = []
            try:
                l = float(l)
            except ValueError:
                t.append('длину')
            try:
                w = float(w)
            except ValueError:
                t.append('ширину')
            try:
                h = float(h)
            except ValueError:
                t.append('высоту')
            try:
                we = float(we)
            except ValueError:
                t.append('максимальный вес')
            if len(t) != 0:
                if len(t) == 1:
                    ttx = 'Пожалуста введите ' + t[0] + ' контейнера\nили выберете существующие варианты!'
                else:
                    ttx = 'Пожалуста введите '
                    for i in range(len(t)):
                        ttx += t[i]
                        if i != len(t) - 1:
                            ttx += ', '
                    ttx += ' контейнера\nили выберете существующие варианты!'
                al = Tk()
                al.title("Предупреждение!")
                TTXX = Label(al, text=ttx, font=5)
                TTXX.grid(row=7, column=0)
                al.mainloop()
            else:
                if l <= 0 and 'длины' not in t:
                    t.append('длины')
                if w <= 0 and 'ширины' not in t:
                    t.append('ширины')
                if h <= 0 and 'высоты' not in t:
                    t.append('высоты')
                if we <= 0 and 'веса' not in t:
                    t.append('максимального веса')

                if len(t) != 0:
                    root2 = Tk()
                    root2.title("Предупреждение!")
                    if len(t) == 1:
                        ttx = 'Значение ' + t[0] + ' должно быть больше 0!'
                    else:
                        ttx = 'Значение '
                        for i in range(len(t)):
                            ttx += t[i]
                            if i != len(t) - 1:
                                ttx += ', '
                        ttx += ' должно быть больше 0!'
                    TTX = Label(root2, text=ttx, font=5)
                    TTX.grid()
                    root2.mainloop()
                else:
                    self.container = Container(l, w, h, we)
        if self.container_value.get() == 2:
            self.container = Container(6, 2, 2, 30480)
        if self.container_value.get() == 1:
            self.container = Container(12, 2, 2, 20320)
        if self.container:
            self.optimizecargos()

    def optimizecargos(self):
        for widget in frame.winfo_children():
            widget.destroy()
        self.cargo_positions = optimize_loading(self.cargos, self.container)
        self.visualize_container()

    def visualize_container(self):
        self.fig = plt.figure(figsize=(6, 3.5), edgecolor='blue')
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)

        self.ax.bar3d(0, 0, 0, self.container.length, self.container.width, self.container.height, color='b', alpha=0.1)
        M = max(self.container.length, self.container.width, self.container.height)
        self.ax.set_xlim(0, M)
        self.ax.set_ylim(0, M)
        self.ax.set_zlim(0, M)
        self.ax.set_xlabel('Длина')
        self.ax.set_ylabel('Ширина')
        self.ax.set_zlabel('Высота')

        frame.grid_columnconfigure(0, minsize=225)
        frame.grid_columnconfigure(1, minsize=250)
        frame.grid_columnconfigure(2, minsize=225)
        frame.grid_rowconfigure(0, minsize=60)
        frame.grid_rowconfigure(2, minsize=50)
        frame.grid_rowconfigure(4, minsize=130)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3)

        self.B1 = Button(frame, text="Вариант 1", width=12, font=35, command=self.visualize1)
        self.B1.grid(row=2, column=0, sticky=E)
        self.B2 = Button(frame, text="Вариант 2", width=12, font=35, command=self.visualize2)
        self.B2.grid(row=2, column=1)
        self.B3 = Button(frame, text="Вариант 3", width=12, font=35, command=self.visualize3)
        self.B3.grid(row=2, column=2, sticky=W)

        sc = Scrollbar(frame)
        sc.grid(row=3, column=3, sticky=W)
        self.Text_cargos = Listbox(frame, yscrollcommand=sc.set, font=25, width=55, height=5)
        self.Text_cargos.grid(row=3, column=0, columnspan=3)
        self.Text_cargos.delete(0, END)
        sc.config(command=self.Text_cargos.yview)

        self.B1.configure(state = 'disabled')
        self.B2.configure(state = 'normal')
        self.B3.configure(state = 'normal')
        self.Text_cargos.delete(0, END)
        cargo_placed = self.cargo_positions[0][0]
        cargo_no_placed = self.cargo_positions[0][1]
        coord = self.cargo_positions[0][2]
        colors = []
        num = len(cargo_placed) + 1
        self.Text_c = Label(frame, text=f"Контейнер заполнен на {round(self.cargo_positions[0][3], 2)}%", font=35)
        self.Text_c.grid(row=0, column=0, columnspan=3)
        for i in range(len(cargo_placed)):
            colors.append((1, 1, random.random()))
        self.ani = FuncAnimation(self.fig, self.animate, fargs=(cargo_placed, coord, colors), interval=700, frames=num)
        self.canvas.draw()
        if len(cargo_no_placed)>0:
            k = 0
            for cargo in cargo_no_placed:
                k += 1
                self.Text_cargos.insert(END, f"{k}. Груз с габаритами {cargo.get_dimensions()} не поместился в контейнер\n")
        else:
            self.Text_cargos.insert(END, "        Все грузы поместились в контейнер! ")

        button1 = Button(frame, text="Рассчитать новый контейнер", font=35, command=self.clear_cargo)
        button1.grid(row=4, column=1, columnspan=2)
        button2 = Button(frame, text="Назад", font=35, command=self.newwindow)
        button2.grid(row=4, column=0)

    def visualize1(self):
        self.ani.event_source.stop()

        self.ax.clear()
        self.ax.bar3d(0, 0, 0, self.container.length, self.container.width, self.container.height, color='b', alpha=0.1)
        M = max(self.container.length, self.container.width, self.container.height)
        self.ax.set_xlim(0, M)
        self.ax.set_ylim(0, M)
        self.ax.set_zlim(0, M)
        self.ax.set_xlabel('Длина')
        self.ax.set_ylabel('Ширина')
        self.ax.set_zlabel('Высота')

        self.B1.configure(state = 'disabled')
        self.B2.configure(state = 'normal')
        self.B3.configure(state = 'normal')
        self.Text_cargos.delete(0, END)
        self.Text_c['text'] = f"Контейнер заполнен на {round(self.cargo_positions[0][3], 2)}%"
        cargo_placed = self.cargo_positions[0][0]
        cargo_no_placed = self.cargo_positions[0][1]
        coord = self.cargo_positions[0][2]
        colors = []
        num = len(cargo_placed) + 1
        for i in range(len(cargo_placed)):
            colors.append((1, 1, random.random()))
        self.ani = FuncAnimation(self.fig, self.animate, fargs=(cargo_placed, coord, colors), interval=700, frames=num)
        self.canvas.draw()
        if len(cargo_no_placed)>0:
            k = 0
            for cargo in cargo_no_placed:
                k += 1
                self.Text_cargos.insert(END, f"{k}. Груз с габаритами {cargo.get_dimensions()} не поместился в контейнер\n")
        else:
            self.Text_cargos.insert(END, "        Все грузы поместились в контейнер! ")
        self.ani.event_source.start()
    def visualize2(self):
        self.ani.event_source.stop()

        self.ax.clear()
        self.ax.bar3d(0, 0, 0, self.container.length, self.container.width, self.container.height, color='b', alpha=0.1)
        M = max(self.container.length, self.container.width, self.container.height)
        self.ax.set_xlim(0, M)
        self.ax.set_ylim(0, M)
        self.ax.set_zlim(0, M)
        self.ax.set_xlabel('Длина')
        self.ax.set_ylabel('Ширина')
        self.ax.set_zlabel('Высота')

        self.B2.configure(state = 'disabled')
        self.B1.configure(state = 'normal')
        self.B3.configure(state = 'normal')
        self.Text_cargos.delete(0, END)
        self.Text_c['text'] = f"Контейнер заполнен на {round(self.cargo_positions[0][3], 2)}%"
        cargo_placed = self.cargo_positions[1][0]
        cargo_no_placed = self.cargo_positions[1][1]
        coord = self.cargo_positions[1][2]
        colors = []
        num = len(cargo_placed) + 1
        for i in range(len(cargo_placed)):
            colors.append((1, 1, random.random()))
        self.ani = FuncAnimation(self.fig, self.animate, fargs=(cargo_placed, coord, colors), interval=800, frames=num)
        self.canvas.draw()
        if len(cargo_no_placed)>0:
            k = 0
            for cargo in cargo_no_placed:
                k += 1
                self.Text_cargos.insert(END, f"{k}. Груз с габаритами {cargo.get_dimensions()} не поместился в контейнер\n")
        else:
            self.Text_cargos.insert(END, "        Все грузы поместились в контейнер! ")
        self.ani.event_source.start()

    def visualize3(self):
        self.ani.event_source.stop()

        self.ax.clear()
        self.ax.bar3d(0, 0, 0, self.container.length, self.container.width, self.container.height, color='b', alpha=0.1)
        M = max(self.container.length, self.container.width, self.container.height)
        self.ax.set_xlim(0, M)
        self.ax.set_ylim(0, M)
        self.ax.set_zlim(0, M)
        self.ax.set_xlabel('Длина')
        self.ax.set_ylabel('Ширина')
        self.ax.set_zlabel('Высота')

        self.B3.configure(state = 'disabled')
        self.B2.configure(state = 'normal')
        self.B1.configure(state = 'normal')
        self.Text_cargos.delete(0, END)
        self.Text_c['text'] = f"Контейнер заполнен на {round(self.cargo_positions[0][3], 2)}%"
        cargo_placed = self.cargo_positions[2][0]
        cargo_no_placed = self.cargo_positions[2][1]
        coord = self.cargo_positions[2][2]
        colors = []
        num = len(cargo_placed) + 1
        for i in range(len(cargo_placed)):
            colors.append((1, 1, random.random()))
        self.ani = FuncAnimation(self.fig, self.animate, fargs=(cargo_placed, coord, colors), interval=700, frames=num)
        self.canvas.draw()
        if len(cargo_no_placed)>0:
            k = 0
            for cargo in cargo_no_placed:
                k += 1
                self.Text_cargos.insert(END, f"{k}. Груз с габаритами {cargo.get_dimensions()} не поместился в контейнер\n")
        else:
            self.Text_cargos.insert(END, "        Все грузы поместились в контейнер! ")
        self.ani.event_source.start()

    def animate(self, num, cargo_placed, coord, colors):
        if num != 0:
            if num == 1:
                self.ax.clear()
                self.ax.bar3d(0, 0, 0, self.container.length, self.container.width, self.container.height, color='b', alpha=0.1)
                M = max(self.container.length, self.container.width, self.container.height)
                self.ax.set_xlim(0, M)
                self.ax.set_ylim(0, M)
                self.ax.set_zlim(0, M)
                self.ax.set_xlabel('Длина')
                self.ax.set_ylabel('Ширина')
                self.ax.set_zlabel('Высота')
            cargo = cargo_placed[num-1]
            self.ax.bar3d(coord[num-1][0], coord[num-1][1], coord[num-1][2], cargo.length, cargo.width, cargo.height, shade=True, color=colors[num-1], alpha=1)


    def clear_cargo(self):
        self.cargos = []
        self.window()


root = Tk()
root.title("Русские контейнеры")
root.geometry("700x700")
root.maxsize(700, 700)
root.minsize(700, 700)
frame = Frame(root)
frame.pack(side="top", expand=True, fill="both")

win = WINDOW(root)

root.mainloop()