from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import sys

engine = create_engine('sqlite:///todo.db?check_same_thread=False')



Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.task}'

Base.metadata.create_all(engine)

def tasks_printing(day=datetime.today()):
    """
    Распечатывает все задачи нужного дня
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    rows = session.query(Table).filter(Table.deadline == day.date()).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        number = 1
        for row in rows:
            print(f"{number}. {row}")
            number += 1
    print('\n')

def all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    number = 1
    for row in rows:
        print(f"{number}. {row}. {row.deadline.strftime('%d %b')}")
        number += 1
    return rows

while True:
    choice = input("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
    """)
    Session = sessionmaker(bind=engine)
    session = Session()
    today = datetime.today()

    if choice == '1':
        print(f"Today {today.day} {today.strftime('%b')}")
        tasks_printing(today)

    elif choice == '2':
        for i in range(7):
            day = today + timedelta(days=i)
            print(day.strftime("%A %d %b"))
            tasks_printing(day)

    elif choice == '3':
        print("All tasks:")
        all_tasks()


    elif choice == '4':
        rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
        print("Missed tasks:")
        if len(rows) == 0:
            print("Nothing is missed!")
        else:
            number = 1
            for row in rows:
                print(f"{number}. {row}. {row.deadline.strftime('%d %b')}")
                number += 1

    elif choice == '5':
        new_task = input("Enter task")
        task_deadline = input("Enter deadline")
        new_row = Table(task=new_task,
                        deadline=datetime.strptime(task_deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    elif choice == '6':
        rows = all_tasks()
        task_choice = input("Choose the number of the task you want to delete:")
        session.query(Table).filter(Table.task == rows[int(task_choice) - 1].task).delete()
        session.commit()
        print("The task has been deleted!")



    elif choice == '0':
        print("Bye!")
        sys.exit()







