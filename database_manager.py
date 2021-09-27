import psycopg2
from faker import Faker


class DatabaseManager:
    connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host="localhost",
            database="MyDB",
            user="postgres",
            password="postgres123"
        )

    def disconnect(self):
        self.connection.close()

    def create_users_table(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users(
                ID SERIAL,
                Name VARCHAR(100) NOT NULL,
                Email VARCHAR(100),
                Phone VARCHAR(100),
                Age INT,
                PRIMARY KEY(ID)
            )
        '''
        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def create_tasks_table(self):
        create_tasks_query = '''
            CREATE TABLE IF NOT EXISTS tasks(
                ID SERIAL,
                Title VARCHAR(100) NOT NULL,
                Estimate_Time INTEGER,
                Value INTEGER,
                Deadline Date,
                UserID INTEGER,
                FOREIGN KEY(UserID)
                    REFERENCES users(ID),
                PRIMARY KEY (ID)
            )
        '''
        cursor = self.connection.cursor()
        cursor.execute(create_tasks_query)
        self.connection.commit()
        cursor.close()

    def create_friendships_table(self):
        create_friendships_query = '''
            CREATE TABLE IF NOT EXISTS friendships(
                FIRST_USER INTEGER,
                SECOND_USER INTEGER,
                FOREIGN KEY (FIRST_USER)
                    REFERENCES users(id),
                FOREIGN KEY (SECOND_USER)
                    REFERENCES users(id)
            )
        '''
        cursor = self.connection.cursor()
        cursor.execute(create_friendships_query)
        self.connection.commit()
        cursor.close()
        fake = Faker()
        for cnt in range(20):
            self.add_friendship(fake.random.randint(1, 20), fake.random.randint(1, 20))

    def add_friendship(self, first_user_id, second_user_id):
        add_friendship_query = ''' INSERT INTO friendships
            VALUES ('{first_user_id}', '{second_user_id}')
        '''
        add_friendship_query = add_friendship_query.format(first_user_id=first_user_id, second_user_id=second_user_id)
        self.execute(add_friendship_query)

    def add_fake_users(self, number):
        fake = Faker()
        cursor = self.connection.cursor()
        for cnt in range(number):
            insert_record_query = '''INSERT INTO users (name, Email, Phone, Age)
             VALUES ('{name}', '{email}', '{phone}', '{age}') '''
            insert_record_query = insert_record_query.format(name=fake.name(), email=fake.email(),
                                                             phone='+' + str(
                                                                 fake.random.randint(111111111111, 999999999999)),
                                                             age=fake.random.randint(1, 100))
            cursor.execute(insert_record_query)
            self.connection.commit()
        cursor.close()

    def add_fake_tasks(self, number):
        fake = Faker()
        cursor = self.connection.cursor()
        for cnt in range(number):
            insert_record_query = '''INSERT INTO tasks (title, estimate_time, value, deadline, userid)
             VALUES ('{title}', '{estimate_time}', '{value}', '{deadline}', '{userid}')'''
            insert_record_query = insert_record_query.format(title=fake.name(),
                                                             estimate_time=fake.random.randint(1, 100),
                                                             value=fake.random.randint(1, 10),
                                                             deadline=fake.date(),
                                                             userid=fake.random.randint(1, 20))
            cursor.execute(insert_record_query)
            self.connection.commit()
        cursor.close()

    def execute_and_fetch(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
