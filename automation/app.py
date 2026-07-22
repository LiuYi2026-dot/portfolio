"""
AI自动化工具 - 网页信息抓取 & Excel数据处理
=============================================
使用 Streamlit 构建，部署到 Streamlit Cloud
作者: 刘毅
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import re
from urllib.parse import urlparse
import time
import csv

# ============ 页面配置 ============
st.set_page_config(
    page_title="AI 自动化工具 · 刘毅",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ 自定义 CSS ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Noto Sans SC', sans-serif; }
    .main-header {
        font-size: 2rem !important; font-weight: 700 !important;
        background: linear-gradient(135deg, #4B3FE3, #6C63FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header { color: #6B7280; font-size: 1rem; margin-bottom: 2rem; }
    .card {
        background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px;
        padding: 1.5rem; margin-bottom: 1rem;
    }
    .badge {
        display: inline-block; padding: 2px 10px; border-radius: 4px;
        font-size: 0.75rem; font-weight: 500; margin-right: 4px;
        background: rgba(75,63,227,0.08); color: #4B3FE3;
    }
    .result-box {
        background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px;
        padding: 1rem; margin: 1rem 0; max-height: 400px; overflow-y: auto;
    }
    footer { text-align: center; color: #9CA3AF; font-size: 0.85rem; margin-top: 3rem; }
    .stButton button {
        background: #4B3FE3; color: white; border-radius: 8px;
        font-weight: 600; border: none; padding: 0.5rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton button:hover { background: #6C63FF; }
    .stDownloadButton button {
        background: #10B981; color: white; border-radius: 8px;
        font-weight: 600; border: none;
    }
    .stDownloadButton button:hover { background: #059669; }
</style>
""", unsafe_allow_html=True)

# ============ 头部 ============
st.markdown('<p class="main-header">🤖 AI 自动化工具</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">网页信息抓取 · Excel 数据处理 · 一键搞定</p>', unsafe_allow_html=True)

# ============ 侧边栏 ============
st.sidebar.markdown("### 🧭 功能选择")
mode = st.sidebar.radio(
    "选择功能",
    ["🌐 网页信息抓取", "📊 Excel 数据处理"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 关于")
st.sidebar.markdown(
    "**刘毅** · AI 辅助开发者<br>"
    "用 AI 工具做出能上线的东西",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    '<a href="https://liuyi2026-dot.github.io/portfolio/" target="_blank" '
    'style="color:#4B3FE3;font-size:0.85rem;">← 返回作品集</a>',
    unsafe_allow_html=True
)

# ================================================================
# 功能一：网页信息抓取
# ================================================================
if mode == "🌐 网页信息抓取":

    st.markdown("## 🌐 网页信息抓取")
    st.markdown("输入网址，自动提取页面中的标题、链接、文章、表格等关键信息。")

    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input(
            "输入网页 URL",
            placeholder="https://example.com",
            label_visibility="collapsed"
        )
    with col2:
        scrape_btn = st.button("🚀 开始抓取", use_container_width=True)

    scrape_type = st.radio(
        "抓取内容类型",
        ["全部信息", "标题和描述", "所有链接", "文章正文", "表格数据"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if scrape_btn and url:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        with st.spinner("正在抓取网页内容..."):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/120.0.0.0 Safari/537.36"
                }
                resp = requests.get(url, headers=headers, timeout=15)
                resp.encoding = resp.apparent_encoding
                soup = BeautifulSoup(resp.text, "html.parser")

                st.success(f"✅ 成功获取网页！状态码: {resp.status_code}")

                # 基本信息
                with st.container():
                    st.markdown("### 📋 页面基本信息")
                    info_col1, info_col2, info_col3 = st.columns(3)
                    with info_col1:
                        st.metric("页面标题", soup.title.string.strip() if soup.title and soup.title.string else "无标题")
                    with info_col2:
                        meta_desc = soup.find("meta", attrs={"name": "description"})
                        desc_content = meta_desc.get("content", "")[:50] + "..." if meta_desc else "无描述"
                        st.metric("描述", desc_content)
                    with info_col3:
                        domain = urlparse(url).netloc
                        st.metric("域名", domain)

                st.markdown("---")

                # 根据类型展示不同内容
                if scrape_type in ["全部信息", "标题和描述"]:
                    st.markdown("### 📰 页面标题")
                    titles = soup.find_all(["h1", "h2", "h3"])
                    if titles:
                        title_data = []
                        for t in titles[:20]:
                            text = t.get_text(strip=True)
                            if text and len(text) > 2:
                                title_data.append({"级别": t.name.upper(), "内容": text})
                        st.dataframe(pd.DataFrame(title_data), use_container_width=True, hide_index=True)
                    else:
                        st.info("未找到标题内容")

                if scrape_type in ["全部信息", "所有链接"]:
                    st.markdown("### 🔗 页面链接")
                    links = soup.find_all("a", href=True)
                    link_data = []
                    for a in links[:50]:
                        href = a["href"]
                        text = a.get_text(strip=True)[:60] if a.get_text(strip=True) else "(无文字)"
                        if href and not href.startswith(("javascript:", "#", "mailto:")):
                            if not href.startswith("http"):
                                href = urlparse(url)._replace(path=href).geturl() if href.startswith("/") else url + "/" + href
                            link_data.append({"文字": text, "链接": href})

                    st.write(f"共找到 {len(link_data)} 个链接（显示前 50 个）")
                    link_df = pd.DataFrame(link_data)
                    st.dataframe(link_df, use_container_width=True, hide_index=True)

                    # 下载链接
                    csv_buffer = BytesIO()
                    link_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
                    st.download_button(
                        "📥 下载链接为 CSV",
                        data=csv_buffer.getvalue(),
                        file_name=f"links_{domain}.csv",
                        mime="text/csv"
                    )

                if scrape_type in ["全部信息", "文章正文"]:
                    st.markdown("### 📝 文章正文摘要")
                    # 尝试多种方式提取正文
                    article = soup.find("article")
                    if not article:
                        article = soup.find("div", class_=re.compile(r"(content|article|post|main|entry)", re.I))
                    if not article:
                        article = soup.find("main")

                    if article:
                        text = article.get_text(strip=True, separator="\n")
                        lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 20]
                        body_text = "\n\n".join(lines[:30])
                        st.markdown(
                            f'<div class="result-box">{body_text[:3000]}</div>',
                            unsafe_allow_html=True
                        )
                        st.caption(f"共提取 {len(lines)} 个段落")
                    else:
                        # fallback: 取所有 p 标签
                        paragraphs = soup.find_all("p")
                        p_texts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
                        if p_texts:
                            st.markdown(
                                f'<div class="result-box">{"<br><br>".join(p_texts[:20])[:3000]}</div>',
                                unsafe_allow_html=True
                            )
                        else:
                            st.info("未找到文章正文内容")

                if scrape_type in ["全部信息", "表格数据"]:
                    st.markdown("### 📊 表格数据")
                    tables = soup.find_all("table")
                    if tables:
                        st.write(f"共发现 {len(tables)} 个表格")
                        for i, table in enumerate(tables[:3]):
                            try:
                                df_table = pd.read_html(str(table))[0]
                                st.markdown(f"**表格 {i+1}** ({df_table.shape[0]}行 × {df_table.shape[1]}列)")
                                st.dataframe(df_table, use_container_width=True)

                                # 下载表格
                                csv_buf = BytesIO()
                                df_table.to_csv(csv_buf, index=False, encoding="utf-8-sig")
                                st.download_button(
                                    f"📥 下载表格 {i+1}",
                                    data=csv_buf.getvalue(),
                                    file_name=f"table_{i+1}_{domain}.csv",
                                    mime="text/csv"
                                )
                            except Exception:
                                st.warning(f"表格 {i+1} 解析失败")
                    else:
                        st.info("页面中未发现表格数据")

            except requests.exceptions.Timeout:
                st.error("⏰ 请求超时，请检查网址是否正确")
            except requests.exceptions.ConnectionError:
                st.error("🔌 无法连接到该网址，请检查网络或网址")
            except Exception as e:
                st.error(f"❌ 抓取失败: {str(e)}")

    elif scrape_btn and not url:
        st.warning("请先输入网页 URL")

    # 示例
    with st.expander("💡 试试这些示例网址"):
        examples = [
            "https://news.ycombinator.com",
            "https://httpbin.org/links/10",
            "https://quotes.toscrape.com",
            "https://books.toscrape.com"
        ]
        for ex in examples:
            st.code(ex)

# ================================================================
# 功能二：Excel 数据处理
# ================================================================
elif mode == "📊 Excel 数据处理":

    st.markdown("## 📊 Excel 数据处理")
    st.markdown("上传 Excel 文件，自动完成数据清洗、统计分析和可视化。")

    uploaded_file = st.file_uploader(
        "上传 Excel 文件（.xlsx / .xls / .csv）",
        type=["xlsx", "xls", "csv"],
        help="支持 Excel 和 CSV 格式"
    )

    if uploaded_file is not None:
        # 读取文件
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success(f"✅ 成功读取文件！共 {df.shape[0]} 行 × {df.shape[1]} 列")
        except Exception as e:
            st.error(f"❌ 读取失败: {str(e)}")
            st.stop()

        # 预览
        with st.expander("📋 数据预览", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)

        # ===== 数据处理选项卡 =====
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧹 数据清洗", "📊 统计分析", "📈 图表", "📤 导出"
        ])

        # ----- Tab 1: 数据清洗 -----
        with tab1:
            st.markdown("### 数据清洗")

            # 基本信息
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("总行数", df.shape[0])
            with col2:
                st.metric("总列数", df.shape[1])
            with col3:
                null_count = df.isnull().sum().sum()
                st.metric("缺失值", null_count)
            with col4:
                dup_count = df.duplicated().sum()
                st.metric("重复行", dup_count)

            # 缺失值统计
            if null_count > 0:
                st.markdown("#### 各列缺失情况")
                null_df = pd.DataFrame({
                    "列名": df.columns,
                    "缺失数": df.isnull().sum().values,
                    "缺失率": (df.isnull().sum().values / len(df) * 100).round(1)
                })
                null_df = null_df[null_df["缺失数"] > 0]
                st.dataframe(null_df, use_container_width=True, hide_index=True)

            # 清洗操作
            st.markdown("#### 清洗操作")
            clean_col1, clean_col2 = st.columns(2)

            with clean_col1:
                if st.button("🗑️ 删除空行", use_container_width=True):
                    before = df.shape[0]
                    df = df.dropna(how="all")
                    st.success(f"删除了 {before - df.shape[0]} 行全空行")

                if st.button("🔄 重置索引", use_container_width=True):
                    df = df.reset_index(drop=True)
                    st.success("索引已重置")

            with clean_col2:
                if st.button("📑 删除重复行", use_container_width=True):
                    before = df.shape[0]
                    df = df.drop_duplicates()
                    st.success(f"删除了 {before - df.shape[0]} 行重复数据")

                if st.button("✂️ 去除空格", use_container_width=True):
                    for col in df.select_dtypes(include=["object"]).columns:
                        df[col] = df[col].astype(str).str.strip()
                    st.success("所有文本列的前后空格已去除")

            st.markdown("#### 处理后预览")
            st.dataframe(df.head(10), use_container_width=True)

        # ----- Tab 2: 统计分析 -----
        with tab2:
            st.markdown("### 统计分析")

            # 数值列统计
            num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
            cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

            if num_cols:
                st.markdown("#### 数值列统计")
                stats_df = df[num_cols].describe().T
                stats_df["缺失值"] = df[num_cols].isnull().sum().values
                st.dataframe(stats_df.round(2), use_container_width=True)

            if cat_cols:
                st.markdown("#### 文本列统计")
                for col in cat_cols[:3]:
                    with st.container():
                        st.markdown(f"**{col}**")
                        value_counts = df[col].value_counts().head(10)
                        vc_df = pd.DataFrame({
                            "值": value_counts.index,
                            "数量": value_counts.values,
                            "占比(%)": (value_counts.values / len(df) * 100).round(1)
                        })
                        st.dataframe(vc_df, use_container_width=True, hide_index=True)

        # ----- Tab 3: 图表 -----
        with tab3:
            st.markdown("### 图表")

            if num_cols:
                chart_type = st.selectbox("图表类型", ["柱状图", "折线图", "散点图", "面积图"], label_visibility="collapsed")
                x_col = st.selectbox("X 轴", df.columns.tolist())
                y_col = st.selectbox("Y 轴", num_cols)

                if x_col and y_col:
                    # 限制数据量防卡
                    plot_df = df[[x_col, y_col]].dropna()
                    if len(plot_df) > 500:
                        st.info("数据超过 500 行，仅显示前 500 行")
                        plot_df = plot_df.head(500)

                    if chart_type == "柱状图":
                        st.bar_chart(plot_df.set_index(x_col))
                    elif chart_type == "折线图":
                        st.line_chart(plot_df.set_index(x_col))
                    elif chart_type == "散点图":
                        st.scatter_chart(plot_df.set_index(x_col))
                    elif chart_type == "面积图":
                        st.area_chart(plot_df.set_index(x_col))
            else:
                st.info("数据中没有数值列，无法生成图表")

            # 自动统计图
            if num_cols:
                st.markdown("#### 数值分布概览")
                st.bar_chart(df[num_cols].describe().T[["mean", "std", "50%"]])

        # ----- Tab 4: 导出 -----
        with tab4:
            st.markdown("### 导出处理结果")

            out_col1, out_col2 = st.columns(2)

            with out_col1:
                # 导出 Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="处理结果")
                st.download_button(
                    "📥 下载为 Excel",
                    data=output.getvalue(),
                    file_name="processed_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            with out_col2:
                # 导出 CSV
                csv_output = BytesIO()
                df.to_csv(csv_output, index=False, encoding="utf-8-sig")
                st.download_button(
                    "📥 下载为 CSV",
                    data=csv_output.getvalue(),
                    file_name="processed_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    else:
        # 未上传时显示示例数据
        st.info("👆 请上传 Excel 或 CSV 文件开始处理")

        with st.expander("💡 没有 Excel 文件？点击生成示例数据"):
            if st.button("生成示例数据并自动加载"):
                sample_data = {
                    "姓名": ["张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十"],
                    "年龄": [25, 32, 28, 35, 22, 41, 29, 38],
                    "城市": ["北京", "上海", "深圳", "北京", "广州", "上海", "深圳", "杭州"],
                    "月收入": [8500, 12000, 9500, 15000, 6000, 18000, 11000, 13500],
                    "部门": ["技术", "市场", "技术", "管理", "设计", "管理", "技术", "市场"],
                    "入职年份": [2022, 2020, 2021, 2019, 2023, 2018, 2021, 2020]
                }
                sample_df = pd.DataFrame(sample_data)
                output_buf = BytesIO()
                with pd.ExcelWriter(output_buf, engine="openpyxl") as writer:
                    sample_df.to_excel(writer, index=False, sheet_name="员工数据")

                st.download_button(
                    "📥 下载示例 Excel",
                    data=output_buf.getvalue(),
                    file_name="sample_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.code("下载后点击上方上传按钮导入即可体验")

# ============ 页脚 ============
st.markdown("---")
st.markdown(
    '<footer>© 2026 刘毅 · 用 AI 工具 · 从零开始 · '
    '<a href="https://github.com/LiuYi2026-dot" target="_blank" style="color:#4B3FE3;">GitHub</a></footer>',
    unsafe_allow_html=True
)
