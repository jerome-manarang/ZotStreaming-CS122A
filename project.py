import sys
import os

from db_connection import connect_db
from booleans import insert_viewer, add_genre, delete_viewer, insert_movie, insert_session, update_release, list_releases, popular_release, release_title, active_viewers, videos_viewed
from import_data import reset_database, import_data

def main():
    if len(sys.argv) < 2:
        print("Error, please input correct parameters: python3 project.py <command> [parameters]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "import":
        if len(sys.argv) != 3:
            print("Error, please input correct parameters: python3 project.py import <folder_name>")
            sys.exit(1)

        folder_name = sys.argv[2]

        #creating absoulte path
        folder_name = os.path.abspath(folder_name)

        #reset to clear
        reset_database()

        success = import_data(folder_name)

        if success == True:
            print("Success")
        else:
            print("Fail")

    elif command == "insertViewer":
        args = sys.argv[2:]  
        if len(args) != 12:
            print("Error, please input correct parameters: python3 project.py insertViewer <uid> <first_name> <last_name> <subscription>")
            sys.exit(1)

        uid, first_name, last_name, subscription = args[:4]
        #genres = args[4]
        #joined_date, first_name, last_name, subscription = args[5:]

        success = insert_viewer(uid, first_name, last_name, subscription)
        if success == True:
            print("Success")
        else:
            print("Fail")

    elif command == "addGenre":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py addGenre <uid> <genre>")
            sys.exit(1)
        success = add_genre(sys.argv[2], sys.argv[3])
        if success == True:
            print("Success")
        else:
            print("Fail")

    elif command == "deleteViewer":
        if len(sys.argv) != 3:
            print("Error, please input correct parameters: python3 project.py deleteViewer <uid>")
            sys.exit(1)
        success = delete_viewer(sys.argv[2])
        if success == True:
            print("Success")
        else:
            print("Fail")

    elif command == "insertMovie":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py insertMovie <rid> <website_url>")
            sys.exit(1)
        success = insert_movie(sys.argv[2], sys.argv[3])
        if success == True:
            print("Success")
        else:
            print("Fail")

    elif command == "insertSession":
        args = sys.argv[2:]  
        if len(args) != 8:
            print("Error, please input correct parameters: python3 project.py insertSession <sid> <uid> <rid> <ep_num> <initiate_at> <leave_at> <quality> <device>")
        else: #parsing
            sid = int(args[0])
            uid = int(args[1])
            rid = int(args[2])
            ep_num = int(args[3])
            initiate_at = args[4]
            leave_at = args[5]
            quality = args[6]
            device = args[7]

        success = insert_session(sid, uid, rid, ep_num, initiate_at, leave_at, quality, device)
        if success == True:
            print("Success")
        else:
            print("Fail")


    elif command == "updateRelease":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py updateRelease <rid> <title>")
            sys.exit(1)
        success = update_release(sys.argv[2], sys.argv[3])
        if success == True:
            print("Success")
        else:
            print("Fail")
    elif command == "listReleases":
        if len(sys.argv) != 3:
            print("Error, please input correct parameters: python3 project.py listReleases <uid>")
            sys.exit(1)
        success = list_releases(sys.argv[2])
        #if success == True:
            #print("Success")
        #else:
            #print("Fail")
    
    elif command == "popularRelease":
        if len(sys.argv) != 3:
            print("Error, please input correct parameters: python3 project.py popularRelease <N>")
            sys.exit(1)
        success = popular_release(sys.argv[2])
        #if success == True:
            #print("Success")
        #else:
            #print("Fail")

    elif command == "releaseTitle":
        if len(sys.argv) != 3:
            print("Error, please input correct parameters: python3 project.py releaseTitle <sid>")
            sys.exit(1)
        success = release_title(sys.argv[2])
        

    elif command == "activeViewer":
        if len(sys.argv) != 5:
            print("Error, please input correct parameters: python3 project.py activeViewer <N> <start:date> <end:date>")
            sys.exit(1)
        success = active_viewers(sys.argv[2], sys.argv[3],sys.argv[4])
      
    elif command == "videosViewed":
        if len(sys.argv) != 3:
            print("Error, please input correct parameters: python3 project.py videosViewed <rid>")
            sys.exit(1)
        success = videos_viewed(sys.argv[2])
        

    #else:
        #print("Unknown command.")
        #sys.exit(1)

if __name__ == "__main__":
    main()