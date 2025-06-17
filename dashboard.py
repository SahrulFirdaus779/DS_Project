import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import geopandas as gpd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os # Import os to check for secrets.toml existence

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Dashboard Analisis Perceraian Indonesia",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Fungsi untuk Memuat Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('finaldata.csv')

        # Rename 'Jumlah Cerai' to 'Jumlah_Perceraian' for consistency
        if 'Jumlah Cerai' in df.columns:
            df = df.rename(columns={'Jumlah Cerai': 'Jumlah_Perceraian'})
        else:
            st.error("Kolom 'Jumlah Cerai' tidak ditemukan. Harap pastikan nama kolom total perceraian sudah benar di file CSV Anda.")
            st.stop()

        # Define factor columns explicitly
        factor_cols = [
            'Zina', 'Mabuk', 'Madat', 'Judi', 'Meninggalkan Salah satu Pihak',
            'Dihukum Penjara', 'Poligami', 'Kekerasan Dalam Rumah Tangga',
            'Cacat Badan', 'Perselisihan dan Pertengkaran Terus Menerus',
            'Kawin Paksa', 'Murtad', 'Ekonomi', 'Lain-lain'
        ]

        # Check if all expected columns exist
        required_cols = ['Provinsi', 'Tahun', 'Jumlah_Perceraian', 'Nikah', 'Cerai Talak', 'Cerai Gugat'] + factor_cols
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Kolom-kolom berikut tidak ditemukan di 'finaldata.csv': {', '.join(missing_cols)}. Harap periksa nama kolom Anda.")
            st.stop()

        # Ensure correct data types
        df['Tahun'] = df['Tahun'].astype(int)
        df['Provinsi'] = df['Provinsi'].astype(str)

        # Calculate Rasio_Perceraian for mapping
        df['Rasio_Perceraian'] = (df['Jumlah_Perceraian'] / df['Nikah']) * 100
        df['Rasio_Perceraian'].replace([np.inf, -np.inf], np.nan, inplace=True) # Handle division by zero if Nikah is 0

        return df, factor_cols
    except FileNotFoundError:
        st.error("File 'finaldata.csv' tidak ditemukan. Pastikan file berada di direktori yang sama dengan aplikasi Streamlit.")
        st.stop()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}. Pastikan format CSV Anda benar dan nama kolom sesuai.")
        st.stop()

# --- Fungsi untuk Memuat GeoJSON (untuk peta) ---
@st.cache_data
def load_geojson():
    try:
        gdf = gpd.read_file("all_maps_state_indo.geojson")
        # Normalisasi nama provinsi di GeoJSON
        alias = {'DAERAH ISTIMEWA YOGYAKARTA': 'DI YOGYAKARTA'}
        gdf['provinsi_fix'] = gdf['state'].replace(alias).str.upper()
        return gdf
    except FileNotFoundError:
        st.error("File 'all_maps_state_indo.geojson' tidak ditemukan. Pastikan file berada di direktori yang sama dengan aplikasi Streamlit.")
        st.stop()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat GeoJSON: {e}. Pastikan file GeoJSON benar.")
        st.stop()

# Load data dan dapatkan daftar kolom faktor
df, factor_cols = load_data()
gdf = load_geojson()

# --- Sidebar (Menu Navigasi) ---
with st.sidebar:
    st.image("logo/Monogram.svg", width=150)
    st.title("🌐 Kelompok Pemula")
    st.markdown("---")

    menu_choice = st.radio(
        "Pilih Halaman",
        ("Beranda / Ringkasan", "Tren Perceraian", "Faktor Penyebab", "Perbandingan Provinsi", "Peta Visualisasi", "Prediksi Perceraian", "Detail Data")
    )

    st.markdown("---")
    st.header("Tentang Proyek")
    st.info("""
        Proyek ini menganalisis tren dan faktor penyebab perceraian di Indonesia.
        Data bersumber dari [Sumber Data Anda, misal: BPS, Kemenag].
        Dibuat oleh Kelompok Pemula.
    """)

# --- Area Utama Berdasarkan Pilihan Menu ---

if menu_choice == "Beranda / Ringkasan":
    st.title("📊 Analisis Tren dan Faktor Penyebab Perceraian di Indonesia")
    if not df.empty and 'Tahun' in df.columns:
        min_year = df['Tahun'].min()
        max_year = df['Tahun'].max()
        st.markdown(f"### Periode Data: {min_year} - {max_year}")
    else:
        st.markdown("### Periode Data Tersedia")
    st.markdown("---")

    st.markdown("""
    Selamat datang di Dashboard Analisis Perceraian di Indonesia. Dashboard ini menyajikan gambaran komprehensif mengenai
    tren dan faktor-faktor yang melatarbelakangi kasus perceraian di berbagai provinsi di Indonesia.
    Kami mengundang Anda untuk menjelajahi data ini lebih lanjut untuk memahami dinamika sosial yang terjadi.
    """)
    st.markdown("---")

    st.header("Infografis Ringkasan Utama")

    if not df.empty:
        total_perceraian_all_time = df['Jumlah_Perceraian'].sum()

        df_prov_sum = df.groupby('Provinsi')['Jumlah_Perceraian'].sum().reset_index()
        top_province = df_prov_sum.loc[df_prov_sum['Jumlah_Perceraian'].idxmax()] if not df_prov_sum.empty else {'Provinsi': 'N/A', 'Jumlah_Perceraian': 0}

        most_dominant_factor = "N/A"
        dominant_factor_percentage = 0
        if factor_cols and not df[factor_cols].empty:
            df_factors_sum_all = df[factor_cols].sum()
            if not df_factors_sum_all.empty and df_factors_sum_all.sum() > 0:
                most_dominant_factor_raw = df_factors_sum_all.idxmax()
                most_dominant_factor = most_dominant_factor_raw.replace('_', ' ').title()
                dominant_factor_percentage = (df_factors_sum_all.max() / df_factors_sum_all.sum()) * 100

        df_yearly_sum = df.groupby('Tahun')['Jumlah_Perceraian'].sum()
        latest_year = df['Tahun'].max() if 'Tahun' in df.columns else 0
        prev_year = latest_year - 1
        perceraian_latest = df_yearly_sum.get(latest_year, 0)
        perceraian_prev = df_yearly_sum.get(prev_year, 0)

        trend_arrow = "➡️"
        trend_text = "Stabil"
        if perceraian_prev > 0:
            if perceraian_latest > perceraian_prev:
                trend_arrow = "⬆️"
                trend_text = "Meningkat"
            elif perceraian_latest < perceraian_prev:
                trend_arrow = "⬇️"
                trend_text = "Menurun"

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Jumlah Total Perceraian (Semua Data)", value=f"{total_perceraian_all_time:,.0f}")
        with col2:
            st.metric(label="Provinsi Perceraian Tertinggi", value=f"{top_province['Provinsi']}", delta=f"{top_province['Jumlah_Perceraian']:,.0f} Kasus")

        col3, col4 = st.columns(2)
        with col3:
            st.metric(label="Faktor Penyebab Paling Dominan", value=f"{most_dominant_factor}", delta=f"{dominant_factor_percentage:.1f}% dari Total Faktor")
        with col4:
            st.metric(label=f"Tren ({prev_year} vs {latest_year})", value=f"{trend_text}", delta=f"{perceraian_latest:,.0f} ({latest_year}) vs {perceraian_prev:,.0f} ({prev_year}) {trend_arrow}")

        st.markdown("---")

        # Top 5 Provinsi with Horizontal Bar Chart (already implemented in previous step)
        st.subheader("Top 5 Provinsi dengan Angka Perceraian Terbanyak")
        df_top_prov = df.groupby('Provinsi')['Jumlah_Perceraian'].sum().nlargest(5).sort_values(ascending=True).reset_index()
        fig_top_prov = px.bar(df_top_prov, x='Jumlah_Perceraian', y='Provinsi', orientation='h',
                                title="Jumlah Perceraian Kumulatif (Semua Data)",
                                labels={'Jumlah_Perceraian': 'Jumlah Perceraian', 'Provinsi': 'Provinsi'},
                                color='Jumlah_Perceraian', color_continuous_scale=px.colors.sequential.Plasma)
        fig_top_prov.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
        fig_top_prov.update_layout(xaxis_title="Jumlah Perceraian", yaxis_title="Provinsi", yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_prov, use_container_width=True)

        # Proporsi Nasional Faktor Penyebab (Horizontal Bar Chart)
        st.subheader("Proporsi Nasional Faktor Penyebab Perceraian")
        if factor_cols:
            df_factors_national_sum = df[factor_cols].sum().sort_values(ascending=True).reset_index()
            df_factors_national_sum.columns = ['Faktor', 'Jumlah']
            df_factors_national_sum['Faktor'] = df_factors_national_sum['Faktor'].str.replace('_', ' ').str.title()
            if not df_factors_national_sum.empty and df_factors_national_sum['Jumlah'].sum() > 0:
                fig_bar_national_factors = px.bar(df_factors_national_sum, x='Jumlah', y='Faktor', orientation='h',
                                                    title="Proporsi Faktor Penyebab Perceraian Nasional (Semua Data)",
                                                    labels={'Jumlah': 'Jumlah Kasus', 'Faktor': 'Faktor Perceraian'},
                                                    color='Jumlah', color_continuous_scale=px.colors.sequential.Plotly3)
                fig_bar_national_factors.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
                fig_bar_national_factors.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_bar_national_factors, use_container_width=True)
            else:
                st.info("Tidak ada data faktor penyebab yang tersedia untuk Proporsi Nasional.")
        else:
            st.info("Tidak ada kolom faktor penyebab yang terdeteksi dalam data Anda untuk Proporsi Nasional.")
    else:
        st.warning("Data kosong. Mohon periksa file 'finaldata.csv' Anda.")

elif menu_choice == "Tren Perceraian":
    st.title("📈 Analisis Tren Perceraian")
    st.markdown("Halaman ini akan menampilkan berbagai grafik tren perceraian dari waktu ke waktu.")
    st.markdown("---")

    all_years = sorted(df['Tahun'].unique()) if 'Tahun' in df.columns and not df.empty else []
    all_provinces = sorted(df['Provinsi'].unique()) if 'Provinsi' in df.columns and not df.empty else []

    st.sidebar.header("Filter Tren")
    selected_provinces_trend = st.sidebar.multiselect(
        "Pilih Provinsi (Kosongkan untuk Nasional)",
        options=all_provinces,
        default=[],
        key='trend_provinces_multiselect'
    )
    if all_years:
        selected_years_trend = st.sidebar.slider(
            "Pilih Rentang Tahun",
            min_value=min(all_years),
            max_value=max(all_years),
            value=(min(all_years), max(all_years)),
            key='trend_years_slider'
        )
    else:
        selected_years_trend = (0,0)

    df_filtered_trend = df[(df['Tahun'] >= selected_years_trend[0]) & (df['Tahun'] <= selected_years_trend[1])]
    if selected_provinces_trend:
        df_filtered_trend_for_plot = df_filtered_trend[df_filtered_trend['Provinsi'].isin(selected_provinces_trend)]
    else:
        # For national view, aggregate by year only
        df_filtered_trend_for_plot = df_filtered_trend.groupby('Tahun').agg({'Jumlah_Perceraian': 'sum', 'Nikah': 'sum', 'Cerai Talak': 'sum', 'Cerai Gugat': 'sum'}).reset_index()
        # Add a 'Provinsi' column for plotting differentiation
        df_filtered_trend_for_plot['Provinsi'] = 'Nasional'


    if not df_filtered_trend_for_plot.empty:
        # --- Tren Jumlah Perceraian Nasional/Per Provinsi (Line with growth) ---
        st.subheader("Tren Jumlah Perceraian (Kumulatif)")
        
        # Determine the grouping for the plot based on province selection
        if selected_provinces_trend:
            df_plot_trend = df_filtered_trend_for_plot.groupby(['Tahun', 'Provinsi'])['Jumlah_Perceraian'].sum().reset_index()
            color_param = 'Provinsi'
            title_suffix = f"di {', '.join(selected_provinces_trend)}"
        else:
            df_plot_trend = df_filtered_trend_for_plot.groupby('Tahun')['Jumlah_Perceraian'].sum().reset_index()
            df_plot_trend['Provinsi'] = 'Nasional' # Add a dummy column for color
            color_param = None # No color differentiation for single line
            title_suffix = "Nasional"

        fig_trend = px.line(df_plot_trend, x='Tahun', y='Jumlah_Perceraian',
                            color=color_param, # This will create separate lines
                            title=f"Tren Jumlah Perceraian {title_suffix} ({selected_years_trend[0]}-{selected_years_trend[1]})",
                            labels={'Jumlah_Perceraian': 'Jumlah Perceraian', 'Tahun': 'Tahun'},
                            markers=True)

        if not selected_provinces_trend or len(selected_provinces_trend) == 1:
            # Add growth annotations only for national or single province view for clarity
            df_plot_trend['Growth %'] = df_plot_trend.groupby(color_param if color_param else 'Provinsi')['Jumlah_Perceraian'].pct_change() * 100
            for i, row in df_plot_trend.iterrows():
                if not pd.isna(row['Jumlah_Perceraian']):
                    label = f"{row['Jumlah_Perceraian']:,.0f}"
                    if i > 0 and pd.notnull(row['Growth %']):
                        label += f"\n({row['Growth %']:+.1f}%)"
                    fig_trend.add_annotation(
                        x=row['Tahun'], y=row['Jumlah_Perceraian'],
                        text=label,
                        showarrow=False,
                        yshift=10,
                        font=dict(color="steelblue", size=9)
                    )
        fig_trend.update_layout(hovermode="x unified")
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("---")

        # --- Perbandingan Cerai Talak vs Cerai Gugat (Line with growth) ---
        st.subheader("Perbandingan Cerai Talak vs Cerai Gugat")

        # Aggregate Talak vs Gugat based on selected provinces for line plot
        if selected_provinces_trend and len(selected_provinces_trend) > 1:
            df_talak_gugat_plot = df_filtered_trend_for_plot.groupby(['Tahun', 'Provinsi']).agg({'Cerai Talak': 'sum', 'Cerai Gugat': 'sum'}).reset_index()
            # Melt for line plot with color differentiation
            df_talak_gugat_plot_melted = df_talak_gugat_plot.melt(id_vars=['Tahun', 'Provinsi'], var_name='Jenis Cerai', value_name='Jumlah Kasus')
            fig_talak_gugat = px.line(df_talak_gugat_plot_melted, x='Tahun', y='Jumlah Kasus', color='Provinsi', line_dash='Jenis Cerai',
                                      title=f"Tren & Persentase Cerai Talak vs Cerai Gugat di {', '.join(selected_provinces_trend)}",
                                      labels={'Jumlah Kasus': 'Jumlah Kasus', 'Tahun': 'Tahun'},
                                      markers=True)
            # Annotations are harder with multiple lines and multiple metrics per year, so focusing on hover
            fig_talak_gugat.update_layout(hovermode="x unified")

        else: # National or single province
            df_talak_gugat = df_filtered_trend_for_plot.groupby('Tahun')[['Cerai Talak', 'Cerai Gugat']].sum().reset_index()
            df_talak_gugat['Talak Growth'] = df_talak_gugat['Cerai Talak'].pct_change() * 100
            df_talak_gugat['Gugat Growth'] = df_talak_gugat['Cerai Gugat'].pct_change() * 100

            fig_talak_gugat = go.Figure()
            fig_talak_gugat.add_trace(go.Scatter(x=df_talak_gugat['Tahun'], y=df_talak_gugat['Cerai Talak'],
                                                mode='lines+markers', name='Cerai Talak (oleh Suami)',
                                                line=dict(color='steelblue')))
            fig_talak_gugat.add_trace(go.Scatter(x=df_talak_gugat['Tahun'], y=df_talak_gugat['Cerai Gugat'],
                                                mode='lines+markers', name='Cerai Gugat (oleh Istri)',
                                                line=dict(color='darkorange')))

            for i, row in df_talak_gugat.iterrows():
                if not pd.isna(row['Cerai Talak']):
                    label_talak = f"{row['Cerai Talak']:,.0f}"
                    if i > 0 and pd.notnull(row['Talak Growth']):
                        label_talak = f"{row['Talak Growth']:+.1f}%\n({label_talak})"
                    fig_talak_gugat.add_annotation(
                        x=row['Tahun'], y=row['Cerai Talak'],
                        text=label_talak, showarrow=False, yshift=15,
                        font=dict(color="steelblue", size=9)
                    )
                if not pd.isna(row['Cerai Gugat']):
                    label_gugat = f"{row['Cerai Gugat']:,.0f}"
                    if i > 0 and pd.notnull(row['Gugat Growth']):
                        label_gugat = f"{row['Gugat Growth']:+.1f}%\n({label_gugat})"
                    fig_talak_gugat.add_annotation(
                        x=row['Tahun'], y=row['Cerai Gugat'],
                        text=label_gugat, showarrow=False, yshift=-15,
                        font=dict(color="darkorange", size=9)
                    )

            fig_talak_gugat.update_layout(
                title=f"Tren & Persentase Cerai Talak vs Cerai Gugat {'Nasional' if not selected_provinces_trend else 'di ' + ' & '.join(selected_provinces_trend)}",
                xaxis_title="Tahun",
                yaxis_title="Jumlah Kasus",
                hovermode="x unified"
            )
        st.plotly_chart(fig_talak_gugat, use_container_width=True)
        st.markdown("---")

        # --- Perbandingan Jumlah Pernikahan dan Perceraian (Grouped Bar Chart) ---
        st.subheader("Perbandingan Jumlah Pernikahan dan Perceraian")
        df_nikah_cerai = df_filtered_trend_for_plot.groupby('Tahun')[['Nikah', 'Jumlah_Perceraian']].sum().reset_index()

        fig_nikah_cerai = go.Figure()
        fig_nikah_cerai.add_trace(go.Bar(x=df_nikah_cerai['Tahun'], y=df_nikah_cerai['Nikah'], name='Jumlah Pernikahan', marker_color='green', texttemplate='%{y:,.0f}', textposition='outside'))
        fig_nikah_cerai.add_trace(go.Bar(x=df_nikah_cerai['Tahun'], y=df_nikah_cerai['Jumlah_Perceraian'], name='Jumlah Perceraian', marker_color='gold', texttemplate='%{y:,.0f}', textposition='outside'))

        fig_nikah_cerai.update_layout(
            barmode='group',
            title=f"Perbandingan Jumlah Pernikahan dan Perceraian {'Nasional' if not selected_provinces_trend else 'di ' + ' & '.join(selected_provinces_trend)}",
            xaxis_title="Tahun",
            yaxis_title="Jumlah Kasus",
            hovermode="x unified"
        )
        st.plotly_chart(fig_nikah_cerai, use_container_width=True)
        st.markdown("---")

        # --- Rasio Perceraian terhadap Pernikahan (Line Chart) ---
        st.subheader("Rasio Perceraian terhadap Pernikahan")
        df_rasio = df_filtered_trend_for_plot.groupby('Tahun')[['Jumlah_Perceraian', 'Nikah']].sum().reset_index()
        df_rasio['Rasio Cerai/Nikah'] = (df_rasio['Jumlah_Perceraian'] / df_rasio['Nikah']) * 100
        df_rasio.replace([np.inf, -np.inf], np.nan, inplace=True)

        fig_rasio = px.line(df_rasio.dropna(), x='Tahun', y='Rasio Cerai/Nikah',
                            title=f"Rasio Jumlah Perceraian terhadap Pernikahan {'Nasional' if not selected_provinces_trend else 'di ' + ' & '.join(selected_provinces_trend)} (%)",
                            labels={'Rasio Cerai/Nikah': 'Rasio (Cerai / Nikah) (%)', 'Tahun': 'Tahun'},
                            markers=True, color_discrete_sequence=['purple'])
        fig_rasio.update_traces(texttemplate='%{y:.2f}%', textposition='top center')
        fig_rasio.update_layout(hovermode="x unified")
        st.plotly_chart(fig_rasio, use_container_width=True)

    else:
        st.warning("Tidak ada data untuk menampilkan tren. Harap sesuaikan filter di sidebar.")

elif menu_choice == "Faktor Penyebab":
    st.title("💔 Analisis Faktor Penyebab Perceraian")
    st.markdown("Halaman ini akan menampilkan proporsi dan distribusi faktor penyebab perceraian.")
    st.markdown("---")

    st.sidebar.header("Filter Faktor")
    all_years_factor = sorted(df['Tahun'].unique()) if 'Tahun' in df.columns and not df.empty else []
    selected_year_factor = None
    if all_years_factor:
        selected_year_factor = st.sidebar.selectbox(
            "Pilih Tahun",
            options=all_years_factor,
            index=len(all_years_factor) - 1,
            key='factor_year_selectbox'
        )
    else:
        st.sidebar.info("Tidak ada data tahun tersedia untuk filter faktor.")

    all_provinces_factor = sorted(df['Provinsi'].unique()) if 'Provinsi' in df.columns and not df.empty else []
    selected_provinces_factor = st.sidebar.multiselect(
        "Pilih Provinsi (Kosongkan untuk Nasional)",
        options=all_provinces_factor,
        default=[],
        key='factor_provinces_multiselect'
    )

    if selected_year_factor is not None:
        df_filtered_factor = df[df['Tahun'] == selected_year_factor]
        if selected_provinces_factor:
            df_filtered_factor = df_filtered_factor[df_filtered_factor['Provinsi'].isin(selected_provinces_factor)]

        if not df_filtered_factor.empty and factor_cols:
            # --- Horizontal Bar Chart for Factor Distribution ---
            st.subheader(f"Distribusi Faktor Penyebab Perceraian Tahun {selected_year_factor}{' di ' + ' & '.join(selected_provinces_factor) if selected_provinces_factor else ' Nasional'}")

            total_per_faktor = df_filtered_factor[factor_cols].sum().sort_values(ascending=True).reset_index()
            total_per_faktor.columns = ['Faktor', 'Jumlah']
            total_per_faktor['Faktor'] = total_per_faktor['Faktor'].str.replace('_', ' ').str.title()

            if not total_per_faktor.empty and total_per_faktor['Jumlah'].sum() > 0:
                fig_factors_bar = px.bar(total_per_faktor, x='Jumlah', y='Faktor', orientation='h',
                                          title="Jumlah Kasus Berdasarkan Faktor",
                                          labels={'Jumlah': 'Jumlah Kasus', 'Faktor': 'Faktor Perceraian'},
                                          color='Jumlah', color_continuous_scale=px.colors.sequential.RdPu)
                fig_factors_bar.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
                fig_factors_bar.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_factors_bar, use_container_width=True)
            else:
                st.info("Tidak ada data faktor penyebab untuk tahun dan provinsi yang dipilih.")

            st.markdown("---")

            # --- Line Chart for Trend of a Specific Factor (National) ---
            st.subheader("Tren Per Faktor Penyebab (Nasional)")
            selected_factor_trend = st.selectbox(
                "Pilih Faktor untuk Melihat Tren Nasional:",
                options=factor_cols,
                format_func=lambda x: x.replace('_', ' ').title(),
                key='selected_factor_trend'
            )

            yearly_data_factor = df.groupby("Tahun")[selected_factor_trend].sum().reset_index()
            fig_single_factor_trend = px.line(yearly_data_factor, x='Tahun', y=selected_factor_trend,
                                                title=f"Tren Perceraian karena '{selected_factor_trend.replace('_', ' ').title()}' Nasional",
                                                labels={selected_factor_trend: 'Jumlah Kasus', 'Tahun': 'Tahun'},
                                                markers=True, color_discrete_sequence=['steelblue'])
            fig_single_factor_trend.update_traces(texttemplate='%{y:,.0f}', textposition='top center')
            fig_single_factor_trend.update_layout(hovermode="x unified")
            st.plotly_chart(fig_single_factor_trend, use_container_width=True)

        else:
            st.warning("Tidak ada data atau faktor penyebab yang tersedia. Harap sesuaikan filter di sidebar.")
    else:
        st.info("Silakan pilih tahun di sidebar untuk menampilkan data faktor penyebab.")


elif menu_choice == "Perbandingan Provinsi":
    st.title("🗺️ Perbandingan Perceraian antar Provinsi")
    st.markdown("Halaman ini akan membandingkan angka perceraian dan faktor penyebab antar provinsi.")
    st.markdown("---")

    st.sidebar.header("Filter Perbandingan")
    all_years_comp = sorted(df['Tahun'].unique()) if 'Tahun' in df.columns and not df.empty else []
    selected_year_comp = None
    if all_years_comp:
        selected_year_comp = st.sidebar.selectbox(
            "Pilih Tahun untuk Perbandingan",
            options=all_years_comp,
            index=len(all_years_comp) - 1,
            key='comp_year_selectbox'
        )
    else:
        st.sidebar.info("Tidak ada data tahun tersedia untuk filter perbandingan provinsi.")

    provinces_in_selected_year = sorted(df[df['Tahun'] == selected_year_comp]['Provinsi'].unique()) if selected_year_comp is not None else []
    selected_provinces_comp = st.sidebar.multiselect(
        "Pilih Provinsi untuk Perbandingan",
        options=provinces_in_selected_year,
        default=provinces_in_selected_year[:min(5, len(provinces_in_selected_year))],
        key='comp_provinces_multiselect'
    )

    if selected_year_comp is not None and not df.empty:
        df_filtered_comp = df[(df['Tahun'] == selected_year_comp) & (df['Provinsi'].isin(selected_provinces_comp))]

        if not df_filtered_comp.empty and len(selected_provinces_comp) >= 1:
            # --- Horizontal Bar Chart: Jumlah Perceraian per Provinsi ---
            st.subheader(f"Jumlah Perceraian per Provinsi Terpilih Tahun {selected_year_comp}")
            df_prov_comp_sum = df_filtered_comp.groupby('Provinsi')['Jumlah_Perceraian'].sum().sort_values(ascending=True).reset_index()

            fig_comp_bar = px.bar(df_prov_comp_sum, x='Jumlah_Perceraian', y='Provinsi', orientation='h',
                                    title="Total Perceraian per Provinsi",
                                    labels={'Jumlah_Perceraian': 'Jumlah Perceraian', 'Provinsi': 'Provinsi'},
                                    color='Jumlah_Perceraian', color_continuous_scale=px.colors.sequential.Viridis)
            fig_comp_bar.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
            fig_comp_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_comp_bar, use_container_width=True)

            st.markdown("---")

            # --- Grouped Horizontal Bar Chart: Komposisi Faktor Penyebab per Provinsi ---
            if factor_cols:
                st.subheader(f"Komposisi Faktor Penyebab Perceraian per Provinsi Terpilih Tahun {selected_year_comp}")

                df_factors_pivot = df_filtered_comp.groupby('Provinsi')[factor_cols].sum().reset_index()
                df_factors_melted = df_factors_pivot.melt(id_vars=['Provinsi'], var_name='Faktor', value_name='Jumlah')
                df_factors_melted['Faktor'] = df_factors_melted['Faktor'].str.replace('_', ' ').str.title()

                if not df_factors_melted.empty and df_factors_melted['Jumlah'].sum() > 0:
                    fig_grouped_bar_comp = px.bar(df_factors_melted, x='Jumlah', y='Faktor', color='Provinsi',
                                                    orientation='h', barmode='group',
                                                    title="Jumlah Kasus Berdasarkan Faktor Penyebab per Provinsi",
                                                    labels={'Jumlah': 'Jumlah Kasus', 'Faktor': 'Faktor Penyebab', 'Provinsi': 'Provinsi'},
                                                    color_discrete_sequence=px.colors.qualitative.Pastel)
                    fig_grouped_bar_comp.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
                    fig_grouped_bar_comp.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_grouped_bar_comp, use_container_width=True)
                else:
                    st.info("Tidak ada data faktor penyebab yang tersedia untuk perbandingan di halaman ini.")
            else:
                st.info("Tidak ada kolom faktor penyebab yang terdeteksi untuk perbandingan di halaman ini.")

        else:
            st.warning("Pilih minimal satu provinsi dan pastikan data tersedia untuk tahun dan provinsi yang dipilih.")
    else:
        st.info("Silakan pilih tahun di sidebar untuk membandingkan provinsi.")

elif menu_choice == "Peta Visualisasi":
    st.title("📍 Peta Visualisasi Rasio Perceraian")
    st.markdown("Halaman ini menampilkan peta interaktif rata-rata rasio perceraian (Perceraian/Pernikahan) di seluruh provinsi di Indonesia.")
    st.markdown("---")

    if not df.empty and not gdf.empty:
        # 1. Hitung rata-rata rasio perceraian per provinsi (dalam persen)
        avg_rasio = df.groupby('Provinsi')['Rasio_Perceraian'].mean().reset_index()
        avg_rasio['Provinsi_fix'] = avg_rasio['Provinsi'].str.upper() # Match for merging

        # 2. Gabungkan data rata-rata rasio ke GeoDataFrame
        merged_gdf = gdf.merge(avg_rasio, how='left', left_on='provinsi_fix', right_on='Provinsi_fix')

        # Mapbox token from Streamlit secrets (recommended) or direct
        # You need to configure this in .streamlit/secrets.toml
        # MAPBOX_ACCESS_TOKEN = "YOUR_MAPBOX_ACCESS_TOKEN"
        # If using st.secrets, ensure you have [mapbox] token="your_token" in secrets.toml
        try:
            px.set_mapbox_access_token(st.secrets["mapbox"]["token"])
        except:
            st.warning("Mapbox access token tidak ditemukan di `st.secrets`. Peta mungkin tidak akan ditampilkan. Dapatkan token Anda dari mapbox.com dan tambahkan ke file `secrets.toml` Anda.")

        # Buat peta choropleth
        fig_map = px.choropleth_mapbox(
            merged_gdf,
            geojson=merged_gdf.geometry,
            locations=merged_gdf.index,
            color='Rasio_Perceraian',
            hover_name='state',
            hover_data={'Rasio_Perceraian': ':.2f', 'state': True},
            color_continuous_scale="YlOrRd",
            mapbox_style="carto-positron",
            zoom=3.5, center={"lat": -2.5, "lon": 118},
            opacity=0.7,
            labels={'Rasio_Perceraian': 'Rasio Perceraian (%)'}
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption("Peta menunjukkan rata-rata rasio perceraian (jumlah cerai dibagi jumlah nikah) per provinsi. Data tidak tersedia untuk provinsi pemekaran baru di Papua.")
    else:
        st.info("Tidak ada data atau GeoJSON peta yang tersedia untuk menampilkan peta.")
elif menu_choice == "Prediksi Perceraian":
    st.title("🔮 Prediksi Jumlah Perceraian Nasional")
    st.markdown("Halaman ini menampilkan prediksi jumlah perceraian nasional menggunakan model regresi linear sederhana.")
    st.markdown("---")

    if not df.empty:
        # Agregasi total nasional per tahun
        yearly = (
            df.groupby('Tahun', as_index=False)
              .agg({'Jumlah_Perceraian': 'sum', 'Nikah': 'sum'})
              .sort_values('Tahun')
        )

        if yearly.shape[0] < 2:
            st.warning("Data historis tidak cukup untuk membuat prediksi. Minimal 2 tahun data diperlukan.")
        else:
            # Siapkan data latih
            X = yearly[['Tahun', 'Nikah']]
            y = yearly['Jumlah_Perceraian']
            model = LinearRegression().fit(X, y)

            # Estimasi nilai fitur untuk 2025 (memprediksi 'Nikah' di 2025)
            # Pastikan yearly memiliki data untuk membuat prediksi nikah model
            if yearly.shape[0] > 0 and 'Tahun' in yearly.columns and 'Nikah' in yearly.columns:
                nikah_model = LinearRegression().fit(yearly[['Tahun']], yearly['Nikah'])
                pred_nikah_2025 = nikah_model.predict(pd.DataFrame({'Tahun': [2025]}))[0]
            else:
                st.warning("Tidak cukup data untuk memprediksi jumlah pernikahan.")
                pred_nikah_2025 = yearly['Nikah'].iloc[-1] if not yearly.empty else 0 # Fallback

            # Prediksi cerai 2025
            X_2025 = pd.DataFrame({'Tahun': [2025], 'Nikah': [pred_nikah_2025]})
            pred_cerai_2025 = model.predict(X_2025)[0]

            # Gabungkan data historis + prediksi
            pred_row = pd.DataFrame({
                'Tahun': [2025],
                'Nikah': [pred_nikah_2025],
                'Jumlah_Perceraian': [pred_cerai_2025]
            })
            yearly_extended = pd.concat([yearly, pred_row], ignore_index=True)

            # Plotting dengan Plotly
            fig_pred = go.Figure()

            # Garis data historis
            fig_pred.add_trace(go.Scatter(x=yearly['Tahun'], y=yearly['Jumlah_Perceraian'],
                                        mode='lines+markers', name='Data Historis',
                                        line=dict(color='blue'), marker=dict(size=8)))

            # Titik prediksi 2025
            fig_pred.add_trace(go.Scatter(x=[2025], y=[pred_cerai_2025],
                                        mode='markers', name='Prediksi 2025',
                                        marker=dict(color='red', size=10, symbol='circle')))

            # Garis putus-putus dari tahun terakhir ke 2025
            fig_pred.add_trace(go.Scatter(x=[yearly['Tahun'].iloc[-1], 2025],
                                        y=[yearly['Jumlah_Perceraian'].iloc[-1], pred_cerai_2025],
                                        mode='lines', name='Garis Prediksi',
                                        line=dict(color='gray', dash='dash')))

            # Tambahkan label jumlah di atas setiap titik
            for i, row in yearly_extended.iterrows():
                fig_pred.add_annotation(
                    x=row['Tahun'], y=row['Jumlah_Perceraian'],
                    text=f"{int(row['Jumlah_Perceraian']):,.0f}",
                    showarrow=False,
                    yshift=10,
                    font=dict(color="black", size=9)
                )

            # Tambahkan garis vertikal sebagai penanda awal prediksi
            fig_pred.add_vline(x=2024.5, line_width=1, line_dash="dash", line_color="black", annotation_text="Awal Prediksi", annotation_position="top right")

            fig_pred.update_layout(
                title='Prediksi Jumlah Perceraian Nasional hingga 2025',
                xaxis_title='Tahun',
                yaxis_title='Jumlah Perceraian',
                hovermode="x unified"
            )
            st.plotly_chart(fig_pred, use_container_width=True)

            st.markdown("---")
            st.subheader("Evaluasi Model Regresi Linear")
            mae = mean_absolute_error(y, model.predict(X))
            mse = mean_squared_error(y, model.predict(X))
            rmse = np.sqrt(mse)
            r2 = r2_score(y, model.predict(X))

            st.write(f"**Mean Absolute Error (MAE):** {mae:,.2f}")
            st.write(f"**Mean Squared Error (MSE):** {mse:,.2f}")
            st.write(f"**Root Mean Squared Error (RMSE):** {rmse:,.2f}")
            st.write(f"**R-squared (R2):** {r2:.4f}")
            st.info("MAE, MSE, dan RMSE mengukur rata-rata error absolut dan kuadrat antara nilai aktual dan prediksi. Semakin rendah nilainya, semakin baik. R-squared menunjukkan proporsi varian dalam variabel dependen yang dapat diprediksi dari variabel independen. Nilai yang lebih dekat ke 1 menunjukkan kecocokan model yang lebih baik.")

    else:
        st.info("Data kosong. Tidak dapat melakukan prediksi.")

elif menu_choice == "Detail Data":
    st.title("🗄️ Detail Data Perceraian Indonesia")
    st.markdown("Halaman ini menampilkan ringkasan statistik dan tabel lengkap dari data yang digunakan dalam dashboard ini.")
    st.markdown("---")

    if not df.empty:
        # --- Filters for Detail Data ---
        st.sidebar.header("Filter Detail Data") 
        
        all_years = sorted(df['Tahun'].unique())
        selected_years_detail = st.sidebar.slider(
            "Pilih Rentang Tahun",
            min_value=min(all_years),
            max_value=max(all_years),
            value=(min(all_years), max(all_years)),
            key='detail_years_slider'
        )

        all_provinces = sorted(df['Provinsi'].unique())
        selected_provinces_detail = st.sidebar.multiselect(
            "Pilih Provinsi (Kosongkan untuk Semua)",
            options=all_provinces,
            default=[],
            key='detail_provinces_multiselect'
        )

        # Apply filters to the DataFrame for this section
        df_filtered_detail = df[(df['Tahun'] >= selected_years_detail[0]) & (df['Tahun'] <= selected_years_detail[1])]
        if selected_provinces_detail:
            df_filtered_detail = df_filtered_detail[df_filtered_detail['Provinsi'].isin(selected_provinces_detail)]

        # --- Check if filtered data is empty ---
        if df_filtered_detail.empty:
            st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Harap sesuaikan filter Anda.")
        else:
            # --- Ringkasan Statistik Global (Sekarang Berdasarkan Filter) ---
            st.subheader("Ringkasan Data Global (Berdasarkan Filter)")
            col_summary1, col_summary2, col_summary3 = st.columns(3)
            with col_summary1:
                st.metric("Jumlah Baris Data", f"{df_filtered_detail.shape[0]:,.0f}")
            with col_summary2:
                st.metric("Jumlah Kolom Data", f"{df_filtered_detail.shape[1]:,.0f}")
            with col_summary3:
                st.metric("Rentang Tahun Data", f"{df_filtered_detail['Tahun'].min()} - {df_filtered_detail['Tahun'].max()}")
            
            st.write(f"**Jumlah Provinsi Unik:** {df_filtered_detail['Provinsi'].nunique()}")
            st.markdown("---")
            
            # --- Tabel Data Lengkap (Sekarang Berdasarkan Filter) ---
            st.subheader("Tabel Data Lengkap (Berdasarkan Filter)")
            st.info("Anda dapat menggunakan fitur pencarian dan pengurutan bawaan tabel di bawah ini.")
            st.dataframe(df_filtered_detail, use_container_width=True)
            st.markdown("---") # Add a separator before the team info

            # --- Bagian Identitas Kelompok (Tidak terpengaruh filter data) - DIPERBARUI ---
            st.subheader("Identitas Kelompok Pengembang")
            st.write("Dashboard ini dikembangkan oleh:")
            st.markdown("""
            * **Tim Peneliti Kelompok Pemula**
                * Abiyyu Cakra (0110221100)
                * Achmad Rifa'i Ramadhan (0110223138)
                * M Irkham Dwi Ramadhan (0110223284)
                * M Rifanul Haq Ihsani (0110221335)
                * Sahrul Firdaus (0110223114)
            """)
            st.info("Proyek ini adalah bagian dari inisiatif untuk menyediakan analisis data perceraian yang transparan dan mudah diakses bagi masyarakat.")

    else:
        st.info("Data kosong. Mohon periksa file 'finaldata.csv' Anda.")