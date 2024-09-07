import os
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_anime_reviews(base_url, total_pages):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    review_list = []

    for page in range(1, total_pages + 1):
        url = f"{base_url}?p={page}"  # Sesuaikan URL untuk setiap halaman
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            reviews = soup.find_all("div", class_="review-element js-review-element")

            for review in reviews:
                text_element = review.find("div", class_="text")
                if text_element:
                    review_text = text_element.get_text(strip=True)
                    review_list.append(review_text)
                else:
                    print("Elemen teks review tidak ditemukan.")
        else:
            print("Gagal mengambil halaman, status code:", response.status_code)

    return review_list


# URL dasar
base_url = "https://myanimelist.net/anime/35968/Wotaku_ni_Koi_wa_Muzukashii/reviews"
total_pages = 10
reviews = get_anime_reviews(base_url, total_pages)
# print(reviews)

csv_path = r"C:\Users\naufa\Documents\DataScienceInit\DS_Project__init\Wotakoi Anime Sentiment Analysis\data\raw\wotakoi_reviews2.csv"

# Print hasil
if reviews:
    # Buat DataFrame dari list
    df = pd.DataFrame(reviews, columns=["Review"])
    df

    # Simpan DataFrame ke CSV
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print("Review berhasil diekspor ke {csv_path}")
else:
    print("Tidak ada review yang ditemukan.")
