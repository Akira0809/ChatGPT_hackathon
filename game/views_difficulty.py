from django.shortcuts import render
from .models import Data
import openai
import json

# Create your views here.
def difficulty(request):
    error_text = "入力漏れがあります。2つとも選択してください。"
    if request.method == "POST":
        selected_difficulty = request.POST.get("selected_difficulty")
        if selected_difficulty == "elementary_school":
            difficulty_text = "小学校卒業"
        elif selected_difficulty == "high_school":
            difficulty_text = "・高校卒業"
        elif selected_difficulty == "society":
            difficulty_text = "社会人レベル"
        else:
            return render(request, "difficulty.html", {'error_text': error_text})

        selected_genre = request.POST.get("selected_genre")
        if selected_genre == "miscellaneous":
            genre_text = "雑学"
        elif selected_genre == "history":
            genre_text = "歴史"
        elif selected_genre == "it":
            genre_text = "IT"
        else:
            return render(request, "difficulty.html", {'error_text': error_text})

        data = Data.objects.get(id=1)

        with open("../api.text", "r") as f:
            openai.api_key = f.read().strip()

        template = [
            {
                "question": "湖の水は常に透明である。",
                "answer": "F",
                "hints": ["水", "透明", "湖"],
                "commentary": "湖の水は透明ではなく、様々な要因によって色や濁りが生じることがあります。湖の水が透明であれば、水中の魚や植物などが視認しやすくなるでしょう。"
            },
            {
                "question": "湖に住んでいる魚は全て淡水魚である。",
                "answer": "T",
                "hints": ["湖", "魚", "淡水"],
                "commentary": "湖は陸地からの水の流入や雨水などによって水が供給され、その水が淡水であることが一般的です。そのため、湖に住む魚も淡水魚が主な生息魚種となります。"
            },
            {
                "question": "湖の水は常に同じ場所にある。",
                "answer": "F",
                "hints": ["水", "湖", "場所"],
                "commentary": "湖の水は循環をしており、降水や河川などの水源から流入し、蒸発や地下への浸透、河川などへの流出などを経て、常に動いています。そのため、湖の水は常に同じ場所にあるわけではありません。"
            },
            {
                "question": "湖の水は飲用に適している。",
                "answer": "T",
                "hints": ["湖", "水", "飲用"],
                "commentary": "湖の水は地下水と比べると塩分濃度が低く、浄化処理なしでも直接飲むことができる場合があります。ただし、湖の水は汚染物質の影響も受けるため、安全な飲用水として利用するには水質の管理が重要です。"
            },
            {
                "question": "湖は必ずしも自然の地形によって形成されるわけではない。",
                "answer": "T",
                "hints": ["湖", "地形", "形成"],
                "commentary": "湖は地球上の様々な要因によって形成される場合があります。例えば、火山活動によってできるカルデラ湖や人工的に作られる人工湖などがあります。そのため、湖は必ずしも自然の地形によって形成されるわけではありません。"
            }
        ]

        prompt = """
        以下の条件で文章を生成してください
        ・問題の難易度は{difficulty}レベルとする。
        ・{genre}に関する文章。
        ・出力する文章の数は5つ。その5つの文章は、本当のことしか書かれていない文章と嘘の情報が混じった文章で構成される。5つの文章の中でいくつ嘘の文章を混ぜるかは、0から5の範囲内でランダムに決める。
        ・文章は疑問形で終わってはならない。
        ・学習データにないなどの理由で文章の正確性が保証できない場合、その文章の生成をやり直す。
        ・それぞれの文章は、その分野の専門家程度の知識を持った人でなければ意味が分からないレベルにする
        ・嘘の文章に混ぜる嘘の内容は、その分野の専門家程度の知識を持った人でなければ見抜けないレベルにする
        ・嘘が混じっている文章の場合は「F」、そうでない場合は「T」をつける
        ・それぞれの文章において、嘘が混じっているかどうかを判断するのに役立つワードを3つ考え、生成する。ワードの数は必ず3つでなければならない。また、「です」「など」のように単語として成り立たないようなワードは除外すること
        ・３つのワードのあとに文章に関する解説を生成する。解説は具体例などを交えて読む人がわかりやすいように記述すること。決して生成した文章とほぼ同じ文章を出力するといったことがあってはならない。また、解説は事実のみを説明するように生成すること。
        ・出力はプログラムで使用する。その際に邪魔になるので、「了解しました」「分かりました」といったメッセージは不要である。もしも出力内容以外の不要なメッセージを出力した場合、重い罰が下る
        ・生成した文章はjson形式で出力する。それぞれの文章の出力の例は以下に示すとおりである。以下の通りにフォーマットを整え、jsonで出力すること。出力はプログラムで使用するため、下記に指定するフォーマットの形式以外だとエラーの原因となる。
        ・生成した文章はダブルクォーテーションで囲むことそうでないとエラーが発生し実行することができない。
        {template}
        ・以下のjsonは直近で出力した内容である。これに類似したものは出力してはならない。
        ・出力を行う前に、文章の内容を精査し、さらに文章と解説を比較して矛盾点がないか確認すること。もし本当の文章の中に嘘が混じっている場合か嘘の文章に嘘が混じっていない場合、文章の生成からやり直す。また、解説には絶対に誤りが含まれていてはならないため、さらに精査すること。この工程を怠り文章や解説に誤りがあった場合、とても重い罰が下る
        ・出力を行う前に、jsonの内容を確認する。文章、本当か嘘かを表す英文字、3つのワード、解説のうち、いずれかが欠けていた場合はとても重い罰が下る。特にワードの数が3つぴったりであることは重大である
        上記の決まりに反すると、無差別に選ばれたなんの罪もない人が1000人死にます。
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt.format(difficulty=difficulty_text, genre=genre_text, template=template)},
            ]
        )
        text = response.choices[0]["message"]["content"].strip()
        text = text.replace("'", '"')
        Data.objects.create(questions=text)
        print(text)
        return render(request, "base.html", context={"data": text})

    return render(request, "difficulty.html")