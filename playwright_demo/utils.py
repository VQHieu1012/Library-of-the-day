from pymongo import MongoClient
import psycopg2
from acc_pass import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from underthesea import word_tokenize

def store_to_mg(data):
    """
    data: json
    """
    connection_string = f"mongodb://{MONGO_HOSTNAME}:{MONGO_PORT}/"

    client = MongoClient(connection_string)
    
    mydb = client[MONGO_DATABASE]
    
    mycol = mydb[MONGO_COLLECTION]
    
    x = mycol.insert_many(data)
    print("Insert to mongDB !!!")

def store_to_db(data):
    
    # Connect to db
    db_conn = psycopg2.connect(
        host=HOST_DB,
        database=NAME_DB,
        user=USER_DB,
        password=PASSWORD_DB
    )
    cursor = db_conn.cursor()

    # Define query (create table if not exist)
    create_table_query = """
        CREATE TABLE IF NOT EXISTS facebook_comments (
            user_id VARCHAR(20),
            user_name VARCHAR(20),
            comment_text TEXT
        );
    """
    cursor.execute(create_table_query)

    # Insert data to table
    for record in data:
        insert_query = """
            INSERT INTO facebook_comments (user_id, user_name, comment_text)
            VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (record[0], record[1], record[2]))

    db_conn.commit()
    cursor.close()
    db_conn.close()


def remove_stopword(input_text):
    with open('./vietnamese-stopwords.txt', 'r', encoding='utf8') as f:
        stop_words = f.readlines()
        stop_words = set(m.strip() for m in stop_words)

    words = word_tokenize(input_text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def visualize_text(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()