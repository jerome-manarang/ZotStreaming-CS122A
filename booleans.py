import mysql.connector
from db_connection import connect_db

###
#FUNCTION REQUIREMENTS NUMBERS 2-7 (those that return a bool):
#INSERT_VIEWER, ADD_GENRES, DELETE_VIEWER, INSERT_MOVIE, INSERT_SESSION, UPDATE_RELEASE
###


def insert_viewer(uid, email, nickname, street, city, state, zip, genres, joined_date, first, last, subscription):
    db = connect_db()
    cursor = db.cursor()
    
    sql = """
    INSERT INTO viewers (uid, email, nickname, street, city, state, zip, genres, joined_date, first, last, subscription)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    try:
        cursor.execute(sql, (uid, email, nickname, street, city, state, zip, genres, joined_date, first, last, subscription))
        db.commit()
        print("Viewer inserted successfully.")
        return True
    except mysql.connector.Error as e:
        print("Error inserting viewer:", e)
        return False
    finally:
        cursor.close()
        db.close()


def add_genre(uid, genre):
    db = connect_db()
    cursor = db.cursor()

    try:
        # Fetch existing subscription (genres)
        cursor.execute("SELECT subscription FROM viewers WHERE uid = %s", (uid,))
        result = cursor.fetchone()  # Fetch the result properly

        if result is None:
            print("Viewer not found.")
            return False
        
        existing_genres = result[0] if result[0] else ""  # Ensure we don't get None
        new_genres = ";".join(set(existing_genres.split(";") + [genre]))

        # Ensure the result is fully fetched before running another query
        cursor.fetchall()  # Prevent "Unread result found" error

        # Update the subscription field
        update_sql = "UPDATE viewers SET subscription = %s WHERE uid = %s"
        cursor.execute(update_sql, (new_genres, uid))
        db.commit()

        print("Genre added successfully.")
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
        print("Viewer deleted successfully.")
        return True
    except mysql.connector.Error as e:
        print("Error deleting viewer:", e)
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
        print("Movie inserted successfully.")
        return True
    except mysql.connector.Error as e:
        print("Error inserting movie:", e)
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
        print("Session inserted successfully.")
        return True
    except mysql.connector.Error as e:
        print("Error inserting session:", e)
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
        print("Release title updated successfully.")
        return True
    except mysql.connector.Error as e:
        print("Error updating release:", e)
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
    JOIN releases r ON rv.rid = r.rid
    WHERE rv.uid = %s
    ORDER BY r.title ASC;
    """

    try:
        cursor.execute(sql, (uid,))
        results = cursor.fetchall()
        if not results:
            print("No releases found for this viewer.")
            return False
        print("Table - rid, genre, title")
        for row in results:
            print(row)
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

    sql = """
    SELECT r.rid, r.title, COUNT(rv.review_id) AS reviewCount
    FROM reviews rv
    JOIN releases r ON rv.rid = r.rid
    GROUP BY r.rid, r.title
    ORDER BY reviewCount DESC, r.rid DESC
    LIMIT %s;
    """

    try:
        cursor.execute(sql, (N,))
        results = cursor.fetchall()
        if not results:
            print("No popular releases found.")
            return False
        print("Table - rid, title, reviewCount")
        for row in results:
            print(row)
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
        print("Table - rid, release_title, genre, video_title, ep_num, length")
        for row in results:
            print(row)
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
    SELECT v.uid, v.first, v.last
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
        print("Table - UID, first name, last name")
        for row in results:
            print(row)
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
    SELECT v.rid, v.ep_num, v.title, v.length, COALESCE(COUNT(DISTINCT s.uid), 0) AS viewer_count
    FROM videos v
    LEFT JOIN sessions s ON v.rid = s.rid AND v.ep_num = s.ep_num
    WHERE v.rid = %s
    GROUP BY v.rid, v.ep_num, v.title, v.length
    ORDER BY v.rid DESC;
    """

    try:
        cursor.execute(sql, (rid,))
        results = cursor.fetchall()
        if not results:
            print("No videos found for this rid.")
            return False
        print("Table - RID, ep_num, title, length, COUNT")
        for row in results:
            print(row)
        return True
    except mysql.connector.Error as e:
        print("Error fetching videos viewed:", e)
        return False
    finally:
        cursor.close()
        db.close()
