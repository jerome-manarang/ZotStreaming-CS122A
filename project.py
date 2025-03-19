import sys
import os
from import_data import reset_database, import_data
from booleans import insert_viewer, add_genre, delete_viewer, insert_movie, insert_session, update_release

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

        # Convert folder_name to an absolute path (supports external folders)
        folder_name = os.path.abspath(folder_name)

        print("Resetting database...")
        reset_database()

        print(f"Importing data from {folder_name}...")
        success = import_data(folder_name)

        if success:
            print("Import successful.")
        else:
            print("Import failed.")

    if command == "insertViewer":
        args = sys.argv[2:]  # Remove 'insertViewer' from args
        if len(args) != 12:
            print("Error, please input correct parameters: python3 project.py insertViewer <uid> <email> <nickname> <street> <city> <state> <zip> <genres> <joined_date> <first> <last> <subscription>")
            sys.exit(1)

        uid, email, nickname, street, city, state, zip_code = args[:7]
        genres = args[7]  # Keep genres as is
        joined_date, first, last, subscription = args[8:]

        success = insert_viewer(uid, email, nickname, street, city, state, zip_code, genres, joined_date, first, last, subscription)
        print(success)

    elif command == "addGenre":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py addGenre <uid> <genre>")
            sys.exit(1)
        success = add_genre(sys.argv[2], sys.argv[3])
        print(success)

    elif command == "deleteViewer":
        if len(sys.argv) != 3:
            print("Error, please input correct parameters: python3 project.py deleteViewer <uid>")
            sys.exit(1)
        success = delete_viewer(sys.argv[2])
        print(success)

    elif command == "insertMovie":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py insertMovie <rid> <website_url>")
            sys.exit(1)
        success = insert_movie(sys.argv[2], sys.argv[3])
        print(success)

    elif command == "insertSession":
        args = sys.argv[2:]  # Remove 'insertSession' from args
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
        print(success)


    elif command == "updateRelease":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py updateRelease <rid> <title>")
            sys.exit(1)
        success = update_release(sys.argv[2], sys.argv[3])
        print(success)

    elif command == "listReleases":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py listReleases <rid> <title>")
            sys.exit(1)
        success = list_releases(sys.argv[2], sys.argv[3])
        print(success)

    elif command == "popularReleases":
        if len(sys.argv) != 4:
            print("Error, please input correct parameters: python3 project.py listReleases <rid> <title>")
            sys.exit(1)
        success = popular_release(sys.argv[2], sys.argv[3])
        print(success)




    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
