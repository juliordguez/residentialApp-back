import aiomysql
import asyncio
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()


class DB:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db = os.getenv('DB_NAME')
        self.port = 3306
        self.remote_port = 3306  # Puerto remoto real de la base de datos
        self.pool = None

    async def start_pool(self):
        if self.pool is None:
            try:
                self.pool = await aiomysql.create_pool(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db,
                    minsize=1,  # Número mínimo de conexiones en el pool
                    maxsize=10,  # Número máximo de conexiones en el pool
                    autocommit=True,
                )
                print("Database connection pool successfully established.")
            except aiomysql.Error as e:
                print(f"Error while establishing database connection pool: {e}")
                raise

    async def run_stored_procedure(self, sp_name, sp_params):
        if self.pool is None:
            await self.start_pool()

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.callproc(sp_name, sp_params)
                    result_sets = []
                    more_results = True
                    while more_results:
                        results = await cursor.fetchall()
                        if cursor.description:
                            column_names = [column[0] for column in cursor.description]
                            result_dicts = [dict(zip(column_names, row)) for row in results]
                            result_sets.extend(result_dicts)
                        more_results = await cursor.nextset()
                    return result_sets
                except aiomysql.Error as error:
                    print(f"Error while calling stored procedure: {error}")
                    return []



    async def run_query(self, query, params=None, display_results=False):
        if self.pool is None:
            await self.start_pool()

        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                result_sets = []
                print(" ")
                print("#########################################")
                print(" ")
                print("db_runqyery_query: ", query)
                print("params: ", params)
                print("###################################333")
                print(" ")

                await cursor.execute(query, params)
                if cursor.description:
                    results = await cursor.fetchall()
                    result_sets.extend(results)
                else:
                    print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
                    return cursor.rowcount  # Retornar el número de filas afectadas
                # except aiomysql.Error as error:
                #     print(f"Error while executing query: {error}")
                #     return []

                return result_sets



    async def close_pool(self):
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None
            print("Database connection pool closed.")
