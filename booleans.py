import mysql.connector
from db_connection import connect_db

###
#FUNCTION REQUIREMENTS NUMBERS 2-7 (those that return a bool):
#INSERT_VIEWER, ADD_GENRES, DELETE_VIEWER, INSERT_MOVIE, INSERT_SESSION, UPDATE_RELEASE
###


def insert_viewer(uid, first_name, last_name, subscription):
    db = connect_db()
    cursor = db.cursor()

    # Check if the uid already exists
    cursor.execute("SELECT uid FROM viewers WHERE uid = %s", (uid,))
    existing_viewer = cursor.fetchone()

    if existing_viewer:
        cursor.close()
        db.close()
        return False  # Duplicate UID found

    
    sql = """
    INSERT INTO viewers (uid, first_name, last_name, subscription)
    VALUES (%s, %s, %s, %s);
    """
    
    try:
        cursor.execute(sql, (uid, first_name, last_name, subscription))
        db.commit()
        #print("Viewer inserted successfully.")
        return True
    except mysql.connector.Error as e:
        #print("Error inserting viewer:", e)
        return False
    finally:
        cursor.close()
        db.close()


def add_genre(uid, genre):
    db = connect_db()
    cursor = db.cursor()

    try:
        
        cursor.execute("SELECT genres FROM users WHERE uid = %s", (uid,))
        result = cursor.fetchone()

        if result is None:
            print("User not found.")
            return False
        
        existing_genres = result[0] if result[0] else "" 

        
        genres_list = existing_genres.split(";") if existing_genres else []
        if genre not in genres_list:
            genres_list.append(genre)
        else:
            return False

        new_genres = ";".join(genres_list)

     
        update_sql = "UPDATE users SET genres = %s WHERE uid = %s"
        cursor.execute(update_sql, (new_genres, uid))
        db.commit()

        
        return True
    except mysql.connector.Error as e:
        print("Error updating genres:", e)
        return False
    finally:
        cursor.close()
        db.close()


def delete_viewer(uid):
    db = connect_db()
    cursor = db.cursor()
    
    sql = "DELETE FROM viewers WHERE uid = %s"
    try:
        cursor.execute(sql, (uid,))
        db.commit()
        #print("Viewer deleted successfully.")
        return True
    except mysql.connector.Error as e:
        #print("Error deleting viewer:", e)
        return False
    finally:
        cursor.close()
        db.close()


def insert_movie(rid, website_url):
    db = connect_db()
    cursor = db.cursor()
    
    sql = "INSERT INTO movies (rid, website_url) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (rid, website_url))
        db.commit()
        #print("Movie inserted successfully.")
        return True
    except mysql.connector.Error as e:
        #print("Error inserting movie:", e)
        return False
    finally:
        cursor.close()
        db.close()


def insert_session(sid, uid, rid, ep_num, initiate_at, leave_at, quality, device):
    db = connect_db()
    cursor = db.cursor()
    
    sql = """
    INSERT INTO sessions (sid, uid, rid, ep_num, initiate_at, leave_at, quality, device)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(sql, (sid, uid, rid, ep_num, initiate_at, leave_at, quality, device))
        db.commit()
        #print("Session inserted successfully.")
        return True
    except mysql.connector.Error as e:
        #print("Error inserting session:", e)
        return False
    finally:
        cursor.close()
        db.close()


def update_release(rid, title):
    db = connect_db()
    cursor = db.cursor()
    
    sql = "UPDATE releases SET title = %s WHERE rid = %s"
    try:
        cursor.execute(sql, (title, rid))
        db.commit()
        #Sprint("Release title updated successfully.")
        return True
    except mysql.connector.Error as e:
        #print("Error updating release:", e)
        return False
    finally:
        cursor.close()
        db.close()

def list_releases(uid):
    db = connect_db()
    cursor = db.cursor()

    sql = """
    SELECT DISTINCT r.rid, r.genre, r.title 
    FROM reviews rv
    JOIN viewers v ON rv.uid = v.uid
    JOIN releases r ON rv.rid = r.rid
    WHERE rv.uid = %s
    ORDER BY r.title ASC;
    """

    try:
        cursor.execute(sql, (uid,))
        results = cursor.fetchall()
        if not results:
            return False
        #print("Table - rid, genre, title")
        for row in results:
            print(",".join(map(str, row)))
        return True
    except mysql.connector.Error as e:
        print("Error fetching releases:", e)
        return False
    finally:
        cursor.close()
        db.close()


def popular_release(N):
    db = connect_db()
    cursor = db.cursor()

    sql = f"""
    SELECT r.rid, r.title, COUNT(rv.rvid) AS reviewCount
FROM reviews rv
JOIN viewers v ON rv.uid = v.uid
JOIN releases r ON rv.rid = r.rid
GROUP BY r.rid, r.title
ORDER BY reviewCount DESC, r.rid DESC
LIMIT %s;

    """

    try:
        cursor.execute(sql, (int(N),))
        results = cursor.fetchall()
        if not results:
            print("No popular releases found.")
            return False
       # print("Table - rid, title, reviewCount")
        for row in results:
            #print(row)
            print(",".join(map(str, row)))
        return True
    except mysql.connector.Error as e:
        print("Error fetching popular releases:", e)
        return False
    finally:
        cursor.close()
        db.close()


def release_title(sid):
    db = connect_db()
    cursor = db.cursor()

    sql = """
    SELECT r.rid, r.title AS release_title, r.genre, v.title AS video_title, s.ep_num, v.length
    FROM sessions s
    JOIN videos v ON s.rid = v.rid AND s.ep_num = v.ep_num
    JOIN releases r ON v.rid = r.rid
    WHERE s.sid = %s
    ORDER BY r.title ASC;
    """

    try:
        cursor.execute(sql, (sid,))
        results = cursor.fetchall()
        if not results:
            print("No release found for this session ID.")
            return False
        #print("Table - rid, release_title, genre, video_title, ep_num, length")
        for row in results:
            print(",".join(map(str, row)))
        return True
    except mysql.connector.Error as e:
        print("Error fetching release title:", e)
        return False
    finally:
        cursor.close()
        db.close()


def active_viewers(N, start_date, end_date):
    db = connect_db()
    cursor = db.cursor()

    sql = """
    SELECT v.uid, v.first_name, v.last_name
    FROM viewers v
    JOIN (
        SELECT uid, COUNT(*) as session_count
        FROM sessions
        WHERE initiate_at BETWEEN %s AND %s
        GROUP BY uid
        HAVING COUNT(*) >= %s
    ) s ON v.uid = s.uid
    ORDER BY v.uid ASC;
    """

    try:
        cursor.execute(sql, (start_date, end_date, N))
        results = cursor.fetchall()
        if not results:
            print("No active viewers found.")
            return False
        #print("Table - UID, first name, last name")
        for row in results:
            print(",".join(map(str, row)))
        return True
    except mysql.connector.Error as e:
        print("Error fetching active viewers:", e)
        return False
    finally:
        cursor.close()
        db.close()


def videos_viewed(rid):
    db = connect_db()
    cursor = db.cursor()

    sql = """
    SELECT v.rid, v.ep_num, v.title, v.length,
       COALESCE(vc.viewer_count, 0) AS viewer_count
FROM videos v
LEFT JOIN (
    SELECT s.rid, COUNT(DISTINCT s.uid) AS viewer_count
    FROM sessions s
    JOIN viewers v ON s.uid = v.uid
    WHERE s.rid = %s
    GROUP BY s.rid
) vc ON v.rid = vc.rid
WHERE v.rid = %s
ORDER BY v.ep_num;


    """

    try:
        cursor.execute(sql, (rid,rid))
        results = cursor.fetchall()
        if not results:
            print("No videos found for this rid.")
            return False
        #print("Table - RID, ep_num, title, length, COUNT")
        for row in results:
            print(",".join(map(str, row)))
        return True
    except mysql.connector.Error as e:
        print("Error fetching videos viewed:", e)
        return False
    finally:
        cursor.close()
        db.close()