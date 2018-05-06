from app.repository import repository

import pandas as pd
from plotly.offline import download_plotlyjs, plot, iplot
import cufflinks as cf
import datetime


class Analytic(object):
    def __init__(self):
        cf.go_offline()

    def analyze_report_humor(self, data):
        content = pd.DataFrame(list(data), columns=['id', 'user_id', 'note', 'description', 'date'])
        image_name = 'analyze_{}.html'.format(datetime.datetime.now())
        fig = content.iplot(kind='scatter', x='date', y='note', categories='user_id', mode=['lines', 'markers'],
                            asFigure=True)
        path = plot(fig, filename=image_name, image='png')

        return path
