import psycopg2
from .config import Config

config = Config()

class Dtabase:
    def __init__(self):
        try:
            self.con = psycopg2.connect(
                host=config['db']['host'],
                database=config['db']['database'],
                user=config['db']['user'],
                password=config['db']['password']
            )

            commands =( """
                    CREATE TABLE IF NOT EXISTS games_ordered  (
                        game_id SERIAL PRIMARY KEY,
                        game_title VARCHAR(255) NOT NULL,
                        game_data JSON NOT NULL
                    )
                """,
                """
                    CREATE TABLE IF NOT EXISTS bot_config (
                        config_id SERIAL PRIMARY KEY,
                        config_data JSON NOT NULL
                    )
                """,
                """
                    CREATE TABLE IF NOT EXISTS browser_cookies (
                        cookie_id SERIAL PRIMARY KEY,
                        cookie_data JSON NOT NULL
                    )
                """
                )
            
            self.cur = self.con.cursor()
            for command in commands:
                self.cur.execute(command)

            self.con.commit()
            print('Created tables')

        except (Exception, psycopg2.DatabaseError) as e:
            print('error db: ' + str(e))

    
    def insert_dta(self, title, data):
        try:
            command = """INSERT INTO games_ordered (game_title, game_data)
                         VALUES ('{0}', '{1}') RETURNING game_id; """.format(title.replace("'", "''"), data.replace("'", "''"))
            
            self.cur.execute(command)

            self.con.commit()
            print('Data_Inserted')

        except (Exception, psycopg2.DatabaseError) as error:
            print('error ins: ' + str(error))

    def ins_conf(self, config):
        try:
            command = """INSERT INTO bot_config (config_id, config_data)
                         VALUES ('1', '{}')
                         ON CONFLICT (config_id)
                         DO
                            UPDATE SET config_data = EXCLUDED.config_data; 
                      """.format(config)
            
            self.cur.execute(command)

            self.con.commit()
            print('Config_Updated')

        except (Exception, psycopg2.DatabaseError) as error:
            print('error cins: ' + str(error))

    def ins_cookie(self, cookie):
        try:
            command = """INSERT INTO browser_cookies (cookie_id, cookie_data)
                         VALUES ('1', '{}')
                         ON CONFLICT (cookie_id)
                         DO
                            UPDATE SET cookie_data = EXCLUDED.cookie_data;
                      """.format(cookie)
            self.cur.execute(command)

            self.con.commit()
            print('Cookie_Updated')
        except Exception as error:
            print('error co: ' + str(error))

    def get_dta(self, tab):
        try:
            self.cur.execute("SELECT * FROM {}".format(tab))
            rows = self.cur.fetchall()
            print('Got_Data')
            
            gdta = {}
            if tab == 'games_ordered':
                for row in rows:
                    gdta[row[1]] = row[2]
                print(gdta)

                return gdta

            elif tab == 'bot_config' or tab == 'browser_cookies':
                print(rows[0][1])
                
                return rows[0][1]

        except (Exception, psycopg2.DatabaseError) as error:
            print('error getd: ' + str(error)) 
            
    def con_close(self):
        self.cur.close()
        self.con.close()
        print('Connection_Closed')

