import streamlit as st
import requests
from lxml import etree

st.set_page_config(page_icon="🧬", page_title="RchFind", layout="wide")

def fetch_pubmed_links(compound, keywords=None, num_papers=10):
    query_parts = [compound]
    if keywords:
        query_parts.extend(keywords)
    query = "+AND+".join([q.replace(" ", "+") for q in query_parts])

    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query}"
    response = requests.get(url)
    tree = etree.HTML(response.text)

    papers = []
    articles = tree.xpath('//article[@class="full-docsum"]')
    for article in articles[:num_papers]:
        title_elems = article.xpath('.//a[@class="docsum-title"]')
        if title_elems:
            title = "".join(title_elems[0].itertext()).strip()
            link = "https://pubmed.ncbi.nlm.nih.gov" + title_elems[0].get("href")
            papers.append({"title": title, "link": link})
    return papers


st.title("RchFind")
st.write("Discover research papers with ease")

with st.form("search_form"):
    compound = st.text_input("Compound Name", placeholder="Enter compound name")
    keywords = st.text_input("Keywords (optional)", placeholder="Enter keywords separated by commas")
    num_papers = st.number_input("Number of Papers", min_value=1, max_value=50, value=10, step=1)
    submitted = st.form_submit_button("Search")

if submitted:
    keywords_list = [k.strip() for k in keywords.split(",")] if keywords else None
    results = fetch_pubmed_links(compound, keywords_list, num_papers)

    if results:
        st.subheader("Search Results")
        cols = st.columns(3)
        for i, paper in enumerate(results):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="
                        padding:15px;
                        border-radius:12px;
                        box-shadow:0px 4px 8px rgba(0,0,0,0.1);
                        margin-bottom:20px;
                        background-color:#f9f9f9;
                        color:#000000;  /* ensures text is visible in dark mode */
                    ">
                        <h4 style="font-size:16px; color:#000000;">{paper['title']}</h4>
                        <a href="{paper['link']}" target="_blank" style="color:#1a0dab; text-decoration:none;">🔗 Read Paper</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("No results found. Try different keywords.")
