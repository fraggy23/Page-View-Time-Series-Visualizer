import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import calendar

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)
df.head()

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025))
            & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots(figsize=(32, 10), dpi=100)
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  sns.lineplot(data=df, x='date', y='value', ax=ax)

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.resample('M').mean()
  df_bar = df_bar.reset_index()
  df_bar['date'] = pd.to_datetime(df_bar['date'])
  df_bar['Years'] = df_bar['date'].dt.year
  df_bar['Months'] = df_bar['date'].dt.month_name()

  month = [calendar.month_name[i] for i in range(1, 13)]

  mapping = {months: i for i, months in enumerate(month)}
  key = df_bar['Months'].map(mapping)
  df_bar.iloc[key.argsort()]
  # Draw bar plot

  fig, ax = plt.subplots()
  df_bar.pivot_table(index='Years', columns=key, values='value',
                     fill_value=0).plot(kind='bar',
                                        label='Months',
                                        stacked=False,
                                        figsize=(9, 6),
                                        ax=ax)
  plt.legend(labels=month, title='Months')
  plt.xlabel('Years')
  plt.ylabel('Average Page Views')

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  # Draw box plots (using Seaborn)
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(35, 12), dpi=100)

  sns.boxplot(data=df_box, x="year", y="value", ax=ax1)
  ax1.set_title("Year-wise Box Plot (Trend)")
  ax1.set_xlabel("Year")
  ax1.set_ylabel("Page Views")

  month_order = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
      'Nov', 'Dec'
  ]
  sns.boxplot(data=df_box, x="month", y="value", order=month_order, ax=ax2)
  ax2.set_title("Month-wise Box Plot (Seasonality)")
  ax2.set_xlabel("Month")
  ax2.set_ylabel("Page Views")

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
