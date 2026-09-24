import streamlit as st
import requests


st.set_page_config(
    page_title="QueryGuard",
    page_icon="🛡️",
    layout="centered"
)


st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }

    .hero {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        font-size: 1.1rem;
        color: #666;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    .info-card {
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        background: #f8fafc;
        margin-bottom: 1rem;
    }

    .footer {
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        margin-top: 2.5rem;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero">
        <h1>🛡️ QueryGuard</h1>
        <p>AI-Powered Text-to-SQL Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-card">
        Ask questions about your database in plain English.
        QueryGuard converts your question into SQL, validates the query,
        executes it safely, and explains the result.
    </div>
    """,
    unsafe_allow_html=True
)


BACKEND_URL = "http://127.0.0.1:8000"


st.markdown(
    '<div class="section-title">💡 Try an example</div>',
    unsafe_allow_html=True
)


example_questions = [
    "December mein total sales kitni hui?",
    "Which product generated the highest sales?",
    "North region mein total sales kitni hui?",
    "December mein kitne products sell hue?",
    "November ki total sales batao."
]


selected_question = st.selectbox(
    "Choose an example question:",
    ["Select a question"] + example_questions
)


question = st.text_input(
    "Or ask your own question:",
    placeholder="Example: December mein total sales kitni hui?"
)


if not question and selected_question != "Select a question":
    question = selected_question


if st.button(
    "🔍 Ask QueryGuard",
    use_container_width=True
):

    if not question.strip():
        st.warning("Please enter a question first.")

    else:

        with st.spinner("Understanding your question..."):

            try:
                response = requests.post(
                    f"{BACKEND_URL}/query",
                    json={"question": question},
                    timeout=60
                )

                if response.status_code != 200:

                    st.error(
                        f"Backend error: {response.status_code}"
                    )

                else:

                    data = response.json()

                    if data.get("success"):

                        st.success(
                            "Query executed successfully!"
                        )


                        st.markdown(
                            '<div class="section-title">💬 Answer</div>',
                            unsafe_allow_html=True
                        )

                        st.info(
                            data.get("answer")
                        )


                        st.markdown(
                            '<div class="section-title">🧠 Generated SQL</div>',
                            unsafe_allow_html=True
                        )

                        st.code(
                            data.get("sql_query"),
                            language="sql"
                        )


                        st.markdown(
                            '<div class="section-title">📊 Database Result</div>',
                            unsafe_allow_html=True
                        )

                        columns = data.get("columns", [])
                        rows = data.get("rows", [])


                        if rows:

                            table_data = [
                                dict(zip(columns, row))
                                for row in rows
                            ]

                            st.dataframe(
                                table_data,
                                use_container_width=True,
                                hide_index=True
                            )

                        else:

                            st.info(
                                "No matching records found."
                            )

                    else:

                        st.error(
                            "Query was blocked or failed."
                        )

                        if data.get("error"):

                            st.warning(
                                data.get("error")
                            )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Backend server se connection nahi ho paaya. "
                    "Please make sure FastAPI server is running."
                )


            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out. Please try again."
                )


            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


st.markdown(
    """
    <div class="footer">
        🛡️ QueryGuard • AI-Powered Text-to-SQL with Query Validation
    </div>
    """,
    unsafe_allow_html=True
)