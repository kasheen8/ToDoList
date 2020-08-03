from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
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
        return f'{self.id}. {self.task}'

Base.metadata.create_all(engine)

while True:
    choice = input("""
1) Today's tasks
2) Add task
0) Exit
    """)
    if choice == '1':
        Session = sessionmaker(bind=engine)
        session = Session()
        rows = session.query(Table).all()
        if len(rows) == 0:
            print("""
Today:
Nothing to do!""")
        else:
            print("Today")
            for row in rows:
                print(row)
    elif choice == '2':
        Session = sessionmaker(bind=engine)
        session = Session()
        new_task = input("Enter task")
        new_row = Table(task=new_task,
                        deadline=datetime.strptime('07-31-2020', '%m-%d-%Y').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif choice == '0':
        print("Bye!")
        sys.exit()







