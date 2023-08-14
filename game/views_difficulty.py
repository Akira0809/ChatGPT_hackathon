from django.shortcuts import render
from .models import Data
import openai

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

        #data = Data.objects.latest("id")

        data = [
            {
                "question": "太陽系の中で最も大きな惑星は木星であり、その巨大なガスの雲を持つ姿は一見すると星座のように見えます。",
                "answer": "F",
                "hints": ["太陽系", "最も大きな惑星", "木星"],
                "commentary": "太陽系の中で最も大きな惑星は木星ですが、その巨大なガスの雲を持つ姿が星座のように見えることはありません。木星はガス巨星であり、その大きなガスの雲が特徴ですが、星座のように見えるわけではありません。"
            },
            {
                "question": "宇宙空間は真空であるため、音の伝わる媒体が存在せず、宇宙では音を聞くことはできません。",
                "answer": "T",
                "hints": ["宇宙空間", "真空", "音の伝わる媒体"],
                "commentary": "宇宙空間はほとんどが真空であり、音の伝わる媒体が存在しません。そのため、宇宙では通常の音を聞くことはできません。宇宙船などの内部では空気などの媒体を使って音が伝わることがありますが、宇宙空間自体では音は聞こえません。"
            },
            {
                "question": "宇宙には一定の境界線が存在し、この境界線を超えることは物理的に不可能です。",
                "answer": "F",
                "hints": ["宇宙", "境界線", "物理的に不可能"],
                "commentary": "宇宙には特定の物理的な境界線は存在せず、理論的には宇宙は無限に広がっていると考えられています。現在の科学的な知識では、宇宙に明確な境界はないとされています。"
            },
            {
                "question": "月は地球から見ると常に同じ面を向けており、裏側の姿を観察することはできません。",
                "answer": "F",
                "hints": ["月", "地球から見る", "同じ面"],
                "commentary": "月は地球から見ると常に同じ面を向けている現象を「潮汐固定」と呼びますが、裏側の姿を観察することも可能です。宇宙船などを利用して月の裏側にもアクセスすることができ、その地形や特徴を観察することが行われています。"
            },
            {
                "question": "宇宙飛行士は長期間宇宙ステーションに滞在する際、重力の影響で身長が少しずつ縮んでしまうことがあるため、ステーション内で特別なトレーニングを行います。",
                "answer": "T",
                "hints": ["宇宙飛行士", "宇宙ステーション", "トレーニング"],
                "commentary": "宇宙ステーションでは重力が微弱なため、宇宙飛行士の身体は長期間滞在するうちに微妙に変化します。宇宙ステーション内でのトレーニングは、骨密度や筋力の維持などを支援するために行われています。"
            }
        ]

        with open("../api.text") as f:
            openai.api_key = f.read().strip()

        with open("../api_js.text") as f:
            API = f.read().strip()

        template = [
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説"
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
        {template}
        ・以下のjsonは直近で出力した内容である。これに類似したものは出力してはならない。
        {data}
        ・出力を行う前に、文章の内容を精査し、さらに文章と解説を比較して矛盾点がないか確認すること。もし本当の文章の中に嘘が混じっている場合か嘘の文章に嘘が混じっていない場合、文章の生成からやり直す。また、解説には絶対に誤りが含まれていてはならないため、さらに精査すること。この工程を怠り文章や解説に誤りがあった場合、とても重い罰が下る
        ・出力を行う前に、jsonの内容を確認する。文章、本当か嘘かを表す英文字、3つのワード、解説のうち、いずれかが欠けていた場合はとても重い罰が下る。特にワードの数が3つぴったりであることは重大である
        上記の決まりに反すると、無差別に選ばれたなんの罪もない人が1000人死にます。
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt.format(difficulty=difficulty_text, genre=genre_text, template=template, data=data)},
            ]
        )
        text = response.choices[0]["message"]["content"].strip()
        text = text.replace("'", '"')
        print(text)
        Data.objects.create(questions=text)
        return render(request, "base.html", context={"data": text, "API": API})

    return render(request, "difficulty.html")