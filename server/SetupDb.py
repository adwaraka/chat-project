import sqlite3

sqlite_file = 'chat_server.sqlite'    # name of the sqlite database file
table_name1 = 'user_credentials'  # name of the table to be created
table_name2 = 'chat_session'  # name of the table to be created

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('CREATE TABLE {table_name_1} (\
    {user_id} {user_id_field} PRIMARY KEY NOT NULL,\
    {user_name} {user_name_field},\
    {user_password} {user_password_field})'.format(table_name_1=table_name1,\
         user_id="user_id", user_id_field="INTEGER",\
         user_name="user_name", user_name_field="BLOB",\
         user_password="password", user_password_field="BLOB"))

c.execute('CREATE TABLE {table_name_2} (\
    {user_id_1} {user_id_field_1} NOT NULL REFERENCES {user_table}({user_table_field}),\
    {user_id_2} {user_id_field_2} NOT NULL REFERENCES {user_table}({user_table_field}),\
    {chats}     {chat_field},\
    PRIMARY KEY ({user_id_1}, {user_id_2}))'.format(table_name_2=table_name2,\
         user_id_1="user_id_1", user_id_field_1="INTEGER", user_table=table_name1, user_table_field="user_id",\
         user_id_2="user_id_2", user_id_field_2="INTEGER",\
         chats="chat_field", chat_field="BLOB"))


# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
