from flask import Flask, render_template, request
from exts import db
import config
import pymysql
from models import GSM, GSE, Quotes

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/Search/', methods=['POST', 'GET'])
@app.route('/Search/<src>,<org>,<exp_type>,<pltf>,<ort>', methods=['POST', 'GET'])
def Search(limit=10, src=None, org=None, exp_type=None, pltf=None, ort=None):
    org = org if org is not None else request.form.get('org') if request.form.get('org') is not None else ""
    src = src if src is not None else request.form.get('src') if request.form.get('src') is not None else ""
    exp_type = exp_type if exp_type is not None else request.form.get('exp_type') if request.form.get('exp_type') is not None else ""
    pltf = pltf if pltf is not None else request.form.get('pltf') if request.form.get('pltf') is not None else ""
    ort = ort if ort is not None else request.form.get('ort') if request.form.get('ort') is not None else ""

    page = int(request.args.get('page', 1))

    gsm_datas = GSM.query.filter(GSM.Source_name.like("%" + src + "%") if src is not None else "",
                                 GSM.Organism.like("%" + org + "%") if org is not None else "",
                                 GSM.Experiment_type.like("%" + exp_type + "%") if exp_type is not None else "",
                                 GSM.Platform.like("%" + pltf + "%") if pltf is not None else "",
                                 GSM.Characteristics.like("%" + ort + "%") if ort is not None else "")
    gsm_data = gsm_datas.paginate(page=page, per_page=limit)
    # print("org:", org, " src: ", src)
    return render_template('Search.html', gsm_data=gsm_data, src=src, org=org, exp_type=exp_type, pltf=pltf, ort=ort)


@app.route('/Data/', methods=['POST', 'GET'])
@app.route('/Data/<title>', methods=['POST', 'GET'])
def Data(limit=10, title=None):
    if title:
        pass
    else:
        title = request.form.get('title')
        if title is None:
            title = ""
    print(title)
    page = int(request.args.get('page', 1))
    quotes = Quotes.query.filter(Quotes.title.like("%" + title + "%") if title is not None else "")
    quote = quotes.paginate(page=page, per_page=limit)

    return render_template('Data.html', quote=quote, title=title)


@app.route('/detail/<pmid>/')
def detail(pmid):
    content = Quotes.query.filter(Quotes.pmid == pmid).first()

    return render_template('detail.html', content=content)


if __name__ == '__main__':
    app.run()
