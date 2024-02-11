from Classes.database import *
from generate import *
from tkinter import *
from tkinter import messagebox 
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox

#главное меню    
class Main():
    
    def __init__(self, title):
        self.window = Tk()    
        self.window.title(title)  
        self.window.geometry('770x770')  
        self.menu = ttk.Notebook(self.window)
        self.informationTab = ttk.Frame(self.menu)
        self.menu.add(self.informationTab, text='Справочники')  
        self.createTab = ttk.Frame(self.menu)
        self.menu.add(self.createTab, text='Сгенирировать')
        self.menu.pack(expand=1, fill='both')
        init_session()
        self._initInfoTab()
        self._initSubject()
        self._initTeacher()
        self._initClassroom()
        self._initClass()
        self._initCall_table()
        self._initHours()
        self._initInfo()
        self.window.mainloop()
#-----------

#справочники
    def _initInfoTab(self):
        buttons = ttk.Notebook(self.informationTab)
        self.Subjects = ttk.Frame(buttons)
        buttons.add(self.Subjects, text='Предметы')
        self.Teachers = ttk.Frame(buttons)
        buttons.add(self.Teachers, text='Преподаватели')
        self.Classrooms = ttk.Frame(buttons)
        buttons.add(self.Classrooms, text='Аудитории')
        self.Classes = ttk.Frame(buttons)
        buttons.add(self.Classes, text='Классы и группы')
        self.Call_time = ttk.Frame(buttons)
        buttons.add(self.Call_time, text='Расписание звонков')
        self.Teachers_time = ttk.Frame(buttons)
        buttons.add(self.Teachers_time, text='Информация об преподавателях')
        self.Lesson_hours = ttk.Frame(buttons)
        buttons.add(self.Lesson_hours, text='Количество пар')
        buttons.pack(expand=1, fill='both')
#---------------

#предметы
    def _initSubject(self):
        global subject_table
        subject_frame= Frame(self.Subjects)
        subject_frame.pack(pady = 10)
        
        subject_scroll = Scrollbar(subject_frame)
        subject_scroll.pack(side = RIGHT, fill = Y)

        subject_table = ttk.Treeview(subject_frame, yscrollcommand = subject_scroll.set, selectmode = "extended")
        subject_table.pack()
        subject_scroll.config(command = subject_table.yview)
        
        subject_table['columns'] = ("subject_id", "subject", "separate", "has_room")

        subject_table.column("#0", width = 0, stretch = NO)
        subject_table.column("subject_id", anchor = CENTER, width = 140)
        subject_table.column("subject", anchor = CENTER, width = 140)
        subject_table.column("separate", anchor = CENTER, width = 140)
        subject_table.column("has_room", anchor = CENTER, width = 140)
        subject_table.heading("#0", text = "", anchor = CENTER)
        subject_table.heading("subject_id", text = "Номер предмета", anchor = CENTER)
        subject_table.heading("subject", text = "Предмет", anchor = CENTER)
        subject_table.heading("separate", text = "Разделён на подгруппы", anchor = CENTER)
        subject_table.heading("has_room", text = "Привязан к аудитории", anchor = CENTER)

        data = []
        for subj in Subject.select():
            data.append([subj.subject_id, subj.subject_name, subj.separate, subj.has_room])
        for record in data:
            if record[2] == 1:
                if record[3] == 1:
                    subject_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], "да", "да"))
                else:
                    subject_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], "да", "нет"))
            else:
                if record[3] == 1:
                    subject_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], "нет", "да"))
                else:
                    subject_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], "нет", "нет"))


        def Add_subj():
            try:
                name = txt_subj.get()
                if name != "":
                    subj = Subject.create(subject_id = None, subject_name = name, separate = 0, has_room = 0)
                    for subj in Subject.select():
                        data.append([subj.subject_id, subj.subject_name, subj.separate, subj.has_room])
                    record = data[-1]
                    subject_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], "нет", "нет"))
                        
            except:
                messagebox.showerror('Ошибка', 'Вы уже добавили этот предмет!')

        def Remove_subj():
            try:
                selected_item = subject_table.selection()[0]
                values = subject_table.item(selected_item, option="values")
                sql = 'delete from lesson_hours where subject_id = {0}'
                db.execute_sql(sql.format(int(values[0])))
                sql = 'delete from lesson_hours_used where subject_id = {0}'
                db.execute_sql(sql.format(int(values[0])))
                sql = 'delete from teachers_has_subjects where subject_id = {0}'
                db.execute_sql(sql.format(int(values[0])))
                sql = 'delete from subjects_has_classrooms where subject_id = {0}'
                db.execute_sql(sql.format(int(values[0])))
                subject_table.delete(selected_item)
                sql = 'delete from subjects where subject_id = {0}'
                db.execute_sql(sql.format(int(values[0])))
                db.execute_sql('delete from teachers_time_used')
                db.execute_sql('delete from lesson_hours_used')
                db.execute_sql('delete from classroom_time')
                db.execute_sql('delete from timetable')
                data2 = []
                for current in subject_has_room_table.get_children():
                    subject_has_room_table.delete(current)
                for subj_has_room in Subjects_has_classroom.select():
                    data2.append([subj_has_room.subject_id, subj_has_room.classroom_id])
                for record in data2:
                    subject = Subject.get_by_id(record[0])
                    room = Classroom.get_by_id(record[1])
                    subject_has_room_table.insert(parent = "", index= "end",text = "", values=(subject.subject_name, room.room_number))
            except:
                messagebox.showerror('Ошибка', 'Перед тем как удалить предмет, вам нужно выбрать его!')

        def Separate_subj():
            try:
                selected_item = subject_table.selection()[0]
                values = subject_table.item(selected_item, option="values")
                subj = Subject()
                subj.subject_id = values[0]
                subj.separate = 1
                subj.save()
                subject_table.item(selected_item, values = (values[0], values[1], "да", values[3]))
            except:
                messagebox.showerror('Ошибка', 'Нужно выбрать предмет, который вы хотите разделить!')

        def Unite_subj():
            try:
                selected_item = subject_table.selection()[0]
                values = subject_table.item(selected_item, option="values")
                subj = Subject()
                subj.subject_id = values[0]
                subj.separate = 0
                subj.save()
                subject_table.item(selected_item, values = (values[0], values[1], "нет", values[3]))

            except:
                messagebox.showerror('Ошибка', 'Нужно выбрать предмет, который вы хотите объединить!')

        def Room_add2():
            try:
                selected_item = subject_table.selection()[0]
                values = subject_table.item(selected_item, option="values")
                subj = Subject()
                subj.subject_id = values[0]
                subj.has_room = 1
                subj.save()
                subject_table.item(selected_item, values = (values[0], values[1], values[2], "да"))
                subj_val = values[1]
                for subj in Subject.select():
                    if subj.subject_name == subj_val:
                        id_subj = subj.subject_id
                room_val = combo_rooms.get()
                for room in Classroom.select():
                    if room.room_number == room_val:
                        id_room = room.classroom_id
                subj_has_room = Subjects_has_classroom.create(subject_id = id_subj, classroom_id = id_room)
                data = []
                for shr in Subjects_has_classroom.select():
                    data.append([shr.subject_id, shr.classroom_id])
                record = data[-1]
                room = Classroom.get_by_id(id_room)
                subject = Subject.get_by_id(id_subj)
                subject_has_room_table.insert(parent = "", index= "end",text = "", values=(subject. subject_name, room.room_number))
                self.window2.destroy()
            except:
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Этот предмет уже привязан!')
                selected_item = subject_table.selection()[0]
                values = subject_table.item(selected_item, option="values")
                subj = Subject()
                subj.subject_id = values[0]
                subj.has_room = 0
                subj.save()
                subject_table.item(selected_item, values = (values[0], values[1], values[2], "нет"))
                
            
        def Room_add():
            try:
                selected_item = subject_table.selection()[0]
                values = subject_table.item(selected_item, option="values")
                if values[3] != "да":
                    self.window2 = Toplevel()#Tk()
                    self.window2.title("")
                    self.window2.geometry('400x200')
                    self.window2.grab_set()
                    self.window2.focus_set()
                    label1 = Label(self.window2, text="Укажите аудиторию, к который вы хотите привязать предмет")
                    label1.pack()
                    label2 = Label(self.window2, text="привязать предмет {} к аудитории:".format(values[1]))
                    label2.pack()
                    global combo_rooms
                    combo_rooms = Combobox(self.window2)
                    rooms = []
                    for room in Classroom.select():
                        rooms.append(room.room_number)
                    combo_rooms['values'] = (rooms)  
                    combo_rooms.current(0)
                    combo_rooms.pack()
                    btn = Button(self.window2, text="Привязать к аудитории", command = Room_add2)
                    btn.pack()
                else:
                    messagebox.showerror('Ошибка', 'Этот предмет уже привязан!')
            except:
                messagebox.showerror('Ошибка', 'Нужно выбрать предмет, который вы хотите привязать к аудитории!')

        def Room_remove():
            try:
                selected_item = subject_has_room_table.selection()[0]
                values = subject_has_room_table.item(selected_item, option="values")
                subject = values[0]
                subject_has_room_table.delete(selected_item)
                for subj in Subject.select():
                    if subj.subject_name == subject:
                        subj_id = subj.subject_id
                        subj.has_room = 0
                        subj.save()
                subj = Subjects_has_classroom.get(Subjects_has_classroom.subject_id == subj_id)
                subj.delete_instance()
                for current in subject_table.get_children():
                    record = subject_table.item(current)["values"]
                    if record[0] == subj_id:
                        subject_table.item(current, values = (record[0], record[1], record[2], "нет"))
            except:
                messagebox.showerror('Ошибка', 'Нужно выбрать связь из таблицы "привязанность предметов к аудиториям", которую вы хотите убрать!')

        label_subj = Label(self.Subjects, text="Введите название предмета")
        label_subj.pack()
        txt_subj = Entry(self.Subjects, width = 25)  
        txt_subj.pack()
        button_subj = Button(self.Subjects, text="добавить", command = Add_subj)
        button_subj.pack()
        button_subj_remove = Button(self.Subjects, text="Убрать выбранный предмет", command = Remove_subj)
        button_subj_remove.pack()
        button_subj_separate = Button(self.Subjects, text="Разделить выбранный предмет на подгруппы", command = Separate_subj)
        button_subj_separate.pack()
        button_subj_unite = Button(self.Subjects, text="Объединить выбранный предмет", command = Unite_subj)
        button_subj_unite.pack()
        #привязанность предметов к кабинетам
        button_subj_has_room_add = Button(self.Subjects, text="Cвязать выбранный предмет с аудиторией", command = Room_add)
        button_subj_has_room_add.pack()
        button_subj_has_room_remove = Button(self.Subjects, text="Отвязать выбранный предмет от аудитории", command = Room_remove)
        button_subj_has_room_remove.pack()
        label_subj_has_room = Label(self.Subjects, text = "Привязанность предметов к аудиториям")
        label_subj_has_room.pack()
        global subject_has_room_table
        subject_has_room_frame = Frame(self.Subjects)
        subject_has_room_frame.pack(pady = 10)
        
        subject_has_room_scroll = Scrollbar(subject_has_room_frame)
        subject_has_room_scroll.pack(side = RIGHT, fill = Y)

        subject_has_room_table = ttk.Treeview(subject_has_room_frame, yscrollcommand = subject_scroll.set, selectmode = "extended")
        subject_has_room_table.pack()
        subject_has_room_scroll.config(command = subject_has_room_table.yview)
        
        subject_has_room_table['columns'] = ("subject_id", "classroom_id")

        subject_has_room_table.column("#0", width = 0, stretch = NO)
        subject_has_room_table.column("subject_id", anchor = CENTER, width = 140)
        subject_has_room_table.column("classroom_id", anchor = CENTER, width = 140)
        subject_has_room_table.heading("#0", text = "", anchor = CENTER)
        subject_has_room_table.heading("subject_id", text = "Предмет", anchor = CENTER)
        subject_has_room_table.heading("classroom_id", text = "Аудитория", anchor = CENTER)

        data2 = []
        for subj_has_room in Subjects_has_classroom.select():
            data2.append([subj_has_room.subject_id, subj_has_room.classroom_id])
        for record in data2:
            subject = Subject.get_by_id(record[0])
            room = Classroom.get_by_id(record[1])
            subject_has_room_table.insert(parent = "", index= "end",text = "", values=(subject.subject_name, room.room_number))
        #----------------------------------
#------------------------

#преподаватели
    def _initTeacher(self):
        teacher_frame= Frame(self.Teachers)
        teacher_frame.pack(pady = 10)
        
        teacher_scroll = Scrollbar(teacher_frame)
        teacher_scroll.pack(side = RIGHT, fill = Y)

        teacher_table = ttk.Treeview(teacher_frame, yscrollcommand = teacher_scroll.set, selectmode = "extended")
        teacher_table.pack()
        teacher_scroll.config(command = teacher_table.yview)
        
        teacher_table['columns'] = ("teacher_id", "teacher")

        teacher_table.column("#0", width = 0, stretch = NO)
        teacher_table.column("teacher_id", anchor = CENTER, width = 140)
        teacher_table.column("teacher", anchor = CENTER, width = 140)
        teacher_table.heading("#0", text = "", anchor = CENTER)
        teacher_table.heading("teacher_id", text = "Номер преподавателя", anchor = CENTER)
        teacher_table.heading("teacher", text = "Имя преподавателя", anchor = CENTER)

        data = []
        for teach in Teacher.select():
            data.append([teach.teacher_id, teach.teacher_name])
        for record in data:
            teacher_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1]))

        def Add_teach():
            try:
                name = txt_teach.get()
                if name != "":
                    subj = Teacher.create(teacher_id = None, teacher_name = name)
                    for teach in Teacher.select():
                        data.append([teach.teacher_id, teach.teacher_name])
                    record = data[-1]
                    teacher_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1]))
                teachers = []
                for teach in Teacher.select():
                    teachers.append(teach.teacher_name)
                combo_teachers['values'] = (teachers)  
            except:
                messagebox.showerror('Ошибка', 'Вы уже добавили этотого преподавателя!')
        def Remove_teach():
            try:
                db.execute_sql('delete from teachers_time_used')
                db.execute_sql('delete from lesson_hours_used')
                db.execute_sql('delete from classroom_time')
                db.execute_sql('delete from timetable')
                selected_item = teacher_table.selection()[0]
                values = teacher_table.item(selected_item, option="values")
                sql = 'delete from teachers_has_subjects where teacher_id = {0}'
                db.execute_sql(sql.format(values[0]))
                sql = 'delete from teachers_time where teacher_id = {0}'
                db.execute_sql(sql.format(values[0]))
                sql = 'delete from teachers_time_used where teacher_id = {0}'
                db.execute_sql(sql.format(values[0]))
                Teacher.delete_by_id(values[0])
                teacher_table.delete(selected_item)
                teachers = []
                for teach in Teacher.select():
                    teachers.append(teach.teacher_name)
                combo_teachers['values'] = (teachers)  
            except:
                messagebox.showerror('Ошибка', 'Перед тем как удалить преподавателя, вам нужно выбрать его!')



        label_teach = Label(self.Teachers, text="Введите имя преподавателя")
        label_teach.pack()
        txt_teach = Entry(self.Teachers, width = 25)  
        txt_teach.pack()
        button_teach = Button(self.Teachers, text="добавить", command = Add_teach)
        button_teach.pack()
        button_teach_remove = Button(self.Teachers, text="Убрать выбранного преподавателя", command = Remove_teach)
        button_teach_remove.pack()
#------------------------

#аудитории
    def _initClassroom(self):
        classroom_frame= Frame(self.Classrooms)
        classroom_frame.pack(pady = 10)
        
        classroom_scroll = Scrollbar(classroom_frame)
        classroom_scroll.pack(side = RIGHT, fill = Y)

        classroom_table = ttk.Treeview(classroom_frame, yscrollcommand = classroom_scroll.set, selectmode = "extended")
        classroom_table.pack()
        classroom_scroll.config(command = classroom_table.yview)
        
        classroom_table['columns'] = ("classroom_id", "classroom")

        classroom_table.column("#0", width = 0, stretch = NO)
        classroom_table.column("classroom_id", anchor = CENTER, width = 140)
        classroom_table.column("classroom", anchor = CENTER, width = 140)
        classroom_table.heading("#0", text = "", anchor = CENTER)
        classroom_table.heading("classroom_id", text = "Номер аудитории", anchor = CENTER)
        classroom_table.heading("classroom", text = "Аудитория", anchor = CENTER)

        data = []
        for room in Classroom.select():
            data.append([room.classroom_id, room.room_number])
        for record in data:
            classroom_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1]))

        def Add_room():
            try:
                name = txt_room.get()
                if name != "":
                    room = Classroom.create(classroom_id = None, room_number = name)
                    for room in Classroom.select():
                        data.append([room.classroom_id, room.room_number])
                    record = data[-1]
                    classroom_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1]))
                rooms = []
            except:
                messagebox.showerror('Ошибка', 'Вы уже добавили эту аудиторию!')
        def Remove_room():
            try:
                selected_item = classroom_table.selection()[0]
                values = classroom_table.item(selected_item, option="values")
                db.execute_sql('delete from teachers_time_used')
                db.execute_sql('delete from lesson_hours_used')
                db.execute_sql('delete from classroom_time')
                db.execute_sql('delete from timetable')
                try:
                    sql = 'delete from classroom_time where classroom_id = {0}'
                    db.execute_sql(sql.format(values[0]))
                    room = Classroom.get_by_id(values[0])
                    room_number = room.room_number
                    for current in subject_has_room_table.get_children():
                        record = subject_has_room_table.item(current)["values"]
                        if str(record[1]) == str(room_number):
                            subject = record[0]
                            subject_has_room_table.delete(current)

                    for current in subject_table.get_children():
                        record = subject_table.item(current)["values"]
                        if str(record[1]) == str(subject):
                            subject_table.item(current, values = (record[0], record[1], record[2], "нет"))
                    db.execute_sql('delete from subjects_has_classrooms where classroom_id = {}'.format(values[0]))
                    classroom_table.delete(selected_item)
                    Classroom.delete_by_id(values[0])
                except:
                    messagebox.showerror('Ошибка', 'Вы не можете удалить эту аудиторию, пока к ней привязан класс!')
            except:
                messagebox.showerror('Ошибка', 'Перед тем как удалить аудиторию, вам нужно выбрать её!')


        label_room = Label(self.Classrooms, text="Введите номер аудитории")
        label_room.pack()
        txt_room = Entry(self.Classrooms, width = 25)  
        txt_room.pack()
        button_room = Button(self.Classrooms, text="добавить", command = Add_room)
        button_room.pack()
        button_room_remove = Button(self.Classrooms, text="Убрать выбранную аудиторию", command = Remove_room)
        button_room_remove.pack()
#------------------------

#классы
    def _initClass(self):
        class_frame= Frame(self.Classes)
        class_frame.pack(pady = 10)
        
        class_scroll = Scrollbar(class_frame)
        class_scroll.pack(side = RIGHT, fill = Y)

        class_table = ttk.Treeview(class_frame, yscrollcommand = class_scroll.set, selectmode = "extended")
        class_table.pack()
        class_scroll.config(command = class_table.yview)
        
        class_table['columns'] = ("class_id", "class_name", "classroom_id", "separate")

        class_table.column("#0", width = 0, stretch = NO)
        class_table.column("class_id", anchor = CENTER, width = 140)
        class_table.column("class_name", anchor = CENTER, width = 140)
        class_table.column("classroom_id", anchor = CENTER, width = 140)
        class_table.column("separate", anchor = CENTER, width = 140)
        class_table.heading("#0", text = "", anchor = CENTER)
        class_table.heading("class_id", text = "Номер класса", anchor = CENTER)
        class_table.heading("class_name", text = "Класс", anchor = CENTER)
        class_table.heading("classroom_id", text = "Аудитория", anchor = CENTER)
        class_table.heading("separate", text = "Разделён на подгруппы", anchor = CENTER)

        data = []
        for cls in Classes.select():
            data.append([cls.class_id, cls.class_name, cls.classroom_id, cls.separate])
        for record in data:
            room = Classroom.get_by_id(record[2])
            if record[3] == 1:
                class_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], room.room_number, "да"))
            else:
                class_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], room.room_number, "нет"))

        def Add_cls():
            self.window2 = Toplevel()
            self.window2.title("Добавить класс")
            self.window2.geometry('400x200')
            self.window2.grab_set()
            self.window2.focus_set()
            label1 = Label(self.window2, text="Введите название класса:")
            label1.pack()
            global txt_class
            txt_class = Entry(self.window2, width = 25)
            txt_class.pack()
            label2 = Label(self.window2, text="Выберите аудиторию дял класса:")
            label2.pack()
            global combo_rooms2
            combo_rooms2 = Combobox(self.window2)
            rooms = []
            for room in Classroom.select():
                rooms.append(room.room_number)
            combo_rooms2['values'] = (rooms)  
            combo_rooms2.current(0)
            combo_rooms2.pack()
            add_button = Button(self.window2, text="Добавить класс", command = Add_cls2)
            add_button.pack()

        def Add_cls2():
            try:
                name = txt_class.get()
                room_val = combo_rooms2.get()
                for room in Classroom.select():
                    if room.room_number == room_val:
                        id_room = room.classroom_id

                if name != "":
                    cls = Classes.create(class_id = None, class_name = name, classroom_id = id_room, separate = 0)
                    data = []
                    for cls in Classes.select():
                        data.append([cls.class_id, cls.class_name, cls.classroom_id, cls.separate])
                    record = data[-1]
                    class_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], room_val, "нет"))
                    self.window2.destroy()
                else:
                    self.window2.destroy()
                    messagebox.showerror('Ошибка', 'Введите название класса!')
            except:
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Уже существует класс с таким названием или выбранная вами аудитория занята другим классом!')
    
                
        def Remove_cls():
            try:
                selected_item = class_table.selection()[0]
                values = class_table.item(selected_item, option="values")
                db.execute_sql('delete from teachers_time_used')
                db.execute_sql('delete from lesson_hours_used')
                db.execute_sql('delete from classroom_time')
                db.execute_sql('delete from timetable')
                if values[3] == "да":
                    Unite_cls()
                delete_ref_classes(values[0])
                class_table.delete(selected_item)
                Classes.delete_by_id(values[0])
            except:
                messagebox.showerror('Ошибка', 'Перед тем как удалить класс, нужно выбрать его!')

        def Separate_cls():
            try:
                selected_item = class_table.selection()[0]
                values = class_table.item(selected_item, option="values")
                if values[3] != "да":
                    self.window2 = Toplevel()
                    self.window2.title("")
                    self.window2.geometry('400x200')
                    self.window2.grab_set()
                    self.window2.focus_set()
                    label1 = Label(self.window2, text="Введите имя первой группы класса {}:".format(values[1]))
                    label1.pack()
                    global txt_1
                    txt_1 = Entry(self.window2, width = 25)
                    txt_1.pack()
                    label2 = Label(self.window2, text="Введите имя первой группы класса {}:".format(values[1]))
                    label2.pack()
                    global txt_2 
                    txt_2 = Entry(self.window2, width = 25)
                    txt_2.pack()
                    separate = Button(self.window2, text="Разделить класс", command = Separate_cls2)
                    separate.pack()
                else:
                    messagebox.showerror('Ошибка', 'Вы уже разделили этот класс')
            except:
                messagebox.showerror('Ошибка', 'Нужно выбрать класс, который вы хотите разделить!')
        def Separate_cls2():
            try:
                name1 = txt_1.get()
                name2 = txt_2.get()
                if name1 != "" and name2 != "":
                    selected_item = class_table.selection()[0]
                    values = class_table.item(selected_item, option="values")
                    cls_id = values[0]
                    cls = Classes()
                    cls.class_id = values[0]
                    cls.separate = 1
                    cls.save()
                    class_table.item(selected_item, values = (values[0], values[1], values[2], "да"))
                    grou1 = Group.create(group_id = None, group_name = name1, class_id = cls_id)
                    grou2 = Group.create(group_id = None, group_name = name2, class_id = cls_id)
                    self.window2.destroy()
                    for grou in Group.select():
                        data.append([grou.group_id, grou.group_name, grou.class_id])
                    record = data[-2]
                    cls = Classes.get_by_id(record[2])
                    group_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], cls.class_name))
                    record = data[-1]
                    cls = Classes.get_by_id(record[2])
                    group_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], cls.class_name))
                else:
                    selected_item = class_table.selection()[0]
                    values = class_table.item(selected_item, option="values")
                    cls_id = values[0]
                    cls = Classes()
                    cls.class_id = values[0]
                    cls.separate = 0
                    cls.save()
                    class_table.item(selected_item, values = (values[0], values[1], values[2], "нет"))
                    self.window2.destroy()
                    messagebox.showerror('Ошибка', 'Нужно ввести названия обеих групп!')
            except:
                selected_item = class_table.selection()[0]
                values = class_table.item(selected_item, option="values")
                cls_id = values[0]
                cls = Classes()
                cls.class_id = values[0]
                cls.separate = 0
                cls.save()
                class_table.item(selected_item, values = (values[0], values[1], "нет"))
                cls = Group.get(Group.class_id == values[0])
                cls.delete_instance()
                cls = Group.get(Group.class_id == values[0])
                cls.delete_instance()
                for current in group_table.get_children():
                    record = group_table.item(current)["values"]
                    cls = Classes.get_by_id(values[0])
                    cls1 = cls.class_name
                    if record[2] == cls1:
                        group_table.delete(current)
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Уже существует группа с таким названием!')
                
        def Unite_cls():
            try:
                selected_item = class_table.selection()[0]
                values = class_table.item(selected_item, option="values")
                if values[3] != "нет":
                    cls = Classes()
                    cls.class_id = values[0]
                    cls.separate = 0
                    cls.save()
                    class_table.item(selected_item, values = (values[0], values[1], values[2], "нет"))
                    db.execute_sql('delete from lesson_hours where class_id = {}'.format(values[0]))
                    db.execute_sql('delete from groups where class_id = {}'.format(values[0]))
                    for current in group_table.get_children():
                        record = group_table.item(current)["values"]
                        cls = Classes.get_by_id(values[0])
                        cls1 = cls.class_name
                        if record[2] == cls1:
                            group_table.delete(current)
                else:
                    messagebox.showerror('Ошибка', 'Вы уже объединили этот класс')
            except:
                messagebox.showerror('Ошибка', 'Нужно выбрать класс, который вы хотите объединить!')

        button_cls = Button(self.Classes, text="Добавить класс", command = Add_cls)
        button_cls.pack()
        button_cls_remove = Button(self.Classes, text="Убрать выбранный класс", command = Remove_cls)
        button_cls_remove.pack()
        button_cls_separate = Button(self.Classes, text="Разделить выбранный класс на подгруппы", command = Separate_cls)
        button_cls_separate.pack()
        button_cls_unite = Button(self.Classes, text="Объединить выбранный класс", command = Unite_cls)
        button_cls_unite.pack()
        label_groups = Label(self.Classes, text="Группы")
        label_groups.pack()
        
        group_frame= Frame(self.Classes)
        group_frame.pack(pady = 10)
        group_scroll = Scrollbar(group_frame)
        group_scroll.pack(side = RIGHT, fill = Y)
        group_table = ttk.Treeview(group_frame, yscrollcommand = class_scroll.set, selectmode = "extended")
        group_table.pack()
        group_scroll.config(command = class_table.yview)
        group_table['columns'] = ("group_id", "group_name", "class_id")
        group_table.column("#0", width = 0, stretch = NO)
        group_table.column("group_id", anchor = CENTER, width = 140)
        group_table.column("group_name", anchor = CENTER, width = 140)
        group_table.column("class_id", anchor = CENTER, width = 140)
        group_table.heading("#0", text = "", anchor = CENTER)
        group_table.heading("group_id", text = "Номер Группы", anchor = CENTER)
        group_table.heading("group_name", text = "Группа", anchor = CENTER)
        group_table.heading("class_id", text = "Класс", anchor = CENTER)
        data2 = []
        for grou in Group.select():
            data2.append([grou.group_id, grou.group_name, grou.class_id])
        for record in data2:
            cls = Classes.get_by_id(record[2])
            group_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], cls.class_name))
#------------------------

#расписание звонков
    def _initCall_table(self):
        def edit_time():
            self.window2 = Toplevel()
            self.window2.title("Расписание звонков")
            self.window2.geometry('400x200')
            self.window2.grab_set()
            self.window2.focus_set()
            lesson1 = Label(self.window2, text="Первая пара:")
            lesson1.grid(column=0, row=1)
            lesson2 = Label(self.window2, text="Вторая пара:")
            lesson2.grid(column=0, row=2)
            lesson3 = Label(self.window2, text="Третья пара:")
            lesson3.grid(column=0, row=3)
            lesson4 = Label(self.window2, text="Четвёртая пара:")
            lesson4.grid(column=0, row=4)
            lesson_begin = Label(self.window2, text = "Начало")
            lesson_begin.grid(column=1, row=0)
            lesson_end = Label(self.window2, text = "Окончание")
            lesson_end.grid(column=2, row=0)
            save = Button(self.window2, text="Сохранить изменения", command = edit_time2)
            save.grid(column=0, row=5)
            global lesson_1_begin1
            global lesson_1_end1
            global lesson_2_begin2
            global lesson_2_end2
            global lesson_3_begin3
            global lesson_3_end3
            global lesson_4_begin4
            global lesson_4_end4
            lesson_1_begin1 = Entry(self.window2, width = 10)  
            lesson_1_begin1.grid(column=1, row=1)
            lesson_1_end1 = Entry(self.window2, width = 10)  
            lesson_1_end1.grid(column=2, row=1)
            lesson_2_begin2 = Entry(self.window2, width = 10)  
            lesson_2_begin2.grid(column=1, row=2)
            lesson_2_end2 = Entry(self.window2, width = 10)  
            lesson_2_end2.grid(column=2, row=2)
            lesson_3_begin3 = Entry(self.window2, width = 10)  
            lesson_3_begin3.grid(column=1, row=3)
            lesson_3_end3 = Entry(self.window2, width = 10)  
            lesson_3_end3.grid(column=2, row=3)
            lesson_4_begin4 = Entry(self.window2, width = 10)  
            lesson_4_begin4.grid(column=1, row=4)
            lesson_4_end4 = Entry(self.window2, width = 10)  
            lesson_4_end4.grid(column=2, row=4)
        def edit_time2():
            begin1 = lesson_1_begin1.get()
            end1 = lesson_1_end1.get()
            begin2 = lesson_2_begin2.get()
            end2 = lesson_2_end2.get()
            begin3 = lesson_3_begin3.get()
            end3 = lesson_3_end3.get()
            begin4 = lesson_4_begin4.get()
            end4 = lesson_4_end4.get()
            if begin1 != "" and end1 != "" and begin2 != "" and end2 != "" and begin3 != "" and end3 != "" and begin4 != "" and end4 != "":
                try:
                    subj = Call_table()
                    subj.lesson_number = 1
                    subj.lesson_begin = begin1
                    subj.lesson_end = end1
                    subj.save()
                    lesson_1_begin.configure(text=begin1)
                    lesson_1_end.configure(text=end1)
                    subj.lesson_number = 2
                    subj.lesson_begin = begin2
                    subj.lesson_end = end2
                    subj.save()
                    lesson_2_begin.configure(text=begin2)
                    lesson_2_end.configure(text=end2)
                    subj.lesson_number = 3
                    subj.lesson_begin = begin3
                    subj.lesson_end = end3
                    subj.save()
                    lesson_3_begin.configure(text=begin3)
                    lesson_3_end.configure(text=end3)
                    subj.lesson_number = 4
                    subj.lesson_begin = begin4
                    subj.lesson_end = end4
                    subj.save()
                    lesson_4_begin.configure(text=begin4)
                    lesson_4_end.configure(text=end4)
                    self.window2.destroy()
                except:
                    self.window2.destroy()
                    messagebox.showerror('Ошибка', 'Время звонков не должно совпадать!')

            else:
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Нужно заполнить все поля!')
        def edit_monday():
            self.window2 = Toplevel()
            self.window2.title("...")
            self.window2.geometry('400x200')
            self.window2.grab_set()
            self.window2.focus_set()
            global date
            label1 = Label(self.window2, text = "Введите новую дату понедельника")
            label1.pack()
            date = Entry(self.window2, width = 10)
            date.pack()
            edit = Button(self.window2, text="Изменить дату понедельника", command = edit_monday2)
            edit.pack()
        def edit_monday2():
            day = date.get()
            if day != "":
                try:
                    data = day.split('.')
                    day_1 = int(data[0])
                    mounth = int(data[1])
                    if day_1 > 31 or mounth > 12 or (day_1 > 28 and mounth == 2) or (day_1 > 30 and (mounth == 4 or mounth == 6 or mounth == 9 or mounth == 11)):
                        self.window2.destroy()
                        messagebox.showerror('Ошибка', 'Введена некорректная дата!')
                    else:
                        subj = Option()
                        subj.option_id = 2
                        subj.option_value = day
                        subj.save()
                        monday.configure(text="Дата понедельника: {}".format(day))
                        self.window2.destroy()
                except:
                    self.window2.destroy()
                    messagebox.showerror('Ошибка', 'Введите дату в формате: ДД.ММ !')
            else:
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Сначала введите дату!')
        def edit_weak():
            self.window2 = Toplevel()
            self.window2.title("...")
            self.window2.geometry('400x200')
            self.window2.grab_set()
            self.window2.focus_set()
            global date
            label1 = Label(self.window2, text = "Введите номер недели")
            label1.pack()
            date = Entry(self.window2, width = 10)
            date.pack()
            edit = Button(self.window2, text="Изменить номер недели", command = edit_weak2)
            edit.pack()
        def edit_weak2():
            day = date.get()
            if day != "":
                subj = Option()
                subj.option_id = 1
                subj.option_value = day
                subj.save()
                weak.configure(text="Номер недели: {}".format(day))
                self.window2.destroy()
            else:
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Сначала введите номер недели!')

        lesson1 = Label(self.Call_time, text="Первая пара:")
        lesson1.grid(column=0, row=1)
        lesson2 = Label(self.Call_time, text="Вторая пара:")
        lesson2.grid(column=0, row=2)
        lesson3 = Label(self.Call_time, text="Третья пара:")
        lesson3.grid(column=0, row=3)
        lesson4 = Label(self.Call_time, text="Четвёртая пара:")
        lesson4.grid(column=0, row=4)
        lesson_begin = Label(self.Call_time, text = "Начало")
        lesson_begin.grid(column=1, row=0)
        lesson_end = Label(self.Call_time, text = "Окончание")
        lesson_end.grid(column=2, row=0)
        call = Call_table.get_by_id(1)
        global lesson_1_begin
        global lesson_1_end
        global lesson_2_begin
        global lesson_2_end
        global lesson_3_begin
        global lesson_3_end
        global lesson_4_begin
        global lesson_4_end
        global weak
        global monday
        lesson_1_begin = Label(self.Call_time, text = call.lesson_begin)
        lesson_1_begin.grid(column=1, row=1)
        lesson_1_end = Label(self.Call_time, text = call.lesson_end)
        lesson_1_end.grid(column=2, row=1)
        call = Call_table.get_by_id(2)
        lesson_2_begin = Label(self.Call_time, text = call.lesson_begin)
        lesson_2_begin.grid(column=1, row=2)
        lesson_2_end = Label(self.Call_time, text = call.lesson_end)
        lesson_2_end.grid(column=2, row=2)
        call = Call_table.get_by_id(3)
        lesson_3_begin = Label(self.Call_time, text = call.lesson_begin)
        lesson_3_begin.grid(column=1, row=3)
        lesson_3_end = Label(self.Call_time, text = call.lesson_end)
        lesson_3_end.grid(column=2, row=3)
        call = Call_table.get_by_id(4)
        lesson_4_begin = Label(self.Call_time, text = call.lesson_begin)
        lesson_4_begin.grid(column=1, row=4)
        lesson_4_end = Label(self.Call_time, text = call.lesson_end)
        lesson_4_end.grid(column=2, row=4)
        edit = Button(self.Call_time, text="Изменить расписание звонков", command = edit_time)
        edit.grid(column=0, row=5)
        call = Option.get_by_id(2)
        monday = Label(self.Call_time, text = "Дата понедельника: {}".format(call.option_value))
        monday.grid(column=0, row=6)
        edit_monday = Button(self.Call_time, text="Изменить дату понедельника", command = edit_monday)
        edit_monday.grid(column=1, row=6)
        call = Option.get_by_id(1)
        weak = Label(self.Call_time, text = "Номер недели: {}".format(call.option_value))
        weak.grid(column=0, row=7)
        edit_weak = Button(self.Call_time, text="Изменить номер недели", command = edit_weak)
        edit_weak.grid(column=1, row=7)
#------------------------

#Количество часов
    def _initHours(self):
        def show():
            #db.execute_sql('delete from lesson_hours')
            for current in hour_table.get_children():
                hour_table.delete(current)
            for subj in Subject.select():
                subj_id = subj.subject_id
                for cls in Classes.select():
                    cls_id = cls.class_id
                    cls_sep = cls.separate
                    if cls_sep == 1:
                        for grou in Group.select():
                            cls_id1 = grou.class_id
                            if str(cls_id1) == str(cls_id):
                                grou_id = grou.group_id
                                try:
                                    abc = Lesson_hour.select().where(Lesson_hour.subject_id == subj_id, Lesson_hour.class_id == cls_id, Lesson_hour.group_id == grou_id).get()
                                except:
                                    abc = Lesson_hour.create(subject_id = subj_id, class_id = cls_id, group_id = grou_id, hours = 0, lesson_hour_id = None)
                    else:
                        try:
                            abc = Lesson_hour.select().where(Lesson_hour.subject_id == subj_id, Lesson_hour.class_id == cls_id, Lesson_hour.group_id == None).get()
                        except:
                            abc = Lesson_hour.create(subject_id = subj_id, class_id = cls_id, group_id = None, hours = 0, lesson_hour_id = None)
            data = []
            for hour in Lesson_hour.select():
                try:
                    grou = Group.get_by_id(hour.group_id)
                    subj = Subject.get_by_id(hour.subject_id)
                    data.append([grou.group_name, subj.subject_name, hour.hours])
                except:
                    cls = Classes.get_by_id(hour.class_id)
                    subj = Subject.get_by_id(hour.subject_id)
                    data.append([cls.class_name, subj.subject_name, hour.hours])
            for record in data:
                hour_table.insert(parent = "", index= "end",text = "", values=(record[0], record[1], record[2]))




        def hour_edit():
            hours = txt_hour.get()
            if hours != '':
                try:
                    hours = int(hours)
                    selected_item = hour_table.selection()[0]
                    if hours < 0:
                        abc = "asd"
                        int(abc)
                    values = hour_table.item(selected_item, option="values")
                    hour_table.item(selected_item, values = (values[0], values[1], hours))
                    subject_name = values[1]
                    clsgrou = values[0]
                    subject_id = Subject.select().where(Subject.subject_name == subject_name).get()
                    try:
                        group_id = Group.select().where(Group.group_name == clsgrou).get()
                        cls = Group.get_by_id(group_id)
                        class_id = cls.class_id
                        lesson_hour_id = Lesson_hour.select().where(Lesson_hour.group_id == group_id, Lesson_hour.subject_id == subject_id).get()
                        subj = Lesson_hour()
                        subj.lesson_hour_id = lesson_hour_id
                        subj.class_id = class_id
                        subj.group_id = group_id
                        subj.subject_id = subject_id
                        subj.hours = hours
                        subj.save()
                    except:
                        class_id = Classes.select().where(Classes.class_name == clsgrou).get()
                        lesson_hour_id = Lesson_hour.select().where(Lesson_hour.class_id == class_id, Lesson_hour.subject_id == subject_id).get()
                        subj = Lesson_hour()
                        subj.lesson_hour_id = lesson_hour_id
                        subj.class_id = class_id
                        subj.group_id = None
                        subj.subject_id = subject_id
                        subj.hours = hours
                        subj.save()
                except:
                    messagebox.showerror('Ошибка', 'Вам нужно выбрать запись из таблицы и ввести целое положительное число')
            else:
                messagebox.showerror('Ошибка', 'Вам нужно ввести число!')

        hour_frame= Frame(self.Lesson_hours)
        hour_frame.pack(pady = 10)        
        hour_scroll = Scrollbar(hour_frame)
        hour_scroll.pack(side = RIGHT, fill = Y)
        hour_table = ttk.Treeview(hour_frame, yscrollcommand = hour_scroll.set, selectmode = "extended")
        hour_table.pack()
        hour_scroll.config(command = hour_table.yview)        
        hour_table['columns'] = ("class_id", "subject", "hours")
        hour_table.column("#0", width = 0, stretch = NO)
        hour_table.column("class_id", anchor = CENTER, width = 140)
        hour_table.column("subject", anchor = CENTER, width = 140)
        hour_table.column("hours", anchor = CENTER, width = 155)
        hour_table.heading("#0", text = "", anchor = CENTER)
        hour_table.heading("class_id", text = "Класс/группа", anchor = CENTER)
        hour_table.heading("subject", text = "Предмет", anchor = CENTER)
        hour_table.heading("hours", text = "Количество пар в неделю", anchor = CENTER)
        Button_show = Button(self.Lesson_hours, text="Обновить таблицу", command = show)
        Button_show.pack()
        label_hour = Label(self.Lesson_hours, text="Введите количество пар")
        label_hour.pack()
        txt_hour = Entry(self.Lesson_hours, width = 15)  
        txt_hour.pack()
        button_hour = Button(self.Lesson_hours, text="Изменить количество пар", command = hour_edit)
        button_hour.pack(pady = 5)


#------------------------

#---Информация об преподавателях---
    def _initInfo(self):
        ths_frame= Frame(self.Teachers_time)
        ths_frame.pack(pady = 10)
        
        ths_scroll = Scrollbar(ths_frame)
        ths_scroll.pack(side = RIGHT, fill = Y)

        ths_table = ttk.Treeview(ths_frame, yscrollcommand = ths_scroll.set, selectmode = "extended")
        ths_table.pack()
        ths_scroll.config(command = ths_table.yview)
        
        ths_table['columns'] = ("teacher_id", "subject_id", "class_id")

        ths_table.column("#0", width = 0, stretch = NO)
        ths_table.column("teacher_id", anchor = CENTER, width = 140)
        ths_table.column("subject_id", anchor = CENTER, width = 140)
        ths_table.column("class_id", anchor = CENTER, width = 155)
        ths_table.heading("#0", text = "", anchor = CENTER)
        ths_table.heading("teacher_id", text = "Преподаватель", anchor = CENTER)
        ths_table.heading("subject_id", text = "Предмет", anchor = CENTER)
        ths_table.heading("class_id", text = "Ведёт предмет в классе", anchor = CENTER)
        
        def teacherSelected(event):
            label1 = Label(time_frame, text = "первая пара")
            label1.grid(column = 0, row = 1, padx=10, pady=10)
            label2 = Label(time_frame, text = "вторая пара")
            label2.grid(column = 0, row = 2, padx=10, pady=10)
            label3 = Label(time_frame, text = "третья пара")
            label3.grid(column = 0, row = 3, padx=10, pady=10)
            label4 = Label(time_frame, text = "четвёртая пара")
            label4.grid(column = 0, row = 4, padx=10, pady=10)
            label5 = Label(time_frame, text = "ПН")
            label5.grid(column = 1, row = 0, padx=10, pady=10)
            label6 = Label(time_frame, text = "ВТ")
            label6.grid(column = 2, row = 0, padx=10, pady=10)
            label7 = Label(time_frame, text = "СР")
            label7.grid(column = 3, row = 0, padx=10, pady=10)
            label8 = Label(time_frame, text = "ЧТ")
            label8.grid(column = 4, row = 0, padx=10, pady=10)
            label9 = Label(time_frame, text = "ПТ")
            label9.grid(column = 5, row = 0, padx=10, pady=10)
            label10 = Label(time_frame, text = "СБ")
            label10.grid(column = 6, row = 0, padx=10, pady=10)

            teacher_name = combo_teachers.get()
            teacher_id = Teacher.select().where(Teacher.teacher_name == teacher_name).get()
            info = Teachers_has_subject.select().where(Teachers_has_subject.teacher_id == teacher_id)

            for current in ths_table.get_children():
                ths_table.delete(current)

            for row in info:
                try:
                    group = Group.get_by_id(row.group_id)                    
                    teacher = Teacher.get_by_id(row.teacher_id)                
                    subject = Subject.get_by_id(row.subject_id)                    
                    ths_table.insert(parent = "", index= "end",text = "", values=(teacher.teacher_name, subject.subject_name, group.group_name))                    
                except:
                    classes = Classes.get_by_id(row.class_id)
                    teacher = Teacher.get_by_id(row.teacher_id)                    
                    subject = Subject.get_by_id(row.subject_id)
                    ths_table.insert(parent = "", index= "end",text = "", values=(teacher.teacher_name, subject.subject_name, classes.class_name))                    
                    
            lessons_count = 4
            week_day = 6
            global days
            days = []
            for i in range(lessons_count):
                days.append([])
                for j in range(week_day):
                    days[i].append(IntVar())
                    try:
                        t = Teacher_time.select().where(Teacher_time.teacher_id == teacher_id, Teacher_time.day_name == j + 1, Teacher_time.lesson_number == i + 1).get()
                        days[i][j].set(1)
                    except:
                        days[i][j].set(0)
            k = 0        
            for i in range(lessons_count):
                for j in range(week_day):
                    check = ttk.Checkbutton(time_frame, text="", variable=days[i][j], onvalue=1, offvalue=0 )
                    check.grid(column = j + 1, row = i + 1, padx=10, pady=10)
                    k += 1

        def Add_subj():
            self.window2 = Toplevel()
            self.window2.title("Добавить предмет")
            self.window2.geometry('400x200')
            self.window2.grab_set()
            self.window2.focus_set()
            button_cls = Button(self.window2, text="Объединить предмет с преподавателем в классе", command = Add_subj2cls)
            button_cls.pack()
            button_grou = Button(self.window2, text="Объединить предмет с преподавателем в группе", command = Add_subj2grou)
            button_grou.pack()            
            
        def Add_subj2cls():
            self.window2.destroy()
            self.window2 = Toplevel()
            self.window2.title("Добавить предмет")
            self.window2.geometry('400x200')
            self.window2.grab_set()
            self.window2.focus_set()
            label1 = Label(self.window2, text = "добавить предмет к {}".format(combo_teachers.get()))
            label1.pack()
            label2 = Label(self.window2, text = "Выберите класс:")
            label2.pack()
            global combo_classes1
            global combo_subjects
            combo_classes1 = Combobox(self.window2)
            classes = []
            for cls in Classes.select():
                if cls.separate != 1:
                    classes.append(cls.class_name)
            combo_classes1['values'] = (classes)
            combo_classes1['state'] = 'readonly'
            combo_classes1.current(0)
            combo_classes1.pack()
            label3 = Label(self.window2, text = "Выберите предмет:")
            label3.pack()
            combo_subjects = Combobox(self.window2)
            subjects = []
            for subj in Subject.select():
                subjects.append(subj.subject_name)
            combo_subjects['values'] = (subjects)
            combo_subjects['state'] = 'readonly'
            combo_subjects.current(0)
            combo_subjects.pack()
            button_add = Button(self.window2, text="Добавить", command = Add_subj3cls)
            button_add.pack()
        
        def Add_subj3cls():
            try:
                teacher_name = combo_teachers.get()
                teacher_id = Teacher.select().where(Teacher.teacher_name == teacher_name).get()
                subject_name = combo_subjects.get()
                class_name = combo_classes1.get()
                subject_id = Subject.select().where(Subject.subject_name == subject_name).get()
                class_id = Classes.select().where(Classes.class_name == class_name).get()
                teach_has_subj = Teachers_has_subject.create(teacher_id = teacher_id, subject_id = subject_id, class_id = class_id, group_id = None)

                teacher_name = combo_teachers.get()
                teacher_id = Teacher.select().where(Teacher.teacher_name == teacher_name).get()
                info = Teachers_has_subject.select().where(Teachers_has_subject.teacher_id == teacher_id)
                for current in ths_table.get_children():
                    ths_table.delete(current)
                for row in info:
                    try:
                        group = Group.get_by_id(row.group_id)                    
                        teacher = Teacher.get_by_id(row.teacher_id)                
                        subject = Subject.get_by_id(row.subject_id)                    
                        ths_table.insert(parent = "", index= "end",text = "", values=(teacher.teacher_name, subject.subject_name, group.group_name))                    
                    except:
                        classes = Classes.get_by_id(row.class_id)
                        teacher = Teacher.get_by_id(row.teacher_id)                    
                        subject = Subject.get_by_id(row.subject_id)
                        ths_table.insert(parent = "", index= "end",text = "", values=(teacher.teacher_name, subject.subject_name, classes.class_name))                    
                self.window2.destroy()
            except:
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Данная запись уже существует')

        def Add_subj2grou():
            self.window2.destroy()
            self.window2 = Toplevel()
            self.window2.title("Добавить предмет")
            self.window2.geometry('400x200')
            self.window2.grab_set()
            self.window2.focus_set()
            label1 = Label(self.window2, text = "добавить предмет к {}".format(combo_teachers.get()))
            label1.pack()
            label2 = Label(self.window2, text = "Выберите Группн:")
            label2.pack()
            global combo_classes1
            global combo_subjects
            combo_classes1 = Combobox(self.window2)
            groups = []
            for grou in Group.select():
                groups.append(grou.group_name)
            combo_classes1['values'] = (groups)
            combo_classes1['state'] = 'readonly'
            combo_classes1.current(0)
            combo_classes1.pack()
            label3 = Label(self.window2, text = "Выберите предмет:")
            label3.pack()
            combo_subjects = Combobox(self.window2)
            subjects = []
            for subj in Subject.select():
                subjects.append(subj.subject_name)
            combo_subjects['values'] = (subjects)
            combo_subjects['state'] = 'readonly'
            combo_subjects.current(0)
            combo_subjects.pack()
            button_add = Button(self.window2, text="Добавить", command = Add_subj3grou)
            button_add.pack()
        def Add_subj3grou():
            try:
                teacher_name = combo_teachers.get()
                teacher_id = Teacher.select().where(Teacher.teacher_name == teacher_name).get()
                subject_name = combo_subjects.get()
                group_name = combo_classes1.get()
                subject_id = Subject.select().where(Subject.subject_name == subject_name).get()
                group_id = Group.select().where(Group.group_name == group_name).get()
                cls = Group.get_by_id(group_id)
                class_id = cls.class_id
                teach_has_subj = Teachers_has_subject.create(teacher_id = teacher_id, subject_id = subject_id, class_id = class_id, group_id = group_id)

                teacher_name = combo_teachers.get()
                teacher_id = Teacher.select().where(Teacher.teacher_name == teacher_name).get()
                info = Teachers_has_subject.select().where(Teachers_has_subject.teacher_id == teacher_id)
                for current in ths_table.get_children():
                    ths_table.delete(current)
                for row in info:
                    try:
                        group = Group.get_by_id(row.group_id)                    
                        teacher = Teacher.get_by_id(row.teacher_id)                
                        subject = Subject.get_by_id(row.subject_id)                    
                        ths_table.insert(parent = "", index= "end",text = "", values=(teacher.teacher_name, subject.subject_name, group.group_name))                    
                    except:
                        classes = Classes.get_by_id(row.class_id)
                        teacher = Teacher.get_by_id(row.teacher_id)                    
                        subject = Subject.get_by_id(row.subject_id)
                        ths_table.insert(parent = "", index= "end",text = "", values=(teacher.teacher_name, subject.subject_name, classes.class_name))                    
                self.window2.destroy()
            except:
                self.window2.destroy()
                messagebox.showerror('Ошибка', 'Данная запись уже существует')

            
        def Remove_subj():
            try:
                selected_item = ths_table.selection()[0]
                values = ths_table.item(selected_item, option="values")
                ths_table.delete(selected_item)
                subject_id = Subject.select().where(Subject.subject_name == values[1]).get()
                try:
                    group_id = Group.select().where(Group.group_name == values[2]).get()
                    subj = Teachers_has_subject.get(Teachers_has_subject.group_id == group_id, Teachers_has_subject.subject_id == subject_id)
                except:
                    class_id = Classes.select().where(Classes.class_name == values[2]).get()
                    subj = Teachers_has_subject.get(Teachers_has_subject.class_id == class_id, Teachers_has_subject.subject_id == subject_id)                    
                subj.delete_instance()
            except:
                messagebox.showerror('Ошибка', 'Сначала вам нужно выбрать запись из таблицы')

        def Save_time():
            lessons_count = 4
            week_day = 6
            teacher_name = combo_teachers.get()
            teacher_id = Teacher.select().where(Teacher.teacher_name == teacher_name).get()
            for t in Teacher_time.select():
                if t.teacher_id == teacher_id:
                    t.delete_by_id(t.teacher_time_id) 
            for i in range(lessons_count):
                for j in range(week_day):
                    lesson_id = i + 1
                    day_id = j + 1
                    if days[i][j].get() == 1:
                        t = Teacher_time.create(teacher_time_id = None, teacher_id = teacher_id, day_name = day_id, lesson_number = lesson_id)

        label1 = Label(self.Teachers_time, text="Выберите преподавателя:")
        label1.pack()
        global combo_teachers
        combo_teachers = Combobox(self.Teachers_time)
        combo_teachers['state'] = 'readonly'
        combo_teachers.bind("<<ComboboxSelected>>", teacherSelected)
        teachers = []
        for teach in Teacher.select():
            teachers.append(teach.teacher_name)
        combo_teachers['values'] = (teachers)  
        combo_teachers.current(0)
        combo_teachers.pack()
        button_add_subj = Button(self.Teachers_time, text="Добавить предмет к преподавателю", command = Add_subj)
        button_add_subj.pack()
        button_remove_subj = Button(self.Teachers_time, text="Открепить предмет от преподавателя", command = Remove_subj)
        button_remove_subj.pack(pady=10)

        button_save = Button(self.Teachers_time, text="Сохранить расписание", command = Save_time)
        button_save.pack(pady=10)
        
        global time_frame
        time_frame = ttk.Frame(self.Teachers_time)
        time_frame.pack()
        
        teacherSelected(None)            

#----------------------------------

#------Генерация-----------------           
        button_save = Button(self.createTab, text="Создать расписание", command = create_time)
        button_save.pack(pady=10)        
        '''
        cursor = get_time_teachers()
        for row in cursor.fetchall():
            print(row[0], ' - ', row[2])
        '''

#--------------------------------
        
main = Main('Timetable Maker')







