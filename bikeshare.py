import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city
        (str) month  - name of the month or "all"
        (str) day    - name of the day  or "all"
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Please choose from: Chicago, New York City, Washington.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? January, February, March, April, May, June or 'all'?\n").strip().lower()
        if month in MONTHS or month == 'all':
            break
        print("Invalid month. Please enter a month from January to June or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day? Monday, Tuesday, ... Sunday or 'all'?\n").strip().lower()
        if day in DAYS or day == 'all':
            break
        print("Invalid day. Please enter a day of the week or 'all'.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month_index = MONTHS.index(month) + 1
        df = df[df['month'] == month_index]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month_index = df['month'].mode()[0]
    common_month = MONTHS[common_month_index - 1].title()
    print(f"Most Common Month: {common_month}")

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0].title()
    print(f"Most Common Day of Week: {common_day}")

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {common_start}")

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(f"Most Common End Station: {common_end}")

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print(f"Most Common Trip: {common_trip}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time:.0f} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time:.2f} seconds")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print("Counts of User Types:")
        print(user_types.to_string())
    else:
        print("User Type data is not available for this city.")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        print(gender_counts.to_string())
    else:
        print("\nGender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])

        print("\nBirth Year Stats:")
        print(f"Earliest Year of Birth: {earliest}")
        print(f"Most Recent Year of Birth: {recent}")
        print(f"Most Common Year of Birth: {common}")
    else:
        print("\nBirth Year data is not available for this city.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def display_raw_data(df):
    """Displays raw data 5 rows at a time on user request."""
    index = 0
    while True:
        show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no.\n").strip().lower()
        if show_data != 'yes':
            break

        print(df.iloc[index:index + 5])
        index += 5

        if index >= len(df):
            print("No more data to display.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
