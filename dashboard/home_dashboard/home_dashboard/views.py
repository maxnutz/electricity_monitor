from django.http import HttpResponse
from django.shortcuts import render
from awattar_price.models import Chart


def home(request):
    return HttpResponse("Willkommen auf der Django-Seite")


import pandas as pd
from plotly.offline import plot
import plotly.express as px


def index(request):
    # qs = Chart.objects.all()
    # projects_data = [
    #     {
    #         "Project": x.name,
    #         "Start": x.start_date,
    #         "Finish": x.finish_date,
    #         "Responsible": x.responsible.username,
    #     }
    #     for x in qs
    # ]
    # df = pd.DataFrame(projects_data)
    # fig = px.timeline(
    #     df, x_start="Start", x_end="Finish", y="Project", color="Responsible"
    # )
    # fig.update_yaxes(autorange="reversed")
    # gantt_plot = plot(fig, output_type="div")
    # context = {"plot_div": gantt_plot}
    # return render(request, "index.html", context)
    return render(request, "index.html")
