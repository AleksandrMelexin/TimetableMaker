import tkinter as tk
from tkinter import ttk
tree_info = [('bc2e13898123', '127.0.0.1', 'asdasdakkkk', 'True', '21:25 06-10-2020'),
             ('bc2e13898128', 'None', 'asdasda', 'False', 'None'),
             ('bc2e13898125', 'None', 'asdasda', 'False', 'None',),
             ('bc2e13898124', '127.0.0.1', '456', 'True', '10:22 06-10-2020'),
             ('bc2e13898126', '127.0.0.1', 'Не_установлено', 'True', '18:54 07-10-2020'),
             ('bc2e13898121', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898122', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898127', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898128', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898129', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898110', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898111', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898112', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898113', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898114', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898115', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898116', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898117', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898118', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898119', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898120', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898131', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898132', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898133', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898134', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898135', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898136', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898137', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898138', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898139', 'None', 'Не_установлено', 'False', 'None'),
             ('bc2e13898140', 'None', 'Не_установлено', 'False', 'None')]
 
def tree_insert():
    count = 1
    for i in tree_info:
        tree.insert('', tk.END, 'item{}'.format(count), value=(i), tag=(i))
        count += 1
 
#Поиск
def search():
    search_entry_get = search_entry.get()
    id_to_select = ()
    if search_entry_get != '':
        all_tags = root.call(str(tree), "tag", "names")
        tags_to_select = tuple(filter(lambda tag: search_entry_get.lower() in tag.lower(), all_tags))
        for sorted_tag in tags_to_select:
            id_to_select += tree.tag_has(sorted_tag)
    tree.selection_set(id_to_select)
 
root = tk.Tk()
root.minsize(width=650, height=450)
root.maxsize(width=650, height=450)
 
# Определение таблицы
tree = ttk.Treeview(root, column=('ID', 'IP', 'Name', 'Confirm', 'Time'))
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.column('#0', width=40, anchor='center')
tree.column('ID', width=125, anchor='center')
tree.column('IP', width=125, anchor='center')
tree.column('Name', width=145, anchor='center')
tree.column('Confirm', width=115, anchor='center')
tree.column('Time', width=125, anchor='center')
tree.heading('#0', text='Статус')
tree.heading('ID', text='ID')
tree.heading('IP', text='IP-адрес')
tree.heading('Name', text='Имя')
tree.heading('Confirm', text='Подтверждение')
tree.heading('Time', text='Время получения')
 
# Кнопки в окне и их местоположение
search_entry = tk.Entry(root, width=90, border=2)
search_button_form = tk.Button(root, text='Поиск', command=search)
tree.place(x=0, y=60, relwidth=1, height=-25, relheight=0.9)
search_entry.place(x=-320, y=17, relx=0.5)
search_button_form.place(x=252, y=16, relx=0.5)
scrollbar.place(x=-18, relx=1, y=79, height=-45, relheight=0.9)
 
tree_insert()
 
root.mainloop()
