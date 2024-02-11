import webbrowser
import pathlib
from Classes.database import *
def create_time():
    text_file = open("Templates/body.html", "r")
    body_data = text_file.read()
    text_file.close()
    text_file = open("Templates/class.html", "r")
    class_data = text_file.read()
    text_file.close()
    text_file = open("Templates/day.html", "r")
    day_data = text_file.read()
    text_file.close()
    text_file = open("Templates/lesson.html", "r")
    lesson_data = text_file.read()
    text_file.close()
    text_file = open("Templates/lesson_group.html", "r")
    lesson_group_data = text_file.read()
    text_file.close()
    text_file = open("Templates/main.html", "r")
    main_data = text_file.read()
    text_file.close()
    db.execute_sql('delete from lesson_hours_used')
    db.execute_sql('delete from teachers_time_used')
    db.execute_sql('delete from classroom_time')
    db.execute_sql('delete from timetable')
    for hour in Lesson_hour.select():
        try:
            new = Lesson_hour_used.create(lesson_hour_id = hour.lesson_hour_id, subject_id = hour.subject_id, class_id = hour.class_id, group_id = hour.group_id, hours = hour.hours)
        except:
            new = Lesson_hour_used.create(lesson_hour_id = hour.lesson_hour_id, subject_id = hour.subject_id, class_id = hour.class_id, group_id = None, hours = hour.hours)

    for time in Teacher_time.select():
        new = Teacher_time_used.create(teacher_time_id = time.teacher_time_id, teacher_id = time.teacher_id, day_name = time.day_name, lesson_number = time.lesson_number)
    

    html_class_data = '';
    info_week = Option.get_by_id(1)
    info_monday = Option.get_by_id(2)
    monday = info_monday.option_value
    data = monday.split('.')
    day1 = int(data[0])
    mounth = int(data[1])
    days = []
    if day1 < 10:
        d = '0' + str(day1)
    else:
        d = str(day1)
    if mounth < 10:
        m = '0' + str(mounth)
    else:
        m = str(mounth)
    days.append(d + '.' + m)
    for day_number in range(5):
        if ((day1 + 1) > 31) or ((day1 + 1) > 28 and mounth == 2) or ((day1 + 1) > 30 and (mounth == 4 or mounth == 6 or mounth == 9 or mounth == 11)):
            day1 = 1
            if mounth == 12:
                mounth = 1
            else:
                mounth = mounth + 1
        else:
            day1 = day1 + 1
        if day1 < 10:
            d = '0' + str(day1)
        else:
            d = str(day1)
        if mounth < 10:
            m = '0' + str(mounth)
        else:
            m = str(mounth)
        days.append(d + '.' + m)
    lesson1 = Call_table.get_by_id(1)
    lesson2 = Call_table.get_by_id(2)
    lesson3 = Call_table.get_by_id(3)
    lesson4 = Call_table.get_by_id(4)
    html_class_data += main_data.format(
        week_number = '{}'.format(info_week.option_value),
        day1 = '{}'.format(days[0]),
        day2 = '{}'.format(days[1]),
        day3 = '{}'.format(days[2]),
        day4 = '{}'.format(days[3]),
        day5 = '{}'.format(days[4]),
        day6 = '{}'.format(days[5]),
        begin1 = '{}'.format(lesson1.lesson_begin),
        end1 = '{}'.format(lesson1.lesson_end),
        begin2 = '{}'.format(lesson2.lesson_begin),
        end2 = '{}'.format(lesson2.lesson_end),
        begin3 = '{}'.format(lesson3.lesson_begin),
        end3 = '{}'.format(lesson3.lesson_end),
        begin4 = '{}'.format(lesson4.lesson_begin),
        end4 = '{}'.format(lesson4.lesson_end)
    );
    for cls in Classes.select():
        if cls.separate == 0:
            days = ['1', '2', '3', '4', '5', '6']
            for day in range(6):
                lessons = ['1', '2', '3', '4']
                for lesson in range(4):
                    possible = []
                    for time in Teacher_time_used.select():
                        flag = 0
                        for teach in Teachers_has_subject.select():
                            if str(teach.class_id) == str(cls.class_id) and str(teach.teacher_id) == str(time.teacher_id):
                                flag = 1
                        if time.day_name == day + 1 and time.lesson_number == lesson + 1 and flag == 1:
                            t = Teacher.get_by_id(time.teacher_id)
                            t_id = t.teacher_id
                            possible.append(t_id)
                    print('-----------------------------')
                    print('День: ', day + 1)
                    print('Пара: ', lesson + 1)
                    print('Класс: ', cls.class_name)
                    print('Могут прийти: ', possible)
                    flag = 0
                    i = 0
                    while flag == 0:
                        try:
                            abc = possible[i] + 1
                            teach = Teacher.get_by_id(possible[i])
                            subj = Teachers_has_subject.get(Teachers_has_subject.class_id == cls.class_id, Teachers_has_subject.teacher_id == possible[i])
                            subject = Subject.get_by_id(subj.subject_id)                    
                            room = Classroom.get_by_id(cls.classroom_id)
                            hour = Lesson_hour_used.select().where(Lesson_hour_used.subject_id == subj.subject_id, Lesson_hour_used.class_id == cls.class_id,).get()
                            hours = Lesson_hour_used.get_by_id(hour)
                            print(hours.hours, 'количество часов')
                            print(subj)
                            if hours.hours != 0:
                                print("проверка")
                                if subject.separate == 1:
                                    print("предмет поделён")
                                    try:
                                        print("stage 1")
                                        print(possible)
                                        for teach in possible:
                                            if teach != possible[i]:
                                                subj1 = Teachers_has_subject.get(Teachers_has_subject.class_id == cls.class_id, Teachers_has_subject.teacher_id == teach)
                                                if str(subj.subject_id) == str(subj1.subject_id):
                                                    teacher2 = subj1.teacher_id
                                        print("stage 2", teacher2, possible[i])
                                        room_id1 = cls.classroom_id
                                        f = 0
                                        print("stage 3")
                                        abc1 = Teacher_time_used.get(Teacher_time_used.teacher_id == possible[i], Teacher_time_used.day_name == day + 1, Teacher_time_used.day_name == lesson + 1)
                                        abc1 = Teacher_time_used.get(Teacher_time_used.teacher_id == teacher2, Teacher_time_used.day_name == day + 1, Teacher_time_used.day_name == lesson + 1)
                                        print("stage 4")
                                        for room in Classroom.select():
                                            if f == 0:
                                                try:
                                                    Classroom_time.select().where(Classroom_time.classroom_id == room.classroom_id, Classroom_time.day_name == day + 1, Classroom_time.lesson_number == lesson + 1).get()
                                                except:
                                                    room_id2 = room.classroom_id
                                                    f = 1
                                        print("stage 5", room_id2)
                                        room = Classroom.get_by_id(room_id1)
                                        room_name1 = room.room_number
                                        print("stage 6", room_name1)
                                        room = Classroom.get_by_id(room_id2)
                                        room_name2 = room.room_number
                                        print("stage 7", room_name2)
                                        teach = Teacher.get_by_id(possible[i])
                                        teach_name1 = teach.teacher_name
                                        print("stage 8", teach_name1)
                                        teach = Teacher.get_by_id(teacher2)
                                        teach_name2 = teach.teacher_name
                                        print("stage 9", teach_name2)
                                        lessons[lesson] = lesson_group_data.format(
                                            subject_name = subject.subject_name,
                                            classroom1 = room_name1,
                                            classroom2 = room_name2,
                                            teacher_name1 = teach_name1,
                                            teacher_name2 = teach_name2
                                        )
                                        print("stage 10")
                                        time = Teacher_time_used.get(Teacher_time_used.teacher_id == possible[i], Teacher_time_used.day_name == day + 1, Teacher_time_used.lesson_number == lesson + 1)
                                        time.delete_instance()
                                        print("stage 11")
                                        time = Teacher_time_used.get(Teacher_time_used.teacher_id == teacher2, Teacher_time_used.day_name == day + 1, Teacher_time_used.lesson_number == lesson + 1)
                                        time.delete_instance()
                                        print("stage 12")
                                        edit = Lesson_hour_used()
                                        edit.lesson_hour_id = hour
                                        edit.hours = hours.hours - 1
                                        edit.save()
                                        print(hours.hours, 'количество часов 2')
                                        flag = 1
                                        abc = Classroom_time.create(classroom_id = room_id1, day_name = day + 1, lesson_number = lesson + 1)
                                        abc = Classroom_time.create(classroom_id = room_id2, day_name = day + 1, lesson_number = lesson + 1)
                                    except:
                                        print("ошибка")
                                else:
                                    print("предмет не поделён")
                                    if subject.has_room == 1:
                                        cabinet = Subjects_has_classroom.select().where(Subjects_has_classroom.subject_id == subj.subject_id).get()
                                        room_id = Classroom.get_by_id(cabinet.classroom_id)
                                        room_name = room_id.room_number
                                        room_id = cabinet.classroom_id
                                    else:
                                        room_name = room.room_number
                                        room_id = cls.classroom_id
                                    try:
                                        abc = Classroom_time.select().where(Classroom_time.classroom_id == room_id, Classroom_time.day_name == day + 1, Classroom_time.lesson_number == lesson + 1).get()
                                    except:    
                                        print('поставили пару')
                                        lessons[lesson] = lesson_data.format(
                                            subject_name = subject.subject_name,
                                            classroom = room_name,
                                            teacher_name = teach.teacher_name
                                        )
                                        time = Teacher_time_used.get(Teacher_time_used.teacher_id == possible[i], Teacher_time_used.day_name == day + 1, Teacher_time_used.lesson_number == lesson + 1)
                                        time.delete_instance()
                                        edit = Lesson_hour_used()
                                        edit.lesson_hour_id = hour
                                        edit.hours = hours.hours - 1
                                        edit.save()
                                        print(hours.hours, 'количество часов 2')
                                        flag = 1
                                        abc = Classroom_time.create(classroom_id = room_id, day_name = day + 1, lesson_number = lesson + 1)
                            i = i + 1
                        except:
                            print('пустая ячейка')
                            lessons[lesson] = lesson_data.format(
                                subject_name = '',
                                classroom = '',
                                teacher_name = ''
                            )
                            flag = 1
                                
                    print('-----------------------------')
                    print('')
                days[day] = day_data.format(
                    lesson1 = lessons[0],
                    lesson2 = lessons[1],
                    lesson3 = lessons[2],
                    lesson4 = lessons[3]
                )            
            html_class_data += class_data.format(
                class_name = cls.class_name,
                monday = days[0],
                tuesday = days[1],
                wednesday = days[2],
                thursday = days[3],
                friday = days[4],
                saturday = days[5],
            );
        else:
            print(cls.class_name, "разделён")
            groups = []
            for grou in Group.select():
                if str(grou.class_id) == str(cls.class_id):
                    groups.append(grou.group_id)
            print(groups, "группы")
            days1 = ['', '', '', '', '', '']
            days2 = ['', '', '', '', '', '']
            for day in range(6):
                lessons1 = ['', '', '', '']
                lessons2 = ['', '', '', '']
                for lesson in range(4):
                    possible = []
                    for time in Teacher_time_used.select():
                        flag = 0
                        for teach in Teachers_has_subject.select():
                            if str(teach.class_id) == str(cls.class_id) and str(teach.teacher_id) == str(time.teacher_id):
                                flag = 1
                        if time.day_name == day + 1 and time.lesson_number == lesson + 1 and flag == 1:
                            t = Teacher.get_by_id(time.teacher_id)
                            t_id = t.teacher_id
                            possible.append(t_id)
                    grou1 = Group.get_by_id(groups[0])
                    grou2 = Group.get_by_id(groups[1])
                    print('-----------------------------')
                    print('День: ', day + 1)
                    print('Пара: ', lesson + 1)
                    print('Группы: ', grou1.group_name, " и ", grou2.group_name)
                    print('Могут прийти: ', possible)
                    flag = 0
                    i = 0
                    while flag == 0:
                        try:
                            possible[i] + 1
                            try:
                                teach = Teacher.get_by_id(possible[i])
                                subj1 = Teachers_has_subject.get(Teachers_has_subject.class_id == cls.class_id, Teachers_has_subject.teacher_id == possible[i], Teachers_has_subject.group_id == groups[0])
                                subj2 = Teachers_has_subject.get(Teachers_has_subject.class_id == cls.class_id, Teachers_has_subject.teacher_id == possible[i], Teachers_has_subject.group_id == groups[1])
                                subject = Subject.get_by_id(subj1.subject_id)                    
                                room = Classroom.get_by_id(cls.classroom_id)
                                hour1 = Lesson_hour_used.select().where(Lesson_hour_used.subject_id == subj.subject_id, Lesson_hour_used.class_id == cls.class_id, Lesson_hour_used.group_id == groups[0]).get()
                                hour2 = Lesson_hour_used.select().where(Lesson_hour_used.subject_id == subj.subject_id, Lesson_hour_used.class_id == cls.class_id, Lesson_hour_used.group_id == groups[1]).get()   
                                hours1 = Lesson_hour_used.get_by_id(hour1)
                                hours2 = Lesson_hour_used.get_by_id(hour2)
                                print(hours1.hours, " часов предмета ", subject.subject_name, " у группы ", grou1.group_name)
                                print(hours2.hours, " часов предмета ", subject.subject_name, " у группы ", grou2.group_name)
                                if str(hours1.hours) == str(hours2.hours) and hours2.hours != 0 and hours1.hours != 0:
                                    lessons1[lesson] = lesson_data.format(
                                        subject_name = subject.subject_name,
                                        classroom = room.room_number,
                                        teacher_name = teach.teacher_name
                                    )
                                    lessons2[lesson] = lesson_data.format(
                                        subject_name = subject.subject_name,
                                        classroom = room.room_number,
                                        teacher_name = teach.teacher_name
                                    )
                                    time = Teacher_time_used.get(Teacher_time_used.teacher_id == possible[i], Teacher_time_used.day_name == day + 1, Teacher_time_used.lesson_number == lesson + 1)
                                    time.delete_instance()
                                    edit = Lesson_hour_used()
                                    edit.lesson_hour_id = hour1
                                    edit.hours = hours1.hours - 1
                                    edit.save()
                                    edit = Lesson_hour_used()
                                    edit.lesson_hour_id = hour2
                                    edit.hours = hours2.hours - 1
                                    edit.save()
                                    flag = 1
                                    abc = Classroom_time.create(classroom_id = room_id, day_name = day + 1, lesson_number = lesson + 1)
                                    print("поставил пару")
                            except:
                                print('Пустая ячейка')
                                lessons1[lesson] = lesson_data.format(
                                    subject_name = '',
                                    classroom = '',
                                    teacher_name = ''
                                )
                                lessons2[lesson] = lesson_data.format(
                                    subject_name = '',
                                    classroom = '',
                                    teacher_name = ''
                                )
                                flag = 1
                        except:
                            print('Пустая ячейка')
                            lessons1[lesson] = lesson_data.format(
                                subject_name = '',
                                classroom = '',
                                teacher_name = ''
                            )
                            lessons2[lesson] = lesson_data.format(
                                subject_name = '',
                                classroom = '',
                                teacher_name = ''
                            )
                            flag = 1
                        i = i + 1
                    print('-----------------------------')
                    print('')
                days1[day] = day_data.format(
                    lesson1 = lessons1[0],
                    lesson2 = lessons1[1],
                    lesson3 = lessons1[2],
                    lesson4 = lessons1[3]
                )            
                days2[day] = day_data.format(
                    lesson1 = lessons2[0],
                    lesson2 = lessons2[1],
                    lesson3 = lessons2[2],
                    lesson4 = lessons2[3]
                )
            html_class_data += class_data.format(
                class_name = grou1.group_name,
                monday = days1[0],
                tuesday = days1[1],
                wednesday = days1[2],
                thursday = days1[3],
                friday = days1[4],
                saturday = days1[5],
            );
            html_class_data += class_data.format(
                class_name = grou2.group_name,
                monday = days2[0],
                tuesday = days2[1],
                wednesday = days2[2],
                thursday = days2[3],
                friday = days2[4],
                saturday = days2[5],
            );


    html_body_data = body_data.format(
        classes = html_class_data
    );
    text_file = open("Templates/test.html", "w")
    text_file.write(html_body_data)
    text_file.close()
    path_url = str(pathlib.Path(__file__).parent.absolute())
    path_url = path_url.replace('\\', '/')
    url = "file://{0}/{1}".format(path_url, 'Templates/test.html')
    print(url, " - путь к файлу")
    webbrowser.open(url, 2)
