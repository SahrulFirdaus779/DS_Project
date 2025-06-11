#!/usr/bin/env python
# coding: utf-8

# #Kelompok Pemula

# # Load dataset

# In[ ]:


#import library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


df=pd.read_csv('finaldata.csv')


# In[ ]:


df


# In[ ]:


df.columns


# In[ ]:


df.info()


# In[ ]:


# Agregasi nasional per tahun
trend_total_cerai = df.groupby('Tahun')['Jumlah Cerai'].sum().reset_index()

# Plot tren jumlah cerai
plt.figure(figsize=(10, 5))
sns.lineplot(data=trend_total_cerai, x='Tahun', y='Jumlah Cerai', marker='o')
plt.title('Tren Jumlah Perceraian Secara Nasional per Tahun')
plt.ylabel('Jumlah Perceraian')
plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:


# Agregasi nasional per tahun
trend_total_cerai = df.groupby('Tahun')['Jumlah Cerai'].sum().reset_index()

# Set gaya visual
sns.set(style='white')

# Ukuran gambar
plt.figure(figsize=(8, 5))

#buat aturan border
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Bar chart dengan warna seragam
barplot = sns.barplot(data=trend_total_cerai, x='Tahun', y='Jumlah Cerai', color='steelblue')

# Tambahkan nilai di atas batang
for index, row in trend_total_cerai.iterrows():
    plt.text(index, row['Jumlah Cerai'] + max(trend_total_cerai['Jumlah Cerai']) * 0.01,
             f"{row['Jumlah Cerai']:,}", ha='center', va='bottom', fontsize=9)

# Judul dan label
plt.title('Tren Jumlah Perceraian Nasional per Tahun', fontsize=14, weight='bold', pad=20)
plt.xlabel('Tahun')
plt.ylabel('Jumlah Perceraian')
plt.xticks(rotation=45)

# Tampilkan plot
plt.tight_layout()
plt.show()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from ipywidgets import interact, widgets

# Gaya visual seaborn
sns.set(style='white')

# List provinsi dengan tambahan 'Semua Provinsi'
provinsi_list = ['Semua Provinsi'] + sorted(df['Provinsi'].unique().tolist())

def plot_trend_per_provinsi(provinsi):
    if provinsi == 'Semua Provinsi':
        data = df.groupby('Tahun')['Jumlah Cerai'].sum().reset_index()
    else:
        data = df[df['Provinsi'] == provinsi].groupby('Tahun')['Jumlah Cerai'].sum().reset_index()

    plt.figure(figsize=(8, 5))

    # Atur border
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Bar chart
    barplot = sns.barplot(data=data, x='Tahun', y='Jumlah Cerai', color='steelblue')

    # Tambahkan nilai di atas batang
    for index, row in data.iterrows():
        plt.text(index, row['Jumlah Cerai'] + max(data['Jumlah Cerai']) * 0.01,
                 f"{row['Jumlah Cerai']:,}", ha='center', va='bottom', fontsize=9)

    # Judul dan label
    plt.title(f'Tren Jumlah Perceraian di {provinsi}', fontsize=14, weight='bold', pad=20)
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Perceraian')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

dropdown_provinsi = widgets.Dropdown(
    options=provinsi_list,
    description='Provinsi:',
    style={'description_width': 'initial'}
)

interact(plot_trend_per_provinsi, provinsi=dropdown_provinsi)


# In[ ]:


# Agregasi nasional per tahun
trend_total_cerai = df.groupby('Tahun')['Jumlah Cerai'].sum().reset_index()

# Hitung pertumbuhan tahunan
trend_total_cerai['Growth %'] = trend_total_cerai['Jumlah Cerai'].pct_change() * 100

# Set gaya visual
sns.set(style='white')

# Ukuran gambar
plt.figure(figsize=(8, 5))

# Line chart dengan marker
sns.lineplot(data=trend_total_cerai, x='Tahun', y='Jumlah Cerai', marker='o', color='steelblue', alpha=0.4)

#buat aturan border
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Tambahkan nilai dan pertumbuhan di atas titik
for i, row in trend_total_cerai.iterrows():
    jumlah = row['Jumlah Cerai']
    growth = row['Growth %']

    label = f"{jumlah:,}"
    if i > 0 and pd.notnull(growth):
        growth_label = f"\n({growth:+.1f}%)"
        label += growth_label

    plt.text(row['Tahun'], jumlah + max(trend_total_cerai['Jumlah Cerai']) * 0.01,
             label, ha='center', va='bottom', fontsize=9, color='crimson', alpha=1)

# Judul dan label
plt.title('Tren dan Persentase Jumlah Perceraian Nasional per Tahun', fontsize=14, weight='bold', pad = 30)
plt.xlabel('Tahun')
plt.ylabel('Jumlah Perceraian')
plt.xticks(rotation=45)

# Tampilkan plot
plt.tight_layout()
plt.show()


# In[ ]:


from ipywidgets import interact, widgets

# Gaya visual
sns.set(style='white')

# List dropdown provinsi
provinsi_options = ['Semua Provinsi'] + sorted(df['Provinsi'].unique().tolist())

# Fungsi visualisasi
def plot_line_per_provinsi(provinsi):
    if provinsi == 'Semua Provinsi':
        data = df.groupby('Tahun')['Jumlah Cerai'].sum().reset_index()
    else:
        data = df[df['Provinsi'] == provinsi].groupby('Tahun')['Jumlah Cerai'].sum().reset_index()

    # Hitung pertumbuhan persentase
    data['Growth %'] = data['Jumlah Cerai'].pct_change() * 100

    # Plot
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=data, x='Tahun', y='Jumlah Cerai', marker='o', color='steelblue', alpha=0.4)

    # Atur border
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Tambahkan label jumlah & pertumbuhan
    for i, row in data.iterrows():
        jumlah = row['Jumlah Cerai']
        growth = row['Growth %']
        label = f"{jumlah:,}"
        if i > 0 and pd.notnull(growth):
            label += f"\n({growth:+.1f}%)"
        plt.text(row['Tahun'], jumlah + max(data['Jumlah Cerai']) * 0.01,
                 label, ha='center', va='bottom', fontsize=9, color='crimson')

    # Judul dan label
    plt.title(f"Tren dan Persentase Jumlah Perceraian di {provinsi}", fontsize=14, weight='bold', pad=20)
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Perceraian")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Widget dropdown
dropdown_provinsi_line = widgets.Dropdown(
    options=provinsi_options,
    description='Provinsi:',
    style={'description_width': 'initial'}
)

interact(plot_line_per_provinsi, provinsi=dropdown_provinsi_line)


# In[ ]:


# Ambil daftar tahun unik
tahun_list = sorted(df['Tahun'].unique().tolist())
# Set gaya visual
sns.set(style='white')


# Fungsi plotting per tahun
def plot_perceraian_per_tahun(tahun):
    # Filter berdasarkan tahun
    data = df[df['Tahun'] == tahun].groupby('Provinsi')['Jumlah Cerai'].sum().reset_index()

    # Urutkan dari yang terbanyak
    data = data.sort_values(by='Jumlah Cerai', ascending=False).reset_index(drop=True)

    # Ukuran gambar
    plt.figure(figsize=(8, len(data) * 0.35))

    # Bar chart horizontal
    ax = sns.barplot(data=data, x='Jumlah Cerai', y='Provinsi', color='steelblue')

    # Tambahkan nilai di ujung kanan bar
    for i, row in data.iterrows():
        bar_width = row['Jumlah Cerai']
        plt.text(
            bar_width + max(data['Jumlah Cerai']) * 0.01,  # sedikit ke kanan dari ujung bar
            i,  # posisi vertikal berdasarkan indeks bar
            f"{int(bar_width):,}",  # label angka dengan pemisah ribuan
            ha='left', va='center',
            fontsize=9, color='black', weight='bold'
        )
     # Atur border
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Judul dan label
    plt.title(f'Jumlah Perceraian per Provinsi di Tahun {tahun}', fontsize=14, weight='bold', pad=20)
    plt.xlabel('Jumlah Perceraian')
    plt.ylabel('Provinsi')
    plt.tight_layout()
    plt.show()

# Dropdown interaktif
interact(plot_perceraian_per_tahun, tahun=widgets.Dropdown(options=tahun_list, description='Tahun:'));


# In[ ]:


# Agregasi nasional per tahun untuk talak dan gugat
cerai_per_jenis = df.groupby('Tahun')[['Cerai Talak', 'Cerai Gugat']].sum().reset_index()

# Plot perbandingan
plt.figure(figsize=(10, 5))
sns.lineplot(data=cerai_per_jenis, x='Tahun', y='Cerai Talak', label='Cerai Talak (oleh Suami)', marker='o')
sns.lineplot(data=cerai_per_jenis, x='Tahun', y='Cerai Gugat', label='Cerai Gugat (oleh Istri)', marker='o')
plt.title('Perbandingan Cerai Talak vs Cerai Gugat per Tahun')
plt.ylabel('Jumlah Kasus')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# In[ ]:


# Gaya visual
sns.set(style='whitegrid')

# Agregasi nasional per tahun untuk talak dan gugat
cerai_per_jenis = df.groupby('Tahun')[['Cerai Talak', 'Cerai Gugat']].sum().reset_index()

# Hitung pertumbuhan tahunan dalam persentase
cerai_per_jenis['Talak Growth'] = cerai_per_jenis['Cerai Talak'].pct_change() * 100
cerai_per_jenis['Gugat Growth'] = cerai_per_jenis['Cerai Gugat'].pct_change() * 100

# Ukuran plot
plt.figure(figsize=(12, 6))

# Plot garis
sns.lineplot(data=cerai_per_jenis, x='Tahun', y='Cerai Talak', marker='o', label='Cerai Talak (oleh Suami)', color='steelblue')
sns.lineplot(data=cerai_per_jenis, x='Tahun', y='Cerai Gugat', marker='o', label='Cerai Gugat (oleh Istri)', color='darkorange')

# Dapatkan axis untuk set spines setelah figure dibuat
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Tambahkan label pertumbuhan dan nilai
for i in range(len(cerai_per_jenis)):
    tahun = cerai_per_jenis['Tahun'][i]
    talak = cerai_per_jenis['Cerai Talak'][i]
    gugat = cerai_per_jenis['Cerai Gugat'][i]

    talak_growth = cerai_per_jenis['Talak Growth'][i]
    gugat_growth = cerai_per_jenis['Gugat Growth'][i]

    # Label Cerai Talak di atas titik (naik)
    if not pd.isna(talak_growth):
        plt.text(tahun, talak + max(cerai_per_jenis['Cerai Talak']) * 0.02,
                 f"{talak_growth:+.1f}%\n({talak:,.0f})",
                 ha='center', va='bottom', fontsize=8, color='steelblue')
    else:
        plt.text(tahun, talak + max(cerai_per_jenis['Cerai Talak']) * 0.02,
                 f"({talak:,.0f})",
                 ha='center', va='bottom', fontsize=8, color='steelblue')

    # Label Cerai Gugat di bawah titik (turun)
    if not pd.isna(gugat_growth):
        plt.text(tahun, gugat - max(cerai_per_jenis['Cerai Gugat']) * 0.08,
                 f"{gugat_growth:+.1f}%\n({gugat:,.0f})",
                 ha='center', va='top', fontsize=8, color='darkorange')
    else:
        plt.text(tahun, gugat - max(cerai_per_jenis['Cerai Gugat']) * 0.08,
                 f"({gugat:,.0f})",
                 ha='center', va='top', fontsize=8, color='darkorange')

# Judul dan label
plt.title('Tren & Persentase Cerai Talak vs Cerai Gugat per Tahun', fontsize=14, weight='bold', pad=20)
plt.xlabel('Tahun')
plt.ylabel('Jumlah Kasus')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# In[ ]:


# Agregasi nasional per tahun untuk talak dan gugat
cerai_per_jenis = df.groupby('Tahun')[['Cerai Talak', 'Cerai Gugat']].sum().reset_index()

# Gaya visual
sns.set(style='white')

# Ukuran plot
plt.figure(figsize=(12, 6))

#buat aturan border
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Lebar batang dan posisi sumbu x
bar_width = 0.4
x = np.arange(len(cerai_per_jenis['Tahun']))

# Bar chart untuk masing-masing jenis
plt.bar(x - bar_width/2, cerai_per_jenis['Cerai Talak'], width=bar_width, label='Cerai Talak (oleh Suami)', color='steelblue')
plt.bar(x + bar_width/2, cerai_per_jenis['Cerai Gugat'], width=bar_width, label='Cerai Gugat (oleh Istri)', color='darkorange')

# Tambahkan label angka di atas batang
for i in range(len(x)):
    plt.text(x[i] - bar_width/2, cerai_per_jenis['Cerai Talak'][i] + max(cerai_per_jenis['Cerai Talak']) * 0.01,
             f"{cerai_per_jenis['Cerai Talak'][i]:,}", ha='center', va='bottom', fontsize=8)
    plt.text(x[i] + bar_width/2, cerai_per_jenis['Cerai Gugat'][i] + max(cerai_per_jenis['Cerai Gugat']) * 0.01,
             f"{cerai_per_jenis['Cerai Gugat'][i]:,}", ha='center', va='bottom', fontsize=8)

# Sumbu dan label
plt.xticks(x, cerai_per_jenis['Tahun'], rotation=45)
plt.title('Perbandingan Cerai Talak vs Cerai Gugat per Tahun', fontsize=14, weight='bold')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Kasus')
plt.legend()
plt.tight_layout()
plt.show()


# In[ ]:


def plot_cerai_per_provinsi(provinsi_terpilih):
    # Filter data sesuai provinsi
    df_filtered = df[df['Provinsi'] == provinsi_terpilih]

    # Agregasi tahunan
    cerai_per_jenis = df_filtered.groupby('Tahun')[['Cerai Talak', 'Cerai Gugat']].sum().reset_index()

    # Visualisasi
    sns.set(style='white')
    plt.figure(figsize=(12, 6))

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    bar_width = 0.4
    x = np.arange(len(cerai_per_jenis['Tahun']))

    plt.bar(x - bar_width/2, cerai_per_jenis['Cerai Talak'], width=bar_width, label='Cerai Talak (oleh Suami)', color='steelblue')
    plt.bar(x + bar_width/2, cerai_per_jenis['Cerai Gugat'], width=bar_width, label='Cerai Gugat (oleh Istri)', color='darkorange')

    for i in range(len(x)):
        plt.text(x[i] - bar_width/2, cerai_per_jenis['Cerai Talak'][i] + 0.01 * max(cerai_per_jenis['Cerai Talak']),
                 f"{cerai_per_jenis['Cerai Talak'][i]:,}", ha='center', va='bottom', fontsize=8)
        plt.text(x[i] + bar_width/2, cerai_per_jenis['Cerai Gugat'][i] + 0.01 * max(cerai_per_jenis['Cerai Gugat']),
                 f"{cerai_per_jenis['Cerai Gugat'][i]:,}", ha='center', va='bottom', fontsize=8)

    plt.xticks(x, cerai_per_jenis['Tahun'], rotation=45)
    plt.title(f'Perbandingan Cerai Talak vs Cerai Gugat per Tahun\nProvinsi: {provinsi_terpilih}', fontsize=14, weight='bold')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Kasus')
    plt.legend()
    plt.tight_layout()
    plt.show()

provinsi_options = df['Provinsi'].unique()
interact(plot_cerai_per_provinsi, provinsi_terpilih=widgets.Dropdown(options=provinsi_options, description='Provinsi:'))


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from ipywidgets import interact, widgets

def plot_tren_cerai_provinsi(provinsi_terpilih):
    # Filter berdasarkan provinsi
    df_filtered = df[df['Provinsi'] == provinsi_terpilih]

    # Agregasi per tahun
    cerai_per_jenis = df_filtered.groupby('Tahun')[['Cerai Talak', 'Cerai Gugat']].sum().reset_index()

    # Hitung pertumbuhan tahunan dalam persentase
    cerai_per_jenis['Talak Growth'] = cerai_per_jenis['Cerai Talak'].pct_change() * 100
    cerai_per_jenis['Gugat Growth'] = cerai_per_jenis['Cerai Gugat'].pct_change() * 100

    # Plot
    sns.set(style='whitegrid')
    plt.figure(figsize=(12, 6))

    sns.lineplot(data=cerai_per_jenis, x='Tahun', y='Cerai Talak', marker='o', label='Cerai Talak (oleh Suami)', color='steelblue')
    sns.lineplot(data=cerai_per_jenis, x='Tahun', y='Cerai Gugat', marker='o', label='Cerai Gugat (oleh Istri)', color='darkorange')

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Tambahkan label angka dan pertumbuhan
    for i in range(len(cerai_per_jenis)):
        tahun = cerai_per_jenis['Tahun'][i]
        talak = cerai_per_jenis['Cerai Talak'][i]
        gugat = cerai_per_jenis['Cerai Gugat'][i]
        talak_growth = cerai_per_jenis['Talak Growth'][i]
        gugat_growth = cerai_per_jenis['Gugat Growth'][i]

        # Label Cerai Talak
        label_talak = f"{talak_growth:+.1f}%\n({talak:,.0f})" if pd.notna(talak_growth) else f"({talak:,.0f})"
        plt.text(tahun, talak + max(cerai_per_jenis['Cerai Talak']) * 0.02,
                 label_talak, ha='center', va='bottom', fontsize=8, color='steelblue')

        # Label Cerai Gugat
        label_gugat = f"{gugat_growth:+.1f}%\n({gugat:,.0f})" if pd.notna(gugat_growth) else f"({gugat:,.0f})"
        plt.text(tahun, gugat - max(cerai_per_jenis['Cerai Gugat']) * 0.08,
                 label_gugat, ha='center', va='top', fontsize=8, color='darkorange')

    # Judul dan keterangan
    plt.title(f'Tren Cerai Talak vs Cerai Gugat per Tahun\nProvinsi: {provinsi_terpilih}', fontsize=14, weight='bold', pad=20)
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Kasus')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Dropdown interaktif
provinsi_options = df['Provinsi'].unique()
interact(plot_tren_cerai_provinsi, provinsi_terpilih=widgets.Dropdown(options=provinsi_options, description='Provinsi:'))


# In[ ]:


df.groupby('Tahun')[['Jumlah Cerai', 'Nikah']].sum().plot()


# In[ ]:


# Agregasi nasional
rasio_df = df.groupby('Tahun')[['Jumlah Cerai', 'Nikah']].sum().reset_index()
rasio_df['Rasio Cerai/Nikah'] = rasio_df['Jumlah Cerai'] / rasio_df['Nikah']

# Plot rasio
plt.figure(figsize=(10, 5))
sns.lineplot(data=rasio_df, x='Tahun', y='Rasio Cerai/Nikah', marker='o', color='purple')
plt.title('Rasio Jumlah Perceraian terhadap Jumlah Pernikahan per Tahun')
plt.ylabel('Rasio (Cerai / Nikah)')
plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:


# Grouping: total jumlah cerai per tahun per provinsi
trend_cerai_prov = df.groupby(['Tahun', 'Provinsi'])['Jumlah Cerai'].sum().reset_index()

# Plot: Multiple lines untuk beberapa provinsi (misal top 5 tertinggi total cerai)
top5_prov = trend_cerai_prov.groupby('Provinsi')['Jumlah Cerai'].sum().nlargest(5).index
subset = trend_cerai_prov[trend_cerai_prov['Provinsi'].isin(top5_prov)]

plt.figure(figsize=(12, 6))
sns.lineplot(data=subset, x='Tahun', y='Jumlah Cerai', hue='Provinsi', marker='o')
plt.title('Tren Jumlah Perceraian per Tahun di 5 Provinsi Teratas')
plt.ylabel('Jumlah Cerai')
plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:


# Grouping total per tahun dan provinsi
jenis_cerai = df.groupby(['Tahun', 'Provinsi'])[['Cerai Talak', 'Cerai Gugat']].sum().reset_index()

# Contoh: Visualisasi untuk 1 provinsi (misalnya: 'Jawa Barat')
provinsi_target = 'Jawa Barat'
subset = jenis_cerai[jenis_cerai['Provinsi'] == provinsi_target]

plt.figure(figsize=(10, 5))
sns.lineplot(data=subset, x='Tahun', y='Cerai Talak', label='Cerai Talak', marker='o')
sns.lineplot(data=subset, x='Tahun', y='Cerai Gugat', label='Cerai Gugat', marker='o')
plt.title(f'Perbandingan Cerai Talak vs Gugat di {provinsi_target}')
plt.ylabel('Jumlah Kasus')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets
import seaborn as sns

# Gaya visualisasi
sns.set(style="whitegrid")

# Daftar kolom faktor perceraian
faktor_cols = [
    "Zina",
    "Mabuk",
    "Madat",
    "Judi",
    "Meninggalkan Salah satu Pihak",
    "Dihukum Penjara",
    "Poligami",
    "Kekerasan Dalam Rumah Tangga",
    "Cacat Badan",
    "Perselisihan dan Pertengkaran Terus Menerus",
    "Kawin Paksa",
    "Murtad",
    "Ekonomi",
    "Lain-lain",
]

# Fungsi visualisasi tren faktor perceraian per provinsi
def plot_trend(faktor, provinsi):
    if provinsi == "Semua Provinsi":
        data_filtered = df.groupby("Tahun")[faktor].sum()
    else:
        data_filtered = df[df["Provinsi"] == provinsi].groupby("Tahun")[faktor].sum()

    plt.figure(figsize=(10, 5))
    plt.plot(data_filtered.index, data_filtered.values, marker='o', linewidth=2.5, color='steelblue')
    plt.title(f"Tren Perceraian karena '{faktor}' di {provinsi}", fontsize=16, fontweight='bold')
    plt.xlabel("Tahun", fontsize=12)
    plt.ylabel("Jumlah Kasus", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)

    for x, y in zip(data_filtered.index, data_filtered.values):
        plt.text(x, y + max(data_filtered.values)*0.02, str(int(y)), ha='center', fontsize=9)

    plt.tight_layout()
    plt.show()

# Dropdown faktor
faktor_dropdown = widgets.Dropdown(
    options=faktor_cols,
    description="Faktor Perceraian:",
    style={'description_width': 'initial'},
)

# Dropdown provinsi + opsi nasional
provinsi_options = ["Semua Provinsi"] + sorted(df["Provinsi"].unique())
provinsi_dropdown = widgets.Dropdown(
    options=provinsi_options,
    description="Provinsi:",
    style={'description_width': 'initial'},
)

# Interaktif
interact(plot_trend, faktor=faktor_dropdown, provinsi=provinsi_dropdown)


# In[ ]:


# Memanggil kolom
faktor_columns = [
    'Zina',
    'Mabuk',
    'Madat',
    'Judi',
    'Meninggalkan Salah satu Pihak',
    'Dihukum Penjara',
    'Poligami',
    'Kekerasan Dalam Rumah Tangga',
    'Cacat Badan',
    'Perselisihan dan Pertengkaran Terus Menerus',
    'Kawin Paksa',
    'Murtad',
    'Ekonomi',
    'Lain-lain'
]

# Hitung total kasus per faktor dan urutkan
faktor_cerai = df[faktor_columns].sum().sort_values(ascending=True).astype(int)

# Visualisasi
plt.figure(figsize=(12, 8))
ax = plt.subplot()

# Plot bar chart
faktor_cerai.plot(kind='barh',
                 ax=ax,
                 color='#3498db',
                 edgecolor='black',
                 width=0.8,
                 zorder=3)

# Atur limit dan format sumbu
max_value = faktor_cerai.max()
ax.set_xlim(0, max_value * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Tambahkan nilai di ujung bar
for i, v in enumerate(faktor_cerai):
    ax.text(v + max_value*0.01, i, f'{v:,}',
            va='center', ha='left',
            color='black', fontsize=10, zorder=5)

# Formatting
plt.title('Faktor Dominan Penyebab Perceraian di Indonesia (2018-2024)',
         pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Total Kasus', fontsize=12, labelpad=10)
plt.ylabel('Faktor Perceraian', fontsize=12, labelpad=10)
plt.yticks(fontsize=10)

# Tambahkan grid vertikal
ax.grid(axis='x', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.show()


# In[ ]:


# Memanggil kolom
faktor_columns = [
    'Zina',
    'Mabuk',
    'Madat',
    'Judi',
    'Meninggalkan Salah satu Pihak',
    'Dihukum Penjara',
    'Poligami',
    'Kekerasan Dalam Rumah Tangga',
    'Cacat Badan',
    'Perselisihan dan Pertengkaran Terus Menerus',
    'Kawin Paksa',
    'Murtad',
    'Ekonomi',
    'Lain-lain'
]

# Hitung total kasus per faktor dan ambil 5 terbesar
top5 = df[faktor_columns].sum().nlargest(5).sort_values(ascending=True).astype(int)

# Visualisasi
plt.figure(figsize=(10, 6))
ax = plt.subplot()

# Plot bar chart
top5.plot(kind='barh',
         ax=ax,
         color='#3498db',
         edgecolor='black',
         width=0.7,
         zorder=3)


# Atur limit dan format sumbu
max_value = top5.max()
ax.set_xlim(0, max_value * 1.1)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Tambahkan grid vertikal yang lebih subtle
ax.grid(axis='x', linestyle=':', color='gray', alpha=0.5, zorder=0)

# Tambahkan nilai di ujung bar
for i, v in enumerate(top5):
    ax.text(v + max_value*0.01, i, f'{v:,}',
            va='center', ha='left',
            color='black', fontsize=10, zorder=5,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# Formatting
plt.title('5 Faktor Utama Penyebab Perceraian di Indonesia (2018-2024)',
         pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Total Kasus', fontsize=12, labelpad=10)
plt.ylabel('Faktor Perceraian', fontsize=12, labelpad=10)
plt.yticks(fontsize=10)

plt.tight_layout()
plt.show()


# In[ ]:


# Agregasi nasional per tahun
perbandingan_df = df.groupby('Tahun')[['Nikah', 'Jumlah Cerai']].sum().reset_index()

# Setup
plt.figure(figsize=(12, 6))
sns.set(style='white')

# Sumbu x dan lebar bar
x = np.arange(len(perbandingan_df['Tahun']))
bar_width = 0.4

# Buat bar chart
plt.bar(x - bar_width/2, perbandingan_df['Nikah'], width=bar_width, label='Jumlah Pernikahan', color='green')
plt.bar(x + bar_width/2, perbandingan_df['Jumlah Cerai'], width=bar_width, label='Jumlah Perceraian', color='gold')

# Tambahkan label pada setiap bar
for i in range(len(x)):
    plt.text(x[i] - bar_width/2, perbandingan_df['Nikah'][i] + max(perbandingan_df['Nikah'])*0.01,
             f"{perbandingan_df['Nikah'][i]:,}", ha='center', va='bottom', fontsize=8, color='green')
    plt.text(x[i] + bar_width/2, perbandingan_df['Jumlah Cerai'][i] + max(perbandingan_df['Jumlah Cerai'])*0.01,
             f"{perbandingan_df['Jumlah Cerai'][i]:,}", ha='center', va='bottom', fontsize=8, color='gold')

# Judul dan tampilan
plt.xticks(x, perbandingan_df['Tahun'], rotation=45)
plt.title('Perbandingan Jumlah Pernikahan dan Perceraian per Tahun', fontsize=14, weight='bold')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Kasus')
plt.legend()
plt.tight_layout()
plt.show()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from ipywidgets import interact, widgets
from IPython.display import display

# Asumsikan df sudah dimuat dan memiliki kolom: 'Tahun', 'Provinsi', 'Nikah', 'Jumlah Cerai'
# Daftar unik provinsi
daftar_provinsi = df['Provinsi'].unique()

# Fungsi plotting
def plot_perbandingan(provinsi_terpilih):
    # Filter data sesuai provinsi
    data = df[df['Provinsi'] == provinsi_terpilih]

    # Agregasi per tahun
    perbandingan_df = data.groupby('Tahun')[['Nikah', 'Jumlah Cerai']].sum().reset_index()

    # Setup
    plt.figure(figsize=(9, 6))
    sns.set(style='white')

    x = np.arange(len(perbandingan_df['Tahun']))
    bar_width = 0.4

    # Buat bar chart
    plt.bar(x - bar_width/2, perbandingan_df['Nikah'], width=bar_width, label='Jumlah Pernikahan', color='green')
    plt.bar(x + bar_width/2, perbandingan_df['Jumlah Cerai'], width=bar_width, label='Jumlah Perceraian', color='gold')

    # Label di atas bar
    for i in range(len(x)):
        plt.text(x[i] - bar_width/2, perbandingan_df['Nikah'][i] + max(perbandingan_df['Nikah'])*0.01,
                 f"{perbandingan_df['Nikah'][i]:,}", ha='center', va='bottom', fontsize=8, color='green')
        plt.text(x[i] + bar_width/2, perbandingan_df['Jumlah Cerai'][i] + max(perbandingan_df['Jumlah Cerai'])*0.01,
                 f"{perbandingan_df['Jumlah Cerai'][i]:,}", ha='center', va='bottom', fontsize=8, color='gold')

    # Judul dan tampilan
    plt.xticks(x, perbandingan_df['Tahun'], rotation=45)
    plt.title(f'Perbandingan Pernikahan vs Perceraian per Tahun di Provinsi {provinsi_terpilih}', fontsize=14, weight='bold')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Kasus')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Dropdown widget
dropdown = widgets.Dropdown(
    options=sorted(daftar_provinsi),
    description='Provinsi:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='50%')
)

# Interaktif
interact(plot_perbandingan, provinsi_terpilih=dropdown)


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact, widgets

# Gaya visual seaborn
sns.set(style="whitegrid")

# Daftar kolom faktor perceraian
faktor_cols = [
    "Zina",
    "Mabuk",
    "Madat",
    "Judi",
    "Meninggalkan Salah satu Pihak",
    "Dihukum Penjara",
    "Poligami",
    "Kekerasan Dalam Rumah Tangga",
    "Cacat Badan",
    "Perselisihan dan Pertengkaran Terus Menerus",
    "Kawin Paksa",
    "Murtad",
    "Ekonomi",
    "Lain-lain",
]

# Fungsi visualisasi
def show_factors_by_year(tahun):
    data_filtered = df[df['Tahun'] == tahun]
    total_per_faktor = data_filtered[faktor_cols].sum().sort_values(ascending=True)

    # Gambar horizontal bar chart
    plt.figure(figsize=(12, 8))
    bars = plt.barh(total_per_faktor.index, total_per_faktor.values,
                    color=sns.color_palette("RdPu", len(total_per_faktor)))

    # Tambah label di ujung bar
    for bar in bars:
        plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
                 f'{int(bar.get_width())}', va='center', fontsize=10)

    plt.title(f"Faktor Perceraian di Indonesia Tahun {tahun}", fontsize=16, fontweight='bold')
    plt.xlabel("Jumlah Kasus", fontsize=12)
    plt.ylabel("Faktor Perceraian", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# Dropdown interaktif
tahun_dropdown = widgets.Dropdown(
    options=sorted(df['Tahun'].unique()),
    description='Tahun:',
    style={'description_width': 'initial'},
)

interact(show_factors_by_year, tahun=tahun_dropdown)


# In[ ]:


# Gaya visual
sns.set(style="whitegrid")

# Daftar kolom faktor perceraian
faktor_cols = [
    "Zina",
    "Mabuk",
    "Madat",
    "Judi",
    "Meninggalkan Salah satu Pihak",
    "Dihukum Penjara",
    "Poligami",
    "Kekerasan Dalam Rumah Tangga",
    "Cacat Badan",
    "Perselisihan dan Pertengkaran Terus Menerus",
    "Kawin Paksa",
    "Murtad",
    "Ekonomi",
    "Lain-lain",
]

# Fungsi visualisasi
def show_factors(tahun, provinsi):
    data_filtered = df[(df['Tahun'] == tahun) & (df['Provinsi'] == provinsi)]

    if data_filtered.empty:
        print(f"Tidak ada data untuk Tahun {tahun} dan Provinsi {provinsi}.")
        return

    total_per_faktor = data_filtered[faktor_cols].sum().sort_values(ascending=True)

    plt.figure(figsize=(12, 8))
    bars = plt.barh(total_per_faktor.index, total_per_faktor.values,
                    color=sns.color_palette("RdPu", len(total_per_faktor)))

    for bar in bars:
        plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
                 f'{int(bar.get_width())}', va='center', fontsize=10)

    plt.title(f"Faktor Perceraian di {provinsi} Tahun {tahun}", fontsize=16, fontweight='bold')
    plt.xlabel("Jumlah Kasus", fontsize=12)
    plt.ylabel("Faktor Perceraian", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# Dropdown tahun dan provinsi
tahun_dropdown = widgets.Dropdown(
    options=sorted(df['Tahun'].unique()),
    description='Tahun:',
    style={'description_width': 'initial'},
)

provinsi_dropdown = widgets.Dropdown(
    options=sorted(df['Provinsi'].unique()),
    description='Provinsi:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='20%')
)

# Interaktif
interact(show_factors, tahun=tahun_dropdown, provinsi=provinsi_dropdown)


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets
import seaborn as sns

# Gaya visualisasi
sns.set(style="whitegrid")

# Daftar kolom faktor perceraian
faktor_cols = [
    "Zina",
    "Mabuk",
    "Madat",
    "Judi",
    "Meninggalkan Salah satu Pihak",
    "Dihukum Penjara",
    "Poligami",
    "Kekerasan Dalam Rumah Tangga",
    "Cacat Badan",
    "Perselisihan dan Pertengkaran Terus Menerus",
    "Kawin Paksa",
    "Murtad",
    "Ekonomi",
    "Lain-lain",
]

# Kelompokkan dan agregasi data per tahun
yearly_data = df.groupby("Tahun")[faktor_cols].sum()

# Fungsi untuk menampilkan line chart
def plot_trend(faktor):
    plt.figure(figsize=(10, 5))
    plt.plot(yearly_data.index, yearly_data[faktor], marker='o', linewidth=2.5, color='steelblue')
    plt.title(f"Tren Perceraian Berdasarkan Faktornya: {faktor}", fontsize=16, fontweight='bold')
    plt.xlabel("Tahun", fontsize=12)
    plt.ylabel("Jumlah Kasus", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    for x, y in zip(yearly_data.index, yearly_data[faktor]):
        plt.text(x, y + max(yearly_data[faktor]) * 0.02, str(y), ha='center', fontsize=9)
    plt.tight_layout()
    plt.show()

# Dropdown untuk memilih faktor perceraian
faktor_dropdown = widgets.Dropdown(
    options=faktor_cols,
    description="Faktor Perceraian:",
    style={'description_width': 'initial'},
)

interact(plot_trend, faktor=faktor_dropdown)


# #GeoPandas

# In[ ]:


import geopandas as gpd
import json
# Baca GeoJSON
gdf = gpd.read_file("all_maps_state_indo.geojson")


# In[ ]:


# df = df.copy()  # untuk menghindari warning jika df hasil dari filter
rasio_perceraian = df['Jumlah'] / df['Nikah']

df['Rasio_Perceraian'] = rasio_perceraian


# In[ ]:


print(gdf.columns)


# In[ ]:


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# 2. Normalisasi nama provinsi
alias = {
    'DAERAH ISTIMEWA YOGYAKARTA': 'DI YOGYAKARTA',
}
gdf['provinsi_fix'] = gdf['state'].replace(alias).str.upper()
df['Provinsi_fix'] = df['Provinsi'].str.upper()

# 3. Drop provinsi pemekaran baru dari df (tidak ada di shapefile)
provinsi_pemekaran_papua = [
    'PAPUA BARAT DAYA', 'PAPUA PEGUNUNGAN', 'PAPUA SELATAN', 'PAPUA TENGAH'
]
df = df[~df['Provinsi_fix'].isin(provinsi_pemekaran_papua)]

# 4. Hitung rata-rata rasio perceraian per provinsi (dalam persen)
avg_rasio = df.groupby('Provinsi_fix')['Rasio_Perceraian'].mean().reset_index()
avg_rasio['Rasio_Perceraian'] *= 100  # ubah jadi persen

# 5. Gabungkan ke GeoDataFrame
merged = gdf.merge(avg_rasio, how='left', left_on='provinsi_fix', right_on='Provinsi_fix')

# 6. Visualisasi
fig, ax = plt.subplots(1, 1, figsize=(20, 15))  # Perbesar ukuran peta
merged.plot(column='Rasio_Perceraian',
            cmap='YlOrRd',
            linewidth=0.8,
            edgecolor='0.8',
            legend=True,
            legend_kwds={'label': "Rasio Perceraian (%)", 'shrink': 0.5},  # perkecil legend
            ax=ax,
            missing_kwds={
                "color": "lightgrey",
                "label": "Data Tidak Tersedia"
            })

# 7. Tambahkan label nama provinsi
for idx, row in merged.iterrows():
    if row['geometry'].centroid.is_empty:
        continue
    plt.annotate(text=row['provinsi_fix'].title(),
                 xy=(row['geometry'].centroid.x, row['geometry'].centroid.y),
                 horizontalalignment='center',
                 fontsize=8,
                 color='black',
                 weight='bold')

# 8. Judul dan tampilan
ax.set_title('peta Rata-rata Rasio Perceraian per Provinsi di Indonesia (2018–2024)', fontsize=20)
ax.axis('off')
plt.tight_layout()
plt.show()


# #Modeling

# In[ ]:


import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# 1) Agregasi total nasional per tahun
yearly = (
    df.groupby('Tahun', as_index=False)
      .agg({'Jumlah': 'sum', 'Nikah': 'sum'})
      .sort_values('Tahun')
)

# 2) Siapkan data latih
X = yearly[['Tahun', 'Nikah']]
y = yearly['Jumlah']
model = LinearRegression().fit(X, y)

# 3) Estimasi nilai fitur untuk 2025
nikah_model = LinearRegression().fit(yearly[['Tahun']], yearly['Nikah'])
pred_nikah_2025 = nikah_model.predict(pd.DataFrame({'Tahun': [2025]}))[0]

# 4) Prediksi cerai 2025
X_2025 = pd.DataFrame({'Tahun': [2025], 'Nikah': [pred_nikah_2025]})
pred_cerai_2025 = model.predict(X_2025)[0]

# 5) Gabungkan data historis + prediksi
pred_row = pd.DataFrame({
    'Tahun': [2025],
    'Nikah': [pred_nikah_2025],
    'Jumlah': [pred_cerai_2025]
})
yearly_extended = pd.concat([yearly, pred_row], ignore_index=True)

# 6) Plot
plt.figure(figsize=(12, 6))
# Garis data historis
plt.plot(yearly['Tahun'], yearly['Jumlah'], marker='o', label='Data Historis', color='blue')
# Titik prediksi 2025
plt.plot(2025, pred_cerai_2025, 'ro', label='Prediksi 2025')
# Garis putus-putus dari tahun terakhir ke 2025
plt.plot([yearly['Tahun'].iloc[-1], 2025],
         [yearly['Jumlah'].iloc[-1], pred_cerai_2025],
         linestyle='--', color='gray', label='Garis Prediksi')

# Tambahkan label jumlah di atas setiap titik
for i, row in yearly_extended.iterrows():
    plt.text(row['Tahun'], row['Jumlah'] + 2, f"{int(row['Jumlah'])}", ha='center', fontsize=9)

# Tambahkan garis vertikal sebagai penanda awal prediksi (misal tahun prediksi mulai setelah 2024)
plt.axvline(x=2024.5, color='black', linestyle='--', label='Prediksi dimulai')


# Format plot
plt.title('Prediksi Jumlah Perceraian Nasional hingga 2025')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Perceraian')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# In[ ]:


from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# y: nilai aktual
# y_pred: nilai prediksi dari model
mae = mean_absolute_error(y, model.predict(X))
mse = mean_squared_error(y, model.predict(X))
rmse = np.sqrt(mse)
r2 = r2_score(y, model.predict(X))

print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"R-squared: {r2}")

