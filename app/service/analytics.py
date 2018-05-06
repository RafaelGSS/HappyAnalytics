import pandas as pd
from plotly.offline import download_plotlyjs, plot, iplot
import cufflinks as cf


class Analytic(object):
    def __init__(self):
        cf.go_offline()

    def analyze_report_humor(self, data, image_name):
        content = pd.DataFrame(list(data), columns=['id', 'user_id', 'user_name', 'note_humor', 'description', 'date'])
        fig = content.iplot(kind='scatter', x='date', y='note_humor', categories='user_name', mode=['lines', 'markers'],
                            text='description', asFigure=True)
        path = plot(fig, filename=image_name)

        return image_name
