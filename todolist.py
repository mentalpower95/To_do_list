from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(Task)


class ToDoList:

    today = datetime.today()
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    def main(self):
        while True:
            print('1) Today\'s tasks', '2) Week\'s tasks', '3) All tasks', '4) Missed tasks', '5) Add a task',
                  '6) Delete a task', '0) Exit\n', sep='\n')
            choice = input()
            if choice == '0':
                print('\nBye!')
                exit()
            elif choice == '1':
                self.today_tasks()
            elif choice == '2':
                self.week_tasks()
            elif choice == '3':
                all_tasks = query.order_by(Task.deadline).all()
                self.print_info_multi('All tasks:', all_tasks, 'Nothing to do!')
            elif choice == '4':
                missed_tasks = query.filter(self.today.date() > Task.deadline).order_by(Task.deadline).all()
                self.print_info_multi('Missed tasks:', missed_tasks, 'All tasks have been completed!')
            elif choice == '5':
                self.add_task()
            elif choice == '6':
                self.delete_task()
            print('')

    def today_tasks(self):
        print('Today', self.today.day, self.today.strftime('%b') + ':')
        today_query = query.filter(self.today.date() == Task.deadline).all()
        self.print_info_single(today_query)

    def week_tasks(self):
        for i in range(0, 7):
            next_day = self.today + timedelta(days=i)
            next_tasks = query.filter(next_day.date() == Task.deadline).all()
            print(self.weekdays[next_day.weekday()], next_day.day, next_day.strftime('%b') + ':')
            self.print_info_single(next_tasks)
            if i < 6:
                print('')

    @staticmethod
    def print_info_single(list_of_entries):
        if len(list_of_entries) == 0:
            print('Nothing to do!')
        else:
            for n, row in enumerate(list_of_entries):
                print(f'{n + 1}. {row}')

    @staticmethod
    def print_info_multi(name, list_of_entries, empty_list):
        print(name)
        if len(list_of_entries) == 0:
            print(empty_list)
        else:
            for n, row in enumerate(list_of_entries):
                print(f'{n + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')

    def delete_task(self):
        intro = 'Choose the number of the task you want to delete:'
        delete_list = query.order_by(Task.deadline).all()
        self.print_info_multi(intro, delete_list, 'Nothing to delete')
        task_to_delete = int(input()) - 1
        session.delete(delete_list[task_to_delete])
        session.commit()
        print('The task has been deleted!')

    def add_task(self):
        print('Enter a task')
        new_task = input()
        print('Enter a deadline (yyyy-mm-dd)')
        new_deadline = datetime.strptime(input(), '%Y-%m-%d')
        session.add(Task(task=new_task, deadline=new_deadline))
        session.commit()
        print('The task has been added!')


if __name__ == '__main__':
    ToDoList().main()
