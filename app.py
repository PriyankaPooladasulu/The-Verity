
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template

from flask import request

app = Flask(__name__)

# Load database settings from the .env file in this project folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/reserve", methods=["POST"])
def reserve():
    form = request.form

    # Collect the dynamically generated member fields
    member_names = form.getlist("member_name")
    member_ages = form.getlist("member_age")
    member_diets = form.getlist("member_diet")

    # Collect checkbox selections
    cuisines = form.getlist("cuisine")
    addons = form.getlist("addons")
    services = form.getlist("services")

    # The member fields must match in number
    if not (
        len(member_names) == len(member_ages) == len(member_diets)
    ):
        return "Member details are incomplete. Please go back and check the form.", 400

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # 1. Save the main booking
        booking_sql = """
            INSERT INTO bookings (
                booker_name, booker_age, email_id, phone_number,
                member_count, visit_date, time_slot, occasion,
                diet, diet_other, allergies, dining_space,
                package_type, feedback, pool_waiver, terms_accepted
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        booking_values = (
            form.get("name", "").strip(),
            int(form.get("age")),
            form.get("email", "").strip(),
            form.get("phone", "").strip(),
            len(member_names),
            form.get("dov"),
            form.get("ts"),
            form.get("occ") or None,
            form.get("diet"),
            form.get("others") or None,
            form.get("allergies") or None,
            form.get("dining"),
            form.get("package", "none"),
            form.get("feedback") or None,
            1 if form.get("pool_waiver") else 0,
            1 if form.get("terms") else 0,
        )

        cursor.execute(booking_sql, booking_values)
        booking_id = cursor.lastrowid

        # 2. Save additional members
        for name, age, diet in zip(
            member_names, member_ages, member_diets
        ):
            cursor.execute(
                """
                INSERT INTO members (
                    booking_id, member_name, member_age, diet
                )
                VALUES (%s, %s, %s, %s)
                """,
                (booking_id, name.strip(), int(age), diet),
            )

        # 3. Save selected cuisines
        for cuisine in cuisines:
            cursor.execute(
                """
                INSERT INTO booking_cuisines (booking_id, cuisine)
                VALUES (%s, %s)
                """,
                (booking_id, cuisine),
            )

        # 4. Save selected add-ons and their notes
        addon_notes = {
            "cake": form.get("cake-note"),
            "bev": form.get("beverage"),
            "gift": form.get("cgifts"),
            "photo": form.get("pshoots"),
            "sounds": form.get("smusic"),
        }

        for addon in addons:
            cursor.execute(
                """
                INSERT INTO booking_addons (booking_id, addon, notes)
                VALUES (%s, %s, %s)
                """,
                (booking_id, addon, addon_notes.get(addon) or None),
            )

        # 5. Save additional services
        for service in services:
            cursor.execute(
                """
                INSERT INTO booking_services (booking_id, service)
                VALUES (%s, %s)
                """,
                (booking_id, service),
            )

        # Commit only after every insert succeeds
        connection.commit()

        return f"""
            <h1>Reservation submitted!</h1>
            <p>Your reservation has been saved successfully.</p>
            <p>Booking ID: {booking_id}</p>
            <a href="/">Back to the reservation form</a>
        """

    except (mysql.connector.Error, ValueError) as error:
        if connection and connection.is_connected():
            connection.rollback()

        app.logger.exception("Reservation could not be saved")

        return (
            "<h1>Reservation could not be saved</h1>"
            "<p>Please check the application terminal for the error.</p>"
            '<a href="/">Return to the form</a>'
        ), 400

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
