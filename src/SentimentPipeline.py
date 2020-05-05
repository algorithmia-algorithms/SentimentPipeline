import Algorithmia


# API calls will begin at the apply() method, with the request body passed as 'input'
# For more details, see algorithmia.com/developers/algorithm-development/languages
def apply(path):
    output = {}
    client = Algorithmia.client()
    for file in client.dir(path).files():
        # extract text from image using OCR
        body = client.algo("util/ExtractText/0.1.1").pipe("data://" + file.path).result
        body = body.rstrip("\n")

        # determine language of text
        lang = client.algo("nlp/LanguageIdentification/1.0.0").pipe({"sentence": body}).result

        # translate non-English text
        if lang != 'en':
            input = {"action": "translate", "text": body}
            body = client.algo("translation/GoogleTranslate/0.1.1").pipe(input).result["translation"]

        # Tokenize text for analysis by sentence
        token_body = client.algo("ApacheOpenNLP/SentenceDetection/0.1.0").pipe(body).result

        # determine sentiment of tokenized text
        keyword_sentiment = []
        for token in token_body:
            print("data://" + file.path + " -> " + token)
            sent = client.algo("nlp/SentimentAnalysis/1.0.5").pipe({"document": token}).result[0]["sentiment"]
            keyword_sentiment.append(sent)

        avg_sent = sum(keyword_sentiment) / len(keyword_sentiment)

        # record output
        output["data://" + file.path] = {"average sentiment": avg_sent}

    return output

# "data://AlgorithmiaSE/sentiment_pipe"