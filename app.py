from flask import (
    Flask, 
    render_template, 
    request,
    redirect,
    url_for, 
    send_from_directory)
import os
import article


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)






database = { 
    "spacex": {
        "article_title": "SpaceX Crew-10",
        "article_text": """
SpaceX Crew-10 — планируемый десятый пилотируемый полёт американского космического корабля
Crew Dragon компании SpaceX в рамках программы NASA Commercial Crew Program.
Корабль доставит четырёх членов экипажа миссии Crew-10 и космических экспедиций МКС-72/73 на Международную космическую станцию (МКС).
Запуск планируется провести 12 марта 2025 года.
""",
        "article_image": "SpaceX_Crew_Dragon.jpg"
    },

    "cosmos": {
        "article_title": "Космос (философия)",
        "article_text": """
Ко́смос (др.-греч. κόσμος «порядок, гармония») — понятие древнегреческой философии и культуры, 
представление о природном мире как о пластически упорядоченном гармоническом целом[1]. "
"Противопоставлялся хаосу. Греки соединяли в понятии «космос» две функции — упорядочивающую и эстетическую[2][3].
""",
        "article_image": "Cosmos.png"
    },

    "Tank": {
        "article_title": "T-18",
        "article_text": """
Т-18 (МС-1 — малый сопровождающий) — советский лёгкий танк непосредственной поддержки пехоты 1920-х годов. 
Создан в 1925—1927 годах. Стал первым танком советской разработки. Серийно производился с 1928 по 1931 год, 
всего в нескольких вариантах было выпущено 959 танков этого типа, не считая прототипа. 
В конце 1920-х — начале 1930-х годов Т-18 составлял основу танкового парка РККА, но довольно быстро был вытеснен более совершенным Т-26. 
Применялся в бою в конфликте на КВЖД, 
но в 1938—1939 годах устаревшие и достигшие крайней степени износа Т-18 были в основном сняты с вооружения или использовались как неподвижные огневые точки. 
В незначительном количестве использовались на начальном этапе Великой Отечественной войны.
""",
        "article_image": "Tank.jpg"
    },

    "Music": {
        "article_title": "Roxy Music",
        "article_text": """
Roxy Music — британская рок-группа, основанная в 1970 году Брайаном Ферри (вокал, пианино, клавишные) и Грэмом Симпсоном (бас-гитара).
Позднее к ним присоединились Фил Манзанера (гитара), Энди Маккей (гобой, саксофон) и Брайан Ино (клавишные, синтезатор), однако 
состав коллектива постоянно менялся, 
а фактическим лидером в ней оставался Брайан Ферри. Композиции группы сочетали в себе ироничную поэзию, 
виртуозное исполнение и стильные сценические постановки, 
наполненные образцами высокой моды, китча и коммерческой фотографии. 
Характерной особенностью ранних работ группы стал симбиоз лирики и модернизма. В творчестве Roxy Music преобладали меланхоличные композиции.
""", 
        "article_image": "Music.jpg"
    },

    "Picture": {
        "article_title": "Земство обедает", 
        "article_text": """
«Зе́мство обе́дает» — картина русского художника Григория Мясоедова (1834—1911), оконченная в 1872 году. 
Хранится в Государственной Третьяковской галерее в Москве. Размер — 74 × 125 см (по другим данным, 75 × 125,5 см). 
На полотне изображены крестьянские представители уездного земского собрания: их обед составляет простой хлеб с луком и солью, в то время как не показанная на картине дворянская часть земства обедает в помещении. 
Употребляются также другие названия: «Уездное земское собрание в обеденное время» и «Земский обед».
""",
        "article_image": "Picture.jpg"
    }
}



@app.route("/article/<name>")
def get_article(name):
    if name not in database:
        return "<h1>Такой статьи не существует!</h1>"
    
    article = database[name]
    return render_template(
        "article.html",
        article=article
        )

@app.route("/create_article", methods=["GET", "POST"])
def create_article():
    if request.method == "GET":
        return render_template('create_article.html')
    
    # Далее обработка Post-запроса
    title = request.form.get("title")
    content = request.form.get("content")
    image = request.files.get("photo")

    if image is not None and image.filename:
        image_path = image.filename
        image.save(app.config["UPLOAD_FOLDER"] + image_path)
    else:
        image_path = None

    database[title] = article.Article(title, content, image_path)
    return redirect(url_for('index'))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
app.run(debug=True, port=8080)