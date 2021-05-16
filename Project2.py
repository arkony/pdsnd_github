import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
citylist=['chicago', 'new york', 'washington']
monthlist=['all', 'january', 'february', 'march', 'april', 'may', 'june']
daydict={0: 'all', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data using Python, pandas, and numpy!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which of the following city\' would you like to view? Chicago, New York or Washington?\n')
        if city.lower() in citylist:
            print("You\'ve entered {}, if you wish to pick a different city, exit now.\n".format(city))
            break
        else:
            print("Please enter a valid city.")
            continue
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to filter? All, January, February, March, April, May, June\n')
        if month.lower() in monthlist:
            print("You\'ve entered {}, if you wish to pick a different month filter, exit now.\n".format(month))
            break
        else:
            print("Please enter a valid month filter.")
            continue
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you like to filter? Please enter an integer. 0=All, 1=Monday, etc.\n')
        try:
            day=int(day)
        except ValueError:
            print('Please input an interger.\n')
        if day in {0,1,2,3,4,5,6,7}:
            print("You\'ve entered {}, if you wish to pick a different day filter, exit now.\n".format(daydict[day]))
            break
        else:
            print("Please enter a valid day filter.")
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df= pd.read_csv(CITY_DATA[city.lower()])
    df["Start Time"]=pd.to_datetime(df["Start Time"])
    df["Month"]=df["Start Time"].dt.month
    df["Weekday"]=df["Start Time"].dt.weekday

    if month != 'all':
        month = monthlist.index(month.lower())
        df = df[df['Month'] == month]
    if day != 0:
        df = df[df['Weekday'] == day-1]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    cm=df['Month'].mode()[0]
    print('The most common month is ' + monthlist[cm] + '.')

    # display the most common day of week
    cd=df['Weekday'].mode()[0] + 1
    print('The most common day of week is ' + daydict.get(cd) + '.')

    # display the most common start hour
    df['Hour']=df['Start Time'].dt.hour
    ch=df['Hour'].mode()[0]
    print('The most common day of hour is ' + str(ch) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    css=df['Start Station'].mode()[0]
    print('The most common start station is ' + css + '.')

    # display most commonly used end station
    ces=df['End Station'].mode()[0]
    print('The most common end station is ' + ces + '.')

    # display most frequent combination of start station and end station trip
    df['SES']='Start: ' + df['Start Station'] + ' and End:' + df['End Station']
    cses=df['SES'].mode()[0]
    print('The most frequent combination of start and end station is:\n    ' + cses + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttt=int(sum(df['Trip Duration']))
    print('The total travel time is '+ str(ttt) + ' seconds.')

    # display mean travel time
    mtt=int(df['Trip Duration'].mean())
    print('The mean travel time is '+ str(mtt) + ' seconds.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cut=df['User Type'].count()
    print('The counts of user types: ' + str(cut))
    cat=df['User Type'].value_counts()
    print('Breakdown of users types:')
    print(cat)
    # Display counts of gender
    if 'Gender' in df:
        gc = df['Gender'].count()
        print('The counts of gender:' + str(gc))
        gd = df['Gender'].value_counts()
        print('Breakdown of Gender:')
        print(gd)
    else:
        print("There is no data for this city's gender.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        ear=df['Birth Year'].min()
        mr=df['Birth Year'].max()
        mc=df['Birth Year'].mode()[0]
        print('The earliest birth year is: ' + str(ear))
        print('The most recent birth year is: ' + str(mr))
        print('The most common birth year is: ' + str(mc))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display(df):
    see = input('Do you want to view the data? Enter \'y\' if you wish to. Enter any key to exit.')
    data=0
    if see.lower() == 'y':
        print(df.head())
        while True:
            more = input('Do you want to view more data? Enter \'y\' if you wish to. Enter any key to exit.')
            if more.lower() == 'y':
                data +=5
                print(df.iloc[data : data + 5])
                continue
            else:
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if month != 'all' and day != 0:
            print('If you wish to calculate the whole data, please restart and don\'t filter.\n')
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
