from flask import Flask, render_template, request
from exts import db
import config
import pymysql
from models import GSM, GSE
from utils.commons import ReConverter

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 为flask添加自定义的转换器
app.url_map.converters['re'] = ReConverter


@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/Search/', methods=['POST', 'GET'])
@app.route('/Search/<re(r".*"):org>/<re(r".*"):src>/<re(r".*"):exp_type>/<re(r".*"):pltf>/<re(r".*"):ort>',
           methods=['POST', 'GET'])
def Search(limit=10, src="", org="", exp_type="", pltf="", ort=""):
    # if org:
    #     pass
    # else:
    #     org = request.form.get('org')
    #     if org is None:
    #         org = ""
    # if src:
    #     pass
    # else:
    #     src = request.form.get('src', None)
    #     if src is None:
    #         src = ""
    # if exp_type:
    #     pass
    # else:
    #     exp_type = request.form.get('exp_type')
    #     if exp_type is None:
    #         exp_type = ""
    # if pltf:
    #     pass
    # else:
    #     pltf = request.form.get('pltf')
    #     if pltf is None:
    #         pltf = ""
    # if ort:
    #     pass
    # else:
    #     ort = request.form.get('ort')
    #     if ort is None:
    #         ort = ""
    org = org if org else request.form.get('org') if request.form.get('org') is not None else ""
    src = src if src else request.form.get('src') if request.form.get('src') is not None else ""
    exp_type = exp_type if exp_type else request.form.get('exp_type') if request.form.get('exp_type') is not None else ""
    pltf = pltf if pltf else request.form.get('pltf') if request.form.get('pltf') is not None else ""
    ort = ort if ort else request.form.get('ort') if request.form.get('ort') is not None else ""

    page = int(request.args.get('page', 1))
    # Organism(种属): org  筛选GSM.Organism
    # Organoid source(细胞类型): src  筛选GSM.Source_name
    # Experiment type(测序类型): exp_type  筛选GSM.Experiment_type
    # Platform(平台): pltf  筛选GSM.Platform
    # Organoid type(类器官类型）: ort  筛选GSM.Characteristics
    gsm_datas = GSM.query.filter(GSM.Organism.like("%" + org + "%") if org is not None else "",
                                 GSM.Source_name.like("%" + src + "%") if src is not None else "",
                                 GSM.Experiment_type.like("%" + exp_type + "%") if exp_type is not None else "",
                                 GSM.Platform.like("%" + pltf + "%") if pltf is not None else "",
                                 GSM.Characteristics.like("%" + ort + "%") if ort is not None else "")
    gsm_data = gsm_datas.paginate(page=page, per_page=limit)
    # print("src=", src, " org=", org, " exp_type=", exp_type, " pltf=", pltf, " ort=", ort)
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
    gses = GSE.query.filter(GSE.Title.like("%" + title + "%") if title is not None else "")
    gse = gses.paginate(page=page, per_page=limit)

    return render_template('Data.html', gse=gse, title=title)


@app.route('/detail/<gse_num>/')
def detail(gse_num):
    content = GSE.query.filter(GSE.GSE_num == gse_num).first()

    return render_template('detail.html', content=content)


if __name__ == '__main__':
    app.run()
