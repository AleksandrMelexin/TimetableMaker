from peewee import *
db = SqliteDatabase('DB/timetable.db')

class Subject(Model):
    subject_id = AutoField()
    subject_name = TextField()
    separate = IntegerField()
    has_room = IntegerField()
    class Meta:
        database = db 
        table_name = 'subjects'

class Classroom(Model):
    classroom_id = AutoField()
    room_number = TextField()
    class Meta:
        database = db 
        table_name = 'classrooms'

class Teacher(Model):
    teacher_id = AutoField()
    teacher_name = TextField()
    class Meta:
        database = db 
        table_name = 'teachers'

class Option(Model):
    option_id = AutoField()
    option_value = TextField()
    class Meta:
        database = db 
        table_name = 'options'

class Classes(Model):
    class_id = AutoField()
    class_name = TextField()
    classroom_id = ForeignKeyField(Classroom, backref='classroom_id')
    separate = IntegerField()
    class Meta:
        database = db 
        table_name = 'classes'

class Group(Model):
    group_id = AutoField()
    group_name = TextField()
    class_id = ForeignKeyField(Classes, backref='class_id')
    class Meta:
        database = db 
        table_name = 'groups'

class Teachers_has_subject(Model):
    teacher_id = ForeignKeyField(Teacher, backref='teacher_id')
    subject_id = ForeignKeyField(Subject, backref='subject_id')
    class_id = ForeignKeyField(Classes, backref='class_id')
    group_id = ForeignKeyField(Classes, backref='group_id')
    class Meta:
        database = db 
        table_name = 'teachers_has_subjects'
        primary_key = CompositeKey('teacher_id', 'subject_id', 'class_id')

class Subjects_has_classroom(Model):
    classroom_id = ForeignKeyField(Classroom, backref='classroom_id')
    subject_id = ForeignKeyField(Subject, backref='subject_id')
    class Meta:
        database = db 
        table_name = 'subjects_has_classrooms'
        primary_key = CompositeKey('subject_id', 'classroom_id')
        
class Lesson_hour(Model):
    lesson_hour_id = AutoField()
    subject_id = ForeignKeyField(Subject, backref='subject_id')
    class_id = ForeignKeyField(Classes, backref='class_id')
    group_id = ForeignKeyField(Group, backref='group_id')
    hours = IntegerField()
    class Meta:
        database = db 
        table_name = 'lesson_hours'

class Lesson_hour_used(Model):
    lesson_hour_id = AutoField()
    subject_id = ForeignKeyField(Subject, backref='subject_id')
    class_id = ForeignKeyField(Classes, backref='class_id')
    group_id = ForeignKeyField(Group, backref='group_id')
    hours = IntegerField()
    class Meta:
        database = db 
        table_name = 'lesson_hours_used'

class Teacher_time(Model):
    day_name = IntegerField()
    teacher_time_id = AutoField()
    lesson_number = IntegerField()
    teacher_id = ForeignKeyField(Teacher, backref='teacher_id')
    class Meta:
        database = db 
        table_name = 'teachers_time'

class Timetable(Model):
    classroom_id = ForeignKeyField(Classroom, backref='classroom_id')
    class_id = ForeignKeyField(Classes, backref='class_id')
    subject_id = ForeignKeyField(Subject, backref='subject_id')
    group_id = ForeignKeyField(Group, backref='group_id')
    teacher_time_id = ForeignKeyField(Teacher_time, backref='teacher_time_id')
    class Meta:
        database = db 
        table_name = 'timetable'
        primary_key = CompositeKey('classroom_id', 'class_id', 'subject_id', 'teacher_time_id')

class Call_table(Model):
    lesson_number = AutoField()
    lesson_begin = TextField()
    lesson_end = TextField()
    class Meta:
        database = db 
        table_name = 'call_table'

class Classroom_time(Model):
    classroom_id = ForeignKeyField(Classroom, backref='classroom_id')
    day_name = IntegerField()
    lesson_number = IntegerField()
    class Meta:
        database = db 
        table_name = 'classroom_time'
        primary_key = CompositeKey('classroom_id', 'day_name', 'lesson_number')
    
def init_session():
    db.execute_sql("PRAGMA foreign_keys = ON")

def get_time_teachers():
    sql = '''
        select ss.cnt, tt.* from teachers_time tt, 
        (
            select count(tt.teacher_id) as cnt, tt.teacher_id from teachers_time tt 
            group by tt.teacher_id
        ) ss
        where tt.teacher_id = ss.teacher_id
        order by tt.day_name, tt.teacher_id , tt.lesson_number           
    '''
    return db.execute_sql(sql)
    
def delete_ref_classes(class_id):
    sql = 'delete from lesson_hours where class_id = {0}'
    db.execute_sql(sql.format(class_id))
    sql = 'delete from teachers_has_subjects where class_id = {0}'
    db.execute_sql(sql.format(class_id))
    
class Teacher_time_used(Model):
    day_name = IntegerField()
    teacher_time_id = AutoField()
    lesson_number = IntegerField()
    teacher_id = ForeignKeyField(Teacher, backref='teacher_id')
    class Meta:
        database = db 
        table_name = 'teachers_time_used'
    

print("classes are ok!")
