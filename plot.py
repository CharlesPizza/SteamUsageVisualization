import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def plot_view_pie(df):

    # Placeholder values, must replace
    mask_rplayed = ~df['playtime_2weeks'].isnull()
    std_day_keys = ['playtime_avg', 'recc_sleep', 'work_day', 'time_left']
    playtime_avg = df[mask_rplayed]['playtime_hours'].sum()/14
    # workday assumes 8hours inoffice + 2 hours for commute and prepare each day, then x5(workdays) /7(days in a week)
    workday_avg = 10*5/7
    std_day_values = [playtime_avg, 8, workday_avg, 24-8-playtime_avg-workday_avg]
    std_drunkday_values = [14/7, 8, workday_avg, 24-8-workday_avg-(14/7)]
    # Generate plot
    fig = Figure(figsize=(6,6),tight_layout=True)
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title("Average Daily Breakdown")
    ax1.pie(std_day_values, labels=std_day_keys,
           autopct=lambda x: '{:1.1f} hours'.format(x*24/100))
    fig.tight_layout()
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return pngImageB64String   

def plotView(df):

    # Placeholder values, must replace
    mask_rplayed = ~df['playtime_2weeks'].isnull()
    std_day_keys = ['playtime_avg', 'recc_sleep', 'work_day', 'time_left']
    playtime_avg = df[mask_rplayed]['playtime_hours'].sum()/14
    # workday assumes 8hours inoffice + 2 hours for commute and prepare each day, then x5(workdays) /7(days in a week)
    workday_avg = 10*5/7
    std_day_values = [playtime_avg, 8, workday_avg, 24-8-playtime_avg-workday_avg]
    std_drunkday_values = [14/7, 8, workday_avg, 24-8-workday_avg-(14/7)]
    # Generate plot
    fig = Figure(figsize=(9,6),tight_layout=True)
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    ax1.set_title("Avg Daily Playtime")
    ax1.pie(std_day_values, labels=std_day_keys,
           autopct=lambda x: '{:1.1f} hours'.format(x*24/100))
    ax2.set_title("Categorized Heavy Drinking")
    ax2.pie(std_drunkday_values, labels=['Time Drunk', 'recc_sleep', 'work_day', 'time_left'],
           autopct=lambda x: '{:1.1f} hours'.format(x*24/100))

    fig.tight_layout()
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return pngImageB64String


def top_10(df):
    top_10df = df.nlargest(10, 'playtime_forever')[['name', 'playtime_forever']]
    fig = Figure(figsize=(6,6))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title("Top 10 Most Played")
    ax1.pie(top_10df['playtime_forever'],
            labels = top_10df['name'],
            autopct = lambda x: str(round(x/100*top_10df['playtime_forever'].sum()/60)) +'hrs'
           )
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return pngImageB64String

