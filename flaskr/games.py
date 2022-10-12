from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort 
import werkzeug.exceptions
from bs4 import BeautifulSoup as bs 
import requests
import re
import lxml
import pandas as pd
import sys
sys.path.append('../')
import DoctorInGaming.web as web
import DoctorInGaming.plot as gen_plots


bp = Blueprint('user', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index(steamid='76561198027985875'):
    if request.method == 'POST':
        image_strings = {}
        steamid = request.form['steam64ID']
        df, summary= web.get_all(steamid)
        print(df)
        image_strings['daily_average'] = gen_plots.plot_view_pie(df)
        image_strings['daily_vs_addiction'] = gen_plots.plotView(df)
        image_strings['top_10_playtimes'] = gen_plots.top_10(df)
        return render_template('user/report.html', steamid=steamid, df=df,
            summary=summary, images=image_strings)
    return render_template('user/index.html', steamid=steamid)

@bp.route('/report', methods=['GET', 'POST'])
def report(steamid, df, summary):
    return(render_template('user/report.html', steamid=steamid,
        df=df, summary=summary, image=pngImageB64String))

@bp.errorhandler(werkzeug.exceptions.BadRequest)
def handle_key_error():
    return render_template('user/index.html', 
        steamid=steamid)
