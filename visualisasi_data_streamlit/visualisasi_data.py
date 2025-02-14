import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
uploaded_file = st.file_uploader("Upload file day.csv", type=["csv"])

if uploaded_file is not None:
    day_df = pd.read_csv(uploaded_file)
    st.write("Data berhasil diupload!")
else:
    st.error("File day.csv tidak ditemukan! Silakan upload file.")

# Data preprocessing
day_df['dteday'] = pd.to_datetime(day_df['dteday'], errors='coerce')
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], errors='coerce')

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_name'] = day_df['season'].map(season_mapping)
day_df['season_name'] = pd.Categorical(day_df['season_name'], categories=['Spring', 'Summer', 'Fall', 'Winter'], ordered=True)

# Pastikan tidak ada nilai NaN di season_name
day_df = day_df.dropna(subset=['season_name'])

# Sidebar Navbar
st.sidebar.title("📌 Menu")
page = st.sidebar.radio("Pilih Halaman:", ["Dashboard", "Exploratory Data Analysis (EDA)", "Visualization & Explanatory Analysis"])

st.title("🚴‍♂️ Bike Sharing Dashboard")

if page == "Dashboard":
    st.write("## 📊 Ringkasan Data")
    st.write("Dataset ini mencatat jumlah peminjaman sepeda berdasarkan hari dan jam.")
    
    st.write("### Data Harian 🌞")
    st.dataframe(day_df.head())
    st.write("### Data Per Jam ⌚")
    st.dataframe(hour_df.head())
    
    st.write("### Statistik Ringkas 🤷‍♂️")
    st.write(day_df.describe())

    st.write("Metode lanjutan yang kami gunakan adalah Metode EDA. Metode Exploratory Data Analysis (EDA) merupakan langkah penting dalam analisis data untuk memahami karakteristik, pola, dan hubungan dalam dataset sebelum melakukan pemodelan lebih lanjut.")
    st.write("Dataset ini mencakup 731 entri yang merepresentasikan data harian selama dua tahun (2011-2012), dengan variabel seperti musim (season), tahun (yr), bulan (mnth), hari libur (holiday), hari dalam seminggu (weekday), hari kerja (workingday), dan kondisi cuaca (weathersit). Distribusi musim berkisar dari 1 hingga 4, menunjukkan variasi sepanjang tahun, sementara data tahun terbagi merata antara 2011 dan 2012. Hari libur hanya mencakup sekitar 2.87% dari total hari, sedangkan hari kerja mencakup sekitar 68.4%. Kondisi cuaca bervariasi dari cerah hingga hujan dengan kategori 1 hingga 3. Ringkasan statistik ini dapat digunakan untuk memahami pola musiman dan pengaruh faktor cuaca terhadap tren harian dalam dataset.")

elif page == "Exploratory Data Analysis (EDA)":
    sub_page = st.sidebar.selectbox("Pilih Grafik:", [
        "Persentase Peminjaman Sepeda Berdasarkan Musim (Pie Chart)",
        "Penyewaan Sepeda Berdasarkan Jam",
        "Penyewaan Sepeda Berdasarkan Hari"
    ])
    
    st.write(f"## 🔍 {sub_page}")

    # Total Peminjaman Sepeda berdasarkan Musim (Pie Chart)
    if sub_page == "Persentase Peminjaman Sepeda Berdasarkan Musim (Pie Chart)":
        fig, ax = plt.subplots(figsize=(6,6))
        day_df.groupby("season_name")["cnt"].sum().plot.pie(autopct='%1.1f%%', startangle=90, cmap='coolwarm', ax=ax)
        ax.set_ylabel('')
        ax.set_title("Penggunaan Sepeda Berdasarkan Musim")
        st.pyplot(fig)

        st.write("Berdasarkan Hasil Pie Chart 🥧")
        st.write("Dari data ini, dapat disimpulkan bahwa penggunaan sepeda paling banyak terjadi pada musim gugur dan paling sedikit pada musim semi. Faktor cuaca dan kondisi lingkungan kemungkinan besar mempengaruhi pola ini.")

    # Penyewaan sepeda berdasarkan jam
    elif sub_page == "Penyewaan Sepeda Berdasarkan Jam":
        fig, ax = plt.subplots(figsize=(8,5))
        hour_avg = hour_df.groupby("hr")["cnt"].mean()
        sns.barplot(x=hour_avg.index, y=hour_avg.values, color="blue", ax=ax)
        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
        st.pyplot(fig)

        st.write("Berdasarkan Hasil Bar Chart 📊")
        st.write("Penyewaan sepeda mencapai puncak pada pukul 08:00 dan 17:00-18:00, mencerminkan jam sibuk kerja dan sekolah. Aktivitas penyewaan rendah pada dini hari (00:00-05:00) dan menurun setelah pukul 19:00. Siang hari relatif stabil tanpa lonjakan signifikan. Pola ini menunjukkan bahwa sepeda banyak digunakan untuk mobilitas harian.")

    # Penyewaan sepeda berdasarkan hari
    elif sub_page == "Penyewaan Sepeda Berdasarkan Hari":
        fig, ax = plt.subplots(figsize=(10,5))
        daily_avg = day_df.groupby("dteday")["cnt"].sum()
        sns.lineplot(x=daily_avg.index, y=daily_avg.values, ax=ax, color='red')
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Total Penyewaan")
        ax.set_title("Total Penyewaan Sepeda Berdasarkan Hari")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.write("Berdasarkan Hasil Line Chart 📈")
        st.write("Grafik menunjukkan tren penyewaan sepeda meningkat dari 2011, mencapai puncak pada pertengahan 2012, lalu menurun menjelang 2013. Fluktuasi harian tinggi, dengan pola lonjakan pada musim tertentu. Penurunan di akhir periode bisa dipengaruhi faktor cuaca atau kondisi eksternal lainnya.")

elif page == "Visualization & Explanatory Analysis":
    sub_page = st.sidebar.selectbox("Pilih Grafik:", [
        "Total Peminjaman Sepeda Berdasarkan Musim (Heatmap)",
        "Total Rental Sepeda: Working Day vs Non-Working Day",
        "Pengaruh Musim terhadap Rata-rata Peminjaman Sepeda",
        "Perbandingan Rata-rata Peminjaman Sepeda antara Tahun 2011 dan 2012",
        "Hubungan Antara Cuaca dan Jenis Pengguna"
    ])

    st.write(f"## 📊 {sub_page}")

    #Total Peminjaman Sepeda berdasarkan Musim (Heatmap)
    if sub_page == "Total Peminjaman Sepeda Berdasarkan Musim (Heatmap)":
        season_rentals = day_df.groupby("season_name")["cnt"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8,5))
        pivot_table = season_rentals.pivot_table(values="cnt", index="season_name")
        sns.heatmap(pivot_table, annot=True, cmap="coolwarm", fmt=".0f", linewidths=1, ax=ax)
        ax.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
        st.pyplot(fig)

        st.write("Berdasarkan Hasil Heatmap 🤒")
        st.write("Musim dengan peminjaman sepeda terbanyak: Musim dengan jumlah peminjaman sepeda terbanyak adalah Musim Gugur(Fall). Hal ini mungkin karena suhu yang lebih hangat di musim panas mendorong lebih banyak orang untuk bersepeda, baik untuk kebutuhan transportasi maupun untuk rekreasi.")
        st.write("Musim dengan peminjaman sepeda tersedikit: Musim dengan jumlah peminjaman sepeda tersedikit adalah musim Semi(Spring). Cuaca cenderung lebih tidak stabil dengan banyak peralihan antara hujan, angin, dan suhu yang lebih sejuk. Hal ini bisa membuat orang lebih memilih menggunakan transportasi lain yang lebih nyaman daripada sepeda.")

    # Peminjaman Working Day vs Non-Working Day
    elif sub_page == "Total Rental Sepeda: Working Day vs Non-Working Day":
        fig, ax = plt.subplots(figsize=(6,6))
        day_df["workingday"].value_counts().plot.pie(labels=["Non-Working Day", "Working Day"], autopct='%1.1f%%', startangle=90, colors=["#ff9999", "#66b3ff"],  ax=ax)
        ax.set_ylabel('')
        ax.set_title("Distribusi Peminjaman Sepeda: Working Day vs Non-Working Day")
        st.pyplot(fig)

        st.write("Berdasarkan hasil Pie Chart 🥧")
        st.write("Jika peminjaman lebih tinggi pada hari kerja : Ini menunjukkan penggunaan sepeda lebih banyak untuk transportasi sehari-hari.")
        st.write("Jika peminjaman lebih tinggi pada hari libur: Ini mungkin menunjukkan bahwa orang menggunakan sepeda lebih untuk rekreasi atau olahraga saat liburan.")
        st.write("Dan berdasarkan pie chart maka kesimpulannya adalah orang-orang lebih banyak meminjam pada hari kerja untuk transportasi sehari hari.")
        st.write("Pie chart membantu kita memahami distribusi peminjaman berdasarkan jenis hari (kerja vs. libur).")

    # Pengaruh Musim terhadap Rata-rata Peminjaman Sepeda
    elif sub_page == "Pengaruh Musim terhadap Rata-rata Peminjaman Sepeda":
        fig, ax = plt.subplots(figsize=(8,5))
        season_avg = day_df.groupby("season_name")["cnt"].mean().reset_index()
        sns.barplot(x="season_name", y="cnt", data=season_avg, palette="Blues", ax=ax)
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Peminjaman")
        ax.set_title("Pengaruh Musim terhadap Rata-rata Peminjaman Sepeda")
        st.pyplot(fig)

        st.write("Berdasarkan hasil Vertical Bar Chart 📊")
        st.write("Rata-rata peminjaman sepeda dengan jumlah tertinggi terjadi pada musim panas (Summer) dan musim gugur (Fall). Sedangkan peminjaman dengan jumlah terendah terjadi pada musim semi (Spring) dan musim dingin (Winter). Hal ini menunjukkan bahwa cuaca hangat dan cerah lebih mendukung aktivitas bersepeda dibandingkan cuaca dingin.")

    # Perbandingan Rata-rata Peminjaman Sepeda antara Tahun 2011 dan 2012
    elif sub_page == "Perbandingan Rata-rata Peminjaman Sepeda antara Tahun 2011 dan 2012" :
        fig, ax = plt.subplots(figsize=(8,5))
        year_avg = day_df.groupby("yr")["cnt"].mean().reset_index()
        year_avg["yr"] = year_avg["yr"].map({0: "2011", 1: "2012"})  # Mengubah label tahun
        sns.barplot(y="yr", x="cnt", data=year_avg, palette="coolwarm", ax=ax)
        ax.set_ylabel("Tahun")
        ax.set_xlabel("Rata-rata Peminjaman")
        ax.set_title("Perbandingan Rata-rata Peminjaman Sepeda antara Tahun 2011 dan 2012")
        st.pyplot(fig)

        st.write("Berdasarkan hasil Horizontal Bar Chart 📊")
        st.write("Rata-rata peminjaman sepeda per hari pada tahun 2011 adalah sekitar 3,406 sepeda, sedangkan pada tahun 2012 meningkat menjadi 5,600 sepeda. Hal ini menunjukkan adanya peningkatan sebesar hampir 64% dari tahun 2011 ke tahun 2012 yang menunjukkan adanya tren peningkatan popularitas atau penggunaan layanan sepeda selama periode tersebut. Tren ini mencerminkan pergeseran positif dalam penggunaan sepeda sebagai moda transportasi.")
    
    # Perbandingan Hubungan Antara Cuaca dan Jenis Pengguna
    elif sub_page == "Hubungan Antara Cuaca dan Jenis Pengguna":
        fig, ax = plt.subplots(figsize=(8,5))
        weather_avg = day_df.groupby("weathersit")[["casual", "registered"]].mean()
        sns.lineplot(data=weather_avg, markers=True, dashes=False, ax=ax)
        ax.set_xticks(ticks=[1, 2, 3], labels=['Clear', 'Mist', 'Rain/Snow'], fontsize=10)
        ax.set_xlabel("Cuaca (Weathersit)")
        ax.set_ylabel("Rata-rata Pengguna")
        ax.set_title("Hubungan Antara Cuaca dan Jenis Pengguna")
        ax.legend(["Casual", "Registered"])
        st.pyplot(fig)

        st.write("Berdasarkan hasil Line Chart 📉")
        st.write("Pengguna Casual: Peminjaman sepeda oleh pengguna casual paling tinggi saat cuaca cerah (Clear). Terjadi penurunan signifikan pada kondisi cuaca berkabut (Mist) dan semakin rendah saat hujan/salju (Rain/Snow).")
        st.write("Pengguna Registered: Peminjaman oleh pengguna registered tetap tinggi pada cuaca cerah dan berkabut, tetapi menurun saat hujan/salju. Penurunan pada pengguna registered lebih kecil dibandingkan pengguna casual dalam kondisi cuaca buruk.")
    
show_team = st.sidebar.checkbox("Tampilkan Anggota Kelompok")
if show_team:
    st.sidebar.subheader("Anggota Kelompok 6 IF-6:")
    team_members = [
        "Yolanda Belva D - 10123228",
        "Taura Farhatsari - 10123230",
        "Anisa - 10123234",
        "Fariz Maulana - 10123248",
        "Naufal Mahdavickia - 10123254"
    ]
    for member in team_members:
        st.sidebar.write(member)
