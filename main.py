from src.auth import AuthenticationSystem


def main():
    auth_system = AuthenticationSystem()
    print("=" * 50)
    print("   SECURE AUTHENTICATION SYSTEM - PHASE 1")
    print("=" * 50)

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. View Audit Log")
        print("4. Exit")
        choice = input("\nChoose option: ").strip()

        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            success, message = auth_system.register(username, password)
            print(message)
        elif choice == '2':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            success, message = auth_system.login(username, password)
            print(message)
        elif choice == '3':
            username = input("Username: ").strip()
            events = auth_system.audit.get_user_events(username)
            for event in events:
                print(f"[{event['timestamp']}] {event['event_type']}: {event['status']}")
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
