from database_manager import DatabaseManager

SELECT_TASKS_QUERY = '''
            SELECT * FROM Tasks ORDER BY Deadline
        '''
SUM_TASKS_VALUE_QUERY = '''
    SELECT users.name, SUM(tasks.value)
        FROM users
    LEFT JOIN tasks ON users.ID = tasks.userid
    GROUP BY users.ID
    '''
ADD_IS_ACTIVE_COLUMN_QUERY = '''
    ALTER TABLE users
    ADD is_active boolean DEFAULT true
'''
CHANGE_IS_ACTIVE_TO_FALSE_QUERY = '''
    UPDATE users
    SET
    is_active = false
    WHERE
    age < 18
'''
GET_USERS_ABOVE_18_FRIENDS_QUERY = '''
    SELECT DISTINCT users.name
        FROM users
        WHERE users.ID IN (SELECT friendships.first_user 
            FROM friendships
            INNER JOIN users ON users.age>18 AND users.ID = friendships.second_user
            UNION
            SELECT friendships.second_user 
            FROM friendships
            INNER JOIN users ON users.age>18 AND users.ID = friendships.first_user) 
'''


def print_sorted_tasks(tasks):
    for task in tasks:
        print("ID: ", task[0])
        print("Title: ", task[1])
        print("Estimated Time: ", task[2])
        print("Value: ", task[3])
        print("Deadline: ", task[4])
        print("Assigned to user with ID: ", task[5])
        print("-------")


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_users_table()
    db_manager.create_tasks_table()
    db_manager.create_friendships_table()
    db_manager.add_fake_users(0)
    db_manager.add_fake_tasks(0)
    print_sorted_tasks(db_manager.execute_and_fetch(SELECT_TASKS_QUERY))
    db_manager.execute(GET_USERS_ABOVE_18_FRIENDS_QUERY)
    db_manager.disconnect()
