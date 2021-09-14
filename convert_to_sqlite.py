import os
import sqlite3
import re


def mysql_to_sqlite(original_file: str, table_schema = None, dest_sql_file = 'script_file.sql') -> str:
    f_read = open(original_file, 'rb')
    header = f_read.read(10000)

    block_size = header.index(b'VALUES')-1
    f_read.seek(block_size)

    if table_schema is None:
        return 'this is not the correct way to do this... but table_schema cannot be none'

    if os.path.exists(dest_sql_file):
        os.remove(dest_sql_file)

    replace_next = False

    with open(dest_sql_file, 'ab') as f:
        f.write(table_schema)
        while True:
            block = f_read.read(block_size)

            block = block.replace(b"\\'", b" ").replace(b'`', b'')

            block = block.replace(b'UNLOCK TABLES;', b'')

            if replace_next:
                block = block.lstrip(b"'")
            if block.endswith(b'\\'):
                replace_next = True
            else:
                replace_next = False


            if not block:
                break
            else:
                f.write(block)

    f_read.close()

    return dest_sql_file

def get_sample_data(op_type: str) -> str:
    file_in = 'script_file.sql'
    file_out = 'sample.sql'

    if os.path.exists(file_out):
        os.remove(file_out)

    with open(file_in, 'rb') as f:
        if op_type == 'subset':
            data = f.read(500000) # for subset of file
        elif op_type == 'full':
            data = f.read() # for full file
        else:
            return 'needs to be subset or full'


    with open(file_out, 'wb') as f:
        f.write(data)

    return file_out

def sanitize_sql_file(file_in, file_out) -> str:
    if file_name.endswith('.sql'):
        return 'just file name, no extension please'
    
    if os.path.exists(file_out):
        os.remove(file_out)

    regex_str_multifield = rb"(',){2}"
    replace_str_multifield = Rb"',"
    
    regex_str_notclosed = rb" ,'"
    replace_str_notclosed = rb"','"

    regex_str_statusnotclosed = rb"\\ ,"
    replace_str_statusnotclosed = rb"\\',"

    regex_str_trailingbackslash = rb"\\,"
    replace_str_trailingbackslash = rb"\\',"

    with open(file_in, 'rb') as f_in:
        with open(file_out, 'wb') as f_out:
            for l in f_in:
                l_utf = l.decode('utf8')
                # only do regex on long lines (the ones with data)
                if len(l) > 1000:
                    res = re.sub(regex_str_multifield, replace_str_multifield, l)
                    res = re.sub(regex_str_notclosed, replace_str_notclosed, res)
                    res = re.sub(regex_str_statusnotclosed, replace_str_statusnotclosed, res)
                    res = re.sub(regex_str_trailingbackslash, replace_str_trailingbackslash, res)

                    f_out.write(res)

                else:
                    f_out.write(l)

    return file_out

def write_db(db_path = 'steamdata.db', file_in = 'steam_14_sqlite.sql') -> None:
    #!! manually correct file before running me!

    # if os.path.exists(db_path):
    #     os.remove(db_path)
    
    with sqlite3.connect(db_path) as conn:
        try:
            data = open(file_in, 'rb').read()
            conn.executescript(data.decode('utf8'))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    file_name = 'steam_13'
    sqlite_file_name = f'{file_name}_sqlite'
    original_sql = f'{file_name}.sql'
    sqlite_sql = f'{sqlite_file_name}.sql'
    sanitized_sql = f'{sqlite_file_name}_sanitized.sql'

#     table_schema  = b"""CREATE TABLE Games_Publishers (appid integer, Publisher text);
# insert into Games_Publishers
# """

    # # only call this for the steam_x.sql
    # new_sql_file = mysql_to_sqlite(
    #     original_sql,
    #     table_schema,
    #     sqlite_sql
    # )

    # sanitized_file_path = sanitize_sql_file(sqlite_sql, sanitized_sql)

# only call this for small files
    # for large files call from command line
    # .\sqlite3 [database] ".read [script.sql]"
    write_db()
