
import io
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="Document Similarity Tool",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document Similarity Tool")
st.write("Compare documents and find similar documents in your dataset.")


def similarity(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform([text1, text2])
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return float(score * 100)
    except ValueError:
        return 0.0


st.sidebar.header("Dataset")
uploaded = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx", "xls"]
)

df = None

if uploaded is not None:
    try:
        if uploaded.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
    except Exception as error:
        st.error(f"Could not read dataset: {error}")

else:
    for filename in ["dataset.csv", "dataset.xlsx"]:
        path = Path(__file__).parent / filename
        if path.exists():
            try:
                if path.suffix == ".csv":
                    df = pd.read_csv(path)
                else:
                    df = pd.read_excel(path)
                break
            except Exception as error:
                st.error(f"Could not read {filename}: {error}")

if df is not None:
    st.subheader("Dataset preview")
    st.dataframe(df.head(10), use_container_width=True)

    if len(df.columns) > 0:
        columns = list(df.columns)

        preferred = next(
            (
                c for c in columns
                if str(c).strip().lower()
                in ["text", "content", "document", "document_text",
                    "description", "body", "full_text"]
            ),
            columns[-1]
        )

        text_col = st.selectbox(
            "Select the column containing document text",
            columns,
            index=columns.index(preferred)
        )

        documents = df[text_col].fillna("").astype(str)
        valid = documents.str.strip().ne("")
        documents = documents[valid].reset_index(drop=True)

        st.write(f"Usable documents: {len(documents)}")

        if len(documents) >= 2:
            query = st.text_area(
                "Enter a document to search for similar documents",
                height=160
            )

            top_k = st.slider(
                "Number of results",
                1,
                min(20, len(documents)),
                min(5, len(documents))
            )

            if st.button("Find Similar Documents"):
                if not query.strip():
                    st.warning("Please enter document text.")
                else:
                    vectorizer = TfidfVectorizer(
                        lowercase=True,
                        stop_words="english",
                        ngram_range=(1, 2)
                    )

                    try:
                        matrix = vectorizer.fit_transform(
                            documents.tolist() + [query]
                        )
                        scores = cosine_similarity(
                            matrix[-1], matrix[:-1]
                        ).ravel()

                        results = pd.DataFrame({
                            "Document": documents.tolist(),
                            "Similarity (%)": scores * 100
                        })

                        results = results.sort_values(
                            "Similarity (%)",
                            ascending=False
                        ).head(top_k)

                        results["Similarity (%)"] = results[
                            "Similarity (%)"
                        ].round(2)

                        st.dataframe(
                            results,
                            use_container_width=True
                        )

                        st.download_button(
                            "Download results as CSV",
                            results.to_csv(index=False).encode("utf-8-sig"),
                            "similarity_results.csv",
                            "text/csv"
                        )

                    except ValueError:
                        st.error(
                            "Unable to process text. "
                            "Check whether the dataset contains valid text."
                        )
        else:
            st.info("At least two non-empty documents are required.")
else:
    st.info(
        "Upload your CSV/Excel dataset in the sidebar. "
        "You can also place dataset.csv or dataset.xlsx "
        "beside app.py."
    )

st.divider()
st.subheader("Compare two documents")

col1, col2 = st.columns(2)

with col1:
    text1 = st.text_area("Document A", height=180)

with col2:
    text2 = st.text_area("Document B", height=180)

if st.button("Compare Documents"):
    if not text1.strip() or not text2.strip():
        st.warning("Enter text in both document fields.")
    else:
        score = similarity(text1, text2)
        st.metric("Cosine Similarity", f"{score:.2f}%")
        st.progress(min(max(score / 100, 0.0), 1.0))
        st.caption(
            "This measures word-based similarity, not the probability "
            "that the documents are copied or have identical meanings."
        )
