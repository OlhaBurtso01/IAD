import pandas as pd
import matplotlib.pyplot as plt


# створюємо функцію для форматування даних з датафрейму
def reformat_data(df):
    # оскільки дані стягнуті за 2019 рік, то додаємо до day/month ще 2019 рік
    df['day/month'] = df['day/month'] + '.2019'
    # для кращої зручності ми поміняємо назву колонки day/month на Date
    df = df.rename(columns={'day/month': 'Date'}, inplace=False)
    # змінюємо формат дати
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%b.%Y')
    df = df.set_index("Date")
    # змінюємо 12-годинний формат часу(американський) на 24-годинний
    df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%H:%M')
    # для наступних даних нам достатньо забрати розмірність і перетворити в тип int
    df['Humidity'] = df['Humidity'].str[:-1].astype(int)
    df['Wind Speed'] = df['Wind Speed'].str[:-4].astype(int)
    df['Wind Gust'] = df['Wind Gust'].str[:-4].astype(int)

    df['Pressure'] = df['Pressure'].replace(',', '.', regex=True).astype(float)

    return df


# считуємо дані з csv  файлу ('DATABASE.csv')
df = pd.read_csv('DATABASE.csv', delimiter=';', header=0)
df = reformat_data(df)
# виводимо останні 100 рядків датафрейму
print(df.tail(100).to_string())
# виводимо типи даних для перевірки чи всі дані добре відформатовані
print(df.dtypes)


# кругова діаграма для розуміння композиції
def pie_diagram(table, column):
    plt.title(column + ' (pie_diagram)')
    table.groupby(column)[column].count().plot.pie(autopct='%1.1f%%',
                                                   wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "w"}, labeldistance=None)
    plt.legend(loc=1)
    plt.axis('equal')
    plt.show()


# для оцінки розподілу даних
# гістограма
def histogram(table, column):
    plt.title(column + ' (histogram)')
    plt.hist(table[column], bins=20, density=True)
    plt.xticks(rotation=30, horizontalalignment="center")
    plt.xlabel(column)
    plt.ylabel('count')
    plt.show()


# стовпчикова діаграма
def bar_diagram(table, column):
    plt.title(column + ' (bar_diagram)')
    plt.bar(table[column].index, table[column])
    plt.xticks(rotation=30, horizontalalignment="center")
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.show()


# графік розсіювання
def scatter_diagram(table, column):
    plt.title(column + ' (scatter diagram)')
    plt.scatter(table.index, table[column])
    plt.xticks(rotation=30, horizontalalignment="center")
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.show()


# лінійний графік для розуміння відношення між даними
def line_plot(table, column):
    plt.title(column + ' (line diagram)')
    plt.plot(table.groupby('Date').agg({column: 'max'}), label="min")
    plt.plot(table.groupby('Date').agg({column: 'min'}), label="max")
    plt.legend(loc=1)
    plt.xticks(rotation=30, horizontalalignment="center")
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.show()


# "ящик з вусами" для порівняння розподілу
def box_diagram(table, column):
    plt.title(column + ' (box_diagram)')
    table['quartiles'] = pd.qcut(table[column], 4)
    table.boxplot(column=column, by='quartiles')
    plt.show()


# вибір типу графіку
def option(table, column):
    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = (15, 15)
    if str(table[column].dtype) == "object":
        print("For this type of data you can only build pie diagram")
        pie_diagram(table, column)
    else:
        while True:
            print("\n What type of diagram you want use?")
            print("1 - linear \t 2 - histogram \t 3 - bar diagram "
                  "\t 4 - box diagram \t 5 - scatter diagram \t 0 - exit")
            ch = int(input())
            if ch == 1:
                line_plot(table, column)
            elif ch == 2:
                histogram(table, column)
            elif ch == 3:
                bar_diagram(table, column)
            elif ch == 4:
                box_diagram(table, column)
            elif ch == 5:
                scatter_diagram(table, column)
            elif ch == 0:
                return


# вибір колонки даних
def graphic(table):
    while True:
        print("\n\n Please choose name of column:")
        print("1 - Temperature \t 2 - Dew Point \t 3 - Humidity "
              "\t 4 - Wind \t 5 - Wind Speed \n6 - Wind Gust"
              "\t 7 - Pressure \t 8 - Precip. \t 9 - Precip.Accum   \t 10 - Condition")
        print("(if you want exit, just enter 0 )\n")
        column = int(input())
        if column == 1:
            option(table, 'Temperature')
        elif column == 2:
            option(table, 'Dew Point')
        elif column == 3:
            option(table, 'Humidity')
        elif column == 4:
            option(table, 'Wind')
        elif column == 5:
            option(table, 'Wind Speed')
        elif column == 6:
            option(table, 'Wind Gust')
        elif column == 7:
            option(table, 'Pressure')
        elif column == 8:
            option(table, 'Precip.')
        elif column == 9:
            option(table, 'Precip.Accum')
        elif column == 10:
            option(table, 'Condition')
        elif column == 0:
            exit("Good bye!")


# вибираємо тип графіку і дані
# виводимо графіки відповідно до вибору
graphic(df)
