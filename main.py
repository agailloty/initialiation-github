import sqlite3
from pathlib import Path

import streamlit as st


DB_PATH = Path(__file__).with_name("app.db")


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def insert_contact(nom: str, email: str, age: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO contacts (nom, email, age) VALUES (?, ?, ?)",
            (nom.strip(), email.strip().lower(), age),
        )


def fetch_contacts() -> list[tuple]:
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT id, nom, email, age, created_at FROM contacts ORDER BY id DESC"
        ).fetchall()


def normalize_rows(rows: list[tuple]) -> list[dict[str, object]]:
    return [
        {
            "ID": row[0],
            "Nom": row[1],
            "Email": row[2],
            "Age": row[3],
            "Cree le": row[4],
        }
        for row in rows
    ]


def main() -> None:
    st.set_page_config(page_title="Saisie SQLite", page_icon="🗃️", layout="centered")
    st.title("Saisie de donnees dans SQLite")
    st.write("Ajoutez un contact via le formulaire ci-dessous.")

    init_db()

    with st.form("contact_form", clear_on_submit=True):
        nom = st.text_input("Nom")
        email = st.text_input("Email")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        submit = st.form_submit_button("Inserer")

    if submit:
        if not nom.strip() or not email.strip():
            st.error("Le nom et l'email sont obligatoires.")
        else:
            try:
                insert_contact(nom, email, int(age))
                st.success("Contact insere avec succes.")
            except sqlite3.IntegrityError:
                st.error("Cet email existe deja dans la base.")

    st.subheader("Contacts enregistres")
    rows = fetch_contacts()
    if rows:
        st.dataframe(normalize_rows(rows), use_container_width=True, hide_index=True)
    else:
        st.info("Aucun contact pour le moment.")


if __name__ == "__main__":
    main()
