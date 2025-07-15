from flask import Flask, request, jsonify
from textblob import TextBlob
from collections import Counter
import random

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    product_link = data.get('link', '')

    product_image = 'Product_Image_From_Link.jpg'
    customer_images = ['Review_Image_1.jpg', 'Review_Image_2.jpg']
    reviews = [
        "Product quality is poor.",
        "Looks different from the listing image.",
        "Very satisfied with the purchase.",
        "Amazing build quality and works as described.",
        "Item not matching the description."
    ]

    image_similarity = random.choice(['Low', 'High'])

    sentiments = []
    positive_count, negative_count = 0, 0
    keywords = []

    for review in reviews:
        polarity = TextBlob(review).sentiment.polarity
        sentiment = 'Positive' if polarity >= 0 else 'Negative'
        if sentiment == 'Positive':
            positive_count += 1
        else:
            negative_count += 1
        sentiments.append({'review': review, 'sentiment': sentiment})

        # Extract keywords
        blob = TextBlob(review)
        keywords.extend(blob.words.lower())

    total_reviews = positive_count + negative_count
    buy_percentage = round((positive_count / total_reviews) * 100, 2)
    not_buy_percentage = round((negative_count / total_reviews) * 100, 2)

    flagged = image_similarity == 'Low' or negative_count > 0

    # Top 3 Keywords
    keyword_freq = Counter(keywords)
    top_keywords = [word for word, freq in keyword_freq.most_common(3)]

    # Recommendation Logic
    recommendation = "Recommended to Buy ✅" if buy_percentage >= 60 and image_similarity == 'High' else "Avoid Buying 🚫"

    # Review trend
    if buy_percentage >= 70:
        review_trend = "Mostly Positive"
    elif buy_percentage >= 40:
        review_trend = "Mixed Reviews"
    else:
        review_trend = "Mostly Negative"

    result = {
        'productLink': product_link,
        'productImage': product_image,
        'customerImages': customer_images,
        'imageSimilarity': image_similarity,
        'sentiments': sentiments,
        'flagged': flagged,
        'buyProbabilityPercentage': buy_percentage,
        'notBuyProbabilityPercentage': not_buy_percentage,
        'topKeywords': top_keywords,
        'recommendation': recommendation,
        'reviewTrend': review_trend,
        'confidenceLevel': f"{random.randint(85, 99)}%"  # Simulated confidence level
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
