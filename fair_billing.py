import sys
from datetime import datetime as dt

def read_input_data(log_file):
    """
    Process the log file to calculate session durations for each user.

    Args:
        log_file (str): Path to the log file.

    Returns:
        user data with session counts and total session times.
    """

    users = {}
    # Initialize start_time and end_time as None
    start_time, end_time = None, None

    # Open and read the log file
    with open(log_file) as file:
        # Iterate through each line in the file
        for line in file:
            parts = line.split()
            if len(parts) != 3:
                continue

            # Extract timestamp, user, and action from line parts
            timestamp_str, user, action = parts
            try:
                timestamp = dt.strptime(timestamp_str, '%H:%M:%S')
            except ValueError:
                continue

            # If action is 'Start', update start_time
            if action == 'Start':
                start_time = timestamp
            # If action is 'End', update end_time and calculate session duration
            elif action == 'End':
                end_time = timestamp
                session_duration = (end_time - start_time).seconds

                # Update user data or initialize if new user
                if user not in users:
                    users[user] = {'sessions': 1, 'total_time': session_duration}
                else:
                    users[user]['sessions'] += 1
                    users[user]['total_time'] += session_duration

    # Handle cases where there are no matching 'End' for 'Start' or vice versa
    for user, data in users.items():
        if start_time and not end_time:
            # If 'End' is missing, add remaining time till the last timestamp
            data['total_time'] += (timestamp - start_time).seconds
        elif end_time and not start_time:
            # If 'Start' is missing, add time from the earliest timestamp
            data['total_time'] += (end_time - timestamp).seconds

    return users

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("insufficient arguments provided please provide command in format: python fair_billing.py input_file_name")
        sys.exit(1)

    # Get input file path from command-line argument
    input_file = sys.argv[1]
    # call function to read data from the input log file
    users = read_input_data(input_file)

    # Write results to 'sample.txt'
    with open('sample.txt', 'w') as output_file:
        for user, data in users.items():
            output_file.write(f"{user} {data['sessions']} {data['total_time']}\n")

if __name__ == "__main__":
    main()
