class ToDoItem:
    item_id = 0

    def __init__(self, title):
        self.title
        self.done = False
        self.item_id = ToDoItem.item_id
        # 項目が追加されるたびにIDをインクリメント
        ToDoItem.item_id += 1

class ToDoList:
    def __init__(self):
        self.todolist = []

    # 項目の追加
    def add(self, title):
        item = ToDoItem(title)
        self.todolist.append(item)

    # 項目の削除
    def delete(self, item_id):
        item = [x for x in self.todolist if x.item_id == item_id]
        del item[0]

    # doneの値を反転(false -> true)
    def update(self, item_id):
        item = [x for x in self.todolist if x.item_id == item_id]
        item[0].done = not item[0].done

    # リストを返す
    def get_all(self):
        return self.todolist

    # 完了項目を削除
    def delete_doneitem(self):
        self.todolist = [x for x in self.todolist if not x.done]