import sqlite3


def create_candidates():
    conn = sqlite3.connect('voting_system.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    result = cur.execute(sql_query)
    tables = result.fetchall()
    if len(tables) == 0:
        print("Metadata does not exist")
        query_create_table = "CREATE TABLE candidates(id text NOT NULL, name text NOT NULL, " \
                             "votes integer NOT NULL DEFAULT 0, image text, brief_introduction text);"
        cur.execute(query_create_table)

        query_create_table = "CREATE TABLE voting_info(user text NOT NULL UNIQUE, candidate_id text NOT NULL, " \
                             "FOREIGN KEY (candidate_id) REFERENCES candidates (id))"
        cur.execute(query_create_table)

        query_create_list_candidates = "INSERT INTO candidates " \
                                       "('id', 'name', 'votes', 'image', 'brief_introduction') VALUES " \
                                       "('C01', 'Name 1', 0, 'Image 1', 'Intro 1'), " \
                                       "('C02', 'Name 2', 0, 'Image 2', 'Intro 2'), " \
                                       "('C03', 'Name 3', 0, 'Image 3', 'Intro 3'), " \
                                       "('C04', 'Name 4', 0, 'Image 4', 'Intro 4'), " \
                                       "('C05', 'Name 5', 0, 'Image 5', 'Intro 5'), " \
                                       "('C06', 'Name 6', 0, 'Image 6', 'Intro 6'), " \
                                       "('C07', 'Name 7', 0, 'Image 7', 'Intro 7'), " \
                                       "('C08', 'Name 8', 0, 'Image 8', 'Intro 8'), " \
                                       "('C09', 'Name 9', 0, 'Image 9', 'Intro 9'), " \
                                       "('C10', 'Name 10', 0, 'Image 10', 'Intro 10'), " \
                                       "('C11', 'Name 11', 0, 'Image 11', 'Intro 11'), " \
                                       "('C12', 'Name 12', 0, 'Image 12', 'Intro 12'), " \
                                       "('C13', 'Name 13', 0, 'Image 13', 'Intro 13'), " \
                                       "('C14', 'Name 14', 0, 'Image 14', 'Intro 14'), " \
                                       "('C15', 'Name 15', 0, 'Image 15', 'Intro 15'), " \
                                       "('C16', 'Name 16', 0, 'Image 16', 'Intro 16'), " \
                                       "('C17', 'Name 17', 0, 'Image 17', 'Intro 17'), " \
                                       "('C18', 'Name 18', 0, 'Image 18', 'Intro 18'), " \
                                       "('C19', 'Name 19', 0, 'Image 19', 'Intro 19'), " \
                                       "('C20', 'Name 20', 0, 'Image 20', 'Intro 20'); "

        cur.execute(query_create_list_candidates)
        conn.commit()
        conn.close()
    else:
        print("Metadata exists")


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
